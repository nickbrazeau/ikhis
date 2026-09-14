import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('candidate', ROOT / 'scripts/build_candidate.py')
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


class ConnectionBoundaryTests(unittest.TestCase):
    def fixture(self):
        left = {'assertion_id': 'A1', 'subject': 'intervention', 'subject_type': 'perturbation',
                'subject_layer': 'G', 'object': 'intermediate', 'object_type': 'protein', 'object_layer': 'P',
                'species': 'Homo sapiens', 'qc_status': 'extracted_pending_review',
                'source_id': 'S1', 'direction': 'increase'}
        right = dict(left, assertion_id='A2', subject='intermediate', subject_type='protein',
                     subject_layer='P', object='response', object_type='phenotype', object_layer='F')
        bridge = {'bridge_type': 'serial_transition', 'bridge_relation': 'supports',
                  'status': 'candidate_pending_review', 'checks': {k: 'supported' for k in candidate.CHECKS},
                  'entity_mapping': 'Same measured protein form.', 'context_comparison': {'same_preparation': True},
                  'temporal_basis': 'Measured intermediate before response.', 'measurement_basis': 'Protein and function measured.',
                  'experimental_linkage': 'Intermediate transferred and blocked in the same preparation.',
                  'source_locators': ['Figure 1'], 'supporting_snapshot_paths': ['source.txt']}
        return bridge, left, right, {'S1': {'access_level': 'full_text_selected_methods_results'}}

    def test_documented_transition_is_only_a_pending_proposal(self):
        result = candidate.classify_bridge(*self.fixture())
        self.assertEqual(result['classification'], 'mechanism_proposal')
        self.assertEqual(result['review_status'], 'pending')
        self.assertFalse(result['production_approved'])

    def test_branches_and_contrasts_cannot_become_serial_paths(self):
        for kind in ('shared_intervention', 'context_contrast'):
            args = self.fixture()
            args[0]['bridge_type'] = kind
            result = candidate.classify_bridge(*args)
            self.assertFalse(result['serial_path'])
            self.assertNotEqual(result['classification'], 'mechanism_proposal')

    def test_same_name_does_not_bridge_rna_and_protein(self):
        args = self.fixture()
        args[1].update(object_type='RNA', object_layer='T')
        self.assertEqual(candidate.classify_bridge(*args)['classification'], 'blocked_connection')

    def test_protein_form_change_is_not_name_equivalence(self):
        args = self.fixture()
        args[2]['subject'] = 'phosphorylated intermediate'
        self.assertFalse(candidate.classify_bridge(*args)['serial_path'])

    def test_null_opposing_and_inconclusive_endpoints_block_serial_claim(self):
        for field, value in [('direction', 'null'), ('evidence_relation', 'opposes'), ('evidence_relation', 'inconclusive')]:
            args = self.fixture()
            args[2][field] = value
            self.assertEqual(candidate.classify_bridge(*args)['classification'], 'blocked_connection')

    def test_cross_species_and_unknown_species_are_blocked(self):
        for species in ('Mus musculus', 'unavailable'):
            args = self.fixture()
            args[1]['species'] = species
            self.assertFalse(candidate.classify_bridge(*args)['serial_path'])

    def test_unknown_context_timing_or_measurement_blocks(self):
        for name in candidate.CHECKS[:-1]:
            args = self.fixture()
            del args[0]['checks'][name]
            self.assertFalse(candidate.classify_bridge(*args)['serial_path'])

    def test_contradictory_context_cannot_be_overridden_by_other_checks(self):
        args = self.fixture()
        args[0]['checks']['context_compatibility'] = {'status': 'contradictory', 'explanation': 'different cells'}
        self.assertFalse(candidate.classify_bridge(*args)['serial_path'])

    def test_mediation_requires_intermediate_perturbation_attestation(self):
        args = self.fixture()
        args[0]['bridge_type'] = 'mediation_test'
        args[0]['checks']['mediation_test'] = 'not_demonstrated'
        self.assertEqual(candidate.classify_bridge(*args)['classification'], 'blocked_connection')

    def test_full_text_gap_cannot_be_upgraded_by_positive_bridge(self):
        args = self.fixture()
        args[2]['qc_status'] = 'needs_full_text'
        self.assertEqual(candidate.classify_bridge(*args)['classification'], 'blocked_connection')
        args = self.fixture()
        args[3]['S1']['access_level'] = 'abstract'
        self.assertFalse(candidate.classify_bridge(*args)['serial_path'])


