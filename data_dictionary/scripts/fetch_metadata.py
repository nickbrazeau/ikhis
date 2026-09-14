#!/usr/bin/env python3
"""Retrieve public metadata with bounded sizes and stable, credential-free provenance."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time
from urllib.parse import urlparse
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT.parent / 'atlas/scripts'))
from sanitize_snapshots import sanitize


def fetch(record):
    relative = record['output']
    target = (ROOT / relative).resolve()
    if not target.is_relative_to(ROOT / 'sources'):
        raise ValueError('Metadata output must be under data_dictionary/sources')
    if urlparse(record['url']).scheme != 'https':
        raise ValueError('HTTPS public sources required')
    target.parent.mkdir(parents=True, exist_ok=True)
    result = {'id': record['id'], 'requested_url': record['url'], 'output': relative,
              'retrieved_at': datetime.now(timezone.utc).isoformat()}
    try:
        response = requests.get(record['url'], timeout=(10, 35), stream=True,
                                headers={'User-Agent': 'IKHIS-data-dictionary/0.1 public metadata research'})
        result['http_status'] = response.status_code
        response.raise_for_status()
        maximum = record.get('max_bytes', 10_000_000)
        data = bytearray()
        for chunk in response.iter_content(65536):
            data.extend(chunk)
            if len(data) > maximum:
                raise ValueError('Response exceeds metadata size limit')
        content_type = response.headers.get('Content-Type', '')
        result['content_type'] = content_type
        # Record only safe selected headers. Redirect URLs, cookies, and authorization
        # metadata are deliberately never persisted.
        result['resource_commit'] = response.headers.get('X-Repo-Commit', 'unavailable')
        result['etag'] = response.headers.get('ETag', 'unavailable')
        result['pagination_link'] = sanitize(response.headers.get('Link', ''))
        raw = bytes(data)
        if target.suffix.lower() in {'.json', '.csv', '.tsv', '.txt', '.html', '.md', '.xml'}:
            clean = sanitize(raw.decode('utf-8-sig')).encode('utf-8')
            result['credential_metadata_redacted'] = clean != raw and sanitize(raw.decode('utf-8-sig')) != raw.decode('utf-8-sig')
            raw = clean
        target.write_bytes(raw)
        result.update(status='retrieved', bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    except Exception as error:
        # Exceptions can include signed redirect URLs, so sanitize before recording.
        result.update(status='failed', error=sanitize(str(error)))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('request_file', type=Path)
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    records = json.loads(args.request_file.read_text())
    with ThreadPoolExecutor(max_workers=min(max(args.workers, 1), 4)) as pool:
        results = list(pool.map(fetch, records))
    log = args.request_file.with_suffix('.results.json')
    log.write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps({'retrieved': sum(r['status'] == 'retrieved' for r in results),
                      'failed': [r['id'] for r in results if r['status'] != 'retrieved'],
                      'log': str(log)}, indent=2))
    return int(any(r['status'] != 'retrieved' for r in results))


if __name__ == '__main__':
    raise SystemExit(main())
