# IKHIS data dictionary

**[Browse the searchable catalog](reports/catalog.html)** · **[Read the coverage report](reports/DATA_DICTIONARY.md)** · [Data model and interpretation](DATA_MODEL.md)

Version 0.1.0, checked 14 September 2026. The inventory covers 2,059 atlas files, all 66 study/cohort rows and 175 files in the pinned HR-VILAGE release, and 30 influenza-related catalog records (26 eligible challenge-related records and four adjacent exclusions). It includes 278 public viral-sequencing run identifiers. These are data records, not independent-cohort counts. Influenza discovery remains expandable; complete global coverage is not claimed.

This sibling project inventories the data behind the [immune evidence atlas](../atlas/README.md) and the original data available for human influenza challenge studies, building on HR-VILAGE-3K3M.

The dictionary distinguishes instrument-level raw data, author-provided expression/count tables, harmonized matrices, clinical/virological/antibody measurements, metadata, literature snapshots, and derived atlas assertions. A locally saved article is a source artifact; it is not a downloaded biological measurement dataset.

The research scope includes controlled human influenza inoculation and challenge arms of mixed vaccination/challenge studies. Vaccine-only studies, natural infection, other respiratory viruses and nonhuman experiments are labelled separately. Dataset and publication counts are not independent-cohort counts.

HR-VILAGE's current V3 release no longer redistributes its former raw-expression folder. Its `study_citations.csv` links all source studies to their original repositories. Source availability, formats, accession relationships, join keys, time references, missing values and provenance are recorded explicitly. Controlled or request-only availability is not represented as a public download.

The atlas's existing scientific review boundary remains intact. This project catalogs data availability and definitions; it does not approve biological assertions or calculate new priors.

## Use the dictionary

Open the searchable HTML catalog locally; it works without a server or network requests. Filter by collection or influenza eligibility, then follow the original repository links. Each catalog table also has CSV and JSON exports under `catalog/`.

| Need | Artifact |
|---|---|
| Search all study/data records | [Catalog](reports/catalog.html), [CSV](catalog/datasets.csv) |
| Original influenza data and restrictions | [Study records](catalog/influenza_studies.json), [file/access entries](catalog/influenza_files.csv), [viral run manifest](catalog/viral_sequence_runs.csv) |
| Every atlas file, with duplicate copies separated | [File inventory](catalog/atlas_files.csv), [distinct assets](catalog/atlas_assets.csv) |
| Atlas sources and original data routes, including gaps | [Source coverage](catalog/atlas_source_coverage.csv), [explicit dataset accessions](catalog/atlas_datasets.json) |
| HR studies, original citations and current file listing | [Studies](catalog/hr_studies.csv), [files](catalog/hr_files.csv) |
| Field definitions and table structure | [HR fields](catalog/hr_fields.csv), [HR object schemas](catalog/hr_schema.json), [atlas fields](catalog/atlas_fields.csv), [atlas table schemas](catalog/atlas_tables.json) |
| Processing and numeric interpretation | [Transformation audit](catalog/hr_transformations.json), [common feature labels](catalog/hr_gene_features.csv) |
| Joins and author-count discrepancies | [Subject join checks](catalog/hr_join_checks.csv), [count checks](catalog/hr_count_checks.csv), [table profiles](catalog/hr_table_profiles.json) |
| Evidence and search coverage | [Source provenance](catalog/source_provenance.json), [search log](catalog/search_log.json), [screening decisions](catalog/geo_screening.json) |
| Remaining data acquisition/mapping work | [Open gaps](catalog/open_gaps.csv) |
| Query everything locally | [SQLite database](catalog/data_dictionary.sqlite), [column inventory](catalog/catalog_columns.csv) |

The 99 directly inspected HR CSV tables provide 3,668 field entries. Many remote archives, instrument files, supplementary workbooks and single-cell layers are identified but not inspected at field level. Missing definitions, units, archive members and subject crosswalks are explicit acquisition gaps. The 41,667 common feature labels come from the author's schema list; they do not establish gene ontology validity or protein measurements.

## Reproduce and verify

Run from the IKHIS root. The compiler uses the Python standard library and local snapshots; it makes no network calls.

```bash
.venv/bin/python data_dictionary/scripts/build_dictionary.py build
.venv/bin/python data_dictionary/scripts/build_dictionary.py verify
.venv/bin/python -m unittest discover -s data_dictionary/tests -v
```

`provenance/build_manifest.json` binds the inputs and outputs with SHA-256 hashes. `provenance/atlas_migration.json` records the 2,751 original moved files, including an old embedded environment excluded from the data inventory. [Subsequent security maintenance](provenance/post_migration_changes.json) records later changes without rewriting that original receipt. Verification detects changed source/output bytes and changes to the atlas file inventory. Dictionary regeneration does not change any atlas input, frozen release or candidate file.

The public-metadata fetcher uses request manifests, bounded responses and credential redaction. It stores requested canonical URLs and selected metadata, never signed redirect URLs, cookies or authorization headers. It does not execute repository code or download large biological matrices by default. The original snapshot and curation files remain under `sources/` for audit.

## Version and scope controls

- HR-VILAGE dataset commit: `c68349578b97af04d1102eac5ad9f30f85362c53`; author code commit: `716c27dccba847875f85be63103e2245acaa3320`; paper: arXiv `2505.14725v2`.
- HR V3 and the paper differ about redistributed raw files. The [documentation audit](sources/hr_vilage_audit/notes.md) records that change, schema differences and processing caveats.
- The [influenza source notes](sources/influenza/notes.md) describe searches, eligibility, shared cohorts, current versus original SRA run coverage and remaining repository gaps.
- Catalog curation is pending review. Public availability does not imply unrestricted reuse: the original repository's data terms and any participant-data agreement apply. No access requests or messages were sent to study authors.
