"""Register source-owned supporting snapshots without changing evidence judgments."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

D = Path('research/mechanisms_activation')
now = datetime.now(timezone.utc).isoformat()
pack = json.loads((D / 'pack.json').read_text())
bridges = json.loads((D / 'bridges.json').read_text())
original_assertion_status = {x['assertion_id']: x['qc_status'] for x in pack['assertions']}
original_bridge_status = {x['bridge_id']: x['status'] for x in bridges}
registry = {}

def classification(path, sid):
    name = path.name
    if '.failed.' in name or name == 'MA_S06_web.json':
        return ('failed_retrieval_response', 'failed_access; not primary evidence', False)
    if '_correction_' in name:
        return ('correction_notice_metadata' if name.endswith('_metadata.json') else 'primary_correction_notice', 'primary_notice_inspected; competing-interest disclosure only', True)
    if '_fig3_' in name or '_fig4_' in name:
        return ('figure_page_metadata' if name.endswith('_metadata.json') else 'primary_figure_caption', 'public_caption_inspected; figure image not inspected', True)
    if '_methods.' in name:
        return ('supplementary_analytical_methods', 'public_analysis_supplement_inspected; main wet-lab Methods unavailable', True)
    if name.endswith('_metadata.json'):
        return ('article_page_metadata', 'metadata_extracted_from_retrieved_primary_page', True)
    if sid == 'MA-S06':
        return ('subscription_limited_primary_article', 'abstract_and_extended_data_captions; main wet-lab Methods/Results unavailable', True)
    return ('primary_article_html' if path.suffix == '.html' else 'primary_article_text_conversion', 'primary_full_text; selected Methods/Results inspected', True)

for source in pack['sources']:
    sid = source['source_id']
    prefix = sid.replace('-', '_')
    additional, failed, details = [], [], []
    for path in sorted((D / 'snapshots').glob(prefix + '*')):
        role, access, supports_evidence = classification(path, sid)
        rel = str(path)
        entry = {'path': rel, 'source_id': sid, 'snapshot_role': role, 'access_level': access, 'eligible_as_supporting_snapshot': supports_evidence}
        if '_correction_' in path.name:
            entry.update(resource_doi='10.1038/s41586-025-09356-6', resource_relation='corrects_competing_interest_disclosure_of_MA-S06', resource_url='https://www.nature.com/articles/s41586-025-09356-6')
        details.append(entry)
        registry[rel] = entry
        if supports_evidence and rel != source['snapshot_path']:
            additional.append(rel)
        elif not supports_evidence:
            failed.append(rel)
    source['additional_snapshot_paths'] = additional
    source['failed_retrieval_snapshot_paths'] = failed
    source['snapshot_provenance'] = details

sources = {x['source_id']: x for x in pack['sources']}
for assertion in pack['assertions']:
    source = sources[assertion['source_id']]
    registered = {source['snapshot_path'], *source['additional_snapshot_paths']}
    for path in assertion['supporting_snapshot_paths']:
        assert path in registered, ('unregistered assertion snapshot', assertion['assertion_id'], path)
        assert Path(path).exists(), path
        assert registry[path]['eligible_as_supporting_snapshot'], path
for bridge in bridges:
    registered = set()
    for sid in bridge['source_ids']:
        source = sources[sid]
        registered.update([source['snapshot_path'], *source['additional_snapshot_paths']])
    for path in bridge['supporting_snapshot_paths']:
        assert path in registered, ('unregistered bridge snapshot', bridge['bridge_id'], path)
        assert Path(path).exists(), path
        assert registry[path]['eligible_as_supporting_snapshot'], path
assert original_assertion_status == {x['assertion_id']: x['qc_status'] for x in pack['assertions']}
assert original_bridge_status == {x['bridge_id']: x['status'] for x in bridges}
(D / 'pack.json').write_text(json.dumps(pack, indent=2, ensure_ascii=False) + '\n')

manifest = []
for path in sorted((D / 'snapshots').iterdir()):
    if not path.is_file():
        continue
    info = registry.get(str(path), {'source_id': 'unavailable', 'snapshot_role': 'search_tool_response', 'access_level': 'discovery_only', 'eligible_as_supporting_snapshot': False})
    manifest.append({'path': str(path), 'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), **{k: v for k, v in info.items() if k != 'path'}})
(D / 'source_manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')

run = json.loads((D / 'run.json').read_text())
run['timestamp_end'] = now
update = {'timestamp': now, 'operation': 'source_snapshot_registration', 'role': 'provenance completion; not scientific review', 'sources_updated': len(sources), 'registered_supporting_files': sum(len(x['additional_snapshot_paths']) + 1 for x in pack['sources']), 'registered_failed_retrieval_files': sum(len(x['failed_retrieval_snapshot_paths']) for x in pack['sources']), 'all_assertion_supporting_files_registered_under_source': True, 'all_bridge_supporting_files_registered_under_source': True, 'assertion_and_bridge_statuses_preserved': True, 'source_access_limitations_preserved': True}
run.setdefault('provenance_updates', []).append(update)
run['structural_validation']['source_snapshot_registration'] = update
run['provenance_integrity'] = {'pack_sha256': hashlib.sha256((D / 'pack.json').read_bytes()).hexdigest(), 'source_manifest_sha256': hashlib.sha256((D / 'source_manifest.json').read_bytes()).hexdigest(), 'checked_at': now, 'scope': 'Source file integrity and registration only; no review or release freeze.'}
(D / 'run.json').write_text(json.dumps(run, indent=2, ensure_ascii=False) + '\n')
print(json.dumps(update, indent=2))
