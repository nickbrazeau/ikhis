# Proteomic lane pilot extraction

This package contains **8 primary sources, 11 cohort/context registry records, and 22 assertions**. It is a bounded pilot corpus, not an exhaustive systematic review. The retrieved publications span 2001–2025.

## What the records support

- **P_A01:** A narrowly described IL34 perturbation changed the total proteome profile of preactivated memory CD4 T cells. It is an aggregate observation; no individual protein edge is reconstructed from atlas coverage.
- **P_A02–P_A06:** Ex vivo cytokine and inhibitor effects are recorded as phosphorylation measurements. IL3RA abundance and an IL3 response are distinct observations; the absent B-cell STAT3 response is retained.
- **P_A07–P_A08:** CITE-seq supplementary captions provide an NK-subset protein distribution contrast and a low-signal control null. Both remain marked for full figure/data review.
- **P_A09–P_A13:** REAP-seq provides separate RNA and protein records. ICOS is discordant across layers; the IL7R measurements agree in direction. Neither result proves altered cytokine responsiveness.
- **P_A14–P_A17:** Plasma pQTLs and disease associations retain the platform and cohort context. IL6 replication failure and CXCL9 reagent disagreement are visible.
- **P_A18–P_A22:** Platelet protein synthesis, extracellular release, fraction-transfer effects, receptor blockade and a specificity-control null remain distinct assertions. The functional outcome is measured adhesion.

## Interpretation and QC

All confidence labels are qualitative. No biological probability was calibrated. No human adjudication has occurred.

The UKB portion of Eldjarn 2023 reuses UKB-PPP samples, and its Icelandic data reuse the deCODE study. The paired-platform Icelandic subset is nested within the larger Icelandic sample. The CKB comparison uses the same samples on two assays. These arrangements cannot be counted as independent replication. Cohort independence remains unresolved pending full donor-manifest reconciliation.

The REAP perturbation includes three donors and unequal recovered cell numbers. RNA and protein are measured in the same cells; donor-level replication must govern uncertainty. Marker changes are not measured memory formation, proliferation or receptor functionality.

Affinity-platform disagreement can reflect measurement precision, normalization, binding or proteoform differences. No plasma observation assigns a producing immune cell or demonstrates secretion. Exact reagent identifiers, epitope specificity and per-target detection limits remain gaps.

The platelet paper has an internal collection-time discrepancy: the relevant figure legend specifies 18 hours while the fractionation methods describe 8 hours. Its TNF antagonist control is partly described as unpublished data and is graded low. Fraction-transfer results retain the possibility of additional vesicle mediators.

## Response to independent review

The independent multi-omic critic review is preserved in `research/review_multiomic.json`. The extracting agent corrected its four proteomic findings and checked every remaining `mixed` direction. P_A07, P_A15 and P_A16 now use `association`: distribution differences, replication failure and reagent disagreement do not establish opposing signed effects. The same correction applies to P_A01 because its accessible caption establishes aggregate proteome differences without signed protein-level estimates. The experimental P2 grade for P_A01 remains unchanged; `association` here records an unsigned direction, not a downgrade of study design. The discordance predicates, context and qualitative uncertainties remain available.

P_A06 now cites the Figure 5C STAT5 main-text passage. Source inspection also identified a panel-label discrepancy: the saved Figure 5 legend labels the STAT5 result B while the main text cites C. Both locators are retained explicitly, with the qualitative null and absence of a formal equivalence test unchanged.

`review_response.json` records every old/new field value, supporting snapshot locator and file hash. These are extracting-agent repairs pending coordinator adjudication, not human adjudication. The authoritative evidence input is `pack.json`; no separate proteomic generator previously existed. `apply_review_corrections.py` provides an idempotent replay of these exact corrections and refuses unexpected field values. The run record retains the original extraction interval and adds this repair event.

## Snapshot access

Full article snapshots are saved for Bendall and Lindemann. REAP-seq is a complete publisher PDF hosted by UCSF. The Rieckmann and CITE-seq publisher snapshots contain abstracts and accessible supplementary captions; their main articles were not fully accessible. Web-tool responses preserve the reviewed sections of the three plasma studies. Snapshot filenames and source access levels distinguish these cases.

The requested Entrez helper failed because its Python requests dependency was unavailable. Web retrieval and public-page downloads supplied the evidence. A Europe PMC XML endpoint returned 404 for the screened HSV macrophage article; no assertions were extracted from it.

## Primary sources

1. [Rieckmann et al. 2017: human immune proteomic atlas](https://doi.org/10.1038/ni.3693)
2. [Bendall et al. 2011: marrow mass cytometry](https://doi.org/10.1126/science.1198704)
3. [Stoeckius et al. 2017: CITE-seq](https://doi.org/10.1038/nmeth.4380)
4. [Peterson et al. 2017: REAP-seq](https://doi.org/10.1038/nbt.3973)
5. [Sun et al. 2023: UKB-PPP](https://doi.org/10.1038/s41586-023-06592-6)
6. [Eldjarn et al. 2023: plasma platform comparison](https://doi.org/10.1038/s41586-023-06563-x)
7. [Wang et al. 2025: paired CKB platforms](https://doi.org/10.1038/s41467-025-56935-2)
8. [Lindemann et al. 2001: platelet IL1B synthesis and function](https://doi.org/10.1083/jcb.200105058)
