"""Guardrails for provenance, raw-data semantics, coverage and safe joins."""
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('dictionary_builder', ROOT / 'scripts/build_dictionary.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def rows(name):
    return b.read(ROOT / 'catalog' / (name + '.json'))


class DictionaryTests(unittest.TestCase):
    def test_all_moved_bytes_preserved(self):
        ledger = b.read(ROOT / 'provenance/atlas_migration.json')
        self.assertEqual(ledger['file_count'], len(ledger['files_sha256']))
        for path, digest in ledger['files_sha256'].items():
            self.assertEqual(b.sha(b.ATLAS / path), digest, path)

    def test_complete_pinned_hr_inventory_and_unique_study_join(self):
        study = rows('hr_studies')
        self.assertEqual(len(study), 66)
        self.assertEqual(len({r['study_ID'] for r in study}), 66)
        listed = rows('hr_files')
        self.assertEqual({r['path_in_resource'] for r in listed}, {r['rfilename'] for r in b.read(b.HF / 'hf_info.json')['siblings']})
        self.assertEqual(len(listed), 175)
        single = [r for r in listed if r['path_in_resource'].startswith('single_cell_gene_expr/') and 'combined' not in r['path_in_resource']]
        self.assertEqual(len(single), 7)
        self.assertTrue(all(r['study_ID'] for r in single))

    def test_influenza_eligibility_and_shared_source_series(self):
        eligible = [r for r in rows('hr_studies') if r['influenza_challenge_eligibility'] == 'source_verified_influenza_challenge_subset']
        self.assertEqual(len(eligible), 6)
        self.assertEqual({a for r in eligible for a in r['canonical_source_accessions']}, {'GSE61754', 'GSE90732', 'GSE73072'})
        by_id = {r['id']: r for r in rows('influenza_studies')}
        for accession in ('GSE68310', 'GSE194378', 'GSE117580', 'GSE111368'):
            self.assertEqual(by_id[accession]['eligibility'], 'adjacent_excluded')
        self.assertEqual(len([r for r in by_id.values() if r['eligibility'] == 'included_human_influenza_challenge']), 26)

    def test_raw_names_do_not_promote_derived_data(self):
        self.assertEqual(b.hr_file_level('bulk_gene_expr/test_gene_expr.csv'), 'harmonized_expression_matrix')
        self.assertIn('unverified', b.hr_file_level('single_cell_gene_expr/test.h5ad'))
        raw_named_counts = [r for r in rows('influenza_files') if r.get('name') == 'GSE175551_Raw_gene_counts_matrix.txt.gz']
        self.assertEqual(len(raw_named_counts), 1)
        self.assertEqual(raw_named_counts[0]['data_level'], 'processed_counts_or_expression')
        self.assertFalse(any(r['instrument_raw_claim'] for r in rows('hr_files')))
        self.assertEqual(b.classify_atlas_file('research/sample.fastq.gz')[0], 'candidate_instrument_raw_requires_format_check')
        self.assertEqual(b.classify_atlas_file('research/snapshots/article.json')[0], 'documentary_or_repository_source_snapshot')

    def test_no_future_requests_labeled_currently_open(self):
        row = next(r for r in rows('datasets') if r['dataset_id'] == 'FLU:IMPERIAL_H3N2_MULTIMODAL2026')
        self.assertEqual(row['raw_access_status'], 'request_window_not_yet_open')
        record = next(r for r in rows('influenza_studies') if r['id'] == 'IMPERIAL_H3N2_MULTIMODAL2026')
        self.assertEqual(record['raw_data']['request_window_begins'], '2027-07-01')

    def test_missing_ids_are_not_zero_participants_or_failed_joins(self):
        counts = rows('hr_count_checks')
        for study in ('GSE220682', 'GSE281864'):
            row = next(r for r in counts if r['study_ID'] == study and r['measure'] == 'num_subjects')
            self.assertIsNone(row['observed_count'])
            self.assertEqual(row['status'], 'not_assessable_from_available_IDs')
        joins = rows('hr_join_checks')
        self.assertEqual(sum(r['status'] == 'requires_join_review' for r in joins), 8)
        self.assertEqual(sum(r['status'] == 'metadata_table_not_inspected' for r in joins), 5)
        self.assertEqual(sum(r['status'] == 'all_antibody_subjects_match_metadata' for r in joins), 24)
        self.assertEqual(b.observed_type(['NA', '<NA>', '']), 'all_missing_in_inspected_table')

    def test_source_hash_change_is_rejected(self):
        with tempfile.NamedTemporaryFile(dir=ROOT / 'tests') as stream:
            stream.write(b'verified metadata'); stream.flush()
            path = b.rel(Path(stream.name))
            digest = b.sha(stream.name)
            b.check_hash(path, digest)
            stream.write(b' changed'); stream.flush()
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                b.check_hash(path, digest)

    def test_file_relationships_and_availability_boundaries(self):
        datasets = rows('datasets')
        keys = {r['dataset_id'] for r in datasets}
        self.assertEqual(len(keys), len(datasets))
        files = rows('influenza_files')
        self.assertTrue(all(r['dataset_id'] in keys for r in files))
        self.assertFalse(any(r['local_biological_payload'] for r in files))
        self.assertTrue(any(r['access_url_kind'] == 'repository_or_publication_landing_page' for r in files))
        self.assertTrue(all(not r['biological_data_downloaded'] for r in rows('atlas_datasets')))

    def test_all_atlas_sources_have_coverage_disposition(self):
        sources = rows('atlas_sources')
        coverage = rows('atlas_source_coverage')
        self.assertEqual({r['source_key'] for r in sources}, {r['source_key'] for r in coverage})
        self.assertTrue(all(r['data_inventory_status'] for r in coverage))
        file_rows = rows('atlas_files')
        self.assertEqual(len({r['path'] for r in file_rows}), len(file_rows))
        self.assertFalse(any('/.venv/' in r['path'] for r in file_rows))

    def test_run_manifest_is_unique_without_participant_claim(self):
        runs = rows('viral_sequence_runs')
        self.assertEqual(len(runs), 278)
        self.assertEqual(len({r['run_accession'] for r in runs}), 278)
        self.assertTrue(all('assignment pending' in r['sample_scope'] for r in runs))

    def test_source_and_output_manifest(self):
        self.assertEqual(b.verify()['status'], 'ok')
        b.validate_sources(rows('influenza_studies'))

    def test_database_matches_json_exports(self):
        db = sqlite3.connect('file:' + str(ROOT / 'catalog/data_dictionary.sqlite') + '?mode=ro', uri=True)
        self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')
        for table in ('datasets', 'hr_fields', 'atlas_files', 'influenza_files', 'viral_sequence_runs'):
            self.assertEqual(db.execute('SELECT count(*) FROM ' + table).fetchone()[0], len(rows(table)))
        db.close()


if __name__ == '__main__':
    unittest.main()
