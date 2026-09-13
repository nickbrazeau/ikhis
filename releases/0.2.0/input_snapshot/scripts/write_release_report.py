#!/usr/bin/env python3
"""Write a source-linked, count-checked continuation report from compiled releases."""
import argparse
import json
from pathlib import Path
import sqlite3

ROOT=Path(__file__).resolve().parents[1]
def connect(version):
    db=sqlite3.connect('file:'+str(ROOT/'releases'/version/'immune_prior.sqlite')+'?mode=ro',uri=True)
    db.row_factory=sqlite3.Row
    return db

def count(db,query): return db.execute(query).fetchone()[0]
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--release',default='0.2.0');args=parser.parse_args()
    current=connect(args.release)
    previous_version=json.loads((ROOT/'data/release_config.json').read_text())[args.release]['previous_release']
    old=connect(previous_version)
    metrics=[('Evidence assertions','SELECT COUNT(*) FROM edge_assertions'),('Reviewed assertions',"SELECT COUNT(*) FROM edge_assertions WHERE status='reviewed'"),('Assertions awaiting full methods',"SELECT COUNT(*) FROM edge_assertions WHERE status='needs_full_text'"),('Assertions awaiting independent review',"SELECT COUNT(*) FROM edge_assertions WHERE status='needs_independent_review'"),('Included source records','SELECT COUNT(*) FROM screening_decisions'),('Priority labels with reviewed protein-involving evidence','SELECT COUNT(*) FROM assay_coverage WHERE reviewed_protein_assertion_count>0'),('Available heuristic existence summaries',"SELECT COUNT(*) FROM prior_parameters WHERE parameter_family='existence' AND availability='available'"),('Materialized mechanistic paths','SELECT COUNT(*) FROM materialized_paths')]
    added=count(current,"SELECT COUNT(*) FROM release_changes WHERE record_type='edge_assertions' AND change_type='added'")
    text=f'# Immune evidence review — Release {args.release}\n\nThis continuation adds **{added} evidence assertions**, recovers primary Methods and Results, and corrects eight inherited assertions. It expands the priority cytokine literature, records candidate screening decisions, and makes evidence/prior changes inspectable. The corpus remains bounded; human adjudication and probability calibration are outstanding.\n\n'
    text+=f'## Compared with Release {previous_version}\n\n| Measure | {previous_version} | {args.release} |\n|---|---:|---:|\n'
    for label,query in metrics: text+=f'| {label} | {count(old,query)} | {count(current,query)} |\n'
    text+='\nSource records are not independent studies; known publication and cohort reuse remain linked. Protein-involving evidence includes ligand interventions and does not certify a direct measurement of an assay analyte. The generic IL-12 and VEGF assay identities remain unresolved.\n\n'
    text+='## Coverage gained\n\n| Original assay label | Prior reviewed count | Current reviewed count |\n|---|---:|---:|\n'
    before={r['original_label']:r['reviewed_protein_assertion_count'] for r in old.execute('SELECT * FROM assay_coverage')}
    for r in current.execute('SELECT * FROM assay_coverage ORDER BY original_label'):
        n=r['reviewed_protein_assertion_count'];prior=before.get(r['original_label'],0)
        if n>prior: text+=f"| {r['original_label']} | {prior} | {n} |\n"
    text+='\nCounts are assertions, not independent replicates. Related RNA, biochemical binding and cellular responses retain their own measurement classes and contexts.\n\n'
    text+='The recovered Scalley-Kim study directly measures extracellular CCL3 and CCL4 in a stimulated human PBMC mixture; its recipient-cell assays are kept separate. Recovered Loetscher Methods add a CXCL10 migration contrast between cultured and freshly isolated primary lymphocytes. The six historical Taub migration assertions remain provisional, outside numerical updates, because their exact preparation methods have not been recovered. New protein measurements do not substitute for those migration experiments. [Chemokine extraction and locators](../research/chemokine_expansion/pack.json).\n\n'
    text+='## Evidence corrections and eligibility\n\n'
    corrected=current.execute("SELECT a.*,e.source_locator,e.evidence_summary,src.url FROM edge_assertions a JOIN evidence_instances e USING(assertion_id) JOIN source_registry src USING(source_id) WHERE a.assertion_id='C-A18'").fetchone()
    if corrected['predicate']=='decreases_intracellular_protein':
        text+='The full primary NK/DC article was inspected through Chrome and selected Methods, Results and figure passages were archived. C-A18 now records intracellular IFN-γ staining after six hours with monensin; C-A19 retains the separate six-day CFSE proliferation endpoint. These assays do not establish extracellular secretion, independent donor counts or a complete signaling path. [Ferlazzo et al., original article]('+corrected['url']+').\n\n'
    else:
        text+='A proposed correction to the older NK/DC extraction remains outside eligible estimates until the exact correction and source snapshot pass independent review.\n\n'
    text+='New evidence enters estimates only when both the extraction file and its supporting source snapshots match the independently reviewed hashes. Open high-severity challenges quarantine dependent evidence. Ordinary nonsignificant results remain descriptive unless adequate absence evidence is available. Agent review and dispositions are recorded separately from human adjudication.\n\n'
    text+='### Recovered inherited evidence\n\n| Assertions | Source recovery and resulting correction |\n|---|---|\n| C-A12 | STAT3 paper: secreted TNF assay, timing, monocyte preparation and seven-donor basis recovered; ordinary null remains inconclusive. |\n| C-A18–C-A20 | NK/DC paper: intracellular IFN-γ, six-day proliferation and surface IL15 nondetection are separate endpoints. |\n| P_A01 | IL34 proteomic perturbation: doses, timing and two-donor/four-culture basis recovered. The source-described memory-cell preparation has an unresolved sorting-gate discrepancy; conventional-memory scoring is withheld. |\n| P_A07–P_A08 | CITE-seq Methods and supplementary captions: CD56/CD8a antibody-tag distribution difference and CD4 control retained separately; cells are not counted as donors. |\n| G-A020 | IL7R association: recruited and analyzed case/control totals remain distinct; the recessive-model odds ratio is separated from the combined family/case-control significance test. |\n\nThe [curation overlay](../data/curation_overrides_0.2.json) contains exact source locators, cohort details and limitations. These eight inherited assertions now have reviewed extractions. Recovering a method closes an access gap; it does not resolve unreported donor overlap, ambiguous cell identity or absent assay sensitivity.\n\n'
    text+=f"The expansion stores {count(current,'SELECT COUNT(*) FROM screening_candidates')} candidate appearances with screening decisions (including repeated hits across queries) and {count(current,'SELECT COUNT(*) FROM quantitative_results')} source-reported quantitative observations. Observed numbers do not become calibrated magnitude or transportability distributions.\n\n"
    text+='## Release lineage\n\n| Record type | Change | Count |\n|---|---|---:|\n'
    for r in current.execute('SELECT record_type,change_type,COUNT(*) n FROM release_changes GROUP BY record_type,change_type ORDER BY record_type,change_type'):
        text+=f"| {r['record_type']} | {r['change_type']} | {r['n']} |\n"
    text+='\nThe CSV change records retain old and new values. Each frozen release carries a complete input snapshot and the verified predecessor dependency. Rebuilding or refreezing a frozen version is rejected. Release 0.1.0 retains its original manifest with one explicit security exception: an expired third-party signed-download credential was redacted from an archived search snapshot. Verification checks the documented replacement hash and reports that exception. [Alert investigation](SECURITY_ALERT_2026-09-13.md).\n\n'
    text+='The gap register preserves original descriptions alongside current follow-up dispositions. A resolved access row does not close separate mechanistic, calibration or cohort-independence gaps.\n\n'
    text+='## Remaining work\n\n- Complete broader corpus screening, source retrieval and ontology mapping; ranked discovery results do not establish literature saturation.\n- Resolve the original measurement platform, particularly IL-12 and VEGF identity.\n- Extract further genomic, transcriptomic and proteomic parameter evidence and source-backed transition bridges.\n- Perform human adjudication and empirical calibration before treating heuristic summaries as predictive probabilities.\n\n'
    text+=f'## Inspect the release\n\n- [Evidence atlas](../releases/{args.release}/EVIDENCE_ATLAS.md)\n- [SQLite knowledge base](../releases/{args.release}/immune_prior.sqlite)\n- [Evidence and prior changes](../releases/{args.release}/release_changes.csv)\n- [Screened candidates](../releases/{args.release}/screening_candidates.csv)\n- [Structural QC](../releases/{args.release}/qc.json)\n- [Original checklist status](PROJECT_STATUS.md)\n- [Reproduction instructions](../RUNNING.md)\n'
    (ROOT/'reports'/f'RELEASE_{args.release}.md').write_text(text)
    old.close();current.close()
if __name__=='__main__': main()
