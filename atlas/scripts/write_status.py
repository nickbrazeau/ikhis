#!/usr/bin/env python3
"""Record every original README checklist item without marking coverage complete."""
from pathlib import Path
import argparse
import json
import re
ROOT=Path(__file__).resolve().parents[1]
IMPLEMENTED={'Greenfield review','Multi-layer mechanistic framework','Adversarial reviewer','Prior-only versioning','LLM/instruction provenance','Expand scope to genomics','Expand scope to transcriptomics','Expand scope to proteomics','Final protocol','Hash/register protocol','Final adjudication rules','Release policy','frozen initial corpus','genomic critique','causal-gene critique','transcriptomic critique','proteomic critique','cytokine critique','cross-omic compatibility critique','duplicate-cohort critique','network topology critique','entity tables','genomic evidence tables','transcriptomic evidence tables','proteomic evidence tables','cytokine interaction tables','critic findings','source manifest','provenance manifest','protocol/instruction manifest','QC report','freeze/hash Release 0.1'}
PENDING={'human adjudication','magnitude priors','temporal priors','genetic-modifier priors','expression priors','protein-availability priors','human-transportability priors','integrated multi-omic paths'}
EXPLANATIONS={
'Final protocol':'Operational v0.1.0 plus coverage/release amendment v0.2.0; no claim of external preregistration or human approval.',
'Hash/register protocol':'SHA-256 registered locally in instruction and release manifests; no external registry.',
'Final adjudication rules':'Agent correction, contested evidence, propagation and human-pending states explicit.',
'Journal modifier':'Bounded proposal implemented and tested; authoritative JCR data unavailable; neutral multiplier.',
'versions/retrieval dates/hashes':'Actual snapshots hashed and dates retained; unspecified external resource versions remain unavailable.',
'Cytokine search':'Actual discovery queries saved; bounded retrieval and pilot extraction only.',
'genomic search':'Actual discovery queries saved; bounded retrieval and pilot extraction only.',
'transcriptomic search':'Actual discovery queries saved; bounded retrieval and pilot extraction only.',
'proteomic search':'Actual discovery queries saved; bounded retrieval and pilot extraction only.',
'family/entity-specific searches':'29 protein-symbol PubMed queries plus four lanes; ten relevance-ranked IDs each; original aliases retained in mapping.',
'citation chaining':'Anchor-driven follow-up sources collected; no exhaustive backward/forward citation graph.',
'deduplication':'Known publication-family and duplicate-preprint relations retained; full search corpus unscreened.',
'cohort deduplication':'Known parent/subset relations and conservative unresolved grouping implemented; sample-level overlap incomplete.',
'frozen initial corpus':'27 included source records / 26 publication families; 72 assertions; explicitly bounded.',
'human adjudication':'Pending. No agent action has been labeled human review.',
'integrated multi-omic paths':'Empty by design: eight candidate joins fail context/bridge checks; complete source-backed path extraction remains.',
'existence priors':'Explicit-hypothesis Beta summaries available for eligible records; heuristic and uncalibrated.',
'direction priors':'Separate Dirichlet summaries; null adequacy and individual eligibility enforced; uncalibrated.',
'effect-class priors':'Observed categorical directions exported; no magnitude inference.',
'context-specific priors':'Context annotations retained; quantitative transport calibration unavailable.',
'journal-modifier sensitivity analysis':'No-journal results exported; equal to default because authoritative metrics unavailable and weighting disabled.',
'prior tables':'All ten parameter families exported; unsupported numeric families explicitly unavailable.',
'freeze/hash Release 0.1':'Original local release and manifest preserved; archived inputs allow verification after working files change. Whole-review completion not claimed.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--release',default='0.2.0');args=parser.parse_args()
    qcpath=ROOT/'releases'/args.release/'qc.json'
    qc=json.loads(qcpath.read_text());counts=qc['counts']
    EXPLANATIONS['frozen initial corpus']='Original 0.1.0 corpus retained; current release has '+str(counts['edge_assertions'])+' assertions. Corpus selection remains bounded.'
    EXPLANATIONS['integrated multi-omic paths']=str(counts['materialized_paths'])+' complete paths; '+str(counts['multiomic_links'])+' candidate joins subjected to context/bridge checks.'
    EXPLANATIONS['prior tables']='All ten families exported; real changes tracked against the preceding release; unsupported quantitative families remain unavailable.'
    EXPLANATIONS['family/entity-specific searches']='Original capped PubMed discovery retained, plus targeted expansion searches with '+str(counts.get('screening_candidates',0))+' candidate-level decisions; search saturation not established.'
    readme=(ROOT/'README.md').read_text()
    block=readme.split('# 20. Revised project checklist',1)[1].split('# Instructions to a new Agentic Session',1)[0]
    category='';rows=[]
    for line in block.splitlines():
        if line.startswith('## '): category=line[3:]
        elif line.startswith('-  '):
            task=line[3:].strip()
            status='implemented for initial release' if task in IMPLEMENTED else 'pending scientific completion' if task in PENDING else 'partial coverage / implementation'
            detail=EXPLANATIONS.get(task,'Schema/interface present; required quantitative evidence or calibration is unavailable.' if task in PENDING else 'Implemented and represented in the frozen initial artifacts; does not imply exhaustive biological coverage.' if task in IMPLEMENTED else 'Represented in the schema, registry or bounded evidence corpus; broader extraction/verification remains.')
            rows.append({'category':category,'task':task,'status':status,'detail':detail})
    (ROOT/'data/project_checklist.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    doc='# Project implementation and scientific completion status\n\n'
    candidate_path=ROOT/'candidates/0.3.0/qc.json'
    if candidate_path.is_file():
        candidate=json.loads(candidate_path.read_text());cc=candidate['counts'];bc=candidate['connection_classifications']
        doc+='All cytokines and broader immune genetic, transcriptional, proteomic, signaling and cellular mechanisms are in scope. The fixed cytokine priority coverage set is retired. Resource inventory size and historical assay labels are not completion denominators.\n\n'
        doc+=f"Steps 1–3 are prepared in the [0.3.0 candidate review packet](../candidates/0.3.0/REVIEW_PACKET.md): {cc['candidate_assertions']} pending-review assertions, {cc['candidate_sources']} source records, {cc['candidate_cohorts']} cohort/context records, {cc['candidate_screening']} candidate appearances and {cc['candidate_graphs']} mechanism dossiers. The inventory has {cc['cytokine_inventory']} resource entries, with reviewed and unreviewed resource annotations distinguished; this is not a count of distinct active cytokines.\n\n"
        doc+=f"The connections comprise {bc.get('mechanism_proposal',0)} mechanism proposals, {bc.get('response_profile',0)} shared-intervention profiles, {bc.get('context_contrast',0)} context contrasts and {bc.get('blocked_connection',0)} blocked proposals. These are extraction-stage distinctions, not scientific approvals. New assertions are stored separately from the accepted baseline. No new priors or approved production paths were created.\n\n"
        doc+='The next action is the separately triggered review: inspect sources, narrow mechanisms, sample overlap, molecular states, contrary results and proposed corrections. Broader systematic corpus completion, human adjudication, empirical calibration and model validation remain later work. No independent review has been started for this candidate.\n\n## Preserved baseline and original checklist\n\n'
    doc+=f"Release {args.release} contains {counts['edge_assertions']} assertions, {counts['screening_decisions']} included publication/resource records, {counts['cohorts']} cohort/subset/context registry entries and historical assay aliases retained for provenance. The release report records recovered sources and corrected evidence. The checklist below distinguishes implemented infrastructure from remaining scientific work; presence of a table is not evidence coverage.\n\n"
    doc+='The initial operational protocol, local knowledge base, independent critic cycle, corrections, heuristic prior interface, exports and hash verification are implemented. The checklist below records the preserved baseline and distinguishes infrastructure from scientific completion. Assay-platform documentation is relevant only for a future measured-panel application; it does not limit project scope. Authoritative journal metrics remain unavailable.\n\n'
    doc+='## Original checklist\n\n| Section | Requirement | Status | Evidence or remaining work |\n|---|---|---|---|\n'
    for r in rows: doc+='| '+' | '.join(r.values())+' |\n'
    doc+=f"\n## Release entry points\n\n- Latest research narrative: `reports/RELEASE_{args.release}.md`\n- Initial synthesis: `reports/RESEARCH_SYNTHESIS.md`\n- Evidence atlas: `releases/{args.release}/EVIDENCE_ATLAS.md`\n- Structural and scientific QC: `releases/{args.release}/qc.json`\n- Table dictionary: `data/DATA_DICTIONARY.md`\n- Reproduction and interpretation: `RUNNING.md`\n- Detailed evidence gaps: `releases/{args.release}/coverage_gaps.csv`\n\nNo unscreened search result, local registry entry, empty table or inferred complete path is counted as a reviewed biological assertion.\n"
    (ROOT/'reports/PROJECT_STATUS.md').write_text(doc)
    print('Tracked',len(rows),'original requirements')
if __name__=='__main__':main()
