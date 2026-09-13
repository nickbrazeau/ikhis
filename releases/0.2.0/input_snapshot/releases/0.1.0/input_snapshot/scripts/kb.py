#!/usr/bin/env python3
"""Frozen evidence compiler. Build and query with Python's standard library only."""
import argparse
from collections import defaultdict
import csv
import datetime
import hashlib
import json
import math
from pathlib import Path
import platform
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / 'releases' / '0.1.0'
NA = 'unavailable'
CONTEXT_FIELDS = 'species ancestry age sex tissue disease disease_severity treatment_status cell_type cell_state developmental_state stimulation dose duration assay genomic_background time_point'.split()
CRITICAL_CONTEXT = 'species tissue disease cell_type cell_state stimulation dose duration genomic_background treatment_status time_point'.split()

# Every core domain is represented, including domains without extractable pilot data.
TABLES = {
'entities': 'entity_id TEXT PRIMARY KEY, name TEXT NOT NULL, entity_type TEXT NOT NULL, layer TEXT NOT NULL, external_id TEXT, species TEXT, mapping_status TEXT',
'entity_aliases': 'alias_id TEXT PRIMARY KEY, entity_id TEXT REFERENCES entities, original_label TEXT NOT NULL, assay_channel TEXT, resolution_status TEXT, source_id TEXT REFERENCES source_registry',
'entity_components': 'complex_id TEXT REFERENCES entities, component_id TEXT REFERENCES entities, stoichiometry TEXT, source_id TEXT REFERENCES source_registry, PRIMARY KEY(complex_id,component_id)',
'cells': 'cell_id TEXT PRIMARY KEY, name TEXT NOT NULL, ontology_id TEXT, mapping_status TEXT',
'cell_states': 'state_id TEXT PRIMARY KEY, cell_id TEXT REFERENCES cells, name TEXT, ontology_id TEXT',
'contexts': 'context_id TEXT PRIMARY KEY, '+', '.join(f'{x} TEXT' for x in CONTEXT_FIELDS),
'cohorts': 'cohort_id TEXT PRIMARY KEY, dataset_id TEXT, accession TEXT, study_id TEXT, participants TEXT, ancestry TEXT, species TEXT, tissue TEXT, cell_type TEXT, disease TEXT, intervention TEXT, sample_count TEXT, donor_count TEXT, parent_cohort TEXT, related_publications TEXT, independence_status TEXT, notes TEXT',
'datasets': 'dataset_id TEXT PRIMARY KEY, cohort_id TEXT REFERENCES cohorts, accession TEXT, study_id TEXT, version TEXT, notes TEXT',
'samples': 'sample_id TEXT PRIMARY KEY, cohort_id TEXT REFERENCES cohorts, dataset_id TEXT REFERENCES datasets, donor_id TEXT, context_id TEXT REFERENCES contexts, notes TEXT',
'genetic_associations': 'record_id TEXT PRIMARY KEY, evidence_id TEXT REFERENCES evidence_instances, variant_entity_id TEXT REFERENCES entities, trait_entity_id TEXT REFERENCES entities, grade TEXT, effect_size TEXT, effect_unit TEXT, genome_build TEXT, causal_gene_status TEXT',
'fine_mapping': 'record_id TEXT PRIMARY KEY, evidence_id TEXT REFERENCES evidence_instances, credible_set TEXT, posterior_probability TEXT, method TEXT, genome_build TEXT',
'molecular_qtls': 'record_id TEXT PRIMARY KEY, evidence_id TEXT REFERENCES evidence_instances, qtl_type TEXT, target_entity_id TEXT REFERENCES entities, effect_size TEXT, effect_unit TEXT, colocalization TEXT',
'regulatory_evidence': 'record_id TEXT PRIMARY KEY, evidence_id TEXT REFERENCES evidence_instances, regulatory_element_id TEXT REFERENCES entities, perturbation TEXT, measured_outcome TEXT',
'transcriptomic_observations': 'record_id TEXT PRIMARY KEY, evidence_id TEXT REFERENCES evidence_instances, observation_type TEXT, target_entity_id TEXT REFERENCES entities, assay TEXT, donor_model TEXT, multiple_testing TEXT, composition_qc TEXT',
'transcriptional_programs': 'program_id TEXT PRIMARY KEY, entity_id TEXT REFERENCES entities, definition TEXT, measured_or_inferred TEXT, evidence_id TEXT REFERENCES evidence_instances',
'proteomic_observations': 'record_id TEXT PRIMARY KEY, evidence_id TEXT REFERENCES evidence_instances, target_entity_id TEXT REFERENCES entities, measurement TEXT, platform TEXT, biological_matrix TEXT, reagent TEXT, isoform TEXT, limit_of_detection TEXT, normalization TEXT, peptide_uniqueness TEXT, localization TEXT, cross_reactivity TEXT',
'protein_modifications': 'record_id TEXT PRIMARY KEY, evidence_id TEXT REFERENCES evidence_instances, protein_entity_id TEXT REFERENCES entities, modification TEXT, site TEXT, measurement_method TEXT',
'edge_assertions': 'assertion_id TEXT PRIMARY KEY, subject_id TEXT NOT NULL REFERENCES entities, predicate TEXT NOT NULL, object_id TEXT NOT NULL REFERENCES entities, context_id TEXT NOT NULL REFERENCES contexts, measurement TEXT NOT NULL, direction TEXT NOT NULL, evidence_tier TEXT, status TEXT, qualitative_confidence TEXT, contradiction_group TEXT, candidate_path TEXT',
'evidence_instances': 'evidence_id TEXT PRIMARY KEY, assertion_id TEXT NOT NULL REFERENCES edge_assertions, source_id TEXT NOT NULL REFERENCES source_registry, cohort_id TEXT NOT NULL REFERENCES cohorts, source_locator TEXT NOT NULL, evidence_summary TEXT NOT NULL, effect_size TEXT, effect_unit TEXT, uncertainty TEXT, causal_directness TEXT, limitations TEXT, qc_status TEXT, extraction_lane TEXT, tested_hypothesis TEXT, evidence_relation TEXT, null_adequacy TEXT',
'multiomic_links': 'link_id TEXT PRIMARY KEY, from_assertion_id TEXT REFERENCES edge_assertions, to_assertion_id TEXT REFERENCES edge_assertions, status TEXT, compatibility_report TEXT, bridge_evidence_id TEXT REFERENCES evidence_instances',
'materialized_paths': 'path_id TEXT PRIMARY KEY, assertion_ids TEXT, context_id TEXT REFERENCES contexts, compatibility_report TEXT, status TEXT',
'prior_parameters': 'prior_id TEXT PRIMARY KEY, assertion_id TEXT REFERENCES edge_assertions, parameter_family TEXT, distribution TEXT, parameters TEXT, estimate REAL, estimate_without_journal REAL, independent_groups INTEGER, calibration_status TEXT, availability TEXT, rationale TEXT',
'prior_changes': 'change_id TEXT PRIMARY KEY, prior_id TEXT REFERENCES prior_parameters, previous_version TEXT, new_version TEXT, previous_parameters TEXT, new_parameters TEXT, reason TEXT',
'critic_runs': 'critic_run_id TEXT PRIMARY KEY, role TEXT, scope TEXT, timestamp_start TEXT, timestamp_end TEXT, independence TEXT',
'critic_findings': 'finding_id TEXT PRIMARY KEY, critic_run_id TEXT REFERENCES critic_runs, severity TEXT, target_type TEXT, target_id TEXT, challenge TEXT, evidence TEXT, recommendation TEXT, disposition TEXT',
'adjudications': 'adjudication_id TEXT PRIMARY KEY, finding_id TEXT REFERENCES critic_findings, adjudicator_role TEXT, decision TEXT, rationale TEXT, human_adjudication_status TEXT',
'journal_metrics': 'metric_id TEXT PRIMARY KEY, journal TEXT, year TEXT, impact_factor REAL, authoritative_source TEXT, verified INTEGER CHECK(verified IN (0,1)), multiplier REAL',
'source_registry': 'source_id TEXT PRIMARY KEY, title TEXT NOT NULL, authors TEXT, year TEXT, url TEXT NOT NULL, doi TEXT, pmid TEXT, source_type TEXT, version TEXT, retrieved_at TEXT, access_level TEXT, snapshot_path TEXT, snapshot_sha256 TEXT, species TEXT, notes TEXT, ingestion_status TEXT, duplicate_of TEXT',
'search_log': 'search_id TEXT PRIMARY KEY, lane TEXT, query TEXT, database TEXT, searched_at TEXT, result_source_ids TEXT, screening_notes TEXT, snapshot_path TEXT, total_hits TEXT, returned_pmids TEXT, retrieval_limit TEXT',
'screening_decisions': 'screening_id TEXT PRIMARY KEY, source_id TEXT REFERENCES source_registry, decision TEXT, reason TEXT, stage TEXT, reviewer_role TEXT',
'agent_runs': 'run_id TEXT PRIMARY KEY, agent_role TEXT, timestamp_start TEXT, timestamp_end TEXT, timezone TEXT, LLM_provider TEXT, LLM_model TEXT, model_snapshot_if_available TEXT, reasoning_mode TEXT, protocol_version TEXT, agent_prompt_version TEXT, instruction_bundle_hash TEXT, source_versions TEXT, retrieval_queries TEXT, retrieval_dates TEXT, source_hashes TEXT, code_commit TEXT, environment_hash TEXT, output_hash TEXT, critic_run_ids TEXT, human_edits TEXT, original_metadata TEXT',
'instruction_versions': 'instruction_id TEXT PRIMARY KEY, version TEXT, path TEXT, sha256 TEXT, scope TEXT',
'artifact_hashes': 'artifact_id TEXT PRIMARY KEY, path TEXT NOT NULL, sha256 TEXT NOT NULL, hash_scope TEXT',
'coverage_gaps': 'gap_id TEXT PRIMARY KEY, lane TEXT, description TEXT, status TEXT',
'assay_coverage': 'original_label TEXT PRIMARY KEY, entity_id TEXT REFERENCES entities, mapping_status TEXT, related_assertion_count INTEGER, reviewed_protein_assertion_count INTEGER, coverage_status TEXT',
}

