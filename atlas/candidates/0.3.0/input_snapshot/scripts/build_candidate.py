#!/usr/bin/env python3
"""Build a source-bound, unreviewed supplement without changing accepted evidence.

Standard library only. This is a candidate compiler, never a review or prior engine.
"""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.3.0'
BASELINE = 'releases/0.2.0/immune_prior.sqlite'
BASELINE_MANIFEST = 'releases/0.2.0/manifest.json'
LANES = ('genetic', 'activation', 'antigen')
CONTEXT_FIELDS = ('species ancestry age sex tissue disease disease_severity treatment_status '
                  'cell_type cell_state developmental_state stimulation dose duration assay '
                  'genomic_background time_point').split()
CHECKS = ('entity_continuity', 'context_compatibility', 'temporal_compatibility',
          'measurement_link', 'experimental_linkage', 'mediation_test')
CHECK_VALUES = {'supported', 'not_demonstrated', 'contradictory', 'not_applicable_nonserial'}
BRIDGE_TYPES = {'serial_transition', 'mediation_test', 'shared_intervention', 'context_contrast'}
PRIMARY_ACCESS_LEVELS = {'full_text', 'full_text_selected_methods_results',
                        'full_text_primary_methods_results_inspected', 'full_text_methods_results_inspected',
                        'primary_pdf_selected_methods_results'}
NA = 'unavailable'


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def identifier(prefix, value):
    return prefix + '_' + hashlib.sha256(encoded(value).encode()).hexdigest()[:20]


def read(path):
    return json.loads(Path(path).read_text())


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def known(value):
    return value is not None and str(value).strip().lower() not in {
        '', 'unavailable', 'unknown', 'not reported', 'n/a', 'na', 'unspecified'}


def local_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Missing or out-of-root input: ' + relative)
    return path


def entity_key(assertion, side):
    # Exact molecular form, layer and species; no RNA/protein or alias coalescing.
    return [assertion[side].strip(), assertion[side + '_type'],
            assertion[side + '_layer'], assertion.get('species', NA)]


def check_status(bridge, name):
    value = bridge.get('checks', {}).get(name, 'not_demonstrated')
    return value.get('status', 'not_demonstrated') if isinstance(value, dict) else value


def classify_bridge(bridge, left, right, sources):
    """Structural triage of extractor proposals, not scientific approval.

    A positive result only means the proposal is ready for review. Assertions,
    interpretation and check attestations still require independent scrutiny.
    """
    kind = bridge['bridge_type']
    reasons = []
    if kind not in BRIDGE_TYPES:
        raise ValueError('Unknown bridge type: ' + kind)
    if kind in {'shared_intervention', 'context_contrast'}:
        blocked = bridge['status'] == 'blocked_missing_evidence' or any(
            a['qc_status'] == 'needs_full_text' for a in (left, right))
        return {'classification': 'blocked_connection' if blocked else 'response_profile' if kind == 'shared_intervention' else 'context_contrast',
                'review_status': 'pending', 'serial_path': False, 'production_approved': False,
                'reasons': ['Nonserial evidence; does not establish an outcome-to-input transition.'] +
                    (['Extractor identified missing evidence or incomplete primary access.'] if blocked else [])}
    if bridge['status'] != 'candidate_pending_review':
        reasons.append('Extractor identified missing evidence.')
    if bridge['bridge_relation'] != 'supports':
        reasons.append('The proposed connection is not supporting evidence.')
    for a in (left, right):
        if a['qc_status'] != 'extracted_pending_review':
            reasons.append(a['assertion_id'] + ': primary extraction is incomplete.')
        if a['direction'] == 'null' or a.get('evidence_relation') in {'opposes', 'inconclusive'}:
            reasons.append(a['assertion_id'] + ': null, opposing or inconclusive endpoint.')
        if sources[a['source_id']].get('access_level') not in PRIMARY_ACCESS_LEVELS:
            reasons.append(a['assertion_id'] + ': relevant primary full text is unavailable.')
    if not known(left.get('species')) or left.get('species') != right.get('species'):
        reasons.append('Species is unknown or differs between endpoints.')
    required = CHECKS if kind == 'mediation_test' else CHECKS[:-1]
    for name in required:
        if check_status(bridge, name) != 'supported':
            reasons.append(name + ': ' + check_status(bridge, name))
    if kind == 'serial_transition' and entity_key(left, 'object') != entity_key(right, 'subject'):
        reasons.append('Exact molecular entity/state continuity is absent; an explicit intermediate assertion is required.')
    for name in ('entity_mapping', 'context_comparison', 'temporal_basis',
                 'measurement_basis', 'experimental_linkage', 'source_locators',
                 'supporting_snapshot_paths'):
        if not bridge.get(name) or not known(bridge.get(name)):
            reasons.append(name + ': supporting documentation is missing.')
    return {'classification': 'blocked_connection' if reasons else 'mechanism_proposal',
            'review_status': 'pending', 'serial_path': kind == 'serial_transition' and not reasons,
            'production_approved': False, 'reasons': reasons or [
                'Extractor attestations and source dependencies are present; scientific review has not begun.']}


