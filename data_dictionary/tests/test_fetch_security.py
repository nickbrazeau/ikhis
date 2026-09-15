import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('metadata_fetch_security', ROOT / 'scripts/fetch_metadata.py')
fetcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetcher)


class Response:
    status_code = 200
    headers = {'Content-Type': 'text/html'}
    def raise_for_status(self): pass
    def iter_content(self, size): yield self.body


class FetchSecurityTests(unittest.TestCase):
    def test_arbitrary_text_suffix_is_sanitized_before_writing(self):
        key = 'AIza' + 'D' * 35
        response = Response()
        response.body = ('<script>key="' + key + '"</script><p>Evidence retained.</p>').encode()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            with patch.object(fetcher, 'ROOT', root), patch.object(fetcher.requests, 'get', return_value=response):
                result = fetcher.fetch({'id': 'test', 'url': 'https://example.invalid/article', 'output': 'sources/article.qmd'})
            self.assertEqual(result['status'], 'retrieved')
            self.assertTrue(result['credential_metadata_redacted'])
            text = (root / 'sources/article.qmd').read_text()
            self.assertNotIn(key, text)
            self.assertIn('Evidence retained.', text)

    def test_failed_request_does_not_echo_key_in_error_or_url(self):
        key = 'AIza' + 'E' * 35
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(fetcher, 'ROOT', Path(folder).resolve()), patch.object(fetcher.requests, 'get', side_effect=RuntimeError('failed ?key=' + key)):
                result = fetcher.fetch({'id': 'test', 'url': 'https://example.invalid/article?key=' + key, 'output': 'sources/article.html'})
            self.assertEqual(result['status'], 'failed')
            self.assertNotIn(key, str(result))


if __name__ == '__main__': unittest.main()
