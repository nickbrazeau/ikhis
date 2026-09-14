#!/usr/bin/env python3
"""Build the IKHIS data catalog from local, versioned metadata; no network calls."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import html
import json
import math
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
IKHIS = ROOT.parent
ATLAS = IKHIS / 'atlas'
OUT = ROOT / 'catalog'
REPORTS = ROOT / 'reports'
HF = ROOT / 'sources/hr_vilage'
MISSING = {'', 'NA', 'N/A', 'NaN', 'nan', 'null', 'None', '<NA>', 'unavailable', 'unknown'}
ACCESSION = re.compile(r'GSE\d+|GSM\d+|SRP\d+|SRR\d+|PRJNA\d+|PRJEB\d+|PRJDB\d+|EGAS\d+|EGAD\d+|phs\d+(?:\.v\d+\.p\d+)?|E-MTAB-\d+|PXD\d+|MSV\d+|MTBLS\d+|SDY\d+|SAMN\d+')


def read(path):
    return json.loads(Path(path).read_text())


def dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def uid(prefix, value):
    return prefix + '_' + hashlib.sha256(dump(value).encode()).hexdigest()[:18]


def rel(path):
    return str(Path(path).relative_to(IKHIS))


def csv_rows(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames or [], [r for r in reader if any(v not in ('', None) for v in r.values())]


def export(name, rows):
    write(OUT / (name + '.json'), rows)
    columns = sorted({k for row in rows for k in row})
    with (OUT / (name + '.csv')).open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows({k: dump(v) if isinstance(v, (dict, list)) else v for k, v in row.items()} for row in rows)


def canonical_accessions(text):
    return sorted(set(ACCESSION.findall(str(text))))


def accession_url(accession):
    if accession.startswith(('GSE', 'GSM')):
        return 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + accession
    if accession.startswith(('EGAD', 'EGAS')):
        return 'https://ega-archive.org/' + ('datasets/' if accession.startswith('EGAD') else 'studies/') + accession
    if accession.startswith('E-MTAB-'):
        return 'https://www.ebi.ac.uk/biostudies/arrayexpress/studies/' + accession
    if accession.startswith('phs'):
        return 'https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=' + accession
    if accession.startswith(('SRP', 'SRR')):
        return 'https://www.ncbi.nlm.nih.gov/sra/?term=' + accession
    if accession.startswith(('PRJNA', 'PRJEB', 'PRJDB')):
        return 'https://www.ncbi.nlm.nih.gov/bioproject/?term=' + accession
    if accession.startswith('SAMN'):
        return 'https://www.ncbi.nlm.nih.gov/biosample/' + accession
    if accession.startswith('PXD'):
        return 'https://www.ebi.ac.uk/pride/archive/projects/' + accession
    if accession.startswith('SDY'):
        return 'https://www.immport.org/shared/study/' + accession
    return 'unavailable'


def classify_atlas_file(path):
    text = str(path)
    logical = text.rsplit('/input_snapshot/', 1)[-1]
    storage = 'archived_input_copy' if '/input_snapshot/' in text else 'frozen_release_output' if text.startswith('releases/') else 'candidate_output' if text.startswith('candidates/') else 'working_input'
    suffix = Path(logical).suffix.lower()
    if re.search(r'\.(?:fastq|fq|bam|cram|cel|idat|fcs)(?:\.gz)?$', logical, re.I):
        kind = 'candidate_instrument_raw_requires_format_check'
    elif 'cytokine_inventory/snapshots/' in logical or 'references/' in logical and suffix in {'.json', '.tsv', '.xml'}:
        kind = 'resource_metadata_snapshot'
    elif '/snapshots/' in logical:
        kind = 'documentary_or_repository_source_snapshot'
    elif logical.endswith('pack.json'):
        kind = 'curated_evidence_extraction'
    elif suffix in {'.sqlite', '.csv'} and (logical.startswith(('releases/', 'candidates/')) or storage.endswith('output')):
        kind = 'derived_atlas_table_or_database'
    elif suffix in {'.json', '.csv', '.tsv'}:
        kind = 'structured_curation_or_provenance'
    elif suffix in {'.py', '.sql', '.lock'} or 'requirements' in logical:
        kind = 'code_or_environment_specification'
    elif suffix == '.md':
        kind = 'documentation_or_protocol'
    else:
        kind = 'other_artifact'
    return kind, storage, logical


def atlas_inventory():
    files = []
    by_hash = defaultdict(list)
    mentions = []
    scanned_hashes = set()
    for path in sorted(ATLAS.rglob('*')):
        if not path.is_file() or any(p in {'.venv', '__pycache__', '.git'} for p in path.parts) or path.name == '.DS_Store':
            continue
        relative = str(path.relative_to(ATLAS))
        kind, storage, logical = classify_atlas_file(relative)
        digest = sha(path)
        record = {'file_id': uid('AFILE', rel(path)), 'path': rel(path), 'atlas_relative_path': relative,
                  'logical_path': logical, 'bytes': path.stat().st_size, 'sha256': digest,
                  'asset_id': 'ASSET_' + digest[:20], 'format': path.suffix.lower().lstrip('.') or 'text_or_extensionless',
                  'data_level': kind, 'storage_role': storage,
                  'classification_basis': 'transparent path/extension rule; documentary snapshots are not biological raw measurements'}
        files.append(record); by_hash[digest].append(record)
        if relative.startswith('research/') and path.suffix.lower() in {'.txt', '.json', '.xml', '.html', '.md'} and digest not in scanned_hashes:
            scanned_hashes.add(digest)
            text = path.read_text(errors='replace')
            for accession in canonical_accessions(text):
                offset = text.find(accession)
                mentions.append({'accession': accession, 'source_file': rel(path), 'source_sha256': digest,
                                 'line': text.count('\n', 0, offset) + 1, 'canonical_record_url': accession_url(accession),
                                 'status': 'text_mention_only; may be a citation or search hit, not verified underlying data'})
    assets = []
    for digest, locations in sorted(by_hash.items()):
        ordered = sorted(locations, key=lambda r: (r['storage_role'] != 'working_input', len(r['path']), r['path']))
        first = ordered[0]
        assets.append({'asset_id': first['asset_id'], 'sha256': digest, 'bytes': first['bytes'],
                       'data_level': first['data_level'], 'format': first['format'], 'preferred_path': first['path'],
                       'copy_count': len(locations), 'all_paths': [r['path'] for r in ordered]})
    return files, assets, mentions, by_hash


def parse_geo(path):
    tags = defaultdict(list)
    if path.is_file():
        for line in path.read_text(errors='replace').splitlines():
            if line.startswith('!Series_') and ' = ' in line:
                key, value = line[8:].split(' = ', 1)
                tags[key].append(value)
    return dict(tags)


def atlas_registries(by_hash):
    database = ATLAS / 'candidates/0.3.0/immune_candidate.sqlite'
    db = sqlite3.connect('file:' + str(database) + '?mode=ro', uri=True)
    db.row_factory = sqlite3.Row
    sources, tables, fields = [], [], []
    rows = [(dict(r), 'preserved_baseline_0.2.0') for r in db.execute('SELECT * FROM source_registry')]
    for row in db.execute('SELECT * FROM candidate_sources'):
        source = json.loads(row['payload'])
        source['snapshot_sha256'] = json.loads(row['source_dependencies']).get(source['snapshot_path'])
        rows.append((source, 'unreviewed_candidate_0.3.0'))
    for source, scope in rows:
        digest = source.get('snapshot_sha256')
        matches = by_hash.get(digest, [])
        paths = sorted({m['path'] for m in matches})
        sources.append({'source_key': scope + ':' + source['source_id'], 'source_id': source['source_id'],
                        'scope': scope, 'title': source['title'], 'doi': source.get('doi'), 'url': source.get('url'),
                        'source_type': source.get('source_type', 'primary_study'), 'access_level': source.get('access_level'),
                        'declared_snapshot_path': source.get('snapshot_path'), 'snapshot_sha256': digest,
                        'matching_local_paths': paths, 'hash_matched_local_snapshot': bool(paths),
                        'raw_biological_data_claim': 'Source registry records document evidence access, not raw biological file availability.'})
    for row in db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name"):
        table, schema = row['name'], row['sql']
        count = db.execute('SELECT count(*) FROM "' + table + '"').fetchone()[0]
        tables.append({'table_id': 'ATLAS_TABLE:' + table, 'name': table, 'rows': count, 'database_path': rel(database),
                       'data_level': 'discovery_inventory' if table == 'cytokine_inventory' else 'curated_or_derived_atlas_data',
                       'review_scope': 'pending' if table.startswith('candidate_') else 'see_preserved_release_review_status', 'sql_schema': schema})
        foreign = {r['from']: r['table'] + '.' + str(r['to']) for r in db.execute('PRAGMA foreign_key_list("' + table + '")')}
        for column in db.execute('PRAGMA table_info("' + table + '")'):
            fields.append({'table_id': 'ATLAS_TABLE:' + table, 'field': column['name'], 'storage_type': column['type'],
                           'primary_key': bool(column['pk']), 'foreign_key': foreign.get(column['name'], ''),
                           'definition': 'Preserved atlas field; see linked schema and scientific dictionary for interpretation.',
                           'definition_source': 'atlas/data/CANDIDATE_DATA_DICTIONARY.md' if table.startswith('candidate_') else 'atlas/data/DATA_DICTIONARY.md',
                           'missingness': 'unavailable marks explicit scientific unknown; SQL NULL follows source table semantics',
                           'units': 'source/measurement dependent; do not infer from storage type'})
    db.close()
    pointers = read(ROOT / 'sources/atlas/recorded_accessions.json')
    datasets = []
    for accession in sorted({r['parsed_accession'] for r in pointers}):
        related = [r for r in pointers if r['parsed_accession'] == accession]
        snapshot = ROOT / 'sources/atlas' / (accession + '.soft.txt')
        geo = parse_geo(snapshot)
        verified = geo.get('geo_accession') == [accession]
        datasets.append({'dataset_id': 'ATLAS_DATA:' + accession, 'accession': accession,
                         'title': '; '.join(geo.get('title', [])) or 'Title not independently retrieved',
                         'record_url': accession_url(accession), 'atlas_source_ids': sorted({r['study_id'] for r in related}),
                         'atlas_cohort_ids': sorted({r['cohort_id'] for r in related}),
                         'original_accession_contexts': [r['accession'] for r in related],
                         'linkage_status': 'recorded in cohort field; related-data and cell-line caveats apply',
                         'repository_metadata_verified': verified,
                         'supplementary_file_links': geo.get('supplementary_file', []),
                         'repository_relations': geo.get('relation', []), 'repository_sample_records': len(geo.get('sample_id', [])),
                         'availability': 'public_record_with_advertised_files' if verified and geo.get('supplementary_file') else 'public_metadata_record' if verified else 'access_route_recorded; availability_not_independently_verified',
                         'biological_data_downloaded': False,
                         'metadata_snapshot': rel(snapshot) if snapshot.exists() else None,
                         'metadata_snapshot_sha256': sha(snapshot) if snapshot.exists() else None})
    return sources, tables, fields, datasets


def is_flu(text):
    return bool(re.search(r'influenza|\bH[1-9]N[1-9]\b', text, re.I))


def hr_eligibility(row, primary_records):
    accession = next(iter(canonical_accessions(row['study_ID'])), '')
    primary = next((r for r in primary_records if r.get('accession') == accession), None)
    influenza = is_flu(row.get('pathogen', ''))
    if not influenza:
        return 'outside_influenza_challenge_scope', 'Pathogen is not influenza in HR metadata.'
    if primary and primary['eligibility'] != 'included_human_influenza_challenge':
        return primary['eligibility'], primary.get('eligibility_reason', '')
    if row.get('study_type') == 'inoculation':
        return ('source_verified_influenza_challenge_subset' if primary else 'author_labelled_influenza_inoculation_pending_primary_check',
                'Restrict to the named influenza subset; original repository may contain other viruses.')
    if 'mixed' in row.get('study_type', ''):
        return 'mixed_exposure_requires_primary_challenge_check', 'Mixed exposure alone does not establish deliberate influenza challenge.'
    return 'vaccine_or_other_nonchallenge_context', 'Vaccination does not by itself establish an influenza challenge design.'


def observed_type(values):
    present = [v for v in values if v not in MISSING and v is not None]
    if not present:
        return 'all_missing_in_inspected_table'
    try:
        numeric = [float(v) for v in present]
        if all(math.isfinite(v) for v in numeric):
            return 'integer_like_text' if all(v.is_integer() for v in numeric) else 'numeric_text'
    except (ValueError, TypeError):
        pass
    return 'text_or_mixed'


def hr_file_level(path):
    if path.startswith('bulk_gene_expr/'):
        return 'harmonized_expression_matrix'
    if path.startswith('single_cell_gene_expr/'):
        return 'integrated_single_cell_object; layer_rawness_unverified'
    if path.startswith('antibody/'):
        return 'reported_antibody_measurements_with_derived_summary_columns'
    if path.startswith('meta/'):
        return 'harmonized_sample_metadata'
    if path.startswith('example_dataset/'):
        return 'example_derived_data'
    return 'resource_documentation_or_metadata'


def hr_registry(primary_records):
    info, tree = read(HF / 'hf_info.json'), read(HF / 'hf_file_tree.json')
    sha_revision = info['sha']
    _, studies = csv_rows(HF / 'study_meta.csv')
    _, citations = csv_rows(HF / 'study_citations.csv')
    citations_by_id = {r['study_ID']: r for r in citations}
    if len({r['study_ID'] for r in studies}) != len(studies) or len(citations_by_id) != len(citations) or {r['study_ID'] for r in studies} != set(citations_by_id):
        raise ValueError('HR study metadata/citations are not a one-to-one complete join.')
    listed = {r['path'] for r in tree if r['type'] == 'file'}
    if listed != {r['rfilename'] for r in info['siblings']}:
        raise ValueError('Pinned HF tree and resource file inventory differ.')
    results = read(HF / 'pinned_requests.results.json')
    tree_result = next(r for r in results if r['id'] == 'hf_file_tree')
    if tree_result.get('pagination_link'):
        raise ValueError('HF file listing still has an unconsumed pagination link.')
    dataset_rows, file_rows, links = [], [], []
    for study in studies:
        citation = citations_by_id[study['study_ID']]
        eligibility, reason = hr_eligibility(study, primary_records)
        accessions = canonical_accessions(citation.get('transcriptomic_data_link', ''))
        row = dict(study, dataset_id='HR:' + study['study_ID'],
                   influenza_challenge_eligibility=eligibility, eligibility_reason=reason,
                   canonical_source_accessions=accessions, **{k: v for k, v in citation.items() if k != 'study_ID'},
                   resource_revision=sha_revision, source_snapshot=rel(HF / 'study_meta.csv'),
                   source_snapshot_sha256=sha(HF / 'study_meta.csv'),
                   raw_data_flag_interpretation='Legacy author flag; not proof of current file-level raw availability.',
                   participant_count_interpretation='Within-study author count; not independent subjects across studies.')
        dataset_rows.append(row)
        for accession in accessions:
            links.append({'from_id': row['dataset_id'], 'to_id': accession, 'relationship': 'derived_study_subset_of_source_record',
                          'basis': 'HR study_citations transcriptomic_data_link', 'source_path': rel(HF / 'study_citations.csv')})
    for file in tree:
        if file['type'] != 'file':
            continue
        path = file['path']; local = HF / path
        study = re.sub(r'_(?:gene_expr|meta|antibody)\.csv$', '', Path(path).name)
        if path.startswith('single_cell_gene_expr/'):
            study = re.sub(r'(?:_processed)?\.h5ad(?:\.gz)?$', '', Path(path).name)
        exact = study in citations_by_id
        candidates = sorted(s for s in citations_by_id if s.startswith(study + '_')) if not exact else [study]
        file_rows.append({'file_id': 'HF:' + path, 'path_in_resource': path,
                          'study_ID': study if exact else None, 'filename_study_label': study,
                          'candidate_study_IDs': candidates,
                          'study_linkage_status': 'exact_study_label' if exact else 'split_cohort_label_requires_mapping' if candidates else 'no_single_study_link_established',
                          'resource_revision': sha_revision, 'bytes_listed': file.get('size'),
                          'git_oid': file.get('oid'), 'lfs_metadata': file.get('lfs'),
                          'canonical_download_url': f'https://huggingface.co/datasets/xuejun72/HR-VILAGE-3K3M/resolve/{sha_revision}/{path}',
                          'data_level': hr_file_level(path), 'file_listing_verified': True,
                          'local_snapshot': rel(local) if local.is_file() else None,
                          'local_snapshot_sha256': sha(local) if local.is_file() else None,
                          'content_inspection': 'local_metadata_or_antibody_table' if local.is_file() else 'listing_and_author_documentation_only',
                          'instrument_raw_claim': False})
    _, definitions = csv_rows(HF / 'Meta_variable_description.csv')
    defs = {r['Variable Name']: r['Description'] for r in definitions}
    audit = read(ROOT / 'sources/hr_vilage_audit/schema.json')
    table_defs = {t['table']: {f['name']: f for f in t.get('fields', [])} for t in audit['tables']}
    profiles, fields, subject_sets = [], [], {}
    paths = sorted((HF / 'meta').glob('*.csv')) + sorted((HF / 'antibody').glob('*.csv'))
    paths += [HF / 'study_meta.csv', HF / 'study_citations.csv', HF / 'Meta_variable_description.csv']
    for path in paths:
        columns, records = csv_rows(path)
        digest = sha(path)
        table_id = 'HF:' + str(path.relative_to(HF))
        is_meta, is_antibody = path.parent.name == 'meta', path.parent.name == 'antibody'
        study_id = re.sub(r'_(?:meta|antibody)\.csv$', '', path.name) if is_meta or is_antibody else None
        keys = {}
        for key in ('X', '', 'row_name', 'geo_accession', 'ID', 'study_ID'):
            if key in columns:
                values = [r.get(key) for r in records if r.get(key) not in MISSING and r.get(key) is not None]
                keys[key or '[unnamed_index]'] = {'nonmissing': len(values), 'distinct': len(set(values)),
                                                'duplicate_nonmissing_rows': len(values) - len(set(values))}
        ids = {r['ID'] for r in records if r.get('ID') not in MISSING and r.get('ID') is not None} if 'ID' in columns else set()
        if study_id:
            subject_sets[(study_id, path.parent.name)] = ids
        profiles.append({'table_id': table_id, 'study_ID': study_id, 'local_path': rel(path), 'sha256': sha(path),
                         'data_rows': len(records), 'column_count': len(columns), 'keys_observed': keys,
                         'distinct_subject_ids_within_table': len(ids) if 'ID' in columns else None,
                         'grain': 'sample/observation' if is_meta else 'subject with repeated measurements in columns' if is_antibody else 'resource metadata row',
                         'matrix_join_status': 'metadata keys inspected; full expression matrix rows not independently compared' if is_meta else 'not_applicable',
                         'namespace_rule': 'Use study_ID plus local ID; ID is not a global participant identifier.'})
        for column in columns:
            values = [r.get(column) for r in records]
            definition = defs.get(column)
            basis = rel(HF / 'Meta_variable_description.csv') if definition else 'Observed file header; biological definition not supplied in common metadata dictionary'
            audit_field = table_defs.get(path.name, {}).get(column, {})
            if audit_field:
                definition = audit_field.get('definition', audit_field.get('author_definition', definition))
                basis = 'data_dictionary/sources/hr_vilage_audit/schema.json: ' + path.name + '.' + column
            caution = ''
            if column in {'X', '', 'row_name'}:
                definition = 'Exported sample/row index; inspect uniqueness and relation to source sample accession per file.'
                basis = 'Observed table keys; author alignment rule in dataset documentation'
            elif is_antibody and column not in {'ID', 'MFC', 'responder'}:
                definition = 'Study-specific antibody measurement or derived column; preserve the literal antigen/visit label.'
                caution = 'Assay, units, dilution limits and suffix interpretation require the original study; do not parse a numeric suffix as a universal day.'
            if column == 'timepoint':
                caution = 'Common description says exact time, but source pipelines can encode pooled visits by a representative value; preserve original visit labels and origin.'
            elif column == 'raw_data':
                caution = 'Legacy HR availability flag survives V3 removal of raw expression files; verify original repository files separately.'
            elif column in {'MFC', 'responder', 'responder_original'}:
                caution = 'Derived response annotation; threshold/antigen set and baseline definitions are study-specific.'
            fields.append({'table_id': table_id, 'study_ID': study_id, 'field': column or '[unnamed_index]',
                           'literal_header': column, 'definition': definition or 'unavailable', 'definition_source': basis,
                           'observed_storage_type': observed_type(values), 'nonmissing_rows': sum(v not in MISSING and v is not None for v in values),
                           'missing_rows': sum(v in MISSING or v is None for v in values),
                           'distinct_nonmissing_values': len({v for v in values if v not in MISSING and v is not None}),
                           'units': 'not inferred; use source-specific assay/time documentation',
                           'interpretation_caution': caution, 'source_path': rel(path), 'source_sha256': digest})
    join_checks = []
    for (study_id, kind), ids in subject_sets.items():
        if kind == 'antibody':
            meta_ids = subject_sets.get((study_id, 'meta'))
            join_checks.append({'study_ID': study_id, 'antibody_distinct_subjects': len(ids),
                                'metadata_distinct_subjects': len(meta_ids) if meta_ids is not None else None,
                                'shared_subject_ids': len(ids & meta_ids) if meta_ids is not None else None,
                                'antibody_ids_absent_from_metadata': len(ids - meta_ids) if meta_ids is not None else None,
                                'status': 'metadata_table_not_inspected' if meta_ids is None else 'metadata_subject_ids_unavailable' if not meta_ids else 'all_antibody_subjects_match_metadata' if ids <= meta_ids else 'requires_join_review',
                                'caution': 'Subject-level agreement does not verify visit/antigen alignment or cross-study independence.'})
    genes = [{'column_position_1based': i + 1, 'gene_label': gene, 'schema_role': 'author_common_bulk_expression_feature',
              'definition': 'Source-provided gene/feature label; no independent ontology verification.',
              'units': 'matrix-specific scale; not a protein or secretion measurement',
              'source_path': rel(HF / 'gene_expr_colnames.txt')} for i, gene in enumerate((HF / 'gene_expr_colnames.txt').read_text().splitlines()) if gene]
    return dataset_rows, file_rows, profiles, fields, join_checks, genes, links


def check_hash(path, expected):
    resolved = (IKHIS / path).resolve()
    if not resolved.is_relative_to(IKHIS) or not resolved.is_file() or sha(resolved) != expected:
        raise ValueError('Source hash mismatch or missing file: ' + path)


def validate_sources(primary):
    ids = [r['id'] for r in primary]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate influenza record identifiers')
    audit = read(ROOT / 'sources/hr_vilage_audit/sources.json')
    source_rows = []
    for source in audit['sources']:
        check_hash(source['snapshot_path'], source['sha256'])
        source_rows.append(dict(source, source_group='HR documentation audit'))
    for derivative in audit.get('reading_derivatives', []):
        check_hash(derivative['path'], derivative['sha256'])
        check_hash(derivative['derived_from'], derivative['original_sha256'])
    for result_path in sorted((ROOT / 'sources').rglob('*.results.json')):
        for source in read(result_path):
            if source.get('status') != 'retrieved':
                continue
            path = rel(ROOT / source['output'])
            check_hash(path, source['sha256'])
            source_rows.append({'source_id': uid('SOURCE', [str(result_path.relative_to(ROOT)), source['id']]),
                                'source_group': str(result_path.parent.relative_to(ROOT / 'sources')),
                                'url': source['requested_url'], 'snapshot_path': path, 'sha256': source['sha256'],
                                'retrieved_on': source['retrieved_at'], 'evidence_status': 'public_metadata_snapshot'})
    for record in primary:
        evidence = record.get('eligibility_evidence', {})
        if not evidence.get('locator') or not (IKHIS / evidence.get('snapshot_path', '')).is_file():
            raise ValueError('Missing eligibility evidence: ' + record['id'])
        for path in record['source_paths']:
            check_hash(path, record['source_hashes'][path])
            source_rows.append({'source_id': uid('SOURCE', [record['id'], path]), 'source_group': 'Influenza primary sources',
                                'catalog_record_id': 'FLU:' + record['id'], 'url': record['source_url'],
                                'url_role': 'record landing page; individual evidence URLs remain in source record citations',
                                'snapshot_path': path, 'sha256': record['source_hashes'][path],
                                'retrieved_on': record['retrieved_on'], 'evidence_status': 'source_checked_catalogue_pending_review'})
    return source_rows


def influenza_registries(primary):
    datasets, files, relationships, gaps = [], [], [], []
    for record in primary:
        dataset_id = 'FLU:' + record['id']
        raw = record['raw_data']
        now_status = raw['availability']
        if raw.get('request_window_begins', '') > '2026-09-14':
            now_status = 'request_window_not_yet_open'
        datasets.append({'dataset_id': dataset_id, 'scope': 'Influenza challenge search',
                         'accession_or_record_id': record['id'], 'title': record['title'], 'repository': record['repository'],
                         'url': record['source_url'], 'eligibility': record['eligibility'],
                         'specimen': record.get('preparation'), 'modality': record['modality'],
                         'raw_access_status': now_status, 'raw_access_evidence': raw['description'],
                         'processed_access_status': record['processed_data']['availability'],
                         'participant_count': record.get('participant_count'),
                         'repository_sample_count': record.get('sample_count_repository'),
                         'independent_cohort_count': None,
                         'subset_rule': record.get('mixed_study_rule', 'Preserve trial, participant, specimen and visit identifiers.'),
                         'full_record_table': 'influenza_studies', 'review_status': 'catalogue_curation_pending_review'})
        for pos, file in enumerate(record['files']):
            url = file.get('url', record['source_url'])
            direct = bool(re.search(r'\.(?:gz|tar|zip|xlsx|pdf|csv|txt)(?:$|\?)', url, re.I))
            files.append(dict(file, file_id=uid('FLUFILE', [record['id'], pos, url, file.get('name')]),
                              dataset_id=dataset_id, eligibility=record['eligibility'],
                              access_url=url, access_url_kind='direct_file_link' if direct else 'repository_or_publication_landing_page',
                              local_biological_payload=False, schema_inspection='not_inspected_at_biological_file_level',
                              source_paths=record['source_paths'], source_hashes=record['source_hashes']))
        for kind in ('relationships', 'cohort_reuse'):
            for value in record.get(kind, []):
                relationships.append({'from_id': dataset_id, 'to_id': None, 'relationship': kind,
                                      'source_statement': value, 'evidence_record': record['id'],
                                      'interpretation': 'Retained source relationship; does not establish a participant-level equivalence map.'})
        for value in record.get('missing_info', []):
            gaps.append({'gap_id': uid('GAP', [dataset_id, value]), 'record_id': dataset_id,
                         'category': 'source_file_or_cohort_mapping', 'description': value,
                         'status': 'open', 'next_action': 'Inspect the named original repository, sample manifest or supplementary table.'})
    return datasets, files, relationships, gaps


def atlas_coverage(sources, datasets, mentions):
    by_path = defaultdict(set)
    for mention in mentions:
        by_path[mention['source_file']].add(mention['accession'])
    rows = []
    for source in sources:
        associated = [r['accession'] for r in datasets if source['source_id'] in r['atlas_source_ids']]
        text_mentions = sorted(set().union(*(by_path[p] for p in source['matching_local_paths'])))
        research = source['source_type'] in {'primary_study', 'preprint'}
        rows.append({'source_key': source['source_key'], 'source_id': source['source_id'], 'title': source['title'],
                     'source_type': source['source_type'], 'source_url': source['url'],
                     'explicit_cohort_accessions': associated, 'unverified_snapshot_accession_mentions': text_mentions,
                     'data_inventory_status': 'explicit_cohort_data_routes_recorded' if associated else 'raw_data_route_not_recorded' if research else 'reference_resource_or_specification',
                     'local_snapshot_available': source['hash_matched_local_snapshot'],
                     'interpretation': 'A cited or related accession is not automatically the original data for every assay in a paper.'})
    return rows


def observed_count_checks(studies, profiles):
    by_study = {r['study_ID']: r for r in profiles if r['table_id'].startswith('HF:meta/')}
    checks = []
    for row in studies:
        profile = by_study.get(row['study_ID'])
        if not profile:
            continue
        for author_field, observed_field in [('num_observations', 'data_rows'), ('num_subjects', 'distinct_subject_ids_within_table')]:
            author = int(row[author_field]) if str(row[author_field]).isdigit() else None
            observed = profile[observed_field]
            assessable = author is not None and observed is not None and not (author_field == 'num_subjects' and observed == 0)
            checks.append({'study_ID': row['study_ID'], 'measure': author_field, 'author_count': author,
                           'observed_count': observed if assessable else None, 'status': 'not_assessable_from_available_IDs' if not assessable else 'match' if author == observed else 'difference_requires_interpretation',
                           'caution': 'Observed IDs/rows describe this table, not deduplicated people across cohorts.'})
    return checks


def sql_export(tables):
    path = OUT / 'data_dictionary.sqlite'
    if path.exists():
        path.unlink()
    db = sqlite3.connect(path)
    schema_rows = []
    for name, rows in sorted(tables.items()):
        columns = sorted({k for row in rows for k in row}) or ['empty_table']
        quote = lambda s: '"' + s.replace('"', '""') + '"'
        types = {}
        for col in columns:
            values = [row[col] for row in rows if row.get(col) is not None]
            types[col] = ('INTEGER' if all(isinstance(v, (int, bool)) for v in values) else
                          'REAL' if all(isinstance(v, (int, float)) for v in values) else 'TEXT') if values else 'TEXT'
            schema_rows.append({'table': name, 'column': col, 'sql_type': types[col],
                                'structured_values': 'JSON encoded in TEXT where a source field contains a list/object',
                                'definition': 'Literal catalog/source field; see README, schema conventions and source provenance.'})
        db.execute('CREATE TABLE ' + quote(name) + ' (' + ','.join(quote(c) + ' ' + types[c] for c in columns) + ')')
        db.executemany('INSERT INTO ' + quote(name) + ' VALUES (' + ','.join('?' for _ in columns) + ')',
                       [[dump(row[c]) if isinstance(row.get(c), (list, dict)) else row.get(c) for c in columns] for row in rows])
        for col in ('dataset_id', 'study_ID', 'table_id', 'source_key', 'file_id', 'run_accession'):
            if col in columns:
                db.execute('CREATE INDEX ' + quote(name + '_' + col) + ' ON ' + quote(name) + '(' + quote(col) + ')')
    db.commit()
    if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
        raise ValueError('SQLite integrity check failed')
    db.close()
    return schema_rows


def catalog_summary(tables):
    eligible = [r for r in tables['influenza_studies'] if r['eligibility'] == 'included_human_influenza_challenge']
    return {'catalog_version': '0.1.0', 'observed_on': '2026-09-14',
            'coverage_claim': 'Complete local atlas file inventory and pinned HR file listing; expandable influenza discovery catalog, not an exhaustive census.',
            'atlas_files': len(tables['atlas_files']), 'atlas_distinct_content_assets': len(tables['atlas_assets']),
            'atlas_registered_sources': len(tables['atlas_sources']), 'atlas_recorded_data_accessions': len(tables['atlas_datasets']),
            'atlas_sources_without_recorded_raw_route': sum(r['data_inventory_status'] == 'raw_data_route_not_recorded' for r in tables['atlas_source_coverage']),
            'hr_study_rows': len(tables['hr_studies']), 'hr_listed_files': len(tables['hr_files']),
            'hr_inspected_tables': len(tables['hr_table_profiles']), 'hr_field_entries': len(tables['hr_fields']),
            'hr_common_gene_labels': len(tables['hr_gene_features']),
            'hr_influenza_challenge_subsets': sum(r['influenza_challenge_eligibility'] == 'source_verified_influenza_challenge_subset' for r in tables['hr_studies']),
            'influenza_catalog_records': len(tables['influenza_studies']), 'influenza_eligible_records': len(eligible),
            'influenza_adjacent_exclusions': len(tables['influenza_studies']) - len(eligible),
            'influenza_file_or_access_entries': len(tables['influenza_files']), 'viral_sequence_runs': len(tables['viral_sequence_runs']),
            'influenza_raw_access_status': dict(sorted(Counter(r['raw_access_status'] for r in tables['datasets'] if r['scope'] == 'Influenza challenge search' and r['eligibility'] == 'included_human_influenza_challenge').items())),
            'antibody_join_checks': dict(Counter(r['status'] for r in tables['hr_join_checks'])),
            'study_count_checks': dict(Counter(r['status'] for r in tables['hr_count_checks'])),
            'open_gaps': len(tables['open_gaps']), 'independent_cohort_count': None,
            'huggingface_revision': read(HF / 'hf_info.json')['sha'],
            'scientific_review': 'Atlas review remains pending; this inventory does not approve candidate claims.'}


def markdown_cell(value):
    return str(value or '').replace('|', '\\|').replace('\n', ' ')


def build_reports(summary, tables):
    rows = ['| Record | Measurements / specimen | Raw access as checked | Source |', '|---|---|---|---|']
    for row in tables['datasets']:
        if row['scope'] != 'Influenza challenge search' or row['eligibility'] != 'included_human_influenza_challenge':
            continue
        rows.append('| ' + ' | '.join([markdown_cell(row['accession_or_record_id']),
                    markdown_cell('; '.join(row['modality']) + ' / ' + str(row['specimen'])),
                    markdown_cell(row['raw_access_status']), '[record](' + row['url'] + ')']) + ' |')
    text = f'''# IKHIS data dictionary · 0.1.0

Checked 14 September 2026. [Browse the catalog](catalog.html) · [Project guide](../README.md) · [Database](../catalog/data_dictionary.sqlite)

## What is covered

The local atlas inventory contains **{summary['atlas_files']:,} files**, representing {summary['atlas_distinct_content_assets']:,} distinct byte-identical assets after deduplication. It excludes Python environments, caches and operating-system files. The migration ledger separately binds all 2,751 moved files, including the old nested environment. Every atlas file has a path, content hash, format and storage/data classification. All {summary['atlas_registered_sources']} registered sources are accounted for, including {summary['atlas_recorded_data_accessions']} explicit cohort-data accessions; {summary['atlas_sources_without_recorded_raw_route']} primary-study/preprint records still have no explicit raw-data route in their cohort records. Those gaps are visible in the source-coverage table. Literature and repository snapshots are documentary inputs, not participant measurement files.

The pinned HR-VILAGE inventory covers **{summary['hr_study_rows']} study/cohort rows and all {summary['hr_listed_files']} listed files**. All 59 bulk-study metadata tables and 37 antibody tables were inspected, together with three root metadata tables: {summary['hr_field_entries']:,} per-table field entries. The author common bulk feature list contains {summary['hr_common_gene_labels']:,} labels; it is not an independently validated gene ontology. Full expression matrices and H5AD layers were not downloaded. Six HR rows are verified influenza challenge subsets; four belong to GSE73072, so these are three original GEO series, not six independent deposits.

The expanded influenza search contains **{summary['influenza_eligible_records']} eligible challenge-related records**, four adjacent exclusions, and **{summary['viral_sequence_runs']} public viral-sequencing run identifiers**. Records include accessions, modalities and reanalyses of shared trials. They are not a count of independent cohorts. The 258 current SRP091397 runs exceed the 13 named in the original 2016 paper; the run manifest preserves the expanded repository, with sample-level challenge/control assignment still required.

## Raw data and access

HR-VILAGE V3 (28 August 2026) removed `bulk_gene_expr_raw/`. Its May 2026 paper predates this change. The remaining legacy `raw_data` flags do not establish present-day raw-file availability. The [pinned dataset card](https://huggingface.co/datasets/xuejun72/HR-VILAGE-3K3M/blob/{summary['huggingface_revision']}/README.md) and [study citations](../sources/hr_vilage/study_citations.csv) provide the current context and original repository routes.

Instrument files, submitter measurement tables, quantified counts, normalized expression, antibody measurements, derived outcomes and metadata are separate levels. A gene-count matrix is not a sequencing-read file. H5AD `.X` is not universally raw counts. Olink NPX is normalized protein expression, not absolute concentration. Antibody tables combine measurements with derived response fields.

Public access means the stated evidence supports a public route; each file records whether this was a repository listing, a primary-paper declaration or inspected table content. EGA requires managed access. The Imperial participant-data request window begins 1 July 2027 and is not currently open. A failed repository fetch does not establish data absence. File-level source evidence and restrictions remain in [influenza_studies.json](../catalog/influenza_studies.json).

## Influenza challenge records

''' + '\n'.join(rows) + f'''

## Joining and interpreting observations

Qualify participant IDs with `study_ID`. Repeated visits, tissues, assays and cells are not independent people. Join sample rows using preserved source row identifiers; subject-ID agreement does not establish antigen/visit alignment. Full metadata-to-expression row alignment still needs matrix inspection. All antibody subjects match the metadata in {summary['antibody_join_checks'].get('all_antibody_subjects_match_metadata', 0)} tables; {summary['antibody_join_checks'].get('requires_join_review', 0)} tables have unmatched IDs; {summary['antibody_join_checks'].get('metadata_table_not_inspected', 0)} require another mapping or metadata inspection. Of the author counts compared with inspected tables, {summary['study_count_checks'].get('match', 0)} match, {summary['study_count_checks'].get('difference_requires_interpretation', 0)} differ and {summary['study_count_checks'].get('not_assessable_from_available_IDs', 0)} cannot be assessed because subject IDs are unavailable. Differences are retained in [count checks](../catalog/hr_count_checks.csv), not silently reconciled.

Preserve original visit labels, baseline origin, specimen, antigen, assay units and detection limits. Author processing can turn pooled `d28+d35` into 31.5; this does not establish an exact collection day. Blank/NA values are unavailable, not zeros or negative outcomes. Misspelled source headers remain literal.

## Coverage limits and next acquisition work

The exact GEO query returned 200 records; all 200 titles plus two known leads were screened. Thirty search/lookup records and citation chasing extend the search. The broad query missed known challenge studies, so the influenza inventory is expandable and **cannot yet establish that every existing dataset has been found**. See [search log](../catalog/search_log.json), [screening decisions](../catalog/geo_screening.json) and [source research notes](../sources/influenza/notes.md).

The remaining work is enumerated in {summary['open_gaps']} [open gap records](../catalog/open_gaps.csv): expand archive members and sample manifests; inspect supplementary workbook fields and immuneACCESS exports; resolve incomplete cytometry, proteomics, cytokine and raw-read routes; obtain subject/arm/time crosswalks; and continue screening repositories beyond the initial discovery set. Unknown raw-file fields and unavailable assay units remain explicitly unknown. No large raw biological files or controlled participant data were downloaded.

The atlas's frozen releases and candidate bytes were preserved. Its independent scientific review remains pending.
'''
    (REPORTS / 'DATA_DICTIONARY.md').write_text(text)
    browser_rows = []
    for row in tables['datasets']:
        browser_rows.append({k: row.get(k) for k in ('dataset_id', 'scope', 'title', 'repository', 'url', 'eligibility', 'specimen', 'modality', 'raw_access_status', 'raw_access_evidence')})
    payload = dump(browser_rows).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>IKHIS · Data dictionary</title><style>
:root{color-scheme:light;--ink:#172e36;--muted:#51676e;--line:#cbd8d9;--accent:#126b65}*{box-sizing:border-box}body{margin:0;background:#f3f6f3;color:var(--ink);font:16px/1.5 system-ui,sans-serif}main{max-width:1250px;margin:48px auto;padding:0 28px}h1{font-size:42px;line-height:1.15;margin:10px 0}h2{font-size:20px}a{color:var(--accent)}.eyebrow{letter-spacing:.12em;font-size:12px;font-weight:700}.lead{max-width:900px;color:var(--muted)}.metrics{display:flex;flex-wrap:wrap;gap:14px;margin:28px 0}.metric{background:white;border:1px solid var(--line);border-radius:10px;padding:16px 22px;min-width:180px}.metric b{font-size:29px;display:block}.metric span{font-size:13px;color:var(--muted)}.toolbar{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}label{display:grid;gap:5px;font-size:13px}input,select{padding:11px;border:1px solid #a8bdbf;border-radius:5px;background:white;font:inherit}input{width:min(500px,80vw)}.notice{border-left:4px solid #bc812a;background:#fff8e9;padding:16px 20px;margin:22px 0}.tablewrap{overflow:auto;background:white;border:1px solid var(--line);border-radius:10px}table{border-collapse:collapse;width:100%}th,td{text-align:left;padding:14px;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:12px;letter-spacing:.04em;background:#e5eeeb}td{font-size:14px}td:first-child{min-width:160px}td:nth-child(2){min-width:310px}small{display:block;color:var(--muted);margin-top:5px}.tag{font-size:12px;padding:3px 7px;display:inline-block;background:#edf3f1;border-radius:4px}footer{margin:32px 0;color:var(--muted);font-size:13px}button{padding:10px 16px;background:var(--accent);color:white;border:0;border-radius:5px;cursor:pointer}button:disabled{opacity:.45}nav{display:flex;align-items:center;gap:18px;margin:18px 0}@media(max-width:650px){main{margin:25px auto;padding:0 16px}h1{font-size:32px}.metric{min-width:140px;flex:1}}
</style><main><div class="eyebrow">IKHIS / DATA DICTIONARY · 14 SEPTEMBER 2026</div><h1>Find the data behind the evidence.</h1>
<p class="lead">Search atlas data routes, every study in the pinned HR-VILAGE release, and the expanded human influenza challenge catalog. Follow each record to its original source.</p>
<p><a href="DATA_DICTIONARY.md">Read the coverage report</a> · <a href="../README.md">Guide and exports</a> · <a href="../catalog/datasets.csv">Download study catalog</a> · <a href="../catalog/data_dictionary.sqlite">Database</a></p>
<div class="metrics">__METRICS__</div><div class="notice"><strong>Coverage is explicit.</strong> All local atlas files and all files in the pinned HR-VILAGE listing are inventoried. The influenza discovery catalog is expandable. Records and sequencing runs are not independent cohorts. HR-VILAGE V3 removed its raw-expression folder; original raw files must be traced to source repositories.</div>
<div class="toolbar"><label>Search datasets<input id="search" type="search" placeholder="Accession, assay, specimen or title"></label><label>Collection<select id="scope"><option value="">All collections</option><option>Influenza challenge search</option><option>Atlas data routes</option><option>HR-VILAGE studies</option></select></label><label>Eligibility<select id="eligibility"><option value="">All records</option><option value="challenge">Verified influenza challenge</option><option value="adjacent_excluded">Adjacent exclusions</option></select></label></div>
<p id="count" aria-live="polite"></p><div class="tablewrap"><table><thead><tr><th>RECORD / COLLECTION</th><th>MEASUREMENTS &amp; CONTEXT</th><th>RAW DATA ACCESS</th><th>ELIGIBILITY</th></tr></thead><tbody id="rows"></tbody></table></div><nav><button id="previous">Previous</button><span id="page"></span><button id="next">Next</button></nav>
<footer>Source metadata checked 14 September 2026. Public access labels include repository listings and paper declarations; file contents may remain uninspected. Use the CSV/JSON exports for provenance, missing fields, file-level verification and access restrictions. This catalog does not approve the atlas's scientific claims.</footer></main>
<script id="catalog-data" type="application/json">__DATA__</script><script>
const data=JSON.parse(document.getElementById('catalog-data').textContent);let page=0;const size=25;
const el=id=>document.getElementById(id);const human=v=>String(v??'unavailable').replaceAll('_',' ');
function append(parent,tag,text,cls){const n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;parent.append(n);return n}
function render(reset=false){if(reset)page=0;const q=el('search').value.trim().toLowerCase(),scope=el('scope').value,elig=el('eligibility').value;
const found=data.filter(r=>(!q||JSON.stringify(r).toLowerCase().includes(q))&&(!scope||r.scope===scope)&&(!elig||(elig==='challenge'?['included_human_influenza_challenge','source_verified_influenza_challenge_subset'].includes(r.eligibility):r.eligibility===elig)));
const pages=Math.max(1,Math.ceil(found.length/size));page=Math.min(page,pages-1);el('rows').replaceChildren();
for(const r of found.slice(page*size,(page+1)*size)){const tr=document.createElement('tr');const first=append(tr,'td','');const link=append(first,'a',r.dataset_id);if(/^https:\/\//.test(r.url||'')){link.href=r.url;link.target='_blank';link.rel='noopener noreferrer'}append(first,'small',r.scope);const context=append(tr,'td',r.title||'Title unavailable');append(context,'small',[Array.isArray(r.modality)?r.modality.join('; '):r.modality,r.specimen].filter(Boolean).join(' · '));const access=append(tr,'td','');append(access,'span',human(r.raw_access_status),'tag');append(access,'small',r.raw_access_evidence||'Follow source record; availability is not independently verified.');append(tr,'td',human(r.eligibility));el('rows').append(tr)}
el('count').textContent=`${found.length} matching catalog records`;el('page').textContent=`Page ${page+1} of ${pages}`;el('previous').disabled=page===0;el('next').disabled=page>=pages-1}
for(const id of ['search','scope','eligibility'])el(id).addEventListener(id==='search'?'input':'change',()=>render(true));el('previous').onclick=()=>{page--;render()};el('next').onclick=()=>{page++;render()};render();
</script></html>'''
    metrics = [(summary['atlas_files'], 'local atlas files'), (summary['hr_study_rows'], 'HR-VILAGE study rows'),
               (summary['influenza_eligible_records'], 'challenge-related records'), (summary['viral_sequence_runs'], 'public viral run identifiers')]
    cards = ''.join('<div class="metric"><b>' + f'{n:,}' + '</b><span>' + html.escape(label) + '</span></div>' for n, label in metrics)
    (REPORTS / 'catalog.html').write_text(page.replace('__METRICS__', cards).replace('__DATA__', payload))


def build():
    OUT.mkdir(exist_ok=True); REPORTS.mkdir(exist_ok=True)
    primary = read(ROOT / 'sources/influenza/studies.json')
    source_rows = validate_sources(primary)
    files, assets, mentions, by_hash = atlas_inventory()
    sources, atlas_tables, atlas_fields, atlas_datasets = atlas_registries(by_hash)
    hr, hr_files, profiles, fields, joins, genes, relationships = hr_registry(primary)
    datasets, flu_files, flu_relationships, gaps = influenza_registries(primary)
    relationships += flu_relationships
    for row in atlas_datasets:
        datasets.append({'dataset_id': row['dataset_id'], 'scope': 'Atlas data routes', 'title': row['title'],
                         'repository': 'Original repository', 'url': row['record_url'], 'eligibility': 'atlas_scope',
                         'raw_access_status': row['availability'], 'raw_access_evidence': '; '.join(row['original_accession_contexts']),
                         'accession_or_record_id': row['accession'], 'full_record_table': 'atlas_datasets'})
    for row in hr:
        datasets.append({'dataset_id': row['dataset_id'], 'scope': 'HR-VILAGE studies', 'title': row['study_ID'],
                         'repository': 'HR-VILAGE / original repository', 'url': row['transcriptomic_data_link'],
                         'eligibility': row['influenza_challenge_eligibility'], 'specimen': row['tissue'], 'modality': row['platform'],
                         'raw_access_status': 'original_repository_route; legacy_raw_flag_not_verified',
                         'raw_access_evidence': 'V3 distributes harmonized matrices; follow the cited original source for raw file availability.',
                         'accession_or_record_id': row['study_ID'], 'full_record_table': 'hr_studies'})
    version = read(ROOT / 'sources/hr_vilage_audit/version_notes.json')
    for relationship in version['relationships']:
        relationships.append({'from_id': None, 'to_id': None, 'relationship': relationship['relationship'],
                              'source_statement': relationship, 'evidence_record': 'HR audit github_readme',
                              'interpretation': 'Author-reported relationship; exact participant equivalence still requires a crosswalk.'})
    coverage = atlas_coverage(sources, atlas_datasets, mentions)
    for row in coverage:
        if row['data_inventory_status'] == 'raw_data_route_not_recorded':
            gaps.append({'gap_id': uid('GAP', row['source_key']), 'record_id': row['source_key'], 'category': 'atlas_original_data_route',
                         'description': 'No explicit cohort-data accession recorded for this primary study/preprint: ' + row['title'],
                         'status': 'open', 'next_action': 'Inspect source data-availability statement and supplements; validate related accession mentions before linking.'})
    for row in joins:
        if row['status'] != 'all_antibody_subjects_match_metadata':
            gaps.append({'gap_id': uid('GAP', row), 'record_id': 'HR:' + row['study_ID'], 'category': 'subject_join',
                         'description': 'Some antibody subject IDs do not match the inspected metadata table.' if row['status'] == 'requires_join_review' else 'Corresponding subject metadata is not inspected or has no usable subject IDs; join cannot yet be assessed.', 'status': 'open',
                         'next_action': 'Recover original subject mapping before joining measurements.'})
    for key, description, action in [
        ('archive_schema', 'Remote raw archives and many supplementary workbooks are listed but their members/fields are not yet inspected.', 'Expand members, inspect headers and register assay units and detection limits.'),
        ('cohort_deduplication', 'No complete participant-level crosswalk across reused challenge cohorts.', 'Map trial, arm, participant, episode, specimen and visit identifiers before pooling.'),
        ('search_completeness', 'Repository discovery and title screening do not establish an exhaustive census of all influenza challenge data.', 'Continue full-record screening, trial/publication citation chaining and non-GEO repository discovery.'),
        ('matrix_layers', 'Current HR expression scales and H5AD layers are not independently inspected.', 'Inspect each matrix/layer and its exact processing provenance before assigning numeric units.')]:
        gaps.append({'gap_id': key, 'record_id': 'catalog', 'category': key, 'description': description, 'status': 'open', 'next_action': action})
    runs = read(ROOT / 'sources/influenza/viral_sequence_runs.json')
    if len({r['run_accession'] for r in runs}) != len(runs):
        raise ValueError('Duplicate sequencing run accession')
    for row in runs:
        row['source_sha256'] = sha(IKHIS / row['source_path'])
        row['sample_scope'] = 'repository run; exact challenge participant/control and original-publication subset assignment pending'
    schema = read(ROOT / 'sources/hr_vilage_audit/schema.json')
    for table in schema['tables']:
        if table['table'].startswith('singel_cell_gene_expr/'):
            table['source_documentation_table_label'] = table['table']
            table['table'] = table['table'].replace('singel_cell_gene_expr/', 'single_cell_gene_expr/')
            table['path_basis'] = 'Current pinned HF tree uses single_cell_gene_expr; source documentation spelling retained separately.'
    tables = {'datasets': datasets, 'atlas_files': files, 'atlas_assets': assets, 'atlas_sources': sources,
              'atlas_tables': atlas_tables, 'atlas_fields': atlas_fields, 'atlas_datasets': atlas_datasets,
              'atlas_source_coverage': coverage, 'atlas_accession_mentions': mentions,
              'hr_studies': hr, 'hr_files': hr_files, 'hr_table_profiles': profiles, 'hr_fields': fields,
              'hr_join_checks': joins, 'hr_count_checks': observed_count_checks(hr, profiles), 'hr_gene_features': genes,
              'hr_schema': schema['tables'], 'hr_transformations': read(ROOT / 'sources/hr_vilage_audit/transformations.json')['transformations'],
              'influenza_studies': primary, 'influenza_files': flu_files, 'viral_sequence_runs': runs,
              'relationships': relationships, 'source_provenance': source_rows, 'open_gaps': gaps,
              'search_log': read(ROOT / 'sources/influenza/searches.json'),
              'geo_screening': read(ROOT / 'sources/influenza/geo_screening.json')}
    for name, records in tables.items():
        export(name, records)
    export('catalog_columns', sql_export(tables))
    summary = catalog_summary(tables)
    write(OUT / 'summary.json', summary)
    build_reports(summary, tables)
    inputs = {rel(path): sha(path) for path in sorted((ROOT / 'sources').rglob('*')) if path.is_file() and '__pycache__' not in path.parts}
    for directory in (ROOT / 'scripts', ROOT / 'tests'):
        inputs.update({rel(path): sha(path) for path in sorted(directory.rglob('*')) if path.is_file() and '__pycache__' not in path.parts})
    inputs.update({rel(path): sha(path) for path in sorted(ROOT.glob('*.md'))})
    inputs[rel(ROOT / 'provenance/atlas_migration.json')] = sha(ROOT / 'provenance/atlas_migration.json')
    inputs.update({r['path']: r['sha256'] for r in files})
    outputs = {rel(path): sha(path) for directory in (OUT, REPORTS) for path in sorted(directory.iterdir()) if path.is_file()}
    write(ROOT / 'provenance/build_manifest.json', {'catalog_version': '0.1.0', 'observed_on': '2026-09-14',
                                                  'inputs_sha256': inputs, 'outputs_sha256': outputs,
                                                  'network_used_by_build': False, 'absolute_paths_embedded': False})
    return summary


def verify():
    manifest = read(ROOT / 'provenance/build_manifest.json')
    current_atlas = {rel(path) for path in ATLAS.rglob('*') if path.is_file() and not any(p in {'.venv', '__pycache__', '.git'} for p in path.parts) and path.name != '.DS_Store'}
    recorded_atlas = {path for path in manifest['inputs_sha256'] if path.startswith('atlas/')}
    if current_atlas != recorded_atlas:
        raise ValueError('Atlas file inventory changed; rebuild the catalog to incorporate additions or removals.')
    for group in ('inputs_sha256', 'outputs_sha256'):
        for path, digest in manifest[group].items():
            check_hash(path, digest)
    return {'status': 'ok', 'inputs_verified': len(manifest['inputs_sha256']), 'outputs_verified': len(manifest['outputs_sha256'])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify'], default='build', nargs='?')
    args = parser.parse_args()
    print(json.dumps(build() if args.command == 'build' else verify(), indent=2))