def keyed(items, key, label):
    result = {}
    for item in items:
        if item[key] in result:
            raise ValueError('Duplicate ' + label + ': ' + item[key])
        result[item[key]] = item
    return result


def source_paths(source):
    paths = [source['snapshot_path']]
    if known(source.get('companion_snapshot_path')):
        paths.append(source['companion_snapshot_path'])
    for field in ('additional_snapshot_paths', 'supporting_snapshot_paths', 'additional_snapshots'):
        paths.extend(source.get(field, []))
    return sorted(set(paths))


def load_bundle(root):
    scope = read(root / 'data/product_scope.json')
    if scope.get('cytokine_scope') != 'all_cytokines' or scope.get('fixed_priority_panel') is not None:
        raise ValueError('Current scope must include all cytokines without a fixed priority panel.')
    if sha(root / BASELINE) != read(root / BASELINE_MANIFEST)['files'][BASELINE]:
        raise ValueError('Baseline database differs from its frozen manifest.')
    bundle = {k: [] for k in ('sources', 'cohorts', 'assertions', 'bridges', 'searches', 'screening', 'gaps')}
    bundle['lanes'] = {}
    inputs = {'README.md', 'RUNNING.md', 'protocol/PROTOCOL.md', 'protocol/PRODUCT_SCOPE.md',
              'protocol/AMENDMENT_0.3.md', 'data/product_scope.json', 'data/cytokine_inventory.json',
              'data/cytokine_inventory.csv', 'data/CANDIDATE_DATA_DICTIONARY.md', 'research/EXTRACTION_CONTRACT_0.3.md',
              'scripts/build_candidate.py', 'scripts/build_cytokine_inventory.py', 'scripts/sanitize_snapshots.py',
              'tests/test_candidate.py', BASELINE, BASELINE_MANIFEST}
    inputs.add('provenance/candidate_preparation_0.3.json')
    for directory in ['research/cytokine_inventory'] + ['research/mechanisms_' + lane for lane in LANES]:
        inputs.update(str(p.relative_to(root)) for p in (root / directory).rglob('*')
                      if p.is_file() and '__pycache__' not in p.parts)
    for lane in LANES:
        folder = 'research/mechanisms_' + lane
        pack = read(root / folder / 'pack.json')
        screening = read(root / folder / 'screening.json')
        bridges = read(root / folder / 'bridges.json')
        bridge_records = bridges['bridges'] if isinstance(bridges, dict) else bridges
        candidates = screening.get('candidate_appearances', screening.get('candidates', [])) if isinstance(screening, dict) else screening
        if not isinstance(candidates, list):
            raise ValueError('Candidate-level screening list required: ' + lane)
        bundle['lanes'][lane] = {'synthesis': pack.get('synthesis', NA),
                                 'screening_metadata': screening,
                                 'run': read(root / folder / 'run.json')}
        for name in ('sources', 'cohorts', 'assertions', 'searches', 'gaps'):
            for row in pack[name]:
                bundle[name].append(dict(row, lane=lane, pack_path=folder + '/pack.json'))
        bundle['bridges'].extend(dict(b, lane=lane, pack_path=folder + '/bridges.json') for b in bridge_records)
        bundle['screening'].extend(dict(c, lane=lane) for c in candidates)
    sources = keyed(bundle['sources'], 'source_id', 'source')
    cohorts = keyed(bundle['cohorts'], 'cohort_id', 'cohort')
    assertions = keyed(bundle['assertions'], 'assertion_id', 'assertion')
    keyed(bundle['bridges'], 'bridge_id', 'bridge')
    searches = keyed(bundle['searches'], 'search_id', 'search')
    keyed(bundle['screening'], 'candidate_id', 'screened candidate')
    for source in sources.values():
        source['source_dependencies'] = {p: sha(local_path(root, p)) for p in source_paths(source)}
        inputs.update(source_paths(source))
    for assertion in assertions.values():
        if assertion['qc_status'] not in {'extracted_pending_review', 'needs_full_text'}:
            raise ValueError('New evidence must remain unreviewed: ' + assertion['assertion_id'])
        if assertion['source_id'] not in sources or assertion['cohort_id'] not in cohorts:
            raise ValueError('Broken assertion source/cohort: ' + assertion['assertion_id'])
        if assertion['qc_status'] == 'extracted_pending_review' and sources[assertion['source_id']].get('access_level') not in PRIMARY_ACCESS_LEVELS:
            raise ValueError('Completed extraction lacks registered primary full-text access: ' + assertion['assertion_id'])
        for field in ('source_locator', 'evidence_summary', 'subject', 'object', 'measurement'):
            if not known(assertion.get(field)):
                raise ValueError('Missing ' + field + ': ' + assertion['assertion_id'])
        if assertion['subject_layer'] not in {'G', 'T', 'P', 'C', 'F'} or assertion['object_layer'] not in {'G', 'T', 'P', 'C', 'F'}:
            raise ValueError('Unknown molecular layer: ' + assertion['assertion_id'])
        measurement_layers = {'RNA_abundance': {'T'}, 'splicing': {'T'},
            'direct_transcriptional_regulation': {'T'}, 'chromatin_accessibility': {'G'},
            'TF_occupancy': {'G', 'P'}, 'protein_abundance': {'P'}, 'protein_activity': {'P'},
            'secreted_protein': {'P'}, 'binding': {'P'}, 'peptide_presentation': {'P'},
            'immunopeptidome': {'P'}, 'receptor_signaling': {'P', 'C'}, 'cellular_phenotype': {'F'}}
        if assertion['measurement'] in measurement_layers and assertion['object_layer'] not in measurement_layers[assertion['measurement']]:
            raise ValueError('Measurement/object-layer mismatch: ' + assertion['assertion_id'])
        paths = set(sources[assertion['source_id']]['source_dependencies'])
        paths.update(assertion.get('supporting_snapshot_paths', []))
        paths.add(assertion['pack_path'])
        assertion['source_dependencies'] = {p: sha(local_path(root, p)) for p in sorted(paths)}
        inputs.update(paths)
    for candidate in bundle['screening']:
        if candidate['decision'] not in {'include', 'exclude', 'await_full_text'}:
            raise ValueError('Unknown screening decision: ' + candidate['candidate_id'])
        if candidate['query_id'] not in searches:
            raise ValueError('Unregistered screening query: ' + candidate['candidate_id'])
    for assertion in assertions.values():
        source = sources[assertion['source_id']]
        decisions = [c['decision'] for c in bundle['screening'] if
            c.get('source_id') == source['source_id'] or
            (known(c.get('doi')) and str(c['doi']).lower() == str(source.get('doi', '')).lower())]
        eligible = {'include'} if assertion['qc_status'] == 'extracted_pending_review' else {'include', 'await_full_text'}
        if not eligible.intersection(decisions):
            raise ValueError('Extracted source lacks an eligible screening decision: ' + assertion['assertion_id'])
    for bridge in bundle['bridges']:
        if bridge['status'] not in {'candidate_pending_review', 'blocked_missing_evidence'}:
            raise ValueError('Bridge cannot be approved in this phase.')
        if bridge['bridge_relation'] not in {'supports', 'opposes', 'inconclusive'}:
            raise ValueError('Unknown bridge evidence relation.')
        for name in CHECKS:
            if check_status(bridge, name) not in CHECK_VALUES:
                raise ValueError('Invalid bridge check: ' + bridge['bridge_id'] + ':' + name)
        left, right = (assertions[bridge[k]] for k in ('from_assertion_id', 'to_assertion_id'))
        paths = set(left['source_dependencies']) | set(right['source_dependencies'])
        paths.update(bridge.get('supporting_snapshot_paths', []))
        paths.add(bridge['pack_path'])
        for source_id in bridge['source_ids']:
            paths.update(sources[source_id]['source_dependencies'])
        bridge['source_dependencies'] = {p: sha(local_path(root, p)) for p in sorted(paths)}
        bridge['triage'] = classify_bridge(bridge, left, right, sources)
        inputs.update(paths)
    bundle['inventory'] = read(root / 'data/cytokine_inventory.json')
    for item in bundle['inventory']:
        if sha(local_path(root, item['snapshot_path'])) != item['snapshot_sha256']:
            raise ValueError('Inventory source hash mismatch: ' + item['inventory_id'])
    bundle['input_hashes'] = {p: sha(local_path(root, p)) for p in sorted(inputs)}
    spec = importlib.util.spec_from_file_location('candidate_snapshot_scanner', root / 'scripts/sanitize_snapshots.py')
    scanner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scanner)
    unsafe = [str(path.relative_to(root)) for path, _, _ in scanner.findings(root / p for p in inputs)]
    if unsafe:
        raise ValueError('Credential metadata must be sanitized before candidate build: ' + ', '.join(unsafe))
    bundle['scope'] = scope
    return bundle


