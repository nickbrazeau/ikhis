# Immune evidence review — Release 0.2.0

This continuation adds **68 evidence assertions**, recovers primary Methods and Results, and corrects eight inherited assertions. It expands the priority cytokine literature, records candidate screening decisions, and makes evidence/prior changes inspectable. The corpus remains bounded; human adjudication and probability calibration are outstanding.

## Compared with Release 0.1.0

| Measure | 0.1.0 | 0.2.0 |
|---|---:|---:|
| Evidence assertions | 72 | 140 |
| Reviewed assertions | 64 | 134 |
| Assertions awaiting full methods | 8 | 6 |
| Assertions awaiting independent review | 0 | 0 |
| Included source records | 27 | 51 |
| Priority labels with reviewed protein-involving evidence | 9 | 28 |
| Available heuristic existence summaries | 53 | 107 |
| Materialized mechanistic paths | 0 | 0 |

Source records are not independent studies; known publication and cohort reuse remain linked. Protein-involving evidence includes ligand interventions and does not certify a direct measurement of an assay analyte. The generic IL-12 and VEGF assay identities remain unresolved.

## Coverage gained

| Original assay label | Prior reviewed count | Current reviewed count |
|---|---:|---:|
| Eotaxin | 0 | 2 |
| Eotaxin-3 | 0 | 3 |
| GM-CSF | 0 | 2 |
| IFN-γ | 3 | 4 |
| IL-12p70 | 0 | 1 |
| IL-13 | 0 | 4 |
| IL-15 | 3 | 4 |
| IL-16 | 0 | 1 |
| IL-17A | 0 | 2 |
| IL-1α | 0 | 3 |
| IL-1β | 0 | 3 |
| IL-2 | 0 | 3 |
| IL-5 | 0 | 1 |
| IL-6 | 0 | 8 |
| IL-8 | 1 | 4 |
| IL-8 high range | 1 | 4 |
| IP-10 | 0 | 4 |
| MCP-4 | 0 | 2 |
| MDC | 0 | 5 |
| MIP-1α | 0 | 1 |
| MIP-1β | 0 | 1 |
| TARC | 0 | 2 |
| TNF-α | 1 | 2 |
| TNF-β | 0 | 2 |

Counts are assertions, not independent replicates. Related RNA, biochemical binding and cellular responses retain their own measurement classes and contexts.

The recovered Scalley-Kim study directly measures extracellular CCL3 and CCL4 in a stimulated human PBMC mixture; its recipient-cell assays are kept separate. Recovered Loetscher Methods add a CXCL10 migration contrast between cultured and freshly isolated primary lymphocytes. The six historical Taub migration assertions remain provisional, outside numerical updates, because their exact preparation methods have not been recovered. New protein measurements do not substitute for those migration experiments. [Chemokine extraction and locators](../research/chemokine_expansion/pack.json).

## Evidence corrections and eligibility

The full primary NK/DC article was inspected through Chrome and selected Methods, Results and figure passages were archived. C-A18 now records intracellular IFN-γ staining after six hours with monensin; C-A19 retains the separate six-day CFSE proliferation endpoint. These assays do not establish extracellular secretion, independent donor counts or a complete signaling path. [Ferlazzo et al., original article](https://pmc.ncbi.nlm.nih.gov/articles/PMC534504/).

New evidence enters estimates only when both the extraction file and its supporting source snapshots match the independently reviewed hashes. Open high-severity challenges quarantine dependent evidence. Ordinary nonsignificant results remain descriptive unless adequate absence evidence is available. Agent review and dispositions are recorded separately from human adjudication.

### Recovered inherited evidence

| Assertions | Source recovery and resulting correction |
|---|---|
| C-A12 | STAT3 paper: secreted TNF assay, timing, monocyte preparation and seven-donor basis recovered; ordinary null remains inconclusive. |
| C-A18–C-A20 | NK/DC paper: intracellular IFN-γ, six-day proliferation and surface IL15 nondetection are separate endpoints. |
| P_A01 | IL34 proteomic perturbation: doses, timing and two-donor/four-culture basis recovered. The source-described memory-cell preparation has an unresolved sorting-gate discrepancy; conventional-memory scoring is withheld. |
| P_A07–P_A08 | CITE-seq Methods and supplementary captions: CD56/CD8a antibody-tag distribution difference and CD4 control retained separately; cells are not counted as donors. |
| G-A020 | IL7R association: recruited and analyzed case/control totals remain distinct; the recessive-model odds ratio is separated from the combined family/case-control significance test. |

The [curation overlay](../data/curation_overrides_0.2.json) contains exact source locators, cohort details and limitations. These eight inherited assertions now have reviewed extractions. Recovering a method closes an access gap; it does not resolve unreported donor overlap, ambiguous cell identity or absent assay sensitivity.

The expansion stores 408 candidate appearances with screening decisions (including repeated hits across queries) and 15 source-reported quantitative observations. Observed numbers do not become calibrated magnitude or transportability distributions.

## Release lineage

| Record type | Change | Count |
|---|---|---:|
| edge_assertions | added | 68 |
| edge_assertions | modified | 8 |
| evidence_instances | added | 68 |
| evidence_instances | modified | 8 |
| prior_parameters | added | 680 |
| prior_parameters | modified | 80 |
| source_registry | added | 24 |
| source_registry | modified | 6 |

The CSV change records retain old and new values. Each frozen release carries a complete input snapshot and the verified predecessor dependency. Rebuilding or refreezing a frozen version is rejected. Release 0.1.0 retains its original manifest with one explicit security exception: an expired third-party signed-download credential was redacted from an archived search snapshot. Verification checks the documented replacement hash and reports that exception. [Alert investigation](SECURITY_ALERT_2026-09-13.md).

The gap register preserves original descriptions alongside current follow-up dispositions. A resolved access row does not close separate mechanistic, calibration or cohort-independence gaps.

## Remaining work

- Complete broader corpus screening, source retrieval and ontology mapping; ranked discovery results do not establish literature saturation.
- Resolve the original measurement platform, particularly IL-12 and VEGF identity.
- Extract further genomic, transcriptomic and proteomic parameter evidence and source-backed transition bridges.
- Perform human adjudication and empirical calibration before treating heuristic summaries as predictive probabilities.

## Inspect the release

- [Evidence atlas](../releases/0.2.0/EVIDENCE_ATLAS.md)
- [SQLite knowledge base](../releases/0.2.0/immune_prior.sqlite)
- [Evidence and prior changes](../releases/0.2.0/release_changes.csv)
- [Screened candidates](../releases/0.2.0/screening_candidates.csv)
- [Structural QC](../releases/0.2.0/qc.json)
- [Original checklist status](PROJECT_STATUS.md)
- [Reproduction instructions](../RUNNING.md)
