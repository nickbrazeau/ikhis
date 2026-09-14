#!/usr/bin/env python3
"""Remove AWS signed-link credential fields; never display matched values."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
ACCESS_ID=re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')
SIGNED_FIELD=re.compile(r'(?i)((?:[?&]|%26|%3F|\\u0026|\\u003[fF])(?:amp;)?(?:X-Amz-Credential|X-Amz-Security-Token|X-Amz-Signature|AWSAccessKeyId|Signature)(?:=|%3D|\\u003[dD]))((?:(?!%26|%3F)[^&\s"<>\\)])+)')
REDACTED='REDACTED'
def sanitize(text):
    text=SIGNED_FIELD.sub(lambda m:m[1]+REDACTED,text)
    return ACCESS_ID.sub('REDACTED_AWS_ACCESS_KEY_ID',text)
def sha(data): return hashlib.sha256(data).hexdigest()
def findings(paths):
    for path in paths:
        if not path.is_file() or path.suffix.lower() not in ('.json','.md','.txt','.xml','.html','.csv','.tsv','.yaml','.yml'): continue
        try:
            raw=path.read_bytes();text=raw.decode('utf-8')
        except (OSError,UnicodeError):continue
        clean=sanitize(text).encode('utf-8')
        if clean!=raw: yield path,raw,clean

def scan_files(paths):
    """Exact-hash exceptions are limited to documented synthetic review fixtures."""
    ledger=ROOT/'provenance/security_scan_exceptions.json'
    exceptions=json.loads(ledger.read_text()) if ledger.exists() else {}
    for path,raw,clean in findings(paths):
        rel=str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)
        exception=exceptions.get(rel,{})
        for parent in path.parents:
            if parent.name=='input_snapshot' and parent.parent.parent.name=='releases':
                archived_ledger=parent/'provenance/security_scan_exceptions.json'
                if archived_ledger.is_file():
                    archived=json.loads(archived_ledger.read_text())
                    exception=archived.get(str(path.relative_to(parent)),exception)
                    break
        if exception.get('sha256')==sha(raw) and exception.get('kind')=='synthetic_review_fixture':
            continue
        yield path,raw,clean

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='Sanitize research inputs only; frozen releases require a separate audit record.')
    args=parser.parse_args()
    paths=[p for folder in ('research','provenance','reports','data','releases','candidates') for p in (ROOT/folder).rglob('*') if not any(x in p.parts for x in ('.venv','__pycache__'))]
    found=[]
    for path,raw,clean in scan_files(paths):
        rel=path.relative_to(ROOT)
        if args.write and rel.parts[0]=='research':path.write_bytes(clean)
        found.append({'path':str(rel),'original_sha256':sha(raw),'sanitized_sha256':sha(clean),'sanitized':args.write and rel.parts[0]=='research'})
    print(json.dumps({'files_with_credential_metadata':found},indent=2))
    return 1 if found and not args.write else 0
if __name__=='__main__':raise SystemExit(main())