SCHEMA = {
    'candidate_entities': 'entity_id TEXT PRIMARY KEY, name TEXT, entity_type TEXT, layer TEXT, species TEXT, mapping_status TEXT',
    'candidate_contexts': 'context_id TEXT PRIMARY KEY, ' + ', '.join(x + ' TEXT' for x in CONTEXT_FIELDS),
    'candidate_sources': 'source_id TEXT PRIMARY KEY, title TEXT, doi TEXT, url TEXT, access_level TEXT, lane TEXT, baseline_source_ids TEXT, source_dependencies TEXT, payload TEXT',
    'candidate_cohorts': 'cohort_id TEXT PRIMARY KEY, source_id TEXT, lane TEXT, payload TEXT',
    'candidate_assertions': ('assertion_id TEXT PRIMARY KEY, subject_id TEXT REFERENCES candidate_entities, predicate TEXT, '
        'object_id TEXT REFERENCES candidate_entities, context_id TEXT REFERENCES candidate_contexts, '
        'source_id TEXT REFERENCES candidate_sources, cohort_id TEXT REFERENCES candidate_cohorts, '
        'measurement TEXT, direction TEXT, qc_status TEXT, lane TEXT, source_locator TEXT, '
        'evidence_summary TEXT, limitations TEXT, source_dependencies TEXT, payload TEXT'),
    'candidate_bridges': ('bridge_id TEXT PRIMARY KEY, mechanism_id TEXT, from_assertion_id TEXT REFERENCES candidate_assertions, '
        'to_assertion_id TEXT REFERENCES candidate_assertions, bridge_type TEXT, bridge_relation TEXT, classification TEXT, '
        'review_status TEXT, production_approved INTEGER CHECK(production_approved=0), reasons TEXT, source_dependencies TEXT, payload TEXT'),
    'candidate_graphs': 'mechanism_id TEXT PRIMARY KEY, lane TEXT, assertion_ids TEXT, bridge_ids TEXT, classifications TEXT, review_status TEXT, graph TEXT',
    'candidate_searches': 'search_id TEXT PRIMARY KEY, lane TEXT, query TEXT, database_name TEXT, searched_at TEXT, payload TEXT',
    'candidate_screening': 'candidate_id TEXT PRIMARY KEY, query_id TEXT REFERENCES candidate_searches, title TEXT, doi TEXT, decision TEXT, reason TEXT, lane TEXT, payload TEXT',
    'candidate_gaps': 'gap_id TEXT PRIMARY KEY, lane TEXT, description TEXT, status TEXT, payload TEXT',
    'cytokine_inventory': 'inventory_id TEXT PRIMARY KEY, uniprot_accession TEXT, gene_symbol TEXT, resource_annotation_status TEXT, inventory_status TEXT, source_url TEXT, payload TEXT',
    'candidate_inputs': 'path TEXT PRIMARY KEY, sha256 TEXT',
    'candidate_metadata': 'key TEXT PRIMARY KEY, value TEXT',
}


