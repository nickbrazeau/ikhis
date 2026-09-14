# Cytokine/signaling and perturbation-transcriptomic evidence pilot

This is a bounded, source-backed pilot corpus for protocol 0.1.0, not an exhaustive systematic review. It contains 9 source records for 8 publication families, 10 cohort/context records, 25 narrow assertions, and 26 real search/retrieval entries. Six assertions retain null findings; four remain flagged `needs_full_text`.

## Anchor resources and duplicate detection

- [Immune Dictionary](https://doi.org/10.1038/s41586-023-06816-9) is a **mouse** lymph-node in-vivo cytokine atlas, published online in December 2023 and in the 2024 Nature issue. The primary screen used 86 cytokines, three mice per cytokine, and a 4-hour readout. Its RNA responses must remain distinct from human evidence.
- [Human Cytokine Dictionary, bioRxiv](https://doi.org/10.64898/2025.12.12.693897) is represented by v1 dated 15 December 2025. The actual bioRxiv API response has `published: NA`; an exact-title publication search found preprints and repository records. This is evidence of current repository linkage status, not a guarantee that no journal article exists anywhere.
- [Research Square v1](https://doi.org/10.21203/rs.3.rs-8337240/v1), indexed as [PMID 41510257](https://pubmed.ncbi.nlm.nih.gov/41510257/), is a second preprint record for the **same** Human Cytokine Dictionary experiment. Matching authors, 12 donors, 9,697,974 cells, 90 cytokines, and methods resolve this duplicate. It receives no second biological evidence weight.
- [CytoSig](https://doi.org/10.1038/s41592-021-01274-5) combines reused transcriptomic studies with a predictive model. Its original A549 cotreatment experiments support separate measured secreted-protein assertions. Predicted cytokine activity is not a direct receptor-activation assay.

## Findings retained

Human IL4 exposure increases B-cell IGHE, IL4R, and IL4I1 RNA in mixed PBMC culture; these records do not assert antibody secretion, receptor surface availability, or direct promoter regulation. Mouse transcriptional observations are separately labeled and are not treated as human replication.

In human monocytes, the IL10 study provides measured secretion and RNA readouts. Added IL10 suppresses TNF release; IL4 suppresses IL10 release. Added IL10 strongly reduces its own RNA at **24 hours** (Fig7); the separate **seven-hour** result has no or only minimal inhibition (Fig6). That early qualitative finding does not establish equivalence or exact absence. The STAT3 paper contributes a provisional functional null: increasing activated STAT3 alone did not suppress LPS-induced TNF production. Its assay compartment remains unavailable until full-text verification.

The engineered DC study distinguishes soluble IL15, DC surface IL15, intracellular NK-cell IFNG, and actual target-cell killing. IL15 mRNA alone produces secretion without a significant surface increase. Co-expression with IL15RA increases surface IL15. Source engineering, transwell separation, and IL15 neutralization support an IL15-dependent DC-to-NK cytotoxicity effect. The paper's IFNG method is intracellular staining; its abstract's secretion wording is not propagated into that assertion.

IL12RB1-deficient expanded T-cell clones show context-specific residual responses and clone-specific nulls. Acute IL12-induced STAT4 DNA-binding activity is absent in deficient PHA blasts and present in controls. These are different preparations and times, so they do not establish one continuously measured pathway.

The older IL12-neutralization/NK IFNG result remains provisional. Its authors describe secretion, but accessible methods do not verify an extracellular assay for the extracted blood-NK result. The record therefore describes protein production with compartment unavailable and remains excluded from mechanistic paths pending full-text verification.

## Source access and extraction quality

`snapshots/` preserves actual web-tool responses, bioRxiv API JSON, and NCBI XML. `pmc_fulltext.xml` is the original mixed NCBI response. Per-article XML files are derived by lossless XML parsing; human-readable text extracts are conveniences. C-S05 and C-S07 XML contain only front matter and abstracts, despite their PMC identifiers. The detailed Ferlazzo excerpts remain search excerpts. C-S04 contains OCR text with errors, so its numerical table effects have not been used. C-S01, C-S08, and C-S09 have full article bodies.

Several PMC browser requests returned CAPTCHA, the publisher preview restricted CytoSig, bioRxiv HTML returned 403, and a large Harvard PDF exceeded the browsing fetch limit. These failures are retained in tool snapshots. Public API retrieval required a small isolated dependency installation and authorized network access; no account was accessed and no external messages were sent. The ignored `.venv/` is a local tool dependency, not review evidence or a release artifact.

## Limits for integration and review

Independent donor counts are unavailable for several older studies. Expanded T-cell clones do not count as independent people. P1/P3 clone donors in C-CO08 are a verified participant subset of the expanded C-CO09 participant set, now recorded using `parent_cohort`. That link records shared people, not derivation of clones from assayed blasts; assay contexts remain separate and sample-level/historical reuse remains unresolved. P1/P3/P4 also overlap earlier publications cited by the article. CytoSig's underlying datasets must be accession-deduplicated before further extraction. HCD's donor-level pseudobulk analysis is distinct from cell-level replication; the mouse atlas's three biological replicates must be retained.

No numerical existence probability, journal impact factor, human adjudication, or complete multi-omic path has been invented. The only candidate path is a limited same-study engineered DC-to-NK functional relationship, with proximal signaling explicitly unmeasured. Dose/time, ancestry, statistical uncertainty, and full priority-set coverage remain important gaps. Inclusion of a cytokine in an atlas does not imply that a narrow human assertion for it has been extracted.

The independent review in [review_cytokine.json](../review_cytokine.json) identified the timing error, excessive compartment specificity, a missing structured overlap link and a protocol-level null-scoring ambiguity. The three extraction findings were repaired as documented in [review_response.json](review_response.json), including original/revised hashes and exact source locators; the original critic findings are preserved. The coordinating agent owns protocol-level null scoring and final dispositions. The natural IL12RB1-deficiency context and distinct clone/blast readouts were reviewed without an additional tier finding. The four provisional assertions still require fuller source access before scientific prior calibration.

The regenerated pack was checked for required assertion fields, identifier uniqueness, source/cohort references, nonempty unknown markers, snapshot existence, cohort-link acyclicity and faithful regeneration from its builder.
