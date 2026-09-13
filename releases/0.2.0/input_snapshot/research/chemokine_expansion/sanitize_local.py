#!/usr/bin/env python3
"""Apply the shared sanitizer plus removal of publisher signed-delivery tokens."""
import importlib.util,json,re
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[1]
spec=importlib.util.spec_from_file_location('shared_sanitizer',ROOT/'scripts/sanitize_snapshots.py')
shared=importlib.util.module_from_spec(spec);spec.loader.exec_module(shared)
SIGNED_TOKEN=re.compile(r'(?i)((?:[?&]|%26)(?:amp;)?(?:token|access_token|auth_token|authorization)(?:=|%3D))((?:(?!%26)[^&\s"<>\\)])+)')
changed=[]
for p in OUT.rglob('*'):
    if not p.is_file() or p.suffix not in ('.json','.md','.txt','.xml','.html','.csv'):continue
    raw=p.read_bytes()
    try:text=raw.decode('utf-8')
    except UnicodeError:continue
    clean=SIGNED_TOKEN.sub(lambda m:m[1]+'REDACTED_SIGNED_DELIVERY_TOKEN',shared.sanitize(text)).encode('utf-8')
    if clean!=raw:
        p.write_bytes(clean)
        changed.append({'path':str(p.relative_to(ROOT)),'original_sha256':shared.sha(raw),'sanitized_sha256':shared.sha(clean)})
if changed:
    prior=OUT/'sanitation_audit.json'
    audit=json.loads(prior.read_text()) if prior.exists() else {}
    audit.setdefault('additional_signed_delivery_sanitation',[]).extend(changed)
    prior.write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps({'files_changed':len(changed),'scope':'research/chemokine_expansion','matched_values_printed':False}))
