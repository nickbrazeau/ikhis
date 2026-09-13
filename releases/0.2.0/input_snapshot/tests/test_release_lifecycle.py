import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from test_kb import kb

class ReleaseLifecycleTests(unittest.TestCase):
    def test_retrieval_date_survives_copy_metadata_changes_but_not_changed_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source.json';source.write_text('source')
            (root/'provenance').mkdir()
            (root/'provenance/source_retrieval_times.json').write_text(json.dumps({'source.json':{'sha256':kb.file_hash(source),'retrieved_at':'2026-09-13T00:00:00Z'}}))
            with patch.object(kb,'ROOT',root):
                os.utime(source,(100,100))
                self.assertEqual(kb.recorded_retrieval_time(source),'2026-09-13T00:00:00Z')
                source.write_text('different source')
                self.assertEqual(kb.recorded_retrieval_time(source),'unavailable')

    def test_documented_security_redaction_is_explicit_and_tamper_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);release=root/'releases/0.1.0';source=release/'input_snapshot/research/source.json'
            source.parent.mkdir(parents=True);source.write_text('sanitized')
            original=hashlib.sha256(b'original').hexdigest()
            manifest=release/'manifest.json';manifest.write_text(json.dumps({'files':{'research/source.json':original}}))
            ledger={'original_manifest_sha256':kb.file_hash(manifest),'redactions':{'research/source.json':{'original_sha256':original,'sanitized_sha256':kb.file_hash(source)}}}
            (release/'security_redactions.json').write_text(json.dumps(ledger))
            with patch.object(kb,'ROOT',root),patch.object(kb,'RELEASE',release):
                self.assertEqual(kb.manifest_mismatches(release),[])
                self.assertIn('research/source.json',kb.verified_security_redactions(release))
                source.write_text('unrecorded change')
                self.assertEqual(kb.manifest_mismatches(release),['research/source.json'])
                ledger['redactions']['research/source.json']['original_sha256']='wrong'
                (release/'security_redactions.json').write_text(json.dumps(ledger))
                with self.assertRaisesRegex(ValueError,'Invalid security-redaction'):kb.manifest_mismatches(release)

    def test_review_approval_expires_when_source_or_extraction_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'source.json';pack=root/'pack.json'
            source.write_text('source methods');pack.write_text('extraction')
            approval={'sha256':kb.file_hash(pack),'source_hashes':{'source.json':kb.file_hash(source)}}
            with patch.object(kb,'ROOT',root):
                self.assertTrue(kb.review_inputs_approved(pack,approval,['source.json']))
                source.write_text('different methods')
                self.assertFalse(kb.review_inputs_approved(pack,approval,['source.json']))
                source.write_text('source methods');pack.write_text('different extraction')
                self.assertFalse(kb.review_inputs_approved(pack,approval,['source.json']))
                pack.write_text('extraction')
                self.assertFalse(kb.review_inputs_approved(pack,approval,['missing.json']))

    def test_old_release_verifies_after_working_input_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);release=root/'releases/0.1.0';release.mkdir(parents=True)
            (root/'data').mkdir();source=root/'data/pack.json';source.write_text('original')
            output=release/'table.csv';output.write_text('frozen')
            manifest={'files':{'data/pack.json':hashlib.sha256(b'original').hexdigest(),'releases/0.1.0/table.csv':hashlib.sha256(b'frozen').hexdigest()}}
            (release/'manifest.json').write_text(json.dumps(manifest))
            with patch.object(kb,'ROOT',root),patch.object(kb,'RELEASE',release):
                kb.snapshot_inputs(manifest)
                source.write_text('next release')
                self.assertTrue(kb.verify())
                (release/'input_snapshot/data/pack.json').write_text('tampered')
                self.assertFalse(kb.verify())

    def test_frozen_release_cannot_be_rebuilt_or_refrozen(self):
        with tempfile.TemporaryDirectory() as temp:
            release=Path(temp);(release/'manifest.json').write_text('{}')
            database=release/'immune_prior.sqlite';database.write_bytes(b'preserve this')
            with patch.object(kb,'RELEASE',release):
                with self.assertRaisesRegex(ValueError,'immutable'): kb.build()
                with self.assertRaisesRegex(ValueError,'immutable'): kb.freeze()
            self.assertEqual(database.read_bytes(),b'preserve this')

    def test_added_changed_removed_and_unchanged_lineage(self):
        old={'same':{'x':1},'changed':{'x':1},'removed':{'x':1}}
        new={'same':{'x':1},'changed':{'x':2},'added':{'x':3}}
        changes=list(kb.compare_records(old,new))
        self.assertEqual({r[0]:r[1] for r in changes},{'added':'added','changed':'modified','removed':'removed'})

    def test_snapshot_conflict_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);release=root/'releases/0.2.0';target=release/'input_snapshot/data/pack.json'
            target.parent.mkdir(parents=True);target.write_text('old')
            (root/'data').mkdir();(root/'data/pack.json').write_text('new')
            manifest={'files':{'data/pack.json':hashlib.sha256(b'new').hexdigest()}}
            with patch.object(kb,'ROOT',root),patch.object(kb,'RELEASE',release):
                with self.assertRaisesRegex(ValueError,'Conflicting'): kb.snapshot_inputs(manifest)
            self.assertEqual(target.read_text(),'old')

if __name__=='__main__':unittest.main()