def insert(db, table, row):
    columns = [r[1] for r in db.execute('PRAGMA table_info(' + table + ')')]
    values = {c: (encoded(row[c]) if isinstance(row.get(c), (dict, list)) else row.get(c)) for c in columns}
    db.execute('INSERT INTO ' + table + ' (' + ','.join(columns) + ') VALUES (' +
               ','.join('?' for _ in columns) + ')', list(values.values()))


def table_fingerprints(db, tables):
    return {table: identifier('ROWS', sorted([list(r) for r in db.execute('SELECT * FROM ' + table)], key=encoded))
            for table in tables}


def graphs_for(bundle, assertion_rows):
    grouped = defaultdict(list)
    for bridge in bundle['bridges']:
        grouped[bridge['mechanism_id']].append(bridge)
    graphs = []
    for mechanism_id, bridges in sorted(grouped.items()):
        aids = sorted({b[k] for b in bridges for k in ('from_assertion_id', 'to_assertion_id')})
        nodes = sorted({assertion_rows[a][k] for a in aids for k in ('subject_id', 'object_id')})
        # Connections are separate from measured assertion edges. In particular,
        # branches and mediation tests cannot be traversed as serial transitions.
        graph = {'entity_ids': nodes, 'assertion_edges': [assertion_rows[a] for a in aids],
                 'connection_proposals': [{k: b[k] for k in ('bridge_id', 'bridge_type', 'from_assertion_id',
                      'to_assertion_id', 'triage')} for b in bridges],
                 'serial_transitions': [b['bridge_id'] for b in bridges if b['triage']['serial_path']],
                 'production_approved_paths': []}
        graphs.append({'mechanism_id': mechanism_id, 'lane': bridges[0]['lane'], 'assertion_ids': aids,
                       'bridge_ids': [b['bridge_id'] for b in bridges],
                       'classifications': dict(Counter(b['triage']['classification'] for b in bridges)),
                       'review_status': 'pending', 'graph': graph})
    return graphs


