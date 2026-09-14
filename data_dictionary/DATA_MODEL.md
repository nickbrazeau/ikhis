# Data model and interpretation

The dictionary is an inventory of evidence artifacts, biological-data routes and observed schemas. The current release binds source metadata to 14 September 2026. A record can be complete as a catalog entry while its biological files, units or participant mapping remain unavailable.

## Identity and grain

| Table group | One row represents | Identity / safe join |
|---|---|---|
| `datasets` | A catalog record in one collection | `dataset_id`; namespace prefixes `HR:`, `FLU:`, `ATLAS_DATA:` |
| `atlas_files` | One local file at one path | `file_id`; `sha256` links identical content across copies |
| `atlas_assets` | Distinct byte content | `asset_id`; identical bytes do not establish independent scientific evidence |
| `atlas_sources`, `atlas_source_coverage` | A baseline or candidate source registration | `source_key` includes release scope; repeated DOI/source identities remain explicit |
| `atlas_datasets` | One explicitly recorded original accession | `accession`; original cohort-field caveats remain attached |
| `atlas_accession_mentions` | An accession found in a documentary file | `accession` + `source_file`; discovery only, never an automatic data link |
| `atlas_tables`, `atlas_fields` | A current candidate database table / column | `table_id`, then `field`; baseline tables are preserved within this database |
| `hr_studies` | One author-defined study or cohort | `study_ID`; one GEO series can produce multiple cohorts |
| `hr_files` | One file in the pinned HF tree | `file_id`; `study_ID` only for an exact label; candidate split-cohort mappings are separate |
| `hr_table_profiles`, `hr_fields` | An inspected CSV table / literal column | `table_id`, then `literal_header`; no source typo silently corrected |
| `hr_gene_features` | One author common bulk feature position | `column_position_1based`; label not independently normalized |
| `hr_join_checks` | A literal subject-ID comparison | Within-study IDs only; missing metadata and unmatched IDs have different statuses |
| `hr_count_checks` | One author count versus observed table count | `study_ID` + `measure`; absent IDs cannot be used to infer zero participants |
| `influenza_studies` | An accession, modality, publication or reanalysis record | `id`; this is not an independent trial or participant count |
| `influenza_files` | An advertised file, archive, run or access route | `file_id`; `dataset_id` references `datasets`; landing pages are labeled separately from direct downloads |
| `viral_sequence_runs` | One public SRA run identifier | `run_accession`; experiment, project and study accessions are separate |
| `relationships` | A retained source relationship | Endpoints may be catalog IDs, original accessions or unresolved source statements; not all are foreign keys |
| `source_provenance` | One evidence-to-source binding | `source_id`, `snapshot_path`, `sha256`; same snapshot may support several records |
| `open_gaps` | A concrete unresolved inventory or interpretation issue | `gap_id`; unknown is preserved until evidence resolves it |

CSV and JSON exports preserve lists/objects; SQLite encodes them as JSON in TEXT columns. Numeric counts use numeric columns where observed. `catalog_columns` is a structural column inventory, not a substitute for scientific variable definitions. Detailed influenza source records and HR object schemas preserve source statements, uncertainty and locators.

## Data levels

| Level | Meaning | Examples / boundaries |
|---|---|---|
| Instrument/read data | Earliest deposited instrument-level observations or sequence reads | CEL, IDAT, FASTQ, FCS, mass-spectrometer files; format alone is insufficient without inspection |
| Submitter measurement exports | Author-provided measured or unnormalized feature tables | Unnormalized array intensities, antibody titers; not necessarily instrument output |
| Quantified or normalized data | Derived numerical measurements | Gene counts, CPM, RMA/QN arrays, Olink NPX; units and processing are dataset-specific |
| Harmonized data | Measurements transformed to a common schema | HR bulk matrices, combined single-cell objects; H5AD `.X` scale needs inspection |
| Derived outcomes | Calculated responses and analysis inputs | MFC, responder flags, model inputs, atlas assertions and priors |
| Metadata | Descriptions and identifiers | Subject/sample characteristics, assay annotations, accession tables |
| Documentary input | Evidence documents and repository responses | Articles, extracted full text, search snapshots, provenance records |

