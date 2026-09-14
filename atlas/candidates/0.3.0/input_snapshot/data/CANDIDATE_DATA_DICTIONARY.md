# Candidate supplement dictionary

Version 0.3.0 candidate. Every new scientific record awaits independent and human review. Resource annotations labelled `reviewed` refer to UniProt curation, not project review.

The database preserves every baseline table and record from Release 0.2.0. New biological evidence is stored only in the tables below. No new candidate record enters `edge_assertions`, `evidence_instances`, `prior_parameters` or `materialized_paths`.

| Table | Meaning and important fields |
|---|---|
| candidate_entities | Exact source-level molecular identity: name, type, layer and species. Stable local IDs do not imply ontology verification. RNA, protein, phospho-state, splice event, complex and intervention remain distinct. |
| candidate_contexts | Species, preparation-related tissue/cell fields, state, disease, stimulation, dose, duration, assay, genomic background and time. The complete source-specific preparation and donor caveats remain in assertion/cohort payloads. |
| candidate_sources | Primary source identity, DOI/URL, access level and exact dependency hashes. `baseline_source_ids` identifies matching DOIs in the preserved corpus; those are not new independent publications. `payload` retains original extraction metadata, related historical source IDs and additional source files. |
| candidate_cohorts | Study-specific cohort or experimental context; `payload` retains donor/sample counts, overlap, preparation and independence limitations. A context count is not a count of independent cohorts. |
| candidate_assertions | Subject/predicate/object, context/source/cohort links, measurement, direction, pending status, source locator, summary and limitations. `payload` retains every original field, including reported quantitative results and proposed historical corrections. |
| candidate_bridges | Explicit proposed connection, endpoints, relation, type, source hashes, structural classification and reasons. `payload` contains six extractor check attestations, experimental linkage, temporal basis and context comparison. `production_approved` is constrained to zero. |
| candidate_graphs | Dossiers grouping measured assertion edges and separately typed connection proposals. `serial_transitions` contains only structurally eligible pending serial proposals. Mediation tests, branches and contrasts do not become serial transitions. Approved production paths are always empty. |
| candidate_searches | Exact query or documented query batch, provider, date and retrieval caveats. Failed queries remain visible and do not imply screened results. |
| candidate_screening | Candidate appearances, query link, include/exclude/await-full-text decision and reason. Repeated appearances are not unique publications or replications. |
| candidate_gaps | Missing source details, unresolved transitions and context-specific limitations. |
| cytokine_inventory | Expandable human cytokine-annotation discovery records, accession, symbol, reviewed/unreviewed resource status, query and snapshot hash. No biological assertion or prior is created by membership. |
| candidate_inputs | Exact SHA-256 digest of each declared build input. |
| candidate_metadata | Review boundary, baseline digest, before/after record fingerprints and scope. |

Layers are G (genetic/regulatory/chromatin), T (transcript/splicing), P (protein/complex/activity), C (cellular communication/stimulation), and F (measured cellular function/phenotype). An intervention's assigned layer is a representation of what was manipulated, not evidence that every intervening biological step was measured. Measurement names retain their biological meaning, including chromatin accessibility and TF occupancy. An extracellular protein measurement alone does not identify its cellular source or prove a secretion mechanism.

Connection types are `serial_transition`, `mediation_test`, `shared_intervention` and `context_contrast`. Structural classifications are `mechanism_proposal`, `response_profile`, `context_contrast` and `blocked_connection`. A mechanism proposal is ready for scientific scrutiny; it is not validated mediation or an approved causal pathway. Positive extractor attestations are unreviewed inputs, never independent evidence.

Missing scientific information is `unavailable` in source records where explicitly recorded; omitted optional fields remain SQL NULL or absent in the original payload. Neither means a negative biological result. The candidate compiler does not calculate biological probabilities, effect distributions, confidence scores or transport weights.

All candidate tables have CSV exports. The input snapshot and input manifest preserve extraction records and code; the candidate artifact manifest binds outputs to exact bytes. Historical source archives are retained in Release 0.2.0 rather than duplicated in full inside the candidate.
