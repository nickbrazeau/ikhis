# Immune evidence candidate 0.3.0

Steps 1–3 are prepared for a review the user will trigger separately. No independent review has been started for this candidate.

All cytokines and broader immune genetic, transcriptional, proteomic, signaling and cellular mechanisms are in scope. Historical assay labels are provenance only.

The candidate contains 76 new pending-review assertions, 19 source records, 83 screened candidate appearances and 24 mechanism dossiers. Publication counts are not independent replication counts. New extracts from inherited papers remain linked to their original records.

3 source records reuse a DOI already present in the baseline. 74 assertions have inspected primary Methods and Results; 2 still need complete primary details. All await review.

The connection proposals comprise 8 mechanisms ready for scientific scrutiny, 14 shared-intervention response profiles, 14 context contrasts and 11 blocked connections. These are extractor proposals, not validated pathways.

The baseline database records, including its uncalibrated priors and review history, are unchanged. New evidence is stored only in candidate tables. No new numerical prior or approved production pathway is created.

## All-cytokine discovery inventory

The complete human UniProt keyword KW-0202 / GO:0005125 queries return 243 reviewed resource entries and 383 unreviewed discovery entries. These are resource records; the total is not a count of distinct active cytokines or evidence-reviewed entities. The inventory does not limit eligibility; literature-supported cytokines, isoforms and complexes outside these annotations remain eligible.

Queries, source snapshots, counts and limits are preserved in `input_snapshot/research/cytokine_inventory/`. No resource membership becomes a biological edge.

## Evidence dossiers

### Genetic

Human immune regulatory mechanisms are represented as context-specific perturbational links and branches. DDX39B depletion/rescue supports a narrow HeLa splicing mechanism. Activated primary CD4 cells provide shared-intervention RNA/supernatant evidence with discordant shRNAs and non-isoform-specific ELISA. Primary-cell CD81 promoter repression supplies RNA and measured surface-protein branches. Enhancer-to-TRAF1 and KCNN4 results broaden regulatory scope without inferring protein or disease causality. No review, priors, or release changes performed. ETS2 source access was subsequently resolved: four bounded primary-macrophage assertions provide enhancer→RNA/function and ETS2 disruption→IL6 protein/function branches, with no forced native-protein mediation.

[Extraction notes](input_snapshot/research/mechanisms_genetic/notes.md) · [Screening](input_snapshot/research/mechanisms_genetic/screening.json)

**MG-B001 · MG-M01 · Intermediate perturbation/rescue · Pending mechanism review**

DDX39B depletion plus complementation identifies a DDX39B-dependent endogenous IL7R splicing phenotype in HeLa.

Endpoints: MG-A001 (DDX39B-targeting siRNA DDX_4 → DDX39B); MG-A002 (siRNA-resistant wild-type DDX39B complementation → IL7R exon6 inclusion).

**Scope and limits:** Supports narrow intermediate dependence. Does not prove direct RNA binding, physiological allele effects, primary-cell transport, or downstream secretion.

**Structural checks:** Extractor attestations and source dependencies are present; scientific review has not begun.