def dump(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'))

def digest(value):
    return hashlib.sha256(value if isinstance(value,bytes) else dump(value).encode()).hexdigest()

def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def uid(prefix,value):
    return prefix+'_'+digest(value)[:16]

def is_known(v):
    return v is not None and str(v).strip().lower() not in {'','unavailable','unknown','not reported','na','n/a','unspecified'}

def value(v):
    if v is None:
        return None
    return dump(v) if isinstance(v,(dict,list)) else v

def insert(db,table,row):
    cols={r[1] for r in db.execute('PRAGMA table_info('+table+')')}
    clean={k:value(v) for k,v in row.items() if k in cols}
    sql='INSERT INTO '+table+' ('+','.join(clean)+') VALUES ('+','.join('?' for _ in clean)+')'
    db.execute(sql,list(clean.values()))

def ensure_entity(db,name,kind,layer,species=NA,external_id=NA):
    # Normalize entity identity, not evidence measurement. Original lane records
    # retain their labels; surface/secreted qualifiers remain in observations.
    if kind in ('cytokine','cytokine_protein','signaling_protein','surface_protein','secreted_protein','intracellular_protein'):
        kind,layer='protein','P'
    if kind=='gene' and layer=='T':
        kind='transcript'
    if kind=='transcript' and name.endswith(' transcript'):
        name=name[:-len(' transcript')]
    if kind=='genetic_variant':
        kind='variant'
    if kind=='protein' and is_known(name):
        existing=db.execute("SELECT entity_id FROM entities WHERE name=? AND entity_type='protein' AND layer='P' AND species=? AND mapping_status='verified'",(name,species)).fetchone()
        if existing:
            return existing[0]
    eid=uid('ENT',[name,kind,layer,species])
    if not db.execute('SELECT 1 FROM entities WHERE entity_id=?',(eid,)).fetchone():
        insert(db,'entities',dict(entity_id=eid,name=name,entity_type=kind,layer=layer,species=species,external_id=external_id,mapping_status='verified' if is_known(external_id) else 'local_only'))
    return eid

def journal_multiplier(jif=None,verified=False):
    if jif is None or not verified:
        return 1.0
    if not isinstance(jif,(float,int)) or not math.isfinite(jif) or jif<0:
        raise ValueError('Impact factor must be finite and nonnegative')
    return 1+0.05*math.tanh(math.log1p(jif)/3)

def summarize_evidence(records):
    """Conservative capped independent groups. Weights are explicitly uncalibrated."""
    groups=defaultdict(list)
    weights={'G1':.25,'G2':.5,'G3':1.,'G4':2.,'P0':.25,'P1':.5,'P2':1.,'P3':1.5,'P4':2.,'observational':.5,'perturbational':1.}
    for r in records:
        if r.get('status')!='reviewed' or r.get('qc_status')!='reviewed_extraction':
            continue
        relation=r.get('evidence_relation','unavailable')
        if relation not in ('supports','opposes') or not is_known(r.get('tested_hypothesis')):
            continue
        if r.get('direction')=='null' and r.get('null_adequacy')!='adequate':
            continue
        # Unknown independence must never be promoted to a new biological replicate.
        group=r['independence_group'] if r.get('independence_status')=='resolved' else 'unresolved'
        w=weights.get(r.get('evidence_tier'),.25)
        if 'abstract' in r.get('access_level','') or 'excerpt' in r.get('access_level',''):
            w*=.5
        if r.get('qualitative_confidence')=='low':
            w*=.5
        groups[group].append((w,r.get('direction','association'),relation))
    alpha,beta=1.,1.
    direction=[1.,1.,1.]
    for group,items in sorted(groups.items()):
        # Preserve conflicts inside a reused cohort without adding replication weight.
        cap=max(w for w,_,_ in items)
        unique={(d,rel):max(w for w,dd,rr in items if (dd,rr)==(d,rel)) for _,d,rel in items}
        total=sum(unique.values())
        for (d,rel),w in unique.items():
            w=cap*w/total
            if rel=='opposes':
                beta+=w
            else:
                alpha+=w
            direction[0 if d=='increase' else 1 if d=='decrease' else 2]+=w
    return {'alpha':alpha,'beta':beta,'estimate':alpha/(alpha+beta),'direction':direction,'independent_groups':len(groups)}

def cohort_group(cohort_id,cohorts):
    """Resolve ancestry of the cohort registry, with cycles/missing parents unresolved."""
    seen=set();current=cohort_id;resolved=True
    while True:
        if current in seen:
            return 'unresolved',False
        seen.add(current)
        row=cohorts.get(current)
        if row is None:
            return current,False
        resolved=resolved and row.get('independence_status')=='resolved'
        parent=row.get('parent_cohort')
        if not is_known(parent):
            return current,resolved
        current=parent

def compatible_path(assertions,contexts,bridges=None):
    """Fail closed: compatible context + a reviewed explicit bridge at every join."""
    reasons=[]
    bridges=bridges or {}
    if len(assertions)<2:
        return False,['path_requires_at_least_two_assertions']
    for a in assertions:
        if a.get('status')!='reviewed':
            reasons.append(a['assertion_id']+':not_reviewed')
        if a.get('evidence_tier')=='P0':
            reasons.append(a['assertion_id']+':inferred_communication')
        if a.get('direction')=='null' or a.get('evidence_relation')!='supports':
            reasons.append(a['assertion_id']+':no_supporting_transition')
        ctx=contexts[a['context_id']]
        for field in CRITICAL_CONTEXT:
            if not is_known(ctx.get(field)):
                reasons.append(a['assertion_id']+':unknown_'+field)
    for left,right in zip(assertions,assertions[1:]):
        if left['object_id']!=right['subject_id']:
            reasons.append('entity_discontinuity')
        pair=(left['assertion_id'],right['assertion_id'])
        bridge=bridges.get(pair,{}) if isinstance(bridges,dict) else {}
        if not (bridge.get('status')=='reviewed' and bridge.get('temporal_compatibility')=='verified' and bridge.get('measurement_bridge')=='verified' and bridge.get('context_compatibility')=='verified' and is_known(bridge.get('evidence_id'))):
            reasons.append('missing_reviewed_transition_and_temporal_bridge')
        lc,rc=contexts[left['context_id']],contexts[right['context_id']]
        for field in CRITICAL_CONTEXT:
            if is_known(lc.get(field)) and is_known(rc.get(field)) and lc[field]!=rc[field]:
                reasons.append('incompatible_'+field)
    return not reasons,sorted(set(reasons))

def read_json(path,default=None):
    return json.loads(path.read_text()) if path.exists() else default

def source_row(source):
    row={k:source.get(k,NA) for k in ['source_id','title','authors','year','url','doi','pmid','source_type','version','retrieved_at','access_level','snapshot_path','species','notes']}
    p=ROOT/str(row['snapshot_path'])
    row['snapshot_sha256']=file_hash(p) if p.is_file() else NA
    row['ingestion_status']=source.get('ingestion_status','extracted')
    overrides=read_json(ROOT/'data/source_overrides.json',{}).get(source['source_id'],{})
    row['duplicate_of']=overrides.get('duplicate_of',source.get('duplicate_of',NA))
    return row

def build_reference_entities(db):
    registry=read_json(ROOT/'research/references/resource_registry.json',[])
    for source in registry:
        insert(db,'source_registry',source_row(source))
    alias_plan=read_json(ROOT/'research/references/alias_plan.json',[])
    ids={}
    for f in sorted((ROOT/'research/references').glob('uniprot_*.json')):
        if f.name.endswith(('.request.json','.response.json')):
            continue
        obj=read_json(f,{})
        symbol=f.stem[len('uniprot_'):]
        records=[r for r in (obj.get('results',[]) if 'results' in obj else [obj]) if any(g.get('geneName',{}).get('value')==symbol for g in r.get('genes',[]))]
        if len(records)!=1:
            continue
        rec=records[0];acc=rec['primaryAccession']
        sid='UP_'+acc
        insert(db,'source_registry',dict(source_id=sid,title=symbol+' human protein identity',authors='UniProt Consortium',year=NA,url='https://rest.uniprot.org/uniprotkb/'+acc+'.json',doi=NA,pmid=NA,source_type='resource',version=str(rec.get('entryAudit',{}).get('entryVersion',NA)),retrieved_at=datetime.datetime.fromtimestamp(f.stat().st_mtime,datetime.timezone.utc).isoformat(),access_level='API_JSON_identity',snapshot_path=str(f.relative_to(ROOT)),snapshot_sha256=file_hash(f),species='Homo sapiens',notes='Identity snapshot only; functional annotations are not imported as assertions. Retrieval timestamp is local snapshot write time.',ingestion_status='identity_only',duplicate_of=NA))
        ids[symbol]=(ensure_entity(db,symbol,'protein','P','Homo sapiens','UniProt:'+acc),sid)
        ensure_entity(db,symbol,'gene','G','Homo sapiens',NA)
    for index,a in enumerate(alias_plan,1):
        symbol=a['canonical_symbol'];label=a['assay_label']
        if symbol in ids:
            eid,sid=ids[symbol];status='biological_identity_verified_assay_platform_unavailable'
        elif symbol=='IL12A:IL12B':
            eid=ensure_entity(db,symbol,'protein_complex','P','Homo sapiens','IUPHAR:4977');sid='R023';status='complex_identity_assay_platform_unavailable'
            for component in ('IL12A','IL12B'):
                if component in ids:
                    insert(db,'entity_components',dict(complex_id=eid,component_id=ids[component][0],stoichiometry='1',source_id=sid))
        elif is_known(symbol):
            eid=ensure_entity(db,symbol,'protein','P','Homo sapiens');sid='SPEC_README';status='specification_mapping_external_identity_unavailable'
        else:
            eid=ensure_entity(db,label,'assay_concept','P','Homo sapiens');sid='SPEC_README';status='unresolved_assay_identity'
        insert(db,'entity_aliases',dict(alias_id='ASSAY_%02d'%index,entity_id=eid,original_label=label,assay_channel=label,resolution_status=status,source_id=sid))
        insert(db,'assay_coverage',dict(original_label=label,entity_id=eid,mapping_status=status,related_assertion_count=0,reviewed_protein_assertion_count=0,coverage_status='not_yet_extracted'))

def load_reviews(db):
    blockers=defaultdict(set)
    resolutions=read_json(ROOT/'provenance/adjudications.json',{})
    for p in sorted((ROOT/'research').glob('review_*.json')):
        review=read_json(p);rid=review.get('critic_run_id',p.stem)
        insert(db,'critic_runs',dict(critic_run_id=rid,role='Adversarial Biological Reviewer',scope=review.get('scope',NA),timestamp_start=review.get('timestamp_start',NA),timestamp_end=review.get('timestamp_end',NA),independence='separate_agent_not_extractor_for_reviewed_lane'))
        for index,f in enumerate(review.get('findings',[]),1):
            fid=f.get('finding_id',rid+'_'+str(index))
            decision=resolutions.get(fid,{})
            row={**f,'finding_id':fid,'critic_run_id':rid,'disposition':decision.get('disposition',f.get('disposition','open'))}
            insert(db,'critic_findings',row)
            if f.get('severity')=='high' and row['disposition']=='open':
                targets=f.get('target_ids',[f.get('target_id')])
                for target in targets:
                    # Multi-target findings may be stored as a comma-delimited locator.
                    if target:
                        blockers[f.get('target_type','unknown')].update(s.strip() for s in str(target).replace(';',',').split(','))
            insert(db,'adjudications',dict(adjudication_id='ADJ_'+fid,finding_id=fid,adjudicator_role='coordinating_agent',decision=decision.get('decision','retain_finding_and_withhold_high_severity_targets'),rationale=decision.get('rationale','Human adjudication has not occurred. Open biological questions remain visible.'),human_adjudication_status='pending'))
    return blockers

def is_contested(assertion,context_id,blockers,cohorts):
    if any(blockers.get(t) for t in ('protocol','code','unknown')):
        return True
    for field,target_type in [('assertion_id','assertion'),('source_id','source')]:
        if assertion[field] in blockers.get(target_type,set()):
            return True
    if context_id in blockers.get('context',set()):
        return True
    cid=assertion['cohort_id'];seen=set()
    while is_known(cid) and cid not in seen:
        if cid in blockers.get('cohort',set()):
            return True
        seen.add(cid);cid=cohorts.get(cid,{}).get('parent_cohort')
    return False

def build():
    RELEASE.mkdir(parents=True,exist_ok=True)
    dbpath=RELEASE/'immune_prior.sqlite'
    if dbpath.exists():
        dbpath.unlink()
    db=sqlite3.connect(dbpath);db.row_factory=sqlite3.Row
    db.execute('PRAGMA foreign_keys=ON')
    for table,definition in TABLES.items():
        db.execute('CREATE TABLE '+table+' ('+definition+')')
    schema='PRAGMA foreign_keys=ON;\n'+''.join('CREATE TABLE '+t+' ('+d+');\n' for t,d in TABLES.items())
    (ROOT/'data/schema.sql').write_text(schema)
    insert(db,'source_registry',dict(source_id='SPEC_README',title='Greenfield Multi-Omic Immune-System Prior Review specification',url='README.md',source_type='specification',version='0.1.0',retrieved_at=NA,access_level='local_specification',snapshot_path='README.md',snapshot_sha256=file_hash(ROOT/'README.md'),ingestion_status='specification_only'))
    build_reference_entities(db)
    blockers=load_reviews(db)
    source_ids=set(r[0] for r in db.execute('SELECT source_id FROM source_registry'))
    all_raw=[]
    scoring=read_json(ROOT/'data/scoring_annotations.json',{})
    for lane in ('cytokine','genomic','proteomic'):
        packpath=ROOT/'research'/lane/'pack.json'
        if not packpath.exists():
            insert(db,'coverage_gaps',dict(gap_id='MISSING_'+lane,lane=lane,description='Evidence pack missing',status='open'));continue
        pack=read_json(packpath)
        for source in pack['sources']:
            if source['source_id'] in source_ids:
                raise ValueError('Duplicate source ID '+source['source_id'])
            source_ids.add(source['source_id']);insert(db,'source_registry',source_row(source))
            insert(db,'screening_decisions',dict(screening_id='SCREEN_'+source['source_id'],source_id=source['source_id'],decision='included_in_bounded_corpus',reason='Purposive anchor/primary evidence selected for pilot; not exhaustive screening',stage=source.get('access_level',NA),reviewer_role=lane+'_extractor'))
        for c in pack['cohorts']:
            insert(db,'cohorts',c)
            dataset=c.get('dataset_id',NA)
            if is_known(dataset) and not db.execute('SELECT 1 FROM datasets WHERE dataset_id=?',(str(dataset),)).fetchone():
                insert(db,'datasets',dict(dataset_id=dataset,cohort_id=c['cohort_id'],accession=c.get('accession',NA),study_id=c.get('study_id',NA),version=NA,notes='Dataset registry does not independently establish cohort independence.'))
        for a in pack['assertions']:
            a={**a,'extraction_lane':lane};all_raw.append(a)
            a.update(scoring.get(a['assertion_id'],{'tested_hypothesis':NA,'evidence_relation':'unavailable','null_adequacy':NA}))
            species=a.get('species',NA)
            subject=ensure_entity(db,a['subject'],a['subject_type'],a['subject_layer'],species)
            obj=ensure_entity(db,a['object'],a['object_type'],a['object_layer'],species)
            context={field:a.get(field,NA) for field in CONTEXT_FIELDS};cid=uid('CTX',context)
            if not db.execute('SELECT 1 FROM contexts WHERE context_id=?',(cid,)).fetchone():
                insert(db,'contexts',dict(context_id=cid,**context))
            cell_id=uid('CELL',context['cell_type'])
            if not db.execute('SELECT 1 FROM cells WHERE cell_id=?',(cell_id,)).fetchone():
                insert(db,'cells',dict(cell_id=cell_id,name=context['cell_type'],ontology_id=NA,mapping_status='local_only'))
            state_id=uid('STATE',[cell_id,context['cell_state']])
            if not db.execute('SELECT 1 FROM cell_states WHERE state_id=?',(state_id,)).fetchone():
                insert(db,'cell_states',dict(state_id=state_id,cell_id=cell_id,name=context['cell_state'],ontology_id=NA))
            aid=a['assertion_id'];ev='EV_'+aid
            cohort_map={r['cohort_id']:dict(r) for r in db.execute('SELECT * FROM cohorts')}
            status='contested' if is_contested(a,cid,blockers,cohort_map) else 'reviewed' if a.get('qc_status')=='reviewed_extraction' else 'needs_full_text'
            insert(db,'edge_assertions',dict(assertion_id=aid,subject_id=subject,predicate=a['predicate'],object_id=obj,context_id=cid,measurement=a['measurement'],direction=a['direction'],evidence_tier=a['evidence_tier'],status=status,qualitative_confidence=a.get('qualitative_confidence','low'),contradiction_group=a.get('contradiction_group',NA),candidate_path=a.get('candidate_path',NA)))
            insert(db,'evidence_instances',dict(evidence_id=ev,**a))
            m=a['measurement'];tier=a['evidence_tier']
            if a['subject_layer']=='G' and a['subject_type'] in ('variant','genetic_variant','variant_allele','genomic_variant'):
                insert(db,'genetic_associations',dict(record_id='GA_'+aid,evidence_id=ev,variant_entity_id=subject,trait_entity_id=obj,grade=tier,effect_size=a.get('effect_size',NA),effect_unit=a.get('effect_unit',NA),genome_build=NA,causal_gene_status='limited_to_asserted_measured_effect' if tier=='G4' else 'not_established_by_association_alone'))
                if tier in ('G2','G3'):
                    insert(db,'molecular_qtls',dict(record_id='QTL_'+aid,evidence_id=ev,qtl_type='sQTL' if m=='splicing' else 'eQTL' if a['object_layer']=='T' else 'pQTL' if a['object_layer']=='P' else 'unavailable',target_entity_id=obj,effect_size=a.get('effect_size',NA),effect_unit=a.get('effect_unit',NA),colocalization=NA))
                if tier=='G4':
                    insert(db,'regulatory_evidence',dict(record_id='REG_'+aid,evidence_id=ev,regulatory_element_id=None,perturbation=a.get('stimulation',NA),measured_outcome=a['object']))
            if m in ('RNA_abundance','splicing','direct_transcriptional_regulation'):
                insert(db,'transcriptomic_observations',dict(record_id='TX_'+aid,evidence_id=ev,observation_type=m,target_entity_id=obj,assay=a.get('assay',NA),donor_model=NA,multiple_testing=NA,composition_qc=NA))
            if a['object_type'] in ('transcriptional_program','gene_program','program'):
                insert(db,'transcriptional_programs',dict(program_id='PROG_'+aid,entity_id=obj,definition=a['object'],measured_or_inferred=m,evidence_id=ev))
            if m in ('protein_abundance','secreted_protein','protein_activity','receptor_signaling'):
                insert(db,'proteomic_observations',dict(record_id='PROT_'+aid,evidence_id=ev,target_entity_id=obj,measurement=m,platform=a.get('assay',NA),biological_matrix=a.get('tissue',NA),reagent=a.get('reagent',NA),isoform=a.get('isoform',NA),limit_of_detection=a.get('limit_of_detection',NA),normalization=a.get('normalization',NA),peptide_uniqueness=a.get('peptide_uniqueness',NA),localization='extracellular' if m=='secreted_protein' else a.get('localization',NA),cross_reactivity=a.get('limitations',NA)))
                if 'phosph' in str(a['object']).lower() or 'pSTAT' in str(a['object']):
                    insert(db,'protein_modifications',dict(record_id='PTM_'+aid,evidence_id=ev,protein_entity_id=obj,modification='phosphorylation',site=a.get('ptm_site',NA),measurement_method=a.get('assay',NA)))
        for s in pack.get('searches',[]):
            insert(db,'search_log',s)
        for index,g in enumerate(pack.get('gaps',[]),1):
            insert(db,'coverage_gaps',dict(gap_id=lane+'_'+str(index),lane=lane,description=g,status='open'))
        run=read_json(ROOT/'research'/lane/'run.json',{})
        row={k:run.get(k,NA) for k in 'run_id agent_role timestamp_start timestamp_end timezone LLM_provider LLM_model model_snapshot_if_available reasoning_mode protocol_version agent_prompt_version instruction_bundle_hash source_versions retrieval_queries retrieval_dates source_hashes code_commit environment_hash output_hash critic_run_ids human_edits'.split()}
        row.update(run_id=run.get('run_id','RUN_'+lane),agent_role=lane+'_extractor',original_metadata=run,output_hash=file_hash(packpath))
        insert(db,'agent_runs',row)
    for s in read_json(ROOT/'research/references/search_registry.json',[]):
        insert(db,'search_log',s)
    compile_priors(db)
    compile_paths(db)
    for label,eid,name in db.execute('SELECT a.original_label,a.entity_id,e.name FROM assay_coverage a JOIN entities e USING(entity_id)').fetchall():
        count=db.execute('SELECT COUNT(DISTINCT a.assertion_id) FROM edge_assertions a JOIN entities s ON a.subject_id=s.entity_id JOIN entities o ON a.object_id=o.entity_id WHERE s.name=? OR o.name=?',(name,name)).fetchone()[0]
        protein_count=db.execute("SELECT COUNT(DISTINCT a.assertion_id) FROM edge_assertions a JOIN entities s ON a.subject_id=s.entity_id JOIN entities o ON a.object_id=o.entity_id WHERE a.status='reviewed' AND ((s.name=? AND s.layer='P') OR (o.name=? AND o.layer='P'))",(name,name)).fetchone()[0]
        db.execute('UPDATE assay_coverage SET related_assertion_count=?,reviewed_protein_assertion_count=?,coverage_status=? WHERE original_label=?',(count,protein_count,'partial_pilot_evidence' if protein_count else 'related_evidence_only' if count else 'not_yet_extracted',label))
    instruction_paths=[ROOT/'README.md',ROOT/'protocol/PROTOCOL.md',ROOT/'research/EXTRACTION_CONTRACT.md',ROOT/'provenance/USER_REQUEST.md']+sorted((ROOT/'provenance/skill_snapshots').glob('*.md'))
    for p in instruction_paths:
        insert(db,'instruction_versions',dict(instruction_id=uid('INS',str(p.relative_to(ROOT))),version='0.1.0' if p.name in ('README.md','PROTOCOL.md','EXTRACTION_CONTRACT.md') else NA,path=str(p.relative_to(ROOT)),sha256=file_hash(p),scope='governing_specification' if p.name=='README.md' else 'operational_instruction'))
    session=read_json(ROOT/'provenance/session.json',{})
    output_tables=['entities','edge_assertions','evidence_instances','prior_parameters']
    semantic_output_hash=digest({t:[dict(r) for r in db.execute('SELECT * FROM '+t+' ORDER BY 1')] for t in output_tables})
    session['output_hash_scope']={'kind':'canonical_JSON_table_contents','tables':output_tables}
    insert(db,'agent_runs',dict(run_id='RUN_COORDINATOR_0.1.0',agent_role='coordinator',timestamp_start=session.get('timestamp_start',NA),timestamp_end=session.get('timestamp_end',NA),timezone='America/New_York',LLM_provider='OpenAI',LLM_model='GPT-6',model_snapshot_if_available=NA,reasoning_mode=NA,protocol_version='0.1.0',agent_prompt_version='0.1.0',instruction_bundle_hash=digest([file_hash(p) for p in instruction_paths]),source_versions='source_registry.csv',retrieval_queries='search_log.csv',retrieval_dates='source_registry.csv',source_hashes='artifact_hashes.csv',code_commit=NA,environment_hash=digest({'python':platform.python_version(),'platform':platform.platform()}),output_hash=semantic_output_hash,critic_run_ids=[r[0] for r in db.execute('SELECT critic_run_id FROM critic_runs')],human_edits=NA,original_metadata=session))
    for p in input_files():
        insert(db,'artifact_hashes',dict(artifact_id=uid('ART',str(p.relative_to(ROOT))),path=str(p.relative_to(ROOT)),sha256=file_hash(p),hash_scope='exact_local_bytes'))
    db.commit()
    errors=validate(db)
    for table in TABLES:
        rows=db.execute('SELECT * FROM '+table+' ORDER BY 1').fetchall()
        with (RELEASE/(table+'.csv')).open('w',newline='') as f:
            w=csv.writer(f);w.writerow([r[1] for r in db.execute('PRAGMA table_info('+table+')')]);w.writerows(rows)
    counts={t:db.execute('SELECT count(*) FROM '+t).fetchone()[0] for t in TABLES}
    qc={'release':'0.1.0','status':'pass_with_documented_limitations' if not errors else 'fail','errors':errors,'counts':counts,'scientific_status':'bounded_pilot_uncalibrated_human_adjudication_pending','unresolved_high_findings':db.execute("SELECT count(*) FROM critic_findings WHERE severity='high' AND disposition='open'").fetchone()[0],'contested_assertions':db.execute("SELECT count(*) FROM edge_assertions WHERE status='contested'").fetchone()[0],'limitations':['Not an exhaustive systematic review','Ontology mappings beyond verified priority protein identities remain local','Some primary sources are abstract/excerpt only','Human adjudication pending','Priors are heuristic and uncalibrated','No numeric effect magnitude or human transportability inferred','Unknown path context/bridges block materialization','Authoritative journal impact factors unavailable; multiplier disabled']}
    (RELEASE/'qc.json').write_text(json.dumps(qc,indent=2)+'\n')
    for filename,tables in {'source_manifest':['source_registry','search_log','screening_decisions'],'provenance_manifest':['agent_runs','critic_runs','adjudications','artifact_hashes'],'protocol_instruction_manifest':['instruction_versions']}.items():
        (RELEASE/(filename+'.json')).write_text(json.dumps({t:[dict(r) for r in db.execute('SELECT * FROM '+t+' ORDER BY 1')] for t in tables},indent=2,ensure_ascii=False)+'\n')
    report(db,qc)
    (ROOT/'data/DATA_DICTIONARY.md').write_text('# Knowledge-base data dictionary\n\nUnknown values are `unavailable`. Foreign-key omissions are SQL NULL only when no record exists; they are not fabricated entity IDs. JSON arrays/objects inside CSV fields are serialized JSON. Numeric estimates are uncalibrated evidence summaries.\n\n'+''.join('## '+t+'\n\n| Field | SQL definition |\n|---|---|\n'+''.join('| '+part.strip().split()[0]+' | '+part.strip()+' |\n' for part in definition.split(', ') if not part.startswith('PRIMARY KEY'))+'\n' for t,definition in TABLES.items()))
    db.close()
    print(json.dumps(qc,indent=2))
    return not errors

def compile_priors(db):
    rows=[dict(r) for r in db.execute('SELECT a.*,e.*,s.access_level,c.independence_status,c.parent_cohort FROM edge_assertions a JOIN evidence_instances e USING(assertion_id) JOIN source_registry s USING(source_id) JOIN cohorts c USING(cohort_id)')]
    hypotheses=defaultdict(list)
    cohort_map={r['cohort_id']:dict(r) for r in db.execute('SELECT * FROM cohorts')}
    for r in rows:
        key=(r['tested_hypothesis'],r['context_id'],r['measurement'])
        group,resolved=cohort_group(r['cohort_id'],cohort_map)
        r['independence_group']=group;r['independence_status']='resolved' if resolved else 'unresolved'
        hypotheses[key].append(r)
    for records in hypotheses.values():
        summary=summarize_evidence(records)
        for r in records:
            aid=r['assertion_id'];eligible=r['status']=='reviewed' and r['qc_status']=='reviewed_extraction'
            numeric_eligible=eligible and is_known(r['tested_hypothesis']) and r['evidence_relation'] in ('supports','opposes') and (r['direction']!='null' or r['null_adequacy']=='adequate')
            families=['existence','direction','effect_class','magnitude','temporal','genetic_modifier','expression','protein_availability','human_transportability','context_specific']
            for family in families:
                pid='PRIOR_'+aid+'_'+family
                available=eligible and family in ('existence','direction','effect_class','context_specific') and (family in ('effect_class','context_specific') or (numeric_eligible and summary['independent_groups']>0))
                if family=='existence' and available:
                    dist='Beta';params={k:summary[k] for k in ('alpha','beta')};estimate=summary['estimate'];reason='Tier/access/confidence weights, biological cohort cap; not calibrated probability of truth.'
                elif family=='direction' and available:
                    dist='Dirichlet';params={'categories':['increase','decrease','other'],'alpha':summary['direction']};estimate=None;reason='Direction uncertainty is separate from existence and from effect magnitude.'
                elif family in ('effect_class','context_specific') and available:
                    dist='categorical_annotation';params={'observed_direction':r['direction']} if family=='effect_class' else {'context_id':r['context_id']};estimate=None;reason='Observed annotation only, no numeric distribution inferred.'
                else:
                    dist=NA;params={};estimate=None;reason='Contested/incomplete extraction withheld.' if not eligible else 'Quantitative parameterization requires compatible effect/uncertainty data or validated calibration; unavailable in this release.'
                insert(db,'prior_parameters',dict(prior_id=pid,assertion_id=aid,parameter_family=family,distribution=dist,parameters=params,estimate=estimate,estimate_without_journal=estimate,independent_groups=summary['independent_groups'] if available else 0,calibration_status='uncalibrated',availability='available' if available else 'withheld' if not eligible else 'unavailable',rationale=reason))
                insert(db,'prior_changes',dict(change_id='CHANGE_'+pid,prior_id=pid,previous_version=NA,new_version='0.1.0',previous_parameters=NA,new_parameters=params,reason='Greenfield initial evidence-derived parameter record; no inherited statistical prior.'))

def compile_paths(db):
    rows=[dict(r) for r in db.execute('SELECT a.*,e.evidence_relation FROM edge_assertions a JOIN evidence_instances e USING(assertion_id)')]
    contexts={r['context_id']:dict(r) for r in db.execute('SELECT * FROM contexts')}
    for a in rows:
        for b in rows:
            if a['assertion_id']==b['assertion_id'] or a['object_id']!=b['subject_id']:
                continue
            ok,reasons=compatible_path([a,b],contexts)
            insert(db,'multiomic_links',dict(link_id=uid('LINK',[a['assertion_id'],b['assertion_id']]),from_assertion_id=a['assertion_id'],to_assertion_id=b['assertion_id'],status='compatible' if ok else 'blocked',compatibility_report=reasons,bridge_evidence_id=None))
            if ok:
                insert(db,'materialized_paths',dict(path_id=uid('PATH',[a['assertion_id'],b['assertion_id']]),assertion_ids=[a['assertion_id'],b['assertion_id']],context_id=a['context_id'],compatibility_report=reasons,status='materialized'))

def input_files():
    paths=[]
    for folder in ('protocol','research','scripts','tests','provenance','reports','data'):
        for p in (ROOT/folder).rglob('*'):
            if p.is_file() and not any(x in p.parts for x in ('.venv','__pycache__')) and p.name not in ('.DS_Store','schema.sql','DATA_DICTIONARY.md'):
                paths.append(p)
    return sorted(set(paths+[p for p in (ROOT/'README.md',ROOT/'RUNNING.md',ROOT/'requirements-research.txt',ROOT/'requirements-research.lock') if p.exists()]))

def validate(db):
    errors=[]
    for row in db.execute('PRAGMA foreign_key_check'):
        errors.append('Foreign key violation: '+str(tuple(row)))
    if db.execute('PRAGMA integrity_check').fetchone()[0]!='ok':
        errors.append('SQLite integrity check failed')
    for r in db.execute('SELECT * FROM evidence_instances'):
        if not is_known(r['source_locator']) or not is_known(r['evidence_summary']):
            errors.append('Missing evidence locator/summary: '+r['evidence_id'])
    for r in db.execute("SELECT DISTINCT s.* FROM source_registry s JOIN evidence_instances e USING(source_id)"):
        if not is_known(r['snapshot_sha256']):
            errors.append('Missing source snapshot for extracted source: '+r['source_id'])
    for r in db.execute('SELECT a.*,s.layer sl,o.layer ol FROM edge_assertions a JOIN entities s ON s.entity_id=a.subject_id JOIN entities o ON o.entity_id=a.object_id'):
        expected={'RNA_abundance':{'T'},'splicing':{'T'},'direct_transcriptional_regulation':{'T'},'protein_abundance':{'P'},'secreted_protein':{'P'},'protein_activity':{'P'},'receptor_signaling':{'P','C'},'cellular_phenotype':{'F'}}
        if r['measurement'] not in set(expected)|{'association','inferred_communication'}:
            errors.append('Unknown measurement vocabulary: '+r['assertion_id'])
        if r['measurement'] in expected and r['ol'] not in expected[r['measurement']]:
            errors.append('Measurement/object-layer mismatch: '+r['assertion_id'])
        if r['evidence_tier']=='P0' and r['measurement']!='inferred_communication':
            errors.append('P0 must be inference: '+r['assertion_id'])
    for r in db.execute("SELECT p.prior_id FROM prior_parameters p JOIN edge_assertions a USING(assertion_id) WHERE a.status<>'reviewed' AND p.availability='available'"):
        errors.append('Withheld evidence entered prior: '+r[0])
    alias={r['original_label']:r for r in db.execute('SELECT * FROM entity_aliases')}
    if len(alias)!=30:
        errors.append('Expected all 30 original assay labels')
    if 'IL-8' in alias and alias['IL-8']['entity_id']!=alias['IL-8 high range']['entity_id']:
        errors.append('CXCL8 alias identity mismatch')
    if 'IL-12' in alias and alias['IL-12']['entity_id']==alias['IL-12p70']['entity_id']:
        errors.append('Ambiguous IL-12 assay silently merged')
    return errors

def report(db,qc):
    counts=qc['counts']
    text='# Initial immune-system evidence release\n\n'
    text+=f"Release 0.1.0 contains {counts['edge_assertions']} evidence assertions, {counts['cohorts']} cohort/context records and {counts['source_registry']} source records (including reference resources and identity snapshots). It is a bounded initial corpus, not an exhaustive systematic review. Human adjudication and probability calibration remain outstanding.\n\n"
    text+='## Release checks\n\n'+('All structural checks passed.\n\n' if not qc['errors'] else 'Structural errors: '+dump(qc['errors'])+'\n\n')
    text+=f"{qc['contested_assertions']} assertions are contested after independent review. {counts['materialized_paths']} complete paths are materialized. Missing or incompatible context and missing temporal bridges prevent unsupported joins. Journal weighting is disabled.\n\n"
    text+='## Evidence assertions\n\n| ID | Assertion | Measurement / tier | Context | Status | Source |\n|---|---|---|---|---|---|\n'
    for r in db.execute('SELECT a.*,s.name subject,o.name object,c.species,c.cell_type,e.source_locator,src.title,src.url FROM edge_assertions a JOIN entities s ON a.subject_id=s.entity_id JOIN entities o ON a.object_id=o.entity_id JOIN contexts c USING(context_id) JOIN evidence_instances e USING(assertion_id) JOIN source_registry src USING(source_id) ORDER BY a.assertion_id'):
        clean=lambda v:str(v).replace('|','/').replace('\n',' ')
        text+='| '+ ' | '.join(map(clean,[r['assertion_id'],r['subject']+' → '+r['predicate']+' → '+r['object'],r['measurement']+' / '+r['evidence_tier'],r['species']+'; '+r['cell_type'],r['status'],'['+r['title']+']('+r['url']+'); '+r['source_locator']]))+' |\n'
    text+='\n## Coverage and limits\n\n'
    for r in db.execute('SELECT * FROM coverage_gaps ORDER BY gap_id'):
        text+='- '+r['lane']+': '+r['description']+'\n'
    (RELEASE/'EVIDENCE_ATLAS.md').write_text(text)

def freeze():
    db=sqlite3.connect(RELEASE/'immune_prior.sqlite');db.row_factory=sqlite3.Row
    errors=validate(db)
    recorded={r['path']:r['sha256'] for r in db.execute('SELECT path,sha256 FROM artifact_hashes')}
    current={str(p.relative_to(ROOT)):file_hash(p) for p in input_files()}
    if recorded!=current:
        errors.append('Inputs changed since build; rebuild before freezing: '+dump(sorted(k for k in set(recorded)|set(current) if recorded.get(k)!=current.get(k))))
    db.close()
    if errors:
        raise ValueError(errors)
    files=input_files()+[p for p in RELEASE.rglob('*') if p.is_file() and p.name!='manifest.json']+[ROOT/'data/schema.sql',ROOT/'data/DATA_DICTIONARY.md']
    manifest={'release':'0.1.0','protocol_version':'0.1.0','scientific_status':'bounded_initial_release','manifest_excludes_itself':True,'hash_algorithm':'sha256','files':{str(p.relative_to(ROOT)):file_hash(p) for p in sorted(set(files))}}
    (RELEASE/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print('Frozen',len(manifest['files']),'artifacts;',file_hash(RELEASE/'manifest.json'))

def verify():
    m=read_json(RELEASE/'manifest.json');bad=[]
    for rel,expected in m['files'].items():
        p=ROOT/rel
        if not p.is_file() or file_hash(p)!=expected:
            bad.append(rel)
    print(json.dumps({'checked':len(m['files']),'mismatches':bad},indent=2))
    return not bad

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['build','freeze','verify','query'])
    parser.add_argument('--entity',default='IL7R')
    args=parser.parse_args()
    if args.command=='build':
        return 0 if build() else 1
    if args.command=='freeze':
        freeze();return 0
    if args.command=='verify':
        return 0 if verify() else 1
    db=sqlite3.connect(RELEASE/'immune_prior.sqlite');db.row_factory=sqlite3.Row
    rows=db.execute('SELECT a.assertion_id,s.name subject,a.predicate,o.name object,a.measurement,a.direction,a.evidence_tier,a.status,c.species,c.cell_type,e.source_locator,src.url FROM edge_assertions a JOIN entities s ON a.subject_id=s.entity_id JOIN entities o ON a.object_id=o.entity_id JOIN contexts c USING(context_id) JOIN evidence_instances e USING(assertion_id) JOIN source_registry src USING(source_id) WHERE s.name LIKE ? OR o.name LIKE ? ORDER BY a.assertion_id',('%'+args.entity+'%','%'+args.entity+'%')).fetchall()
    print(json.dumps([dict(r) for r in rows],indent=2,ensure_ascii=False));db.close();return 0

if __name__=='__main__':
    sys.exit(main())
