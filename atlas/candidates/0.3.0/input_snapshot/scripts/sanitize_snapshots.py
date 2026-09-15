#!/usr/bin/env python3
"""Redact AWS signed-link credentials and Google API keys; never display values."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
ACCESS_ID=re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b')
GOOGLE_API_KEY=re.compile(r'(?<![A-Za-z0-9_-])AIza[0-9A-Za-z_-]{35}(?![A-Za-z0-9_-])')
SIGNED_FIELD=re.compile(r'(?i)((?:[?&]|%26|%3F|\\u0026|\\u003[fF])(?:amp;)?(?:X-Amz-Credential|X-Amz-Security-Token|X-Amz-Signature|AWSAccessKeyId|Signature)(?:=|%3D|\\u003[dD]))((?:(?!%26|%3F)[^&\s"<>\\)])+)')
REDACTED='REDACTED'
def sanitize(text):
    text=SIGNED_FIELD.sub(lambda m:m[1]+REDACTED,text)
    text=ACCESS_ID.sub('REDACTED_AWS_ACCESS_KEY_ID',text)
    return GOOGLE_API_KEY.sub('REDACTED_GOOGLE_API_KEY',text)
def sha(data): return hashlib.sha256(data).hexdigest()
def findings(paths):
    for path in paths:
        # Source snapshots also use .qmd, .text, .js and extensionless names.
        # Inspect every UTF-8 file; exclude runtime/git directories at traversal.
        if not path.is_file(): continue
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
    parser.add_argument('--write',action='store_true',help='Sanitize working research/data-dictionary sources only; archived copies require an audited rebuild or redaction.')
    parser.add_argument('--root',type=Path,default=ROOT.parent,help='Repository tree to scan; defaults to IKHIS, including the data dictionary.')
    args=parser.parse_args()
    args.root=args.root.resolve()
    paths=[p for p in args.root.rglob('*') if not any(x in p.parts for x in ('.git','.venv','__pycache__'))]
    found=[]
    for path,raw,clean in scan_files(paths):
        rel=path.relative_to(args.root)
        writable=path.is_relative_to(ROOT/'research') or path.is_relative_to(ROOT.parent/'data_dictionary/sources')
        if args.write and writable:path.write_bytes(clean)
        found.append({'path':str(rel),'original_sha256':sha(raw),'sanitized_sha256':sha(clean),'sanitized':args.write and writable})
    print(json.dumps({'files_with_credential_metadata':found},indent=2))
    return int(any(not row['sanitized'] for row in found))
if __name__=='__main__':raise SystemExit(main())
