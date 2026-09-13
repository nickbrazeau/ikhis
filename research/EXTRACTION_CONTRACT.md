# Evidence extraction contract, version 0.1.0

Read README.md as the governing specification. Research external sources read-only. Write only inside your assigned research directory. Never manufacture missing metadata, numeric effects, quotes, sample sizes, impact factors or causal claims. Unknowns use the literal `unavailable`. Date/time must come from the runtime clock. Human and nonhuman evidence are separate. Save retrieved source content or source-tool responses that actually support extraction in your directory; identify whether a snapshot is full text, abstract, metadata, or search excerpt. Do not call a search excerpt a full-text review.

Deliver `pack.json` with keys `sources`, `cohorts`, `assertions`, `searches`, `gaps`, and `synthesis` (a concise research narrative). IDs must use your lane prefix (C, G, P). Include 6–10 carefully selected primary publications/resources per lane, including recent anchors and seminal causal or observational contrasts; seek null/contradictory evidence. More evidence is welcome only with adequate extraction fidelity. A source is not an assertion. Focus on directly extractable, narrow results and avoid extrapolating atlas-level coverage into molecule-specific edges.

## Source object
`source_id`, `title`, `authors`, `year`, `url`, `doi`, `pmid`, `source_type` (primary_study, resource, review, preprint), `version`, `retrieved_at`, `access_level`, `snapshot_path`, `species`, `notes`.

## Cohort object
`cohort_id`, `dataset_id`, `accession`, `study_id`, `participants`, `ancestry`, `species`, `tissue`, `cell_type`, `disease`, `intervention`, `sample_count`, `donor_count`, `parent_cohort`, `related_publications`, `independence_status` (resolved or unresolved), `notes`. Lists may be arrays; other fields strings or numbers.

## Assertion object
`assertion_id`, `subject` (canonical name), `subject_type`, `predicate`, `object` (canonical name), `object_type`, `subject_layer` and `object_layer` (G,T,P,C,F), `measurement` (association, RNA_abundance, splicing, direct_transcriptional_regulation, protein_abundance, secreted_protein, protein_activity, receptor_signaling, cellular_phenotype, inferred_communication), `evidence_tier` (G1–G4 or P0–P4 or observational or perturbational), `direction` (increase, decrease, mixed, null, association, binding), `source_id`, `cohort_id`, `source_locator` (figure/table/section or abstract sentence), `evidence_summary` (paraphrase; narrow and source-faithful), `species`, `ancestry`, `age`, `sex`, `tissue`, `disease`, `disease_severity`, `treatment_status`, `cell_type`, `cell_state`, `developmental_state`, `stimulation`, `dose`, `duration`, `assay`, `genomic_background`, `time_point`, `effect_size`, `effect_unit`, `uncertainty`, `causal_directness`, `limitations`, `contradiction_group`, `candidate_path`, `qc_status` (reviewed_extraction or needs_full_text), `qualitative_confidence` (low or moderate; high only unusually well justified). Unknown fields use `unavailable`. A cohort independence group must not be asserted resolved without inspection. Candidate paths are suggestions for compatibility checking, never direct path proof.

## Search object
`search_id`, `lane`, `query`, `database`, `searched_at`, `result_source_ids`, `screening_notes`. Log real queries only. Record searches and sources not yielding extractable results. Distinguish a bounded pilot corpus from an exhaustive systematic review. Do not claim human adjudication or scientific calibration of heuristic probabilities.

Write a readable `notes.md` with findings and remaining gaps. Source hashes will be computed centrally from the saved snapshots. Each agent must retain its role, actual start/end, known model (otherwise unavailable), and instruction versions in `run.json`.
