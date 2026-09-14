#!/usr/bin/env python3
"""Record every original README checklist item without marking coverage complete."""
from pathlib import Path
import json
import re
ROOT=Path(__file__).resolve().parents[1]
IMPLEMENTED={'Greenfield review','Multi-layer mechanistic framework','Adversarial reviewer','Prior-only versioning','LLM/instruction provenance','Expand scope to genomics','Expand scope to transcriptomics','Expand scope to proteomics','Final protocol','Hash/register protocol','Final adjudication rules','Release policy','frozen initial corpus','genomic critique','causal-gene critique','transcriptomic critique','proteomic critique','cytokine critique','cross-omic compatibility critique','duplicate-cohort critique','network topology critique','entity tables','genomic evidence tables','transcriptomic evidence tables','proteomic evidence tables','cytokine interaction tables','critic findings','source manifest','provenance manifest','protocol/instruction manifest','QC report','freeze/hash Release 0.1'}
PENDING={'human adjudication','magnitude priors','temporal priors','genetic-modifier priors','expression priors','protein-availability priors','human-transportability priors','integrated multi-omic paths'}
EXPLANATIONS={
'Final protocol':'Operational v0.1.0 written; no claim of external preregistration or human approval.',
'Hash/register protocol':'SHA-256 registered locally in instruction and release manifests; no external registry.',
'Final adjudication rules':'Agent correction, contested evidence, propagation and human-pending states explicit.',
'Journal modifier':'Bounded proposal implemented and tested; authoritative JCR data unavailable; neutral multiplier.',
'versions/retrieval dates/hashes':'Actual snapshots hashed and dates retained; unspecified external resource versions remain unavailable.',
'Cytokine search':'Actual discovery queries saved; bounded retrieval and pilot extraction only.',
'genomic search':'Actual discovery queries saved; bounded retrieval and pilot extraction only.',
'transcriptomic search':'Actual discovery queries saved; bounded retrieval and pilot extraction only.',
'proteomic search':'Actual discovery queries saved; bounded retrieval and pilot extraction only.',
'family/entity-specific searches':'29 protein-symbol PubMed queries plus four lanes; ten relevance-ranked IDs each; original aliases retained in mapping.',
'citation chaining':'Anchor-driven follow-up sources collected; no exhaustive backward/forward citation graph.',
'deduplication':'Known publication-family and duplicate-preprint relations retained; full search corpus unscreened.',
'cohort deduplication':'Known parent/subset relations and conservative unresolved grouping implemented; sample-level overlap incomplete.',
'frozen initial corpus':'27 included source records / 26 publication families; 72 assertions; explicitly bounded.',
'human adjudication':'Pending. No agent action has been labeled human review.',
'integrated multi-omic paths':'Empty by design: eight candidate joins fail context/bridge checks; complete source-backed path extraction remains.',
'existence priors':'Explicit-hypothesis Beta summaries available for eligible records; heuristic and uncalibrated.',
'direction priors':'Separate Dirichlet summaries; null adequacy and individual eligibility enforced; uncalibrated.',
'effect-class priors':'Observed categorical directions exported; no magnitude inference.',
'context-specific priors':'Context annotations retained; quantitative transport calibration unavailable.',
'journal-modifier sensitivity analysis':'No-journal results exported; equal to default because authoritative metrics unavailable and weighting disabled.',
'prior tables':'All ten parameter families exported; unsupported numeric families explicitly unavailable.',
'freeze/hash Release 0.1':'Local initial release hash manifest; verify after rebuilding. Whole-review completion not claimed.'}

def main():
    readme=(ROOT/'README.md').read_text()
    block=readme.split('# 20. Revised project checklist',1)[1].split('# Instructions to a new Agentic Session',1)[0]
    category='';rows=[]
    for line in block.splitlines():
        if line.startswith('## '): category=line[3:]
        elif line.startswith('-  '):
            task=line[3:].strip()
            status='implemented for initial release' if task in IMPLEMENTED else 'pending scientific completion' if task in PENDING else 'partial coverage / implementation'
            detail=EXPLANATIONS.get(task,'Schema/interface present; required quantitative evidence or calibration is unavailable.' if task in PENDING else 'Implemented and represented in the frozen initial artifacts; does not imply exhaustive biological coverage.' if task in IMPLEMENTED else 'Represented in the schema, registry or bounded evidence corpus; broader extraction/verification remains.')
            rows.append({'category':category,'task':task,'status':status,'detail':detail})
    (ROOT/'data/project_checklist.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False)+'\n')
    doc='# Project implementation and scientific completion status\n\n'
    doc+='Release 0.1.0 is a completed **bounded initial evidence release**, not completion of the entire README research program. It contains 72 assertions, 27 included publication/resource records, 38 cohort/subset/context registry entries and all 30 original assay labels. All scientific gaps below remain open; presence of a table is not evidence coverage.\n\n'
    doc+='The initial operational protocol, local knowledge base, independent critic cycle, corrections, heuristic prior interface, exports and hash verification are implemented. Exhaustive corpus construction, broad cytokine extraction, full ontology mapping, human adjudication, calibrated quantitative priors and complete multi-omic paths remain unfinished. Assay-platform documentation and authoritative journal metrics are unavailable.\n\n'
    doc+='## Original checklist\n\n| Section | Requirement | Status | Evidence or remaining work |\n|---|---|---|---|\n'
    for r in rows: doc+='| '+' | '.join(r.values())+' |\n'
    doc+='\n## Release entry points\n\n- Research narrative: `reports/RESEARCH_SYNTHESIS.md`\n- Evidence atlas: `releases/0.1.0/EVIDENCE_ATLAS.md`\n- Structural and scientific QC: `releases/0.1.0/qc.json`\n- Table dictionary: `data/DATA_DICTIONARY.md`\n- Reproduction and interpretation: `RUNNING.md`\n- Detailed evidence gaps: `releases/0.1.0/coverage_gaps.csv`\n\nNo unscreened search result, local registry entry, empty table or inferred complete path is counted as a reviewed biological assertion.\n'
    (ROOT/'reports/PROJECT_STATUS.md').write_text(doc)
    print('Tracked',len(rows),'original requirements')
if __name__=='__main__':main()
