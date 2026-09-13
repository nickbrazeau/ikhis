"""Independent IMPL02 regressions; every evidence fixture is synthetic."""
import contextlib
import copy
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from test_kb import kb
import sanitize_snapshots as sanitizer


class ReviewedInputIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.release = self.root / 'releases/0.2.0'
        for rel in (
            'README.md', 'protocol/PROTOCOL.md', 'protocol/AMENDMENT_0.2.md',
            'research/EXTRACTION_CONTRACT.md',
            'research/EXTRACTION_CONTRACT_0.2.md', 'provenance/USER_REQUEST.md',
        ):
            self.write_text(rel, 'Synthetic test instruction.\n')
        (self.root / 'data').mkdir()

    def write_text(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def write_json(self, rel, value):
        return self.write_text(rel, json.dumps(value, sort_keys=True) + '\n')

    def make_pack(self, lane='cytokine_expansion', relation='supports'):
        self.lane = lane
        self.previous_version = None
        # C-A01 exercises the carried-forward annotation ID without using its
        # real assertion, source, context, or other biological content.
        self.assertion_id = 'C-A01' if lane == 'cytokine' else 'TEST_A'
        self.source_rel = 'research/' + lane + '/source.txt'
        self.source = self.write_text(self.source_rel, 'Synthetic source methods.\n')
        self.annotation = {
            'tested_hypothesis': 'Synthetic X increases synthetic Y',
            'evidence_relation': relation,
            'null_adequacy': 'unavailable',
        }
        assertion = {
            'assertion_id': self.assertion_id,
            'source_id': 'TEST_S', 'cohort_id': 'TEST_C',
            'subject': 'synthetic X', 'subject_type': 'protein',
            'subject_layer': 'P', 'object': 'synthetic Y',
            'object_type': 'protein', 'object_layer': 'P',
            'species': 'synthetic species', 'predicate': 'increases',
            'measurement': 'protein_abundance', 'direction': 'increase',
            'evidence_tier': 'P3', 'qc_status': 'reviewed_extraction',
            'source_locator': 'Synthetic locator',
            'evidence_summary': 'Synthetic summary',
            'qualitative_confidence': 'moderate',
            'scoring_annotation': copy.deepcopy(self.annotation),
        }
        self.pack = {
            'sources': [{
                'source_id': 'TEST_S', 'title': 'Synthetic source',
                'url': 'https://example.invalid/source',
                'snapshot_path': self.source_rel, 'access_level': 'full_text',
            }],
            'cohorts': [{
                'cohort_id': 'TEST_C', 'parent_cohort': 'unavailable',
                'independence_status': 'resolved',
            }],
            'assertions': [assertion],
            'searches': [{
                'search_id': 'TEST_QUERY', 'lane': lane,
                'query': 'synthetic query', 'database': 'synthetic fixture',
                'searched_at': '2026-09-13T00:00:00Z',
            }],
        }
        self.pack_rel = 'research/' + lane + '/pack.json'
        self.pack_path = self.write_json(self.pack_rel, self.pack)
        self.screening = self.write_json('research/' + lane + '/screening.json', [{
            'candidate_id': 'TEST_CANDIDATE', 'query_id': 'TEST_QUERY',
            'title': 'Synthetic source', 'url': 'https://example.invalid/source',
            'source_id': 'TEST_S', 'decision': 'include',
            'reason': 'Synthetic fixture meets the synthetic inclusion rule.',
        }])
        self.write_json('data/scoring_annotations.json', {
            self.assertion_id: copy.deepcopy(self.annotation),
        })
        self.write_json('data/reviewed_expansion_packs.json', {lane: {
            'sha256': kb.file_hash(self.pack_path),
            'source_hashes': {self.source_rel: kb.file_hash(self.source)},
            'screening_sha256': kb.file_hash(self.screening),
        }})

    def add_supporting_snapshot(self):
        rel = 'research/' + self.lane + '/additional_source.txt'
        additional = self.write_text(rel, 'Synthetic additional outcome passage.\n')
        self.pack['sources'][0]['additional_snapshot_paths'] = [rel]
        self.write_json(self.pack_rel, self.pack)
        self.write_json('data/reviewed_expansion_packs.json', {self.lane: {
            'sha256': kb.file_hash(self.pack_path),
            'source_hashes': {
                self.source_rel: kb.file_hash(self.source), rel: kb.file_hash(additional),
            },
            'screening_sha256': kb.file_hash(self.screening),
        }})
        return additional

    @staticmethod
    def synthetic_references(db):
        entity_id = kb.ensure_entity(db, 'synthetic reference', 'protein', 'P')
        for index in range(30):
            kb.insert(db, 'entity_aliases', {
                'alias_id': 'TEST_ALIAS_' + str(index),
                'entity_id': entity_id,
                'original_label': 'synthetic alias ' + str(index),
            })

    def archive_legacy(self):
        self.previous_version = '0.1.0'
        previous = self.root / 'releases/0.1.0'
        previous.mkdir(parents=True)
        database = previous / 'immune_prior.sqlite'
        with sqlite3.connect(database) as db:
            for table, definition in kb.TABLES.items():
                db.execute('CREATE TABLE ' + table + ' (' + definition + ')')
        paths = [self.pack_path, self.source, database,
                 self.root / 'data/scoring_annotations.json']
        paths.extend(self.root / rel for source in self.pack['sources']
                     for rel in source.get('additional_snapshot_paths', []))
        manifest = {
            'release': '0.1.0', 'previous_release': None,
            'hash_algorithm': 'sha256',
            'files': {str(p.relative_to(self.root)): kb.file_hash(p) for p in paths},
        }
        self.write_json('releases/0.1.0/manifest.json', manifest)
        with patch.object(kb, 'ROOT', self.root), patch.object(kb, 'RELEASE', previous):
            kb.snapshot_inputs(manifest)
        (self.root / 'data/reviewed_expansion_packs.json').unlink()

    def run_build(self):
        with contextlib.ExitStack() as stack:
            for name, value in (
                ('ROOT', self.root), ('RELEASE', self.release),
                ('PACK_LANES', (self.lane,)),
                ('PREVIOUS_VERSION', self.previous_version),
                ('build_reference_entities', self.synthetic_references),
            ):
                stack.enter_context(patch.object(kb, name, value))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            try:
                succeeded = kb.build()
            except ValueError as error:
                return {'rejected': True, 'reason': str(error)}
        with sqlite3.connect(self.release / 'immune_prior.sqlite') as db:
            db.row_factory = sqlite3.Row
            row = db.execute(
                "SELECT a.status, e.evidence_relation, p.availability, p.estimate "
                "FROM edge_assertions a JOIN evidence_instances e USING(assertion_id) "
                "JOIN prior_parameters p USING(assertion_id) "
                "WHERE a.assertion_id=? AND p.parameter_family='existence'",
                (self.assertion_id,),
            ).fetchone()
            count = db.execute('SELECT COUNT(*) FROM screening_candidates').fetchone()[0]
        return {'rejected': not succeeded, 'row': dict(row), 'screening_count': count}

    def assert_numeric_withheld(self, result):
        if not result['rejected']:
            self.assertNotEqual(result['row']['availability'], 'available', result)
            self.assertIsNone(result['row']['estimate'], result)

    def assert_legacy_baseline(self):
        result = self.run_build()
        self.assertFalse(result['rejected'], result)
        self.assertEqual(result['row']['availability'], 'available', result)

    def test_impl02_001_external_scoring_cannot_upgrade_approved_inconclusive(self):
        self.make_pack(relation='inconclusive')
        self.write_json('data/scoring_annotations.json', {
            self.assertion_id: dict(self.annotation, evidence_relation='supports'),
        })
        self.assert_numeric_withheld(self.run_build())

    def test_impl02_002_changed_legacy_pack_loses_review_eligibility(self):
        self.make_pack(lane='cytokine')
        self.archive_legacy()
        self.assert_legacy_baseline()
        self.pack['assertions'][0]['object'] = 'unreviewed replacement'
        self.write_json(self.pack_rel, self.pack)
        self.assert_numeric_withheld(self.run_build())

    def test_impl02_002_changed_legacy_source_loses_review_eligibility(self):
        self.make_pack(lane='cytokine')
        self.archive_legacy()
        self.assert_legacy_baseline()
        self.source.write_text('Unreviewed replacement source methods.\n')
        self.assert_numeric_withheld(self.run_build())

    def test_impl02_003_missing_expansion_screening_prevents_successful_build(self):
        self.make_pack()
        baseline = self.run_build()
        self.assertFalse(baseline['rejected'], baseline)
        self.assertEqual(baseline['screening_count'], 1)
        self.screening.unlink()
        result = self.run_build()
        self.assertTrue(result['rejected'], result)

    def test_impl02_003_unrelated_or_exclude_only_candidate_cannot_cover_source(self):
        self.make_pack()
        candidates = json.loads(self.screening.read_text())
        self.assertFalse(self.run_build()['rejected'])
        for case in ('unrelated', 'excluded', 'awaiting_full_text'):
            with self.subTest(case=case):
                changed = copy.deepcopy(candidates)
                if case == 'unrelated':
                    changed[0]['source_id'] = 'UNRELATED_SOURCE'
                    changed[0]['url'] = 'https://example.invalid/unrelated'
                elif case == 'excluded':
                    changed[0]['decision'] = 'exclude'
                else:
                    changed[0]['decision'] = 'await_full_text'
                self.screening.write_text(json.dumps(changed))
                result = self.run_build()
                self.assertTrue(result['rejected'], result)

    def test_additional_expansion_source_mutation_invalidates_review(self):
        self.make_pack()
        additional = self.add_supporting_snapshot()
        self.assert_legacy_baseline()
        additional.write_text('Unreviewed additional outcome passage.\n')
        self.assert_numeric_withheld(self.run_build())

    def test_additional_legacy_source_mutation_invalidates_review(self):
        self.make_pack(lane='cytokine')
        additional = self.add_supporting_snapshot()
        self.archive_legacy()
        self.assert_legacy_baseline()
        additional.write_text('Unreviewed additional outcome passage.\n')
        self.assert_numeric_withheld(self.run_build())

    def test_annotation_generator_rechecks_additional_source(self):
        import annotate_scoring
        self.make_pack()
        additional = self.add_supporting_snapshot()
        for lane in ('cytokine', 'genomic', 'proteomic'):
            self.write_json('research/' + lane + '/pack.json', {
                'sources': [], 'cohorts': [], 'assertions': [],
            })
        with patch.object(annotate_scoring, 'ROOT', self.root), \
                patch.object(annotate_scoring, 'kb', kb), \
                patch.object(kb, 'ROOT', self.root):
            annotate_scoring.main()
            annotations = json.loads((self.root / 'data/scoring_annotations.json').read_text())
            self.assertEqual(annotations[self.assertion_id]['evidence_relation'], 'supports')
            additional.write_text('Unreviewed additional outcome passage.\n')
            annotate_scoring.main()
            annotations = json.loads((self.root / 'data/scoring_annotations.json').read_text())
            self.assertEqual(annotations[self.assertion_id]['evidence_relation'], 'unavailable')

    def test_curation_rechecks_base_and_overlay_additional_sources(self):
        self.make_pack(lane='cytokine')
        inherited = self.add_supporting_snapshot()
        dependencies = [self.pack_path, self.source, inherited]
        for lane in ('genomic', 'proteomic'):
            dependencies.append(self.write_json('research/' + lane + '/pack.json', {
                'sources': [], 'cohorts': [], 'assertions': [],
            }))
        overlay_source = self.write_text('research/curation_additional.txt',
                                         'Synthetic curated outcome passage.\n')
        dependencies.append(overlay_source)
        curations = {'sources': {'TEST_S': {'additional_snapshot_paths': [
            'research/curation_additional.txt',
        ]}}}
        overlay = self.write_json('data/curation_overrides_0.2.json', curations)
        self.write_json('data/reviewed_curations.json', {
            'sha256': kb.file_hash(overlay),
            'source_hashes': {str(p.relative_to(self.root)): kb.file_hash(p) for p in dependencies},
        })
        with patch.object(kb, 'ROOT', self.root):
            self.assertEqual(kb.approved_curations(), curations)
            for source in (inherited, overlay_source):
                with self.subTest(path=source.name):
                    original = source.read_bytes()
                    source.write_text('Unreviewed additional source.\n')
                    self.assertEqual(kb.approved_curations(), {})
                    source.write_bytes(original)
                    self.assertEqual(kb.approved_curations(), curations)


class EncodedCredentialRegressionTests(unittest.TestCase):
    def assert_sanitized_and_detected(self, original, marker):
        clean = sanitizer.sanitize(original)
        self.assertNotIn(marker, clean)
        self.assertEqual(sanitizer.sanitize(clean), clean)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'synthetic.json'
            path.write_text(original)
            self.assertEqual(len(list(sanitizer.findings([path]))), 1)
            path.write_text(clean)
            self.assertEqual(list(sanitizer.findings([path])), [])
        return clean

    def test_impl02_004_percent_encoded_first_query_separator(self):
        text = ('https%3A%2F%2Fexample.invalid%2Fa%3FX-Amz-Signature%3D'
                'SYNTHETIC_SIGNATURE%26X-Amz-Expires%3D3600')
        clean = self.assert_sanitized_and_detected(text, 'SYNTHETIC_SIGNATURE')
        self.assertIn('X-Amz-Expires%3D3600', clean)

    def test_impl02_004_json_unicode_escaped_query_separator(self):
        text = ('{"url":"https://example.invalid/a?x=1'
                '\\u0026X-Amz-Security-Token=SYNTHETIC_TOKEN'
                '\\u0026X-Amz-Expires=3600","text":"Unrelated source text."}')
        clean = self.assert_sanitized_and_detected(text, 'SYNTHETIC_TOKEN')
        decoded = json.loads(clean)
        self.assertEqual(decoded['text'], 'Unrelated source text.')
        self.assertIn('X-Amz-Expires=3600', decoded['url'])

    def test_synthetic_review_exception_is_bound_to_exact_bytes_and_kind(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            review = root / 'research/review_fixture.json'
            review.parent.mkdir()
            review.write_text('{"url":"https://example.invalid/a?'
                              'X-Amz-Signature=SYNTHETIC_SIGNATURE"}')
            source = root / 'research/source_fixture.json'
            source.write_bytes(review.read_bytes())
            ledger = root / 'provenance/security_scan_exceptions.json'
            ledger.parent.mkdir()
            record = {'sha256': kb.file_hash(review), 'kind': 'synthetic_review_fixture'}
            ledger.write_text(json.dumps({'research/review_fixture.json': record}))
            archived_reviews = []
            for prefix in (
                'releases/0.2.0/input_snapshot',
                'releases/0.3.0/input_snapshot/releases/0.2.0/input_snapshot',
            ):
                archived_review = root / prefix / 'research/review_fixture.json'
                archived_review.parent.mkdir(parents=True)
                archived_review.write_bytes(review.read_bytes())
                archived_ledger = root / prefix / 'provenance/security_scan_exceptions.json'
                archived_ledger.parent.mkdir()
                archived_ledger.write_bytes(ledger.read_bytes())
                archived_reviews.append(archived_review)
            with patch.object(sanitizer, 'ROOT', root):
                self.assertEqual(len(list(sanitizer.findings([review]))), 1)
                matches = [p for p, _, _ in sanitizer.scan_files([review, source] + archived_reviews)]
                self.assertEqual(matches, [source])
                archived_reviews[0].write_text(archived_reviews[0].read_text() + '\n')
                self.assertEqual(len(list(sanitizer.scan_files([archived_reviews[0]]))), 1)
                record['kind'] = 'unrecognized_exception'
                ledger.write_text(json.dumps({'research/review_fixture.json': record}))
                self.assertEqual(len(list(sanitizer.scan_files([review]))), 1)
                record['kind'] = 'synthetic_review_fixture'
                ledger.write_text(json.dumps({'research/review_fixture.json': record}))
                review.write_text(review.read_text() + '\n')
                self.assertEqual(len(list(sanitizer.scan_files([review]))), 1)


if __name__ == '__main__':
    unittest.main()