Sources: [MG01](https://pmc.ncbi.nlm.nih.gov/articles/PMC5456452/). Locators: Fig1A,E,F; Methods DDX39B RNAi-mediated knockdown and rescue; Fig1E,F; Results first subsection; Methods DDX39B RNAi-mediated knockdown and rescue

**MG-B002 · MG-M02 · Shared intervention · Response profile**

Activated primary CD4 cells show exon6 skipping and altered extracellular IL7R under DDX39B shRNAs.

Endpoints: MG-A003 (DDX39B sh3/sh5 depletion → IL7R exon6); MG-A004 (DDX39B sh3/sh5 depletion → extracellular IL7R immunoreactivity).

**Scope and limits:** Branched response only; sh3 all six and sh5 only two protein increases; cannot equate all extracellular IL7R with splice-derived soluble isoform.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MG01](https://pmc.ncbi.nlm.nih.gov/articles/PMC5456452/). Locators: Fig6; Methods primary human CD4 culture and transduction; Results accompanying Fig6; FigS10 caption; Methods transduction and ELISA

**MG-B003 · MG-M02 · Serial transition · Blocked connection**

Proposed exon6-skipped RNA→soluble IL7R transition cannot be assigned to the measured extracellular protein in this experiment.

Endpoints: MG-A003 (DDX39B sh3/sh5 depletion → IL7R exon6); MG-A004 (DDX39B sh3/sh5 depletion → extracellular IL7R immunoreactivity).

**Scope and limits:** Need selective splice manipulation and isoform-specific protein or equivalent direct translation evidence.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. entity_continuity: not_demonstrated. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. Exact molecular entity/state continuity is absent; an explicit intermediate assertion is required.

Sources: [MG01](https://pmc.ncbi.nlm.nih.gov/articles/PMC5456452/). Locators: Fig6; Methods primary human CD4 culture and transduction; Results accompanying Fig6; FigS10 caption; Methods transduction and ELISA

**MG-B004 · MG-M03 · Context contrast · Context contrast**

Primary CD4 depletion/protein response and monocyte DDX39B RNA/protein null are contextual contrasts.

Endpoints: MG-A004 (DDX39B sh3/sh5 depletion → extracellular IL7R immunoreactivity); MG-A009 (DDX39B RNA at2 h or24 h LPS → 24-h supernatant IL7R).

**Scope and limits:** Cannot treat monocyte transcript null as refutation of DDX39B protein-dependent splicing in CD4 cells.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MG01](https://pmc.ncbi.nlm.nih.gov/articles/PMC5456452/); [MG03](https://pmc.ncbi.nlm.nih.gov/articles/PMC6783569/). Locators: Results accompanying Fig6; FigS10 caption; Methods transduction and ELISA; Results sIL7R regulated by rs6897932 and associated with DDX39A; Fig3 and Supplementary Fig7

**MG-B005 · MG-M04 · Serial transition · Blocked connection**

UTR luciferase reporter effect is directionally compatible with native LCL protein association but not an explicit same-system native translation transition.

Endpoints: MG-A005 (rs2523506 A versus C in DDX39B 5-prime UTR → Renilla luciferase reporter); MG-A016 (rs2523506 A carriage → DDX39B).

**Scope and limits:** Native primary-cell allele→DDX39B translation requires further evidence; linked-locus alternatives remain for LCL genotype association.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. entity_continuity: not_demonstrated. context_compatibility: not_demonstrated. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. experimental_linkage: not_demonstrated. Exact molecular entity/state continuity is absent; an explicit intermediate assertion is required.

Sources: [MG01](https://pmc.ncbi.nlm.nih.gov/articles/PMC5456452/). Locators: Fig4; Methods Luciferase translation efficiency assays; Fig3C; Results allele-specific DDX39B protein; Methods DDX39B western blot analyses in LCLs

**MG-B006 · MG-M05 · Shared intervention · Response profile**

CD81 TSS repression lowers target RNA and measured cell-surface CD81 in activated primary CD4 cells.

Endpoints: MG-A012 (CD81 TSS-directed ZIM3-dCas9 CRISPRi → CD81 transcript); MG-A013 (CD81 TSS-directed ZIM3-dCas9 CRISPRi → surface CD81).

**Scope and limits:** RNA/flow correlation and shared guide treatment do not independently test translation, protein turnover or trafficking mediation.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MG04](https://link.springer.com/article/10.1186/s13059-024-03176-z). Locators: Fig1D; Results implementation; Methods gRNA transduction; Fig1B,C; Methods gRNA transduction and flow

**MG-B007 · MG-M05 · Serial transition · Blocked connection**

Direct CD81 transcript reduction→surface protein reduction is plausible but not established as a serial intervention-tested transition.

Endpoints: MG-A012 (CD81 TSS-directed ZIM3-dCas9 CRISPRi → CD81 transcript); MG-A013 (CD81 TSS-directed ZIM3-dCas9 CRISPRi → surface CD81).

**Scope and limits:** Retain promoter→RNA and promoter→surface-protein branches until intermediate-specific evidence is found.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. entity_continuity: not_demonstrated. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. Exact molecular entity/state continuity is absent; an explicit intermediate assertion is required.

Sources: [MG04](https://link.springer.com/article/10.1186/s13059-024-03176-z). Locators: Fig1D; Results implementation; Methods gRNA transduction; Fig1B,C; Methods gRNA transduction and flow

**MG-B008 · MG-M06 · Context contrast · Context contrast**

Allele-directed HeLa minigene and healthy PBMC junction-RNA association are directionally compatible with exon6 exclusion.

Endpoints: MG-A007 (rs6897932 C versus T in IL7R minigene → IL7R reporter exon6); MG-A008 (rs6897932 C carriage → IL7R exon6–7 RNA amplicon).

**Scope and limits:** Compatible splice-related observations, not serial RNA→protein transition or primary immune-cell allele editing.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MG02](https://www.nature.com/articles/ng2103). Locators: Fig2b; Results differential splicing; Methods analysis of exon6 inclusion; Results allele-specific expression; Methods allele-specific IL7R isoform expression

**MG-B009 · MG-M03 · Context contrast · Context contrast**

Within stimulated monocyte data, DDX39B RNA shows null association while DDX39A RNA is inversely associated with extracellular IL7R.

Endpoints: MG-A009 (DDX39B RNA at2 h or24 h LPS → 24-h supernatant IL7R); MG-A011 (DDX39A RNA abundance after24 h LPS → supernatant IL7R).

**Scope and limits:** Paralogue contrast is observational; it does not establish DDX39A causal splicing or protein-dependent mechanism.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MG03](https://pmc.ncbi.nlm.nih.gov/articles/PMC6783569/). Locators: Results sIL7R regulated by rs6897932 and associated with DDX39A; Fig3 and Supplementary Fig7; Fig3c; Results sIL7R subsection

**MG-B010 · MG-M07 · Shared intervention · Response profile**

Chr21q22 enhancer deletion reduces ETS2 RNA induction and phagocytosis in separately sized primary-macrophage panels under the same differentiation protocol.

Endpoints: MG-A017 (chr21q22 1.85-kb enhancer CRISPR deletion → ETS2 transcript); MG-A020 (chr21q22 1.85-kb enhancer CRISPR deletion → zymosan phagocytosis).

**Scope and limits:** Shared intervention only. No native ETS2 protein measurement or enhancer rescue in the extracted arms; no IL6 neutralization or transfer test mediating phagocytosis. These panels cannot be counted as independent donor replications.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MG05](https://pmc.ncbi.nlm.nih.gov/articles/PMC11168933/). Locators: Fig1e,f; Results Resolving molecular mechanisms at chr21q22; Methods monocyte differentiation, CRISPR editing and PrimeFlow; selected L303,309,391–399; ExtendedDataFig5c,d; Results deletion phenocopies ETS2 disruption; Methods Phagocytosis; selected L332,334,417–418

**MG-B011 · MG-M08 · Shared intervention · Response profile**

ETS2 coding-exon disruption reduces day6 supernatant IL6 protein and fluorescent-zymosan phagocytosis in separately sized primary-macrophage panels.

Endpoints: MG-A018 (ETS2 CRISPR coding-exon disruption → IL6); MG-A019 (ETS2 CRISPR coding-exon disruption → zymosan phagocytosis).

**Scope and limits:** Shared intervention only. No native ETS2 protein measurement or enhancer rescue in the extracted arms; no IL6 neutralization or transfer test mediating phagocytosis. These panels cannot be counted as independent donor replications.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MG05](https://pmc.ncbi.nlm.nih.gov/articles/PMC11168933/). Locators: Fig2b; Results Macrophage inflammation requires ETS2; Methods CRISPR editing and Cytokine quantification; selected L325,328,395–396,415–416; Fig2c; Results Macrophage inflammation requires ETS2; Methods Phagocytosis; selected L325,328,417–418

### Activation

Bounded primary-human activation/regulatory mechanism screen. All cytokines are in scope, with receptor, transcription factor, chromatin, protein and functional mechanisms beyond ligand lists. Candidate mediation and shared-intervention branches remain distinct; no independent review or numerical priors.

[Extraction notes](input_snapshot/research/mechanisms_activation/notes.md) · [Screening](input_snapshot/research/mechanisms_activation/screening.json)

**MA-B01 · MA-M01 · Intermediate perturbation/rescue · Pending mechanism review**

CD28 withdrawal reduces nuclear AP-1; perturbing AP-1 with A-FOS reduces activation-induced chromatin opening. This supports an AP-1 requirement within CD3/CD28 activation, without identifying a natural indirect-effect fraction.

Endpoints: MA-A01 (CD28 costimulation omission → nuclear FOS/JUNB protein); MA-A02 (A-FOS dominant-negative protein → AP-1-bound activation-induced chromatin accessibility).

**Scope and limits:** No rescue of CD28 omission by AP-1, broad dominant-negative effects, and other CD28 signaling branches remain possible.

**Structural checks:** Extractor attestations and source dependencies are present; scientific review has not begun.

Sources: [MA-S01](https://pmc.ncbi.nlm.nih.gov/articles/PMC7037242/). Locators: Results Co-stimulation is required for open chromatin formation; FigS5A; Methods nuclear proteins/Western blot; Fig5D–G; Results AP-1 inhibition; Methods A-FOS preparation/electroporation/ATAC-seq

**MA-B02 · MA-M01 · Shared intervention · Response profile**

AP-1 inhibition produces chromatin and RNA branches. Co-occurrence does not prove that a measured accessibility change caused a particular RNA change.

Endpoints: MA-A02 (A-FOS dominant-negative protein → AP-1-bound activation-induced chromatin accessibility); MA-A03 (A-FOS dominant-negative protein → activation-inducible RNA program including IRF8, TBX21, IFNG and CSF2).

**Scope and limits:** Cannot infer secretion, protein abundance, or functional anergy from the RNA/chromatin profile.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S01](https://pmc.ncbi.nlm.nih.gov/articles/PMC7037242/). Locators: Fig5D–G; Results AP-1 inhibition; Methods A-FOS preparation/electroporation/ATAC-seq; Fig5H; Methods RNA-seq and A-FOS electroporation

**MA-B03 · MA-M01 · Context contrast · Context contrast**

Under CD28 omission nuclear AP-1 falls strongly while most NFAT1 binding remains detectable. This opposes treating NFAT1 presence as sufficient for chromatin opening in this context.

Endpoints: MA-A01 (CD28 costimulation omission → nuclear FOS/JUNB protein); MA-A05 (CD28 costimulation omission → NFAT1 chromatin binding).

**Scope and limits:** IL2 locus is an exception to retained NFAT binding; no universal NFAT dispensability claim.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S01](https://pmc.ncbi.nlm.nih.gov/articles/PMC7037242/). Locators: Results Co-stimulation is required for open chromatin formation; FigS5A; Methods nuclear proteins/Western blot; FigS5D; Results Co-stimulation is required

**MA-B04 · MA-M02 · Shared intervention · Response profile**

STAT5B depletion reduces both FOXP3 RNA and protein, a transcriptional/protein response profile.

Endpoints: MA-A06 (STAT5B siRNA depletion → FOXP3 RNA); MA-A07 (STAT5B siRNA depletion → FOXP3 intracellular protein).

**Scope and limits:** No rescue and no measured suppression in the knockdown preparation.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S02](https://pmc.ncbi.nlm.nih.gov/articles/PMC4169138/). Locators: Methods2.4; Results3.1; Fig2D; Methods2.4/flow; Results3.1; Fig2E

**MA-B05 · MA-M02 · Context contrast · Context contrast**

STAT5B and STAT5A depletion produce differing FOXP3 RNA responses in the tested preparation.

Endpoints: MA-A06 (STAT5B siRNA depletion → FOXP3 RNA); MA-A08 (STAT5A siRNA depletion → FOXP3 RNA).

**Scope and limits:** Partial knockdown and small groups; STAT5A null is not equivalence or proof of global dispensability.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S02](https://pmc.ncbi.nlm.nih.gov/articles/PMC4169138/). Locators: Methods2.4; Results3.1; Fig2D; Methods2.4; Results3.1; Fig2D

**MA-B06 · MA-M02 · Serial transition · Blocked connection**

A proposed STAT5B→FOXP3→suppression connection is blocked: knockdown protein data and patient correlation do not demonstrate FOXP3 mediation of function.

Endpoints: MA-A07 (STAT5B siRNA depletion → FOXP3 intracellular protein); MA-A09 (FOXP3-positive Treg fraction across STAT5B genotypes → suppression of responder proliferation).

**Scope and limits:** Genotype, disease and alternative STAT5 targets confound transport.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. entity_continuity: not_demonstrated. context_compatibility: not_demonstrated. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. experimental_linkage: not_demonstrated. Exact molecular entity/state continuity is absent; an explicit intermediate assertion is required.

Sources: [MA-S02](https://pmc.ncbi.nlm.nih.gov/articles/PMC4169138/). Locators: Methods2.4/flow; Results3.1; Fig2E; Methods2.2/2.7; Results3.2; Fig3

**MA-B07 · MA-M03 · Intermediate perturbation/rescue · Pending mechanism review**

IL12-associated intracellular IFNG induction is sensitive to TBX21 perturbation in expanded primary human Tregs. This is conditional TBX21 dependence, not a demonstrated IL12→TBX21 induction edge.

Endpoints: MA-A13 (IL12 → intracellular IFNG protein); MA-A12 (TBX21 CRISPR knockout → IL12-induced intracellular IFNG protein).

**Scope and limits:** Pooled-screen enrichment, incomplete editing, no TBX21 rescue, and cytokine-restimulation context limit the claim to a required regulator of the assayed response.

**Structural checks:** Extractor attestations and source dependencies are present; scientific review has not begun.

Sources: [MA-S03](https://pmc.ncbi.nlm.nih.gov/articles/PMC7577958/). Locators: Fig1b,f; Results Novel regulators; Methods pooled RNP screen; Fig1f pooled discovery; Fig2c arrayed validation; Fig4/Methods arrayed screen

**MA-B08 · MA-M04 · Shared intervention · Response profile**

FOXP3 knockout changes RNA programs and intracellular cytokine proteins across the study, preserved as a branched regulatory profile.

Endpoints: MA-A10 (FOXP3 CRISPR knockout → intracellular IL2 and IFNG protein program); MA-A11 (FOXP3 CRISPR knockout → IL12-context FOXP3-regulated RNA program).

**Scope and limits:** Preparation mismatch and2-donor size preclude a serial RNA→protein/function claim.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S03](https://pmc.ncbi.nlm.nih.gov/articles/PMC7577958/). Locators: Figs3a,b; Results Multidimensional analysis; Methods arrayed Cas9 RNP screen; Figs5/6; Methods scRNA-seq and computational analysis

**MA-B09 · MA-M05 · Shared intervention · Response profile**

IL2RA disruption reduces acute pSTAT5 responsiveness and later measured suppressive function; these are separate branches of the receptor perturbation.

Endpoints: MA-A14 (IL2RA CRISPR knockout → IL2-stimulated STAT5 phosphorylation); MA-A15 (IL2RA CRISPR knockout → Treg suppression of CD4/CD8 responder proliferation).

**Scope and limits:** IL2 consumption, cell persistence and other CD25-related effects may contribute; pSTAT5 is not established mediator of suppression.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S04](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2021.655122/full). Locators: Fig4E; Methods Phosflow, nucleofection/sorting; Fig4F; Methods Suppression Assay

**MA-B10 · MA-M05 · Intermediate perturbation/rescue · Blocked connection**

The stronger hypothesis that the suppression defect is mediated by deficient STAT5 phosphorylation remains untested in these experiments.

Endpoints: MA-A14 (IL2RA CRISPR knockout → IL2-stimulated STAT5 phosphorylation); MA-A15 (IL2RA CRISPR knockout → Treg suppression of CD4/CD8 responder proliferation).

**Scope and limits:** Receptor perturbation alone cannot distinguish STAT5 mediation from IL2 deprivation or survival effects.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. mediation_test: not_demonstrated.

Sources: [MA-S04](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2021.655122/full). Locators: Fig4E; Methods Phosflow, nucleofection/sorting; Fig4F; Methods Suppression Assay

**MA-B11 · MA-M05 · Shared intervention · Response profile**

Suppression is impaired while FOXP3 abundance shows no detectable change, opposing use of FOXP3 protein alone as the functional endpoint.

Endpoints: MA-A15 (IL2RA CRISPR knockout → Treg suppression of CD4/CD8 responder proliferation); MA-A16 (IL2RA CRISPR knockout → FOXP3 intracellular protein).

**Scope and limits:** Neither unchanged FOXP3 nor its expression alone establishes preserved Treg function.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S04](https://www.frontiersin.org/journals/immunology/articles/10.3389/fimmu.2021.655122/full). Locators: Fig4F; Methods Suppression Assay; Fig4D; Results CD25-KO; Methods Flow Cytometry

**MA-B12 · MA-M06 · Shared intervention · Response profile**

IL2 increases FOXP3 RNA at6h and protein at18h in sorted CD25bright cells.

Endpoints: MA-A17 (IL2 → FOXP3 RNA); MA-A18 (IL2 → FOXP3 protein).

**Scope and limits:** Does not prove that measured RNA caused measured protein or that either caused suppression.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S05](https://pmc.ncbi.nlm.nih.gov/articles/PMC1895505/). Locators: Fig1A,C; Methods IL2 induction and quantitative PCR; Fig1B; Methods Western blot analysis

**MA-B13 · MA-M06 · Context contrast · Context contrast**

IL2 response differs between freshly sorted CD25bright and CD25-negative human CD4 cells at6h.

Endpoints: MA-A17 (IL2 → FOXP3 RNA); MA-A19 (IL2 → FOXP3 RNA in CD25-negative cells).

**Scope and limits:** CD25 strata contain other state differences; cannot assign all difference to CD25 or transport to activated cells.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S05](https://pmc.ncbi.nlm.nih.gov/articles/PMC1895505/). Locators: Fig1A,C; Methods IL2 induction and quantitative PCR; Fig1A,C; Methods IL2 induction/quantitative PCR

**MA-B14 · MA-M07 · Intermediate perturbation/rescue · Pending mechanism review**

The anti-CD3-associated FOXP3 protein response depends partly on endogenous IL2 activity in the PBMC culture, supported by neutralization and IL2 competition.

Endpoints: MA-A22 (CD3 triggering → FOXP3 intracellular protein-positive T cells); MA-A23 (IL2 neutralization during CD3 triggering → FOXP3 intracellular protein induction).

**Scope and limits:** Neither antibody fully inhibitory alone; mixed-cell indirect effects possible. No STAT5 assay or stable Treg-function claim.

**Structural checks:** Extractor attestations and source dependencies are present; scientific review has not begun.

Sources: [MA-S07](https://pmc.ncbi.nlm.nih.gov/articles/PMC2265256/). Locators: Fig1B,D; Methods PBMC isolation/activation and flow; Fig3C,D; Fig4; Methods antibody/activation and flow

**MA-B15 · MA-M07 · Intermediate perturbation/rescue · Pending mechanism review**

Neutralization/CD25 blockade and IL2 competition strengthen the narrow IL2/CD25 dependence of FOXP3 induction; high combined blockade resists10nM IL2 rescue.

Endpoints: MA-A23 (IL2 neutralization during CD3 triggering → FOXP3 intracellular protein induction); MA-A24 (IL2 supplementation during CD25 blockade → CD3-induced FOXP3 protein expression).

**Scope and limits:** Competitive rescue is concentration dependent. High combined blocker failure is retained; a complete negative-feedback loop is not established.

**Structural checks:** Extractor attestations and source dependencies are present; scientific review has not begun.

Sources: [MA-S07](https://pmc.ncbi.nlm.nih.gov/articles/PMC2265256/). Locators: Fig3C,D; Fig4; Methods antibody/activation and flow; Fig3A,B; Fig4A,B; Methods antibody/activation and flow

**MA-B16 · MA-M07 · Context contrast · Context contrast**

FOXP3 induction in activated PBMCs does not by itself establish suppression of neighboring FOXP3-negative-cell IL2 responses.

Endpoints: MA-A22 (CD3 triggering → FOXP3 intracellular protein-positive T cells); MA-A25 (CD3/CD28 restimulation → intracellular IL2 in FOXP3-negative CD4 cells).

**Scope and limits:** Does not oppose all Treg suppressive activity; culture ratios, timing and activated non-Treg FOXP3 expression matter.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MA-S07](https://pmc.ncbi.nlm.nih.gov/articles/PMC2265256/). Locators: Fig1B,D; Methods PBMC isolation/activation and flow; Fig5C; TableS1 summarized in Results; Methods cytokine production

**MA-B17 · MA-M08 · Intermediate perturbation/rescue · Blocked connection**

RBPJ/HDAC3 repression and RBPJ-dependent suppression are promising follow-up hypotheses, blocked until complete primary wet-lab Methods and Results are inspected.

Endpoints: MA-A21 (RBPJ overexpression with HDAC3 deletion → RBPJ-mediated FOXP3 protein repression); MA-A20 (RBPJ CRISPR knockout → iTreg suppression of responder proliferation).

**Scope and limits:** Source correction adds competing-interest disclosure. No claims from mouse-host GvHD transported into human in vivo.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. MA-A21: primary extraction is incomplete. MA-A21: null, opposing or inconclusive endpoint. MA-A21: relevant primary full text is unavailable. MA-A20: primary extraction is incomplete. MA-A20: relevant primary full text is unavailable. entity_continuity: not_demonstrated. context_compatibility: not_demonstrated. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. experimental_linkage: not_demonstrated. mediation_test: not_demonstrated.

Sources: [MA-S06](https://www.nature.com/articles/s41586-025-08795-5). Locators: Public Fig4b,d,e; main wet-lab Methods unavailable; Public Fig3j caption; main wet-lab Methods unavailable

### Antigen

Seven primary articles broaden immune evidence to antigen processing, presentation, and recognition. The strongest human-effector restoration result is B2M replacement in HLA-compatible melanoma. Primary human DCs demonstrate opposing RNA and surface-HLA trends, and patient TAP2-deficient EBV-B targets retain selected autologous CTL recognition. ERAP1 and recent B-cell experiments add perturbational, peptide, and reporter evidence with explicit preparation/species limits. These are pending-review assertions and connection proposals, not a frozen pathway or a prior model.

[Extraction notes](input_snapshot/research/mechanisms_antigen/notes.md) · [Screening](input_snapshot/research/mechanisms_antigen/screening.json)

**MP_B001 · MP_M001 · Intermediate perturbation/rescue · Pending mechanism review**

Restoring functional B2M in 1074mel supports B2M-dependent susceptibility to HLA-compatible human CTL lysis.

Endpoints: MP_A001 (B2M-expressing vaccinia → intracellular immunoreactive B2M in 1074mel); MP_A003 (B2M-expressing vaccinia → 1074mel lysis by HLA-A2.1-restricted human antimelanoma CD8 T cells).

**Scope and limits:** Human melanoma target; human allogeneic expanded CD8 recipient. Single compatible tumor line; viral-vector rescue could affect additional variables. No claim of peptide identity, direct binding or exclusive HLA-surface mediation.

**Structural checks:** Extractor attestations and source dependencies are present; scientific review has not begun.

Sources: [MP_S001](https://pmc.ncbi.nlm.nih.gov/articles/PMC2248456/). Locators: Fig3; Methods Western Blot Analyses; parsed text lines 116–117,230–233; Fig5; Methods Cytotoxic T Lymphocytes and Microcytotoxicity Assays; Results preceding Fig5

**MP_B002 · MP_M001 · Shared intervention · Response profile**

B2M rescue changes surface HLA and CTL lysis as a branched response.

Endpoints: MP_A002 (B2M-expressing vaccinia → surface folded HLA class I); MP_A003 (B2M-expressing vaccinia → 1074mel lysis by HLA-A2.1-restricted human antimelanoma CD8 T cells).

**Scope and limits:** HLA-intermediate necessity was not independently perturbed in this experiment. Do not relabel this profile as surface HLA causing killing.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S001](https://pmc.ncbi.nlm.nih.gov/articles/PMC2248456/). Locators: Fig1; Methods Cytofluorography; Results after Fig3; Fig5; Methods Cytotoxic T Lymphocytes and Microcytotoxicity Assays; Results preceding Fig5

**MP_B003 · MP_M001 · Context contrast · Context contrast**

HLA-mismatched 1259mel remains near background despite B2M restoration, limiting a universal rescue-to-killing claim.

Endpoints: MP_A003 (B2M-expressing vaccinia → 1074mel lysis by HLA-A2.1-restricted human antimelanoma CD8 T cells); MP_A004 (B2M-expressing vaccinia in HLA-A2.1-negative 1259mel → lysis by HLA-A2.1-restricted human antimelanoma CD8 T cells).

**Scope and limits:** Negative graph control is qualitative; target antigens and other line-specific differences are not fully matched.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S001](https://pmc.ncbi.nlm.nih.gov/articles/PMC2248456/). Locators: Fig5; Methods Cytotoxic T Lymphocytes and Microcytotoxicity Assays; Results preceding Fig5; Fig5 caption and visually inspected Fig5 image; Methods Microcytotoxicity Assays

**MP_B004 · MP_M001 · Context contrast · Context contrast**

Mouse vaccinia recognition provides a different antigen-processing context, not independent human-recipient replication.

Endpoints: MP_A003 (B2M-expressing vaccinia → 1074mel lysis by HLA-A2.1-restricted human antimelanoma CD8 T cells); MP_A005 (B2M replacement plus mouse H-2Kd vaccinia in human targets → vaccinia-specific murine CD8-mediated target lysis).

**Scope and limits:** Recipient taxon, MHC molecule and antigen differ. H82 non-rescue limits sufficiency of B2M across targets.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S001](https://pmc.ncbi.nlm.nih.gov/articles/PMC2248456/). Locators: Fig5; Methods Cytotoxic T Lymphocytes and Microcytotoxicity Assays; Results preceding Fig5; Fig4; Methods Cytotoxic T Lymphocytes and Microcytotoxicity Assays

**MP_B005 · MP_M002 · Context contrast · Context contrast**

TAP1-specific, not TAP2, complementation supports the TND-3 surface-HLA defect being attributable to TAP1.

Endpoints: MP_A006 (TAP1-expressing vaccinia → surface HLA class I on TND-3); MP_A007 (TAP2-expressing vaccinia → surface HLA class I on TAP1-deficient TND-3).

**Scope and limits:** Surface rescue only; no downstream antigen-specific T-cell endpoint in this complementation experiment.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S002](https://www.jci.org/articles/view/5687). Locators: Fig2b; Methods Cell lines and recombinant vaccinia viruses; Results TAP1 complementation; Fig2b; Results TAP1/TAP2 complementation

**MP_B006 · MP_M003 · Serial transition · Blocked connection**

The variant-to-splicing observation cannot yet form a measured transcript-to-TAP2-protein-to-HLA pathway.

Endpoints: MP_A008 (TAP2 intron IX splice-acceptor G>A (article numbering) → TAP2 cDNA lacking G at coding nucleotide 1635); MP_A009 (TAP2-expressing vaccinia → surface HLA class I on HA-L).

**Scope and limits:** Whole-gene rescue does not establish a measured translation bridge or isolate the causal nucleotide.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. entity_continuity: not_demonstrated. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. Exact molecular entity/state continuity is absent; an explicit intermediate assertion is required.

Sources: [MP_S003](https://pmc.ncbi.nlm.nih.gov/articles/PMC1906261/). Locators: Fig3; Methods Mutation analysis; Results mutation characterization; Fig2a; Methods Complementation assay; Results mutation section

**MP_B007 · MP_M003 · Context contrast · Context contrast**

Residual autologous CTL lysis occurs in uncomplemented HA-L, so low surface class I does not imply absent antigen recognition.

Endpoints: MP_A009 (TAP2-expressing vaccinia → surface HLA class I on HA-L); MP_A011 (uncomplemented autologous TAP2-deficient HA-L EBV-B targets → lysis by patient-2 expanded CD8 alpha-beta T cells).

**Scope and limits:** One patient and expanded CTL specificity; antigen identity tested separately using nonhuman COS targets. No general antiviral-protection claim.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S003](https://pmc.ncbi.nlm.nih.gov/articles/PMC1906261/). Locators: Fig2a; Methods Complementation assay; Results mutation section; Fig5a; Methods Anti-EBV T-cell responses; Results Anti-EBV T-cell response

**MP_B008 · MP_M004 · Shared intervention · Response profile**

LPS lowers CIITA RNA and protein; the observations remain separate molecular layers.

Endpoints: MP_A013 (LPS maturation → CIITA type-I/type-III RNA); MP_A014 (LPS maturation → CIITA protein isoforms).

**Scope and limits:** No precise isoform translation bridge or antigen-specific human CD4 endpoint.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S004](https://pmc.ncbi.nlm.nih.gov/articles/PMC2193505/). Locators: Fig3B–E; Methods DCs, RPA, Real Time PCR; Fig2C; Methods Immunoprecipitation and Immunoblotting

**MP_B009 · MP_M004 · Shared intervention · Response profile**

Maturing human DCs show reduced DRA RNA at 24 h alongside increased surface HLA-DR.

Endpoints: MP_A015 (LPS maturation → HLA-DRA RNA); MP_A016 (LPS maturation → cell-surface HLA-DR).

**Scope and limits:** Contradicts using RNA direction as a surface-protein proxy. No measured T-cell function follows from surface staining.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S004](https://pmc.ncbi.nlm.nih.gov/articles/PMC2193505/). Locators: Fig1C–D; Methods DCs and Real Time PCR; Fig1A–B; Methods DCs and Cytofluorometry

**MP_B010 · MP_M005 · Shared intervention · Response profile**

ERAP1 knockout lowers HLA-C-enriched surface staining and mouse reporter stimulation as parallel outcomes.

Endpoints: MP_A018 (ERAP1 knockout → DT-9-reactive surface HLA-C-enriched signal); MP_A019 (ERAP1 knockout → activation of human-TCR-expressing mouse hybridoma by melanoma targets).

**Scope and limits:** Surface abundance is not proven to mediate reporter loss; DT-9 specificity and mouse-recipient limits retained.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S005](https://pmc.ncbi.nlm.nih.gov/articles/PMC7611875/). Locators: Fig1A–J; Methods Evaluation of HLA expression; Results ERAP1 controls cell surface-expression; Fig3A–B; Methods reporter stimulation

**MP_B011 · MP_M005 · Intermediate perturbation/rescue · Pending mechanism review**

ERAP1 reconstitution after knockout supports an ERAP1-dependent reporter-stimulation mechanism within WM793.

Endpoints: MP_A019 (ERAP1 knockout → activation of human-TCR-expressing mouse hybridoma by melanoma targets); MP_A020 (ERAP1 Hap2 versus Hap10 reconstitution of ERAP1-null WM793 → activation of human-TCR-expressing mouse hybridoma).

**Scope and limits:** Narrow ERAP1-dependence only. Does not prove exclusive HLA-abundance mediation, exact presented peptide length, physiological allotype dosage or primary human-CD8 function.

**Structural checks:** Extractor attestations and source dependencies are present; scientific review has not begun.

Sources: [MP_S005](https://pmc.ncbi.nlm.nih.gov/articles/PMC7611875/). Locators: Fig3A–B; Methods reporter stimulation; Fig2A and Fig3C–D; Methods Plasmid-based transfection

**MP_B012 · MP_M005 · Serial transition · Blocked connection**

Biochemical trimming supports plausibility but cannot be equated to direct delivery of the measured digest products into the reporter experiment.

Endpoints: MP_A021 (purified human ERAP1 Hap2 versus Hap10 → ADAMTSL5 11mer trimming products); MP_A022 (ERAP1 knockout with ADAMTSL5 precursor-length variation → mouse TCR-hybridoma sGFP activation).

**Scope and limits:** No same-species/state peptide transfer, absolute peptide-HLA quantification or cell-context equivalence.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. Species is unknown or differs between endpoints. entity_continuity: not_demonstrated. context_compatibility: not_demonstrated. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. experimental_linkage: not_demonstrated. Exact molecular entity/state continuity is absent; an explicit intermediate assertion is required.

Sources: [MP_S005](https://pmc.ncbi.nlm.nih.gov/articles/PMC7611875/). Locators: Fig5A–C; Methods In vitro peptide digestion assays; Fig4A–C; Methods Plasmid-based transfection; Results Generation of the autoantigenic epitope

**MP_B013 · MP_M006 · Context contrast · Context contrast**

B2M knockout lowers TCR1 activation but preserves TCR22 activation, limiting class-I-generalized claims.

Endpoints: MP_A023 (B2M knockout in matched-TMG MEL9 B cells → MEL9 TCR1 Jurkat CD69 activation); MP_A024 (B2M knockout in matched-TMG MEL9 B cells → MEL9 TCR22 Jurkat CD69 activation).

**Scope and limits:** Immortalized human cells, engineered murine TCR constant domains, no primary effector function or surface-class-I mediation claim.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S006](https://www.nature.com/articles/s41467-024-55420-6). Locators: Supplementary Fig4i (PDF pp8–9); Methods Antigen presentation/additional engineering and T cell activation assays; Supplementary Fig4i (PDF pp8–9); main Results HLA restriction

**MP_B014 · MP_M006 · Context contrast · Context contrast**

TCR22 remains active under B2M knockout but is inhibited by HLA-II blockade, supporting class-II restriction.

Endpoints: MP_A024 (B2M knockout in matched-TMG MEL9 B cells → MEL9 TCR22 Jurkat CD69 activation); MP_A025 (IVA12 HLA-class-II blocking antibody → MEL9 TCR22 Jurkat CD69 activation).

**Scope and limits:** Restricting class supported; no precise HLA-II allele/ligand quantity or clinical response inferred.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S006](https://www.nature.com/articles/s41467-024-55420-6). Locators: Supplementary Fig4i (PDF pp8–9); main Results HLA restriction; Supplementary Fig4i (PDF pp8–9); Methods T cell activation and TCR characterization assays

**MP_B015 · MP_M007 · Intermediate perturbation/rescue · Pending mechanism review**

Depletion and autologous add-back support B-cell contribution to bulk spontaneous PBMC proliferation.

Endpoints: MP_A026 (B-cell depletion from patient PBMCs → bulk autologous PBMC proliferation); MP_A027 (autologous B-cell re-addition to B-depleted PBMCs → bulk autologous PBMC proliferation).

**Scope and limits:** This is a B-cell-dependence mechanism for bulk PBMC proliferation. It does not establish antigen identity, B-cell-specific HLA mechanism or CD8-specific response.

**Structural checks:** Extractor attestations and source dependencies are present; scientific review has not begun.

Sources: [MP_S007](https://pmc.ncbi.nlm.nih.gov/articles/PMC12732238/). Locators: Fig3B; Methods 2.7; Results 3.4; Fig3B; Methods 2.7; Results 3.4

**MP_B016 · MP_M007 · Intermediate perturbation/rescue · Blocked connection**

Bulk class-I blockade is insufficient to assign the B-cell add-back effect specifically to B-cell HLA-I.

Endpoints: MP_A027 (autologous B-cell re-addition to B-depleted PBMCs → bulk autologous PBMC proliferation); MP_A028 (W6/32 pan-HLA-class-I blockade → bulk psoriasis PBMC proliferation).

**Scope and limits:** B-cell-specific HLA perturbation and matching donor readouts needed.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. entity_continuity: not_demonstrated. context_compatibility: not_demonstrated. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. experimental_linkage: not_demonstrated. mediation_test: not_demonstrated.

Sources: [MP_S007](https://pmc.ncbi.nlm.nih.gov/articles/PMC12732238/). Locators: Fig3B; Methods 2.7; Results 3.4; Fig3D; Methods 2.7; Results 3.4

**MP_B017 · MP_M007 · Serial transition · Blocked connection**

B-depletion-associated bulk proliferation loss cannot be assigned directly to the separately measured CD8 CFSE response.

Endpoints: MP_A026 (B-cell depletion from patient PBMCs → bulk autologous PBMC proliferation); MP_A029 (psoriasis versus healthy donor PBMC context → CD8-positive-cell proliferation).

**Scope and limits:** No CD8-resolved readout under the same B-cell manipulation; no antigen specificity.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. entity_continuity: not_demonstrated. context_compatibility: not_demonstrated. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. experimental_linkage: not_demonstrated. Exact molecular entity/state continuity is absent; an explicit intermediate assertion is required.

Sources: [MP_S007](https://pmc.ncbi.nlm.nih.gov/articles/PMC12732238/). Locators: Fig3B; Methods 2.7; Results 3.4; Fig3E; Methods 2.7; Results 3.4

**MP_B018 · MP_M008 · Serial transition · Blocked connection**

Antigen-specific mouse reporter stimulation by tonsillar B cells cannot be joined to the primary-human blood CD8 proliferation observation.

Endpoints: MP_A030 (W6/32 blockade of primary tonsillar B-cell/hybridoma coculture → Vα3S1/Vβ13S1 mouse T-hybridoma activation); MP_A029 (psoriasis versus healthy donor PBMC context → CD8-positive-cell proliferation).

**Scope and limits:** Species, tissue, cell state, time and specificity mismatch block transport.

**Structural checks:** Extractor identified missing evidence. The proposed connection is not supporting evidence. Species is unknown or differs between endpoints. entity_continuity: not_demonstrated. context_compatibility: contradictory. temporal_compatibility: not_demonstrated. measurement_link: not_demonstrated. experimental_linkage: not_demonstrated. Exact molecular entity/state continuity is absent; an explicit intermediate assertion is required.

Sources: [MP_S007](https://pmc.ncbi.nlm.nih.gov/articles/PMC12732238/). Locators: Fig1C; Methods 2.5–2.6; Results 3.1; Fig3E; Methods 2.7; Results 3.4

**MP_B019 · MP_M008 · Context contrast · Context contrast**

ADAMTSL5 biochemical/target-cell evidence cannot imply its presentation by the four B-cell lines where the peptide was not detected.

Endpoints: MP_A021 (purified human ERAP1 Hap2 versus Hap10 → ADAMTSL5 11mer trimming products); MP_A031 (four HLA-C*06:02-homozygous EBV-B ligand preparations → detected ADAMTSL5 autoantigen peptide).

**Scope and limits:** Nondetection has sensitivity limits. Cell-line identifiers/FDR-file inconsistencies unresolved; no absence claim.

**Structural checks:** Nonserial evidence; does not establish an outcome-to-input transition.

Sources: [MP_S005](https://pmc.ncbi.nlm.nih.gov/articles/PMC7611875/); [MP_S007](https://pmc.ncbi.nlm.nih.gov/articles/PMC12732238/). Locators: Fig5A–C; Methods In vitro peptide digestion assays; Methods 2.9–2.12; Results 3.6

## Questions for the later review

1. Do the primary Methods, results and original figures support each narrow assertion and reported result?
2. Do rescue/intermediate perturbations support the proposed dependence, with appropriate off-target and engineered-system limits?
3. Are donor overlap, species, cell preparation, timing, assay specificity and original cohort reuse accurately represented?
4. Are nulls and contrary observations preserved without interpreting nonsignificance as absence?
5. Should any blocked transition be reconsidered only after additional primary evidence, rather than by relabeling a branch?
6. Are proposed corrections to inherited records justified, especially whole-blood versus PBMC preparation?

## Remaining evidence gaps

- **MG-GAP01**: Need isoform-specific protein measurement or selective splice-product manipulation with downstream protein readout in the same primary CD4 preparation. Current sh5 discordance and shared-epitope ELISA block serial transition.
- **MG-GAP02**: HeLa luciferase reporter is not endogenous DDX39B. Native allele editing with DDX39B protein, IL7R isoform RNA and isoform-specific protein in compatible primary cells needed.
- **MG-GAP03**: Whole-blood PAXgene versus PBMC Trizol provenance must be resolved per individual in n86 panel; old record unchanged.
- **MG-GAP04**: 2024 enhancer screen measures RNA only for these candidates. Recover exact enhancer genomic coordinates, guides, source-data values and donor counts before fine-grained variant-to-protein path.
- **MG-GAP05**: Same promoter intervention affects both endpoints; correlation supports a branch. No transcript-specific rescue, translation/trafficking test, or measured RNA-first ordering establishes serial mediation.
- **MG-GAP06**: Source-access gap resolved by complete primary PMC HTML recovered through parent approved curl. Four narrow enhancer/ETS2 perturbation assertions extracted. Full allele-specific mechanism, native ETS2 protein bridge, rescue and remaining experiments await detailed extraction.
- **MG-GAP07**: No matching correction notice found in bounded queries or G03 PubMed Erratum/Retraction find and MG04 publisher Correction find. Structured Entrez relationships unavailable; G08/G10 PubMed returned zero text. This is not proof no corrections exist.
- **MG-GAP08**: Sequencing Methods specify fresh cells10 days after guide transduction and frozen same-experiment cells with3-day recovery, whereas preceding culture Methods describe48h +4 days selection +6 days further culture. Do not silently harmonize arithmetic or infer unique biological donors.
- **MA-G01**: Direct chromatin→specific RNA→secreted protein/function chain after AP-1 mediation remains absent; no serial pathway is materialized.
- **MA-G02**: STAT5 phosphorylation→FOXP3→Treg suppression requires matched intermediate perturbation/rescue with human functional endpoints.
- **MA-G03**: Recent2025 RBPJ/HDAC3 study: public figures and analytical supplement accessible; main wet-lab Methods/Results inaccessible on attempted primary/public routes. Retain needs_full_text.
- **MA-G04**: Full TCR-proximal LCK/ZAP70/LAT/calcium causal extraction, tissue-resident contexts, receptor dose titration and matched donor kinetics remain to be screened.
- **MA-G05**: Ancestry, age/sex, genotype, exact cross-figure donor linkage and measurement calibration often unavailable. Do not assume transport or replicate independence.
- **MA-G06**: Independent scientific review and human adjudication intentionally pending user trigger; no numerical priors or release approval.
- **MP_G001**: Surface HLA abundance does not quantify a specific peptide-HLA complex; no selective surface-HLA mediation test between B2M replacement and human CTL lysis in S001.
- **MP_G002**: TAP2 sequence-to-aberrant RNA observation lacks measured mutant TAP2 protein. HLA rescue and residual CTL experiments use different intervention states.
- **MP_G003**: CIITA RNA, protein isoforms and surface HLA-DR measured in separate experiments with donor overlap unavailable; no antigen-specific human CD4 endpoint.
- **MP_G004**: ERAP1 biochemical digestion does not determine exact 8mer versus 9mer surface product or direct transfer into the reporter assay. Mouse recipient assays cannot establish human primary-CD8 function.
- **MP_G005**: He2025 depletion/add-back bulk proliferation and CD8 CFSE assays have different cohort sizes with unresolved individual overlap. Antigen specificity of the primary-human proliferation endpoint is unmeasured.
- **MP_G006**: He2025 Methods HG00131/HG00313 and Results 1%-FDR versus filename FDR_0.1 are unresolved. W6/32 pan-HLA immunoprecipitation plus prediction must not be labeled direct HLA-C*06:02 ligand isolation.
- **MP_G007**: No independent or human review yet. Ranked web retrieval does not provide exhaustive recall; corrections/retractions may be missed. Modern effectors/autologous B2M rescue and additional primary human APC variant studies remain follow-up priorities.

## Validation and use

Structural checks cover references, exact source hashes, pending-review states, molecular entity separation and conservative connection rules. These checks do not replace biological review. Ranked literature searches are documented focused retrievals, not an exhaustive systematic review.

`immune_candidate.sqlite` includes the unchanged baseline tables plus `candidate_*` tables and the discovery-only `cytokine_inventory`. All candidate tables are also exported as CSV. `mechanism_graphs.json` stores measured assertion edges separately from connection proposals; response profiles and context contrasts cannot be traversed as serial paths.

`input_manifest.json` and `input_snapshot/` preserve the exact candidate inputs. The copied baseline database is bound to its frozen manifest; the full historical evidence provenance remains in Release 0.2.0. Candidate inputs do not duplicate the entire historical source archive.
