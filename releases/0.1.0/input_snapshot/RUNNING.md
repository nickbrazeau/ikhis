# Working with the immune evidence knowledge base

Start with [the research synthesis](reports/RESEARCH_SYNTHESIS.md), [the project checklist](reports/PROJECT_STATUS.md), and [the evidence atlas](releases/0.1.0/EVIDENCE_ATLAS.md).

Release 0.1.0 is a local, bounded initial release. It is not a completed whole-immune-system systematic review. Numerical priors are explicitly uncalibrated; human adjudication remains pending. The original README governs biological scope. No external hosting, manuscript submission or registry registration has occurred.

## Files

| Artifact | Purpose |
|---|---|
| `protocol/PROTOCOL.md` | Search, extraction, grading, adjudication, prior and release rules |
| `research/*/pack.json` | Authoritative frozen lane extractions |
| `research/*/snapshots/` | Actual retrieved primary-source text, metadata or tool responses |
| `research/references/` | Priority protein identity snapshots, anchor-resource registry and PubMed discovery index |
| `research/review_*.json` | Immutable independent critic findings |
| `research/*/review_response.json` | Lane corrections with original/revised hashes |
| `provenance/adjudications.json` | Coordinator dispositions; not human approval |
| `data/scoring_annotations.json` | Explicit hypotheses and evidence relations used for weighting |
| `releases/0.1.0/immune_prior.sqlite` | Queryable normalized knowledge base |
| `releases/0.1.0/*.csv` | Every normalized table, including intentionally empty domains |
| `releases/0.1.0/qc.json` | Structural checks, counts and scientific limitations |
| `releases/0.1.0/manifest.json` | SHA-256 inventory of inputs and release artifacts |
| `data/DATA_DICTIONARY.md` | Table and field definitions |

## Reproduce and inspect

Python 3.9 or later is sufficient for the compiler, tests and query commands. The frozen release requires no network access and no external packages.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/kb.py build
python3 scripts/kb.py freeze
python3 scripts/kb.py verify
python3 scripts/kb.py query --entity IL7R
```

`build` intentionally recreates only the generated SQLite database and table exports under Release 0.1.0. It does not modify evidence packs or primary snapshots. A build must succeed before freezing. `freeze` rejects inputs changed since the build; `verify` checks every recorded digest. A subsequent biological revision should be assigned a new release after reviewing its evidence/prior changes; this initial compiler targets 0.1.0 explicitly and is not an automatic release-version manager.

The assertions can also be inspected directly in SQLite:

```sql
SELECT a.assertion_id, s.name AS subject, a.predicate, o.name AS object,
       a.measurement, a.direction, a.evidence_tier, a.status,
       c.species, c.cell_type, c.stimulation, c.time_point,
       e.source_locator, e.evidence_summary, src.url
FROM edge_assertions a
JOIN entities s ON s.entity_id = a.subject_id
JOIN entities o ON o.entity_id = a.object_id
JOIN contexts c USING (context_id)
JOIN evidence_instances e USING (assertion_id)
JOIN source_registry src USING (source_id)
WHERE s.name LIKE '%IL7R%' OR o.name LIKE '%IL7R%';
```

## Add evidence

Follow `research/EXTRACTION_CONTRACT.md`; preserve original species, cohort, molecular measurement and context. Add an actual supporting snapshot with a locator. Do not derive new edges solely from resource membership or search results. Assign immutable assertion/source/cohort IDs and preserve negative results as observations.

Run an independent critic over changed evidence. Preserve the original finding record, record the repair separately, and disposition it in `provenance/adjudications.json`. Open high-severity assertion/source/cohort/context findings quarantine dependent evidence. Open high-severity protocol/compiler findings fail conservatively by withholding numerical priors pending repair. A separate future implementation gate can narrow that compiler-wide hold when its dependency semantics are validated.

Explicitly annotate the tested hypothesis and whether evidence supports, opposes or is inconclusive for it. `scripts/annotate_scoring.py` reproduces the reviewed initial ID set; new IDs are unannotated until deliberately reviewed. It is not an automatic polarity classifier. Nulls need justified absence evidence before they can oppose an existence hypothesis. Missing magnitude and transportability distributions remain unavailable.

The current compiler does not ingest externally asserted pathway bridges. All candidate joins fail closed. Future bridge ingestion requires source-backed temporal, measurement and context validation, plus independent review. This prevents a configuration flag from creating a purported mechanistic path.

## Refresh discovery sources

The optional retrieval script calls the installed life-science helpers and uses the host HTTP client as a documented fallback for failed TLS transport. It requires network permission and the `requests` dependency in a local environment. Its helper locations are host-specific; adjust `SKILLS` and `SKILL_PYTHON` when moving to another host. No dependency is needed to consume the frozen release.

```sh
python3 -m venv .venv
.venv/bin/python3 -m pip install -r requirements-research.txt
python3 scripts/retrieve_references.py
```

The script reuses cached successful snapshots and retries missing ones. It is a resumable initial-discovery fetch, not a fresh systematic search update. For a new dated search, use a new output directory and preserve the previous snapshot corpus. PubMed queries are capped at ten relevance-ranked IDs each; `total_hits` and `returned_pmids` have different meanings. The returned IDs are not automatically screened, extracted or scored.

## Interpretation notes

`related_assertion_count` includes matching entity names in any layer or review state. `reviewed_protein_assertion_count` counts reviewed assertions involving the protein as subject or object, including ligand interventions; it is not a count of direct assay-analyte measurements or independent causal experiments. Assay-platform identity is still required before using any of these as measured-panel coverage.

`independent_groups` in the initial prior interface counts capped effective evidence groups, including a conservatively pooled unresolved group. It does not certify independent replication. Check the cohort registry and scientific limitations before use. `unavailable` is an explicit unknown; an empty table is a coverage gap. SQL NULL denotes an absent relational object or numeric parameter, never a fabricated reference.