def build_database(root, target, bundle):
    shutil.copyfile(root / BASELINE, target)
    db = sqlite3.connect(target)
    db.execute('PRAGMA foreign_keys=ON')
    baseline_tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
    before = table_fingerprints(db, baseline_tables)
    for table, schema in SCHEMA.items():
        db.execute('CREATE TABLE ' + table + ' (' + schema + ')')
    inherited_dois = defaultdict(list)
    for sid, doi in db.execute('SELECT source_id, doi FROM source_registry'):
        if known(doi):
            inherited_dois[doi.lower().removeprefix('https://doi.org/')].append(sid)
    reused_sources = {}
    for item in bundle['sources']:
        previous = sorted(inherited_dois.get(str(item.get('doi', '')).lower().removeprefix('https://doi.org/'), []))
        if previous:
            reused_sources[item['source_id']] = previous
        insert(db, 'candidate_sources', dict(item, baseline_source_ids=previous, payload=item))
    for item in bundle['cohorts']:
        insert(db, 'candidate_cohorts', dict(item, source_id=item.get('study_id'), payload=item))
    entities, contexts, assertions = {}, {}, {}
    for a in bundle['assertions']:
        entity_ids = {}
        for side in ('subject', 'object'):
            key = entity_key(a, side)
            eid = identifier('CENTITY', key)
            entities[eid] = dict(zip(('name', 'entity_type', 'layer', 'species'), key), entity_id=eid,
                                 mapping_status='local_exact_form; external_mapping_unavailable')
            entity_ids[side + '_id'] = eid
        context = {k: a.get(k, NA) for k in CONTEXT_FIELDS}
        cid = identifier('CCONTEXT', context)
        contexts[cid] = dict(context, context_id=cid)
        assertions[a['assertion_id']] = dict(a, **entity_ids, context_id=cid, payload=a)
    for entity in entities.values():
        insert(db, 'candidate_entities', entity)
    for context in contexts.values():
        insert(db, 'candidate_contexts', context)
    for assertion in assertions.values():
        insert(db, 'candidate_assertions', assertion)
    for b in bundle['bridges']:
        insert(db, 'candidate_bridges', dict(b, **b['triage'], payload=b))
    graphs = graphs_for(bundle, assertions)
    for graph in graphs:
        insert(db, 'candidate_graphs', graph)
    for search in bundle['searches']:
        insert(db, 'candidate_searches', dict(search, database_name=search.get('database'), payload=search))
    for item in bundle['screening']:
        insert(db, 'candidate_screening', dict(item, payload=item))
    for item in bundle['gaps']:
        insert(db, 'candidate_gaps', dict(item, payload=item))
    for item in bundle['inventory']:
        insert(db, 'cytokine_inventory', dict(item, payload=item))
    for path, digest in bundle['input_hashes'].items():
        insert(db, 'candidate_inputs', {'path': path, 'sha256': digest})
    after = table_fingerprints(db, baseline_tables)
    if before != after:
        raise ValueError('Candidate changed baseline records.')
    if db.execute('PRAGMA foreign_key_check').fetchall():
        raise ValueError('Candidate foreign-key validation failed.')
    metadata = {'version': VERSION + '-candidate', 'review_status': 'pending_user_triggered_review',
                'scope': bundle['scope'], 'baseline_sha256': sha(root / BASELINE),
                'baseline_tables_unchanged': before == after,
                'baseline_table_fingerprints': before, 'sources_reusing_baseline_doi': reused_sources,
                'new_priors': 0, 'new_approved_paths': 0}
    for key, value in metadata.items():
        insert(db, 'candidate_metadata', {'key': key, 'value': encoded(value)})
    db.commit()
    counts = {t: db.execute('SELECT COUNT(*) FROM ' + t).fetchone()[0] for t in SCHEMA}
    for table in SCHEMA:
        if table == 'candidate_metadata':
            continue
        cursor = db.execute('SELECT * FROM ' + table + ' ORDER BY 1')
        with (target.parent / (table + '.csv')).open('w', newline='') as out:
            writer = csv.writer(out)
            writer.writerow([c[0] for c in cursor.description])
            writer.writerows(cursor)
    db.close()
    return metadata, counts, graphs


