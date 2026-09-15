"""Compatibility adapter for saved influenza request lists; use the safe fetcher."""
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('ikhis_metadata_fetcher', ROOT / 'scripts/fetch_metadata.py')
fetcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fetcher)


def fetch(item):
    name, url = item
    result = fetcher.fetch({'id': name, 'url': url, 'output': 'sources/influenza/snapshots/' + name})
    return {'path': 'data_dictionary/' + result['output'], 'url': result['requested_url'],
            'status': result.get('http_status'), 'bytes': result.get('bytes'),
            'sha256': result.get('sha256'), 'credential_metadata_redacted': result.get('credential_metadata_redacted'),
            **({'error': result['error']} if result.get('error') else {})}


if __name__ == '__main__':
    request_path = Path(sys.argv[1])
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, json.loads(request_path.read_text())))
    Path(str(request_path) + '.results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({'retrieved': sum('error' not in r for r in results),
                      'failed': [r['path'] for r in results if 'error' in r]}))
    raise SystemExit(int(any('error' in r for r in results)))