Archives are containers and can mix levels. The word `RAW` in a filename does not establish the level of every member. Original instrument files and unnormalized gene-count matrices are different representations. A primary paper's public-data statement is distinct from an inspected repository listing, and both are distinct from inspected file contents.

## Availability and verification

`raw_access_status` and source `raw_data.availability` summarize access with accompanying evidence. Values include `public`, `controlled`, `request_only`, `request_window_not_yet_open`, and `unverified`. The unified table exposes a future request window as not yet open while retaining the full original request terms in `influenza_studies`. Atlas access-route labels do not assert raw-file verification. HR's legacy `raw_data` yes/no flag is preserved as an author field and is never converted to public raw availability.

`access_url_kind` distinguishes direct file links from repository or paper landing pages. `verification`, `schema_inspection`, `content_inspection`, source locators and source hashes state what was actually checked. A complete repository run manifest still does not establish a complete sample-to-participant map, file download, raw-read quality or correspondence to one original paper.

`local_biological_payload` is false for influenza remote access entries. Local HR metadata and antibody snapshots are separately identified. The atlas inventory's documentary snapshots and curated tables must not be described as downloaded raw participant measurements.

## Subject, sample and assay joins

Participant keys are `(study_ID, ID)`. Sample keys are `(study_ID, source_row_identifier)` using the original row label or repository sample ID. Repeated observations per person are expected. Qualify visit, challenge episode, tissue, assay and antigen before joining measurement columns. A bare `ID` can collide across cohorts. Metadata-to-expression joins are author-described but not independently checked against the full matrices in this release.

GSE73072 contains influenza, rhinovirus and RSV cohorts; only the four named influenza arms qualify here. GSE17156 and GSE52428 also need subgroup restrictions. Multiple deposits or modalities from the same participants remain related records until an exact crosswalk is available. The HR README explicitly reports overlap among GSE17156, GSE30550, GSE52428 and GSE73072. Neither catalog records, sequencing runs, arrays nor cells should be summed as independent people.

Five HR antibody tables lack a directly corresponding inspected metadata table under the same label: some require a parent/split-cohort mapping, some refer to single-cell objects, and SDY312/SDY314 have no corresponding row in the current 66-row study table. These files remain in the complete file listing. The dictionary does not invent matches.

## Values, units and missingness

Source text is preserved before numeric interpretation. Blank, `NA`, `N/A`, `NaN`, `nan`, `<NA>`, `null`, `None`, `unavailable` and `unknown` are treated as explicit unavailable markers for profiling, not zeros. The original bytes and literal headers remain available. Missingness reasons are not uniform across studies.

`observed_storage_type` describes values in the inspected table; it is not a biological data type. `distinct_nonmissing_values`, `nonmissing_rows` and `missing_rows` are descriptive counts. Missing IDs make participant counts unassessable. No phenotype absence is inferred from a missing field.

Variable definitions come from the author's dictionary or explicitly labeled schema interpretation. Original field spellings such as `turbo_reatment` remain literal. Assay units, antigen/strain identifiers, LOD/LLOQ, censoring, baseline choice, response thresholds and exact time origins require source-specific documentation. Numeric antibody column suffixes are not universally visit days. Pooled visits can use representative times such as 31.5 for `d28+d35`.

## Eligibility and completeness

The target includes deliberate human influenza challenge, including challenge arms following vaccination, interventions or ex vivo assays on samples collected during challenge. Vaccine-only studies, natural infection, pneumococcal challenge after influenza vaccination, other pathogens and animal studies do not qualify merely because influenza appears in a label.

The atlas file inventory and version-pinned HF file listing are complete within their stated exclusions. Original atlas data availability remains unresolved for many papers, and the influenza discovery catalog is not yet an exhaustive census. Query text, automatic term expansion, result caps, title decisions, targeted followups and negative-search limitations are retained. Catalog completeness is assessed separately from scientific review; this work does not approve candidate atlas assertions.
