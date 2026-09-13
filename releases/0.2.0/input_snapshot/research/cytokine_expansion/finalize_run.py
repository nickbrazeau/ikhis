"""Finalize only this lane's evidence artifacts after source sanitization."""
import collections
import datetime
import hashlib
import json
import runpy
from pathlib import Path

B = Path('research/cytokine_expansion')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
sanitizer = runpy.run_path('scripts/sanitize_snapshots.py')
changes = list(sanitizer['findings'](B.rglob('*')))
for path, raw, clean in changes:
    path.write_bytes(clean)
assert not list(sanitizer['findings'](B.rglob('*')))

pack = json.loads((B/'pack.json').read_text())
screen = json.loads((B/'screening.json').read_text())
run = json.loads((B/'run.json').read_text())
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
old_hash = run['output_hash']
new_hash = sha(B/'pack.json')
if old_hash != new_hash:
    run.setdefault('output_history', []).append({
        'output_hash': old_hash,
        'timestamp_end': run['timestamp_end'],
        'status': 'Superseded initial excerpt-based pack; full-method continuation follows',
    })
run.update(
    timestamp_end=now,
    output_hash=new_hash,
    builder_hash=sha(B/'build_pack.py'),
    finalizer_hash=sha(B/'finalize_run.py'),
    continuation_status='Full-method continuation complete; independent review pending',
    retrieval_queries=pack['searches'],
    source_versions=[{k: s[k] for k in ['source_id','version','snapshot_path']} for s in pack['sources']],
    source_hashes={str(p):sha(p) for p in sorted((B/'snapshots').glob('*')) if p.is_file()},
    validation={
        'required_fields':'pass', 'foreign_keys':'pass', 'snapshot_exists':'pass',
        'null_scoring_annotation':'pass', 'sanitizer':'pass',
        'assertions':len(pack['assertions']),
        'needs_full_text':sum(a['qc_status']=='needs_full_text' for a in pack['assertions']),
        'null_observations':sum(a['direction']=='null' for a in pack['assertions']),
        'screened_candidates':len(screen['candidates']),
        'sources_with_inspected_primary_methods':8,
    },
    access_limits=[
        'NCBI sandbox DNS failure; elevated retry aborted after approval wait; no source XML downloaded.',
        'Initial web openings returned CAPTCHA for six sources; four EuropePMC web requests returned non-retryable safety-tool failures.',
        'Chrome then displayed all eight primary articles without CAPTCHA. Selected relevant passages were archived; no full-article file export claimed.',
        'Supplementary methods/raw data were not independently inspected; unique donor identities and some exact dose-axis values remain unavailable.',
    ],
    sanitization={
        'script':'scripts/sanitize_snapshots.py',
        'scope':'research/cytokine_expansion only',
        'script_changes_in_final_pass':len(changes),
        'remaining_detected_signed_credential_metadata':0,
        'additional_preventive_redaction':'An irrelevant search03 publisher token parameter was redacted; screening URLs omit query metadata. Selected Chrome snapshots exclude navigation/account data and external link metadata.',
    },
    review_required='Independent biological review of exact output_hash; no numerical prior or human adjudication claimed',
)
(B/'run.json').write_text(json.dumps(run,indent=2,ensure_ascii=False)+'\n')
(B/'sanitize_audit.json').write_text(json.dumps({
    'timestamp':now,'scope':str(B),'script':'scripts/sanitize_snapshots.py',
    'remaining_findings':0,'changes_in_final_pass':len(changes),
    'notes':'Selected Chrome snapshots exclude account and external URL metadata. Irrelevant publisher token redacted from search03. No raw snapshot was duplicated.'
},indent=2)+'\n')

