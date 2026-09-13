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
if __name__=='__main__':unittest.main()
