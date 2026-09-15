import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('sanitize_snapshots',Path(__file__).resolve().parents[1]/'scripts/sanitize_snapshots.py')
sanitizer=importlib.util.module_from_spec(spec);spec.loader.exec_module(sanitizer)
class SnapshotSecurityTests(unittest.TestCase):
    def test_presigned_link_loses_credentials_and_preserves_source_and_expiry(self):
        key='ASIA'+'A'*16
        source='https://example.invalid/paper.pdf?X-Amz-Credential='+key+'%2Fscope&X-Amz-Security-Token=sample-token&X-Amz-Signature=sample-signature&X-Amz-Date=20260312T133919Z&X-Amz-Expires=3600'
        clean=sanitizer.sanitize(source)
        self.assertNotIn(key,clean);self.assertNotIn('sample-token',clean);self.assertNotIn('sample-signature',clean)
        self.assertIn('paper.pdf',clean);self.assertIn('X-Amz-Expires=3600',clean)
        self.assertEqual(sanitizer.sanitize(clean),clean)
    def test_json_escaping_and_unrelated_evidence_are_preserved(self):
        source='{"text":"IL5 increased survival. (https://example.invalid/a?X-Amz-Signature=sample)\\nResults unchanged."}'
        clean=sanitizer.sanitize(source)
        import json
        self.assertIn('Results unchanged.',json.loads(clean)['text'])
        self.assertEqual(sanitizer.sanitize('IL5 10 ng/mL; p<0.05.'),'IL5 10 ng/mL; p<0.05.')
    def test_encoded_credential_and_bare_key_are_removed(self):
        source='url%26X-Amz-Credential%3D'+'ASIA'+'B'*16+'%26q%3Dvalue'
        self.assertIn('REDACTED%26q',sanitizer.sanitize(source))
        self.assertEqual(sanitizer.sanitize('AKIA'+'C'*16),'REDACTED_AWS_ACCESS_KEY_ID')
    def test_inventory_tsv_is_included_in_file_scans(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'inventory.tsv'
            path.write_text('source\turl\npaper\thttps://example.invalid/paper?X-Amz-Signature=synthetic\n')
            hits=list(sanitizer.findings([path]))
            self.assertEqual(len(hits),1)
            self.assertNotIn(b'=synthetic',hits[0][2])
    def test_google_key_in_publisher_config_and_query_is_redacted(self):
        import json
        key='AIza'+'A'*35
        source='<script>window.config='+json.dumps({'impactGoogleMapsApiKey':key})+';</script><p>FOXP3 results unchanged.</p>'
        clean=sanitizer.sanitize(source)
        self.assertNotIn(key,clean)
        self.assertIn('REDACTED_GOOGLE_API_KEY',clean)
        self.assertIn('<p>FOXP3 results unchanged.</p>',clean)
        self.assertEqual(sanitizer.sanitize(clean),clean)
        self.assertEqual(sanitizer.sanitize('https://example.invalid/map?key='+key+'&language=en'),
                         'https://example.invalid/map?key=REDACTED_GOOGLE_API_KEY&language=en')
    def test_google_key_scanned_in_other_text_formats_without_echoing_value(self):
        import tempfile
        key='AIza'+'B'*35
        with tempfile.TemporaryDirectory() as folder:
            for name in ('snapshot.qmd','snapshot.text','config.js','snapshot'):
                path=Path(folder)/name;path.write_text('key="'+key+'"')
                hits=list(sanitizer.findings([path]))
                self.assertEqual(len(hits),1)
                self.assertNotIn(key.encode(),hits[0][2])
    def test_google_pattern_does_not_mask_short_or_long_nonkeys(self):
        for value in ('AIza'+'C'*34,'AIza'+'C'*36,'gene_AIzalike_expression'):
            self.assertEqual(sanitizer.sanitize(value),value)
if __name__=='__main__':unittest.main()