def make_report(bundle, qc, graphs):
    classes = qc['connection_classifications']
    inventory_counts = Counter(i['resource_annotation_status'] for i in bundle['inventory'])
    bridge_labels = {'serial_transition': 'Serial transition', 'mediation_test': 'Intermediate perturbation/rescue',
                     'shared_intervention': 'Shared intervention', 'context_contrast': 'Context contrast'}
    class_labels = {'mechanism_proposal': 'Pending mechanism review', 'response_profile': 'Response profile',
                    'context_contrast': 'Context contrast', 'blocked_connection': 'Blocked connection'}
    lines = ['# Immune evidence candidate 0.3.0', '',
             'Steps 1–3 are prepared for a review the user will trigger separately. No independent review has been started for this candidate.', '',
             'All cytokines and broader immune genetic, transcriptional, proteomic, signaling and cellular mechanisms are in scope. Historical assay labels are provenance only.', '',
             f"The candidate contains {len(bundle['assertions'])} new pending-review assertions, {len(bundle['sources'])} source records, "
             f"{len(bundle['screening'])} screened candidate appearances and {len(graphs)} mechanism dossiers. "
             'Publication counts are not independent replication counts. New extracts from inherited papers remain linked to their original records.', '',
             f"{len(qc['sources_reusing_baseline_doi'])} source records reuse a DOI already present in the baseline. "
             f"{qc['assertion_review_states'].get('extracted_pending_review', 0)} assertions have inspected primary Methods and Results; "
             f"{qc['assertion_review_states'].get('needs_full_text', 0)} still need complete primary details. All await review.", '',
             f"The connection proposals comprise {classes.get('mechanism_proposal', 0)} mechanisms ready for scientific scrutiny, "
             f"{classes.get('response_profile', 0)} shared-intervention response profiles, {classes.get('context_contrast', 0)} context contrasts "
             f"and {classes.get('blocked_connection', 0)} blocked connections. These are extractor proposals, not validated pathways.", '',
             'The baseline database records, including its uncalibrated priors and review history, are unchanged. New evidence is stored only in candidate tables. No new numerical prior or approved production pathway is created.', '',
             '## All-cytokine discovery inventory', '',
             f"The complete human UniProt keyword KW-0202 / GO:0005125 queries return {inventory_counts['reviewed']} reviewed resource entries and {inventory_counts['unreviewed']} unreviewed discovery entries. "
             'These are resource records; the total is not a count of distinct active cytokines or evidence-reviewed entities. The inventory does not limit eligibility; '
             'literature-supported cytokines, isoforms and complexes outside these annotations remain eligible.', '',
             'Queries, source snapshots, counts and limits are preserved in `input_snapshot/research/cytokine_inventory/`. No resource membership becomes a biological edge.', '',
             '## Evidence dossiers', '']
    assertions = {a['assertion_id']: a for a in bundle['assertions']}
    for lane, data in bundle['lanes'].items():
        lines.extend(['### ' + lane.capitalize(), '', data['synthesis'], '',
                      f"[Extraction notes](input_snapshot/research/mechanisms_{lane}/notes.md) · "
                      f"[Screening](input_snapshot/research/mechanisms_{lane}/screening.json)", ''])
        for b in [b for b in bundle['bridges'] if b['lane'] == lane]:
            left, right = assertions[b['from_assertion_id']], assertions[b['to_assertion_id']]
            lines.extend([f"**{b['bridge_id']} · {b['mechanism_id']} · {bridge_labels[b['bridge_type']]} · {class_labels[b['triage']['classification']]}**", '',
                          b['evidence_summary'], '',
                          f"Endpoints: {left['assertion_id']} ({left['subject']} → {left['object']}); "
                          f"{right['assertion_id']} ({right['subject']} → {right['object']}).", '',
                          '**Scope and limits:** ' + str(b.get('limitations', NA)), '',
                          '**Structural checks:** ' + '. '.join(r.rstrip('.') for r in b['triage']['reasons']) + '.', '',
                          'Sources: ' + '; '.join('[' + sid + '](' + next(s['url'] for s in bundle['sources'] if s['source_id'] == sid) + ')' for sid in b['source_ids']) +
                          '. Locators: ' + '; '.join(b['source_locators']), ''])
    lines.extend(['## Questions for the later review', '',
                  '1. Do the primary Methods, results and original figures support each narrow assertion and reported result?',
                  '2. Do rescue/intermediate perturbations support the proposed dependence, with appropriate off-target and engineered-system limits?',
                  '3. Are donor overlap, species, cell preparation, timing, assay specificity and original cohort reuse accurately represented?',
                  '4. Are nulls and contrary observations preserved without interpreting nonsignificance as absence?',
                  '5. Should any blocked transition be reconsidered only after additional primary evidence, rather than by relabeling a branch?',
                  '6. Are proposed corrections to inherited records justified, especially whole-blood versus PBMC preparation?', '',
                  '## Remaining evidence gaps', ''])
    for gap in bundle['gaps']:
        lines.append('- **' + gap['gap_id'] + '**: ' + gap.get('description', str(gap)))
    lines.extend(['', '## Validation and use', '',
                  'Structural checks cover references, exact source hashes, pending-review states, molecular entity separation and conservative connection rules. '
                  'These checks do not replace biological review. Ranked literature searches are documented focused retrievals, not an exhaustive systematic review.', '',
                  '`immune_candidate.sqlite` includes the unchanged baseline tables plus `candidate_*` tables and the discovery-only `cytokine_inventory`. '
                  'All candidate tables are also exported as CSV. `mechanism_graphs.json` stores measured assertion edges separately from connection proposals; '
                  'response profiles and context contrasts cannot be traversed as serial paths.', '',
                  '`input_manifest.json` and `input_snapshot/` preserve the exact candidate inputs. The copied baseline database is bound to its frozen manifest; '
                  'the full historical evidence provenance remains in Release 0.2.0. Candidate inputs do not duplicate the entire historical source archive.', ''])
    return '\n'.join(lines)


