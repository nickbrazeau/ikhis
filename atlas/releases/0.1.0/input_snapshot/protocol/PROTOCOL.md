# Greenfield multi-omic immune evidence review protocol

Version: 0.1.0. Status: operational protocol for an initial, bounded evidence release; not prospectively registered in an external registry. Governing specification: README.md. Scope: human immune-system biology with separately retained animal and experimental-system evidence. Search cutoff: 2026-09-12. No previous statistical-model priors are imported.

## Review question and scope

For the prioritized cytokine assay labels and immune-system entities, which individual genomic, transcriptional, protein, signaling and cellular relationships are supported, in which contexts, and by which independent biological studies? The unit of extraction is an assertion supported by an evidence instance. A complete communication chain is never the default extraction unit.

Release 0.1 is an explicitly bounded, critically reviewed initial evidence corpus and working knowledge base. It does not certify saturation of the immune-system literature. The full README checklist is tracked separately; an empty evidence table is an acknowledged gap rather than a negative biological result. A systematic-review-complete designation requires uncapped database retrieval, documented dual screening/full-text extraction, resolved cohort identity, and human adjudication. This protocol makes those requirements executable and visible without claiming they have occurred.

## Eligibility

Include primary human immune-cell perturbation studies, genetics/QTL studies, multi-omic atlases and relevant curated resources with traceable provenance. Retain nonhuman studies in separate contexts. Include original research of any publication date through the cutoff; recent 2024–2026 resources receive targeted discovery. Include null and opposing results with their original context. Preprints are retained with status and version. Reviews support discovery and context; they are not counted as additional biological replication of the original study.

Exclude unsupported mechanistic claims, inaccessible details presented as extracted facts, nonimmune results without a specified immune bridge, retracted results as positive support, and computational ligand–receptor predictions represented as causal evidence. Full text is preferred. Abstract-only and metadata records are explicitly labeled and cannot establish details absent from the accessible text. Corrections, retractions and preprint/publication links must be checked during full curation; unverified status remains a coverage limitation.

## Search and screening

Four lanes cover cytokine/signaling, genomics, transcription and proteomics. Save exact queries, provider, retrieval time, response snapshots and screening decisions. Entity searches use canonical symbols plus original assay aliases. Citation chaining begins at the dictionary/atlas anchors and follows relevant original experiments. DOI/PMID/accession deduplication precedes assertion weighting. Results screened for the bounded pilot must not be described as a PRISMA-complete retrieval. Unscreened search hits remain excluded from assertion priors.

## Normalization and molecular layers

Use distinct identifiers for genes, transcripts, proteins, protein complexes, variants, regulatory elements, cells, states, pathways, programs, processes and assay concepts. External ontology identifiers are assigned only when verified; otherwise retain a stable local ID and mark external mapping unavailable. Preserve original assay labels. CXCL8 has separate standard/high-range channels; unresolved IL-12 and VEGF channels cannot be silently resolved to a protein. Define complexes with explicit components where established.

DNA, RNA, protein abundance, extracellular secretion, phosphorylation/activity and cellular phenotype are separate measurements. An edge crossing these layers requires evidence of that transition. A perturbation-to-RNA response does not establish a direct transcription-factor interaction or a measured phenotype.

## Context and cohort identity

Capture species, ancestry, age, sex, tissue, disease/severity, treatment, cell type/state, developmental state, stimulation, dose, duration, assay, genomic background and time point. Unknown is `unavailable`, never an inferred default. Context mismatch reduces transportability; incompatible or unknown critical context blocks materialized mechanistic paths. Unknown context does not prove equivalence.

Cohorts and datasets have separate registry entries. Reused samples, atlas reanalyses and related publications are assigned an independence group only after evidence supports the assignment. Within a known group and assertion/context, repeated evidence contributes at most the largest single weight. Unknown independence is pooled conservatively into one unresolved group. Publication counts are not replication counts. Participant counts must not be inferred from single-cell counts.

## Evidence grades and quality

Genomics: G1 association; G2 molecular QTL; G3 fine mapping/colocalization with a credible mechanism; G4 experimentally demonstrated variant effect. Reporter validation establishes the assayed regulatory effect and does not by itself establish the complete in-vivo disease mechanism. A nearest gene is never a causal assignment.

