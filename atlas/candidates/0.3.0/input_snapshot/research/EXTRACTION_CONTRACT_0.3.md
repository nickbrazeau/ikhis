# Mechanism candidate extraction contract, 0.3.0

The user authorized steps 1–3: define a usable scientific scope, deepen and systematically screen evidence, and assemble supported biological connections. The user will trigger independent review afterward. Do not initiate a critic review, mark new material reviewed, construct numerical priors, or freeze a production release in this phase. All cytokines are in scope. The former fixed cytokine priority set has been removed from current scope; historical assay labels are provenance only. Broader immune mechanisms are equally in scope.

Research external sources read-only. Write only in the assigned new `research/mechanisms_*/` directory. Existing packs, reviews and frozen releases are read-only. Follow the molecular-layer, source-fidelity, cohort and null-evidence principles in the original extraction contract. Unknown is `unavailable`. Record real query strings, dates, accessed Methods/Results and failed attempts. Prefer primary articles; reviews are discovery only. Preserve supporting snapshots as concise source extracts or source-tool output with exact locators and access level. Remove signed-download credentials before saving. Avoid long CUA calls: their timeouts have failed; use web/publisher/primary-PDF routes and do not stall on one access path.

## Research deliverables

- `pack.json`: sources, cohorts, assertions, searches, gaps, synthesis, using the original pack structure and lane-specific immutable IDs.
- `screening.json`: candidate_id, query_id, title, url, doi, pmid, decision (include/exclude/await_full_text), reason. Distinguish candidate appearances and unique papers. Record citation chains and corrections/retractions checked. Do not claim exhaustive retrieval when using ranked searches.
- `bridges.json`: explicit connection proposals described below; no cross-paper connection based only on shared names.
- `notes.md`: what was checked, main findings, conflicts, unavailable information, proposed mechanisms and the most consequential remaining gaps.
- `run.json`: actual runtime dates, extraction role, known model/instruction/source metadata; independent and human review are pending.

New assertions use `qc_status: extracted_pending_review` when the relevant primary Methods and Results have been inspected, otherwise `needs_full_text`. They may include qualitative confidence, source-reported quantitative_result and an explicit tested hypothesis/evidence relation, but no calibrated probability. Numerical results are observations only. A new narrower assertion based on an inherited source must identify its related original assertion; do not alter the old record or count it as independent replication.

## Connection proposals

Aim for small, well-supported two- or three-step mechanisms within an explicit experimental context. Do not force a complete chain. Each bridge record includes:

```
bridge_id, mechanism_id, from_assertion_id, to_assertion_id,
bridge_type, bridge_relation, source_ids, source_locators,
supporting_snapshot_paths, evidence_summary,
entity_mapping, context_comparison, temporal_basis,
measurement_basis, experimental_linkage, limitations,
status
```

`bridge_type` is `serial_transition`, `mediation_test`, `shared_intervention`, or `context_contrast`. `bridge_relation` is `supports`, `opposes`, or `inconclusive`. Status is always `candidate_pending_review` or `blocked_missing_evidence` in this phase.

- A serial transition requires evidence linking the left outcome to the right input, with the same molecular species/state. Distinct RNA and protein measurements require an explicit translation/isoform bridge; a name match is insufficient.
- A mediation test requires a relevant perturbation of the proposed intermediate and a measured downstream endpoint. It may support a narrow mediated mechanism without demonstrating direct biochemical binding or every unmeasured intermediate. Record inhibitor specificity, off-target and rescue limitations.
- Two outcomes under a shared intervention are a branched response profile, not a serial mechanism. A context contrast is not a serial pathway.
- Context comparison must separately state species, biological preparation, cell identity/state, tissue, stimulation/dose, time and cohort linkage for both experiments. Same-paper experiments are not automatically the same donors. Unknown cross-cohort transport is not equivalence.
- Temporal basis distinguishes measured ordering, documented experimental scheduling and ordering merely assumed from biological convention.
- Experimental linkage identifies same samples, same preparation/protocol but donor overlap unavailable, directly tested transfer/conditioned medium, or separate-study synthesis. Each claim needs a primary source locator.
- No source cell is inferred from plasma protein; no secretion from RNA; no function from expression; no human pathway from a mouse host expressing a human receptor.

Search for contrary/null/context-dependent observations and preserve them. Document when a proposed mechanism is blocked. A well-supported branched response or a precisely documented missing connection is preferable to a fabricated serial chain.