def build(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output.is_relative_to(root / 'releases') or output == root:
        raise ValueError('Candidate output cannot overwrite a release or project root.')
    bundle = load_bundle(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='immune-candidate-', dir=output.parent) as temporary:
        staging = Path(temporary)
        metadata, counts, graphs = build_database(root, staging / 'immune_candidate.sqlite', bundle)
        qc = dict(metadata, counts=counts,
                  connection_classifications=dict(Counter(b['triage']['classification'] for b in bundle['bridges'])),
                  screening_decisions=dict(Counter(c['decision'] for c in bundle['screening'])),
                  assertion_review_states=dict(Counter(a['qc_status'] for a in bundle['assertions'])),
                  candidate_source_dois=len({s['doi'].lower() for s in bundle['sources'] if known(s.get('doi'))}),
                  source_binding_status='exact_sha256; pending scientific review',
                  literature_search_status='focused ranked searches; not exhaustive')
        write(staging / 'qc.json', qc)
        write(staging / 'mechanism_graphs.json', graphs)
        write(staging / 'input_manifest.json', {'version': VERSION + '-candidate', 'files': bundle['input_hashes']})
        (staging / 'REVIEW_PACKET.md').write_text(make_report(bundle, qc, graphs))
        for relative in bundle['input_hashes']:
            target = staging / 'input_snapshot' / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / relative, target)
            if sha(target) != bundle['input_hashes'][relative]:
                raise ValueError('Input changed during build: ' + relative)
        write(staging / 'manifest.json', {'status': 'candidate_pending_review; not production release',
              'files': {str(p.relative_to(staging)): sha(p) for p in sorted(staging.rglob('*')) if p.is_file()}})
        if output.exists():
            # Only replace an output previously generated by this compiler.
            if not (output / 'manifest.json').is_file() or not (output / 'input_manifest.json').is_file():
                raise ValueError('Refusing to replace an unrelated directory: ' + str(output))
            shutil.rmtree(output)
        shutil.copytree(staging, output)
    return qc