Communication: P0 expression/inference; P1 observational or curated biochemical relationship; P2 cytokine target perturbation; P3 demonstrated receptor/pathway dependence; P4 source manipulation demonstrating cytokine-dependent target effects. Transcriptomic/proteomic observational and perturbational labels are retained rather than forced into a causal cytokine grade.

Track assay specificity, isoforms, peptide/reagent identity, detection limits, normalization, surface/extracellular location and PTM site when available. Track pseudoreplication, donor/batch effects, composition and multiple testing. Missing essential method details lower quality and block unsupported causal upgrades.

## Prior construction

The initial implementation supplies transparent, heuristic Beta/Dirichlet evidence summaries for explicitly specified hypotheses, not calibrated probabilities of biological truth. Starting existence prior is Beta(1,1). Each scored record has a `tested_hypothesis` and a separately reviewed `evidence_relation` of supports, opposes or inconclusive. Relation must never be inferred from whether the observed direction is increase, decrease, mixed or null. A supporting evidence group contributes its weight to alpha; an explicitly opposing group contributes to beta. A mixed transcriptional program can support a relationship without supplying any evidence against its existence. Direction uses a separate Dirichlet(1,1,1) over increase/decrease/other. Direction estimates never imply the existence posterior.

Null-evidence adequacy must document a relevant detection/response threshold, measurement precision and an equivalence or other justified absence assessment before a null can oppose an existence hypothesis. Nonsignificance alone is inconclusive. Negative predicates remain searchable descriptive assertions; no silent switch to their positive complement is allowed. All pilot nulls have inadequate or unavailable absence evidence and are excluded from numerical existence/direction updates. Their observed classes, context and uncertainty remain in the release. Scoring annotations explicitly identify the narrow hypothesis; an unannotated record cannot update a prior.

Default tier weights: G1/P0=0.25, G2/P1/observational=0.5, G3/P2/perturbational=1, P3=1.5, G4/P4=2. Abstract-only extractions are downweighted; unreviewed assertions are withheld. These are explicit engineering choices pending calibration, not an inherited or agreed scientific scoring system. Priors remain context-specific. No multiplication of edge probabilities produces a path probability. No transportability probability is invented from species labels.

Magnitude, temporal, genetic-modifier, expression, protein-availability, transportability and context dimensions are exported as separate prior-parameter families. Numeric distributions require extractable quantitative evidence or validated calibration. Otherwise their distribution is `unavailable` with a reason; categorical observed classes remain available. This prevents false precision and documents the full intended prior interface.

Journal impact factors: authoritative JCR metric, metric year and licensing/provenance are mandatory before use. Because the README refers to an agreement not supplied in this greenfield folder, no agreed formula is assumed. The proposed optional multiplier is 1 + 0.05*tanh(log(1+JIF)/3), bounded [1,1.05); missing/unverified metrics use 1. All outputs include the no-journal sensitivity estimate. Journal weighting is disabled by default and cannot dominate design.

## Integration, adversarial review and adjudication

Candidate paths require entity continuity, explicit evidence for every transition, compatible species/tissue/cell state and measured temporal ordering, no unresolved high-severity challenge, and approved bridge links. Unknown critical fields block materialization, while preserving the individual assertions. No graph path is promoted solely because database endpoints match.

An independent adversarial reviewer checks extraction fidelity, grades, cohort reuse, molecular layers, incompatible contexts, causal-gene assignments, temporal assumptions and prior calibration. Findings are retained with severity, target, rationale, source and disposition. The coordinating agent may repair clerical/schema/extraction errors and document automated/agent adjudication. It cannot label its own decision human adjudication. Unresolved high-severity biological findings mark affected evidence contested and exclude it from default priors/paths. Human adjudication remains pending where required.

## Versioning and release

Version evidence, sources, instruction bundles, biological priors and knowledge-base releases. Record source retrieval dates and actual release/version or `unavailable`. Snapshot hashes refer to the exact saved payload, with access level identified. Model/provider/snapshot/reasoning metadata are recorded only if known. Code commit is unavailable when the folder has no Git repository. Register the protocol locally with SHA-256; this is not external preregistration.

Each release exports normalized CSVs, SQLite, data dictionary, corpus/search and cohort manifests, critic/adjudication tables, prior changes, QC, evidence synthesis and a SHA-256 manifest. The manifest excludes itself to avoid a circular digest. Rebuilding is deterministic from frozen inputs; the release is overwritten only through an explicit build command and the authoritative inputs are preserved. No external publication is implied by a local release.