notes = '''# Primary human cytokine evidence expansion

The completed expansion contains **22 narrow assertions, eight primary publications and eight cohort/context records**, with 48 ranked candidate records from three actual search batches. It covers CSF2 (GM-CSF), IL2, IL5, IL16, IL17A and IL1A. This is targeted coverage, not an exhaustive systematic review. Earlier corpus files were preserved.

All eight primary articles now have relevant Methods, Results and figure captions inspected through Chrome. The 13 initial access-only `needs_full_text` flags are closed. Selected verbatim source passages are saved with article/section locators; these are not complete downloaded articles. `reviewed_extraction` describes the extractor's source check, not independent adjudication. Default prior eligibility still requires independent review of the exact pack hash.

| Cytokine | Retained observations | Important limit |
|---|---|---|
| CSF2 | Total eosinophil ICAM1 increase; total CSF2RA decrease; ICAM1 antisense reduces CSF2-supported survival | Total lysate receptor protein is not surface availability; antisense does not establish direct CSF2 binding to ICAM1 |
| IL5 | Wild-type and E12K survival support; anti-IL5 inhibition; E12K adhesion nondetection | E12K is a distinct reagent; primary eosinophil responses are separate from transfected COS or TF1 binding experiments |
| IL2 | CD4 pSTAT5 response and CD25 strata; low quiescent-cell proliferation versus PHA-competent response | Figure1 uses CD4 gates within PBMCs; the separate cell-cycle paper has inconsistent numerical/dose labels |
| IL16 | Anti-IL16 reduces amniotic-fluid-induced adult CD4 migration; gestational mixture-response and protein-abundance contrasts | Fluid mixtures do not identify secreting cells, establish CD4 receptor dependence or prove fetal in vivo trafficking |
| IL17A | Extracellular IL6 increase; TAK1-inhibitor reduction; IRAK-inhibitor and low-dose nulls | Pharmacological inhibition is not unique target or receptor proof; technical experiments are not extra patients |
| IL1A | Imiquimod-associated extracellular IL1A; neutralization context; keratinocyte and fibroblast CXCL8 responses | Early release precedes reported LDH increase but export mechanism remains unknown; mouse knockouts are excluded |

The five ordinary null/context observations remain **inconclusive for relationship absence**. IL5 E12K supports survival despite an adhesion null; low-dose IL17A is nonsignificant despite a higher-dose response. These contrasts show why dose, time, cell state and readout must stay attached to each record. No complete path or numerical prior was created.

Two IL2 records, XCI-A09 and XCI-A22, are deliberately low confidence. Table1 and Results disagree on IL2-only cycling (2.3% versus 4.3%) and table dose/timing labels conflict. The pack retains a qualitative failure to elicit a full mitogenic response, not zero cycling, and separately retains the PHA-preconditioned context. A harmonized quantitative estimate is withheld. In the IL1A skin-cell paper, Figure3 explicitly gives a 24-hour response while generic Methods give 48 hours; the figure-specific duration is retained and the discrepancy is recorded.

Human-system distinctions are explicit. Healthy-donor eosinophils, PBMC-gated CD4 cells, mixed lymphocyte cultures, cultured TMD fibroblasts, commercial pooled primary keratinocytes, other primary skin cultures and adult target T cells exposed to amniotic fluid are separate contexts. Ancestry, unique donors, donor overlap, exact untranscribed concentration ranges and supplementary details remain unavailable when not recoverable from inspected passages. Fluid-donor counts are not target-cell-donor counts. Same-study arms do not count as independent replication.

The Entrez skill helper failed at sandbox DNS resolution and its elevated retry was interrupted while awaiting approval. Six web PMC requests returned CAPTCHA; four EuropePMC web requests returned non-retryable tool failures. Chrome subsequently opened the known primary PMC pages without a challenge and supplied the methods/results used here. There was no CAPTCHA bypass and no full-file export. The real outcomes are preserved in the retrieval log.

All saved text was checked using the project's snapshot sanitizer, restricted to this lane. Selected Chrome passages omit navigation/account details and external link metadata. An irrelevant publisher access-token parameter in a ranked search result was redacted; screening URLs omit query metadata. Final source and output hashes are recorded in run.json. No potential credential values are reproduced in notes or audit records.

The builder checks required fields, unique identifiers, reference integrity, snapshot existence and null-scoring annotations. The finalizer records artifact hashes and sanitization results. Independent biological review, empirical probability calibration and human adjudication remain distinct activities and are not claimed by this extraction.
'''
(B/'notes.md').write_text(notes)
print(json.dumps({'assertions':len(pack['assertions']),'sources':len(pack['sources']),
                  'candidates':len(screen['candidates']),'output_hash':new_hash,
                  'remaining_sanitizer_findings':0,'timestamp_end':now}))