def verify(output, working_root=None):
    output = Path(output)
    manifest = read(output / 'manifest.json')
    mismatches = [p for p, expected in manifest['files'].items()
                  if not (output / p).is_file() or sha(output / p) != expected]
    if working_root:
        mismatches.extend('working:' + p for p, expected in read(output / 'input_manifest.json')['files'].items()
                          if not (Path(working_root) / p).is_file() or sha(Path(working_root) / p) != expected)
    return {'ok': not mismatches, 'mismatches': mismatches, 'review_status': 'pending'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'query'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check-working', action='store_true')
    parser.add_argument('--entity', default='')
    args = parser.parse_args()
    output = args.output or args.root / 'candidates' / VERSION
    if args.command == 'build':
        result = build(args.root, output)
        print(json.dumps({k: result[k] for k in ('counts', 'connection_classifications', 'baseline_tables_unchanged', 'review_status')}, indent=2))
    elif args.command == 'verify':
        result = verify(output, args.root if args.check_working else None)
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if result['ok'] else 1)
    else:
        db = sqlite3.connect('file:' + str(output / 'immune_candidate.sqlite') + '?mode=ro', uri=True)
        db.row_factory = sqlite3.Row
        rows = db.execute('SELECT a.assertion_id, s.name AS subject, a.predicate, o.name AS object, '
                          'a.measurement, a.direction, a.qc_status, a.source_locator, a.evidence_summary '
                          'FROM candidate_assertions a JOIN candidate_entities s ON s.entity_id=a.subject_id '
                          'JOIN candidate_entities o ON o.entity_id=a.object_id WHERE s.name LIKE ? OR o.name LIKE ? '
                          'ORDER BY a.assertion_id', ('%' + args.entity + '%', '%' + args.entity + '%'))
        print(json.dumps([dict(r) for r in rows], ensure_ascii=False, indent=2))
        db.close()


if __name__ == '__main__':
    main()
