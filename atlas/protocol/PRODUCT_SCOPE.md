# Immune-system evidence product scope

Status: 0.3.0 candidate preparation; independent review will be triggered by the user after steps 1–3. This document implements the user's instruction to include all cytokines and remove the former fixed cytokine priority set.

## End product and intended use

A versioned, queryable human immune-system knowledge base connects genetic regulation, transcripts and programs, protein forms and activity, cell communication, and measured immune function. It records what is supported in a specific biological context, the original evidence, contrary observations, uncertainty and review history. The downstream use is mechanistic interpretation and preparation of biological inputs for immune-response models. Clinical prediction, treatment recommendations and calibrated probabilities require later validation and are not outputs of this phase.

All cytokines are eligible. The initial inventory is a dated union of authoritative cytokine annotations, with reviewed and unreviewed resource records distinguished. Literature-supported entities missing from those annotations can be added with provenance. The inventory is expandable; its initial size is neither a permanent biological boundary nor a claim that every cytokine relationship has been extracted. Proteins, subunits, active complexes and isoforms are distinct. Receptors and downstream regulators remain separately typed, even when a resource gives them overlapping functions.

Genetic variants, regulatory elements, transcription factors, antigen processing and presentation, immunopeptidomes, innate and adaptive activation, immune-cell differentiation and measured cellular functions remain in scope independently of cytokines. No historical assay panel determines inclusion, research priority or project completion.

## Evidence contexts

The primary reference organism is human. Primary human immune cells, human tissue/coculture experiments, human genetic cohorts and human target cells involved in immune recognition are eligible. Human cell lines and engineered experimental systems are retained with their actual identity. Nonhuman experiments can provide separate mechanistic context but cannot silently complete a human pathway. Resting, activated, disease-associated and engineered states remain distinct.

Each assertion records species, ancestry when relevant, biological preparation, tissue, cell type/state, perturbation and dose, schedule, assay, molecular form, donor/sample basis, cohort relationship, measured outcome and exact source locator. Missing fields remain explicit. Unknown genotype in a within-study perturbation experiment does not become a genotype-specific conclusion; unknown cross-cohort transport remains unresolved.

## Questions the product should support

1. Which genomic or regulatory perturbations affect a transcript, splice event or measured protein, and in which cells?
2. Which receptor or signaling interventions change a transcriptional program, protein state or cellular response?
3. Which cytokines are produced, detected or functionally active, and what source/recipient evidence distinguishes these statements?
4. Which antigen-processing and presentation components affect surface complexes, presented peptides or antigen-specific immune recognition?
5. Which proposed connections are supported by serial or mediation experiments, which are only shared-intervention responses, and which are blocked by missing or conflicting evidence?

## Steps 1–3 acceptance criteria

| Work item | Candidate milestone acceptance |
|---|---|
| Scope | Active README/protocol include all cytokines and broad immune mechanisms; no fixed panel count is an inclusion rule or completion metric. |
| Inventory | Save the actual all-cytokine resource query/results, provenance, expandable identity registry and annotation-status distinctions. Resource membership supplies no biological edge or numerical prior. |
| Corpus deepening | Document searches, candidate-level decisions, unique-paper/cohort relationships, original/correction links, primary Methods/Results access and contrary observations for each mechanism dossier. State retrieval limits explicitly. |
| Genetic regulation | Prepare at least one source-linked genetic/regulatory mechanism dossier spanning multiple measured layers; preserve unproven RNA-to-protein connections as blocked or branched. |
| Activation | Prepare source-linked receptor/signaling/transcriptional-program and measured protein/function dossiers beyond cytokine-label lookup. |
| Antigen presentation | Prepare source-linked processing/presentation and immune-recognition dossiers, preserving human versus nonhuman recipient and primary versus engineered-cell distinctions. |
| Integration | Build typed candidate entities, assertions, bridges and mechanism graphs with exact source dependencies; test invalid joins, nulls, species/context mismatch and layer changes. |
| Review boundary | Every new record remains pending review; accepted Release 0.2.0 evidence/priors stay intact. Export a review packet and specific unresolved questions, without starting review. |

These are evidence-processing acceptance criteria, not a required number of positive pathways. A missing transition must remain visible. A shared intervention with RNA and protein endpoints can be a useful response profile without establishing that one endpoint mediated the other.

## Later work, after the requested review

Human/independent adjudication of the candidate, broader systematic corpus completion, empirical calibration, quantitative effect/time/transport distributions, and model-facing validation remain later steps. The current candidate must not label heuristic scores or graph reachability as calibrated biological probability.