class CandidateIntegrityTests(unittest.TestCase):
    def test_source_dependencies_include_companions_figures_and_supplements(self):
        source = {'snapshot_path': 'primary.html', 'companion_snapshot_path': 'primary.txt',
                  'additional_snapshots': ['figure.png'], 'additional_snapshot_paths': ['supplement.pdf']}
        self.assertEqual(candidate.source_paths(source), ['figure.png', 'primary.html', 'primary.txt', 'supplement.pdf'])

    def test_modified_source_fails_candidate_verification(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / 'source.txt').write_text('original evidence')
            candidate.write(root / 'manifest.json', {'files': {'source.txt': candidate.sha(root / 'source.txt')}})
            self.assertTrue(candidate.verify(root)['ok'])
            (root / 'source.txt').write_text('different evidence')
            self.assertFalse(candidate.verify(root)['ok'])

    def test_changed_working_inputs_do_not_invalidate_preserved_snapshot_but_are_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            working, output = root / 'working', root / 'output'
            working.mkdir(); output.mkdir()
            (working / 'source.txt').write_text('original evidence')
            candidate.write(output / 'input_manifest.json', {'files': {'source.txt': candidate.sha(working / 'source.txt')}})
            candidate.write(output / 'manifest.json', {'files': {'input_manifest.json': candidate.sha(output / 'input_manifest.json')}})
            (working / 'source.txt').write_text('updated evidence')
            self.assertTrue(candidate.verify(output)['ok'])
            self.assertFalse(candidate.verify(output, working)['ok'])

    def test_source_path_cannot_escape_declared_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inside = root / 'inside'; inside.mkdir()
            (root / 'outside.txt').write_text('outside')
            with self.assertRaises(ValueError):
                candidate.local_path(inside, '../outside.txt')

    def test_real_candidate_keeps_every_baseline_table_unchanged(self):
        bundle = candidate.load_bundle(ROOT)
        with tempfile.TemporaryDirectory() as temporary:
            metadata, counts, graphs = candidate.build_database(ROOT, Path(temporary) / 'candidate.sqlite', bundle)
            self.assertTrue(metadata['baseline_tables_unchanged'])
            self.assertEqual(metadata['new_priors'], 0)
            self.assertEqual(metadata['new_approved_paths'], 0)
            self.assertEqual(counts['candidate_assertions'], len(bundle['assertions']))
            self.assertTrue(all(g['review_status'] == 'pending' for g in graphs))
            self.assertTrue(all(not g['graph']['production_approved_paths'] for g in graphs))

    def test_abstract_source_cannot_claim_completed_primary_extraction(self):
        original = candidate.read
        def altered(path):
            data = original(path)
            if str(path).endswith('mechanisms_genetic/pack.json'):
                data['sources'][0]['access_level'] = 'abstract_only'
            return data
        with patch.object(candidate, 'read', side_effect=altered):
            with self.assertRaisesRegex(ValueError, 'lacks registered primary full-text'):
                candidate.load_bundle(ROOT)

    def test_excluded_source_cannot_supply_extracted_assertions(self):
        original = candidate.read
        def altered(path):
            data = original(path)
            if str(path).endswith('mechanisms_genetic/screening.json'):
                for row in data['candidate_appearances']:
                    row['decision'] = 'exclude'
            return data
        with patch.object(candidate, 'read', side_effect=altered):
            with self.assertRaisesRegex(ValueError, 'lacks an eligible screening decision'):
                candidate.load_bundle(ROOT)

    def test_real_inventory_is_expansive_and_only_discovery(self):
        scope = json.loads((ROOT / 'data/product_scope.json').read_text())
        inventory = json.loads((ROOT / 'data/cytokine_inventory.json').read_text())
        self.assertEqual(scope['cytokine_scope'], 'all_cytokines')
        self.assertIsNone(scope['fixed_priority_panel'])
        manifest = json.loads((ROOT / 'research/cytokine_inventory/inventory_manifest.json').read_text())
        self.assertEqual(len(inventory), sum(q['result_count'] for q in manifest['queries']))
        self.assertEqual(len(inventory), len({i['uniprot_accession'] for i in inventory}))
        self.assertTrue(all(i['biological_evidence_status'] == 'inventory_only_no_assertion_or_prior' for i in inventory))


if __name__ == '__main__':
    unittest.main()
