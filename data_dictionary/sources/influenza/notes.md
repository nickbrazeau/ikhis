# Human influenza challenge catalogue

Prepared 2026-09-14. This lane contributes 30 accession or publication-level data records: 26 eligible challenge-related records and four explicit adjacent exclusions. These are **not 26 independent studies**: several accessions describe different modalities or reanalyses of the same participants. The root data dictionary combines this lane with the separately pinned HR-VILAGE source inventory.

## Search coverage

The exact GEO Entrez query, including its automatic vocabulary expansion, returned 200 series. The first 10 identifiers were followed by all 200 identifiers, then summaries. All 200 titles were screened; not every unselected title underwent full summary or primary-paper screening. Two explicit known leads were appended to the summary retrieval, giving 202 title-screening rows. GSE73072 itself was missed by the broad search, and GSE253685/GSE253686 were recovered only by citation chasing. Therefore this is a documented, expandable catalogue, **not a claim that every existing human influenza challenge dataset has been found**.

Thirty search or lookup records are in `searches.json`. Ranked web results were used for discovery across host and viral sequencing, antibody/repertoire, proteomics, cytokines, cytometry and metabolomics. Primary repositories and original articles support inclusion and data-availability conclusions. Secondary aggregators were discovery leads only. Negative search results do not establish absence of available data.

An accession-specific SRA lookup returned 265 experiment records. All experiment summaries were retrieved; they identify 278 distinct public runs: 258 in SRP091397 and 20 in SRP189350 / PRJNA528931. The 2016 SRP091397 primary paper specifically names only SRR4416113–SRR4416125; subsequent repository additions are retained but must not be attributed to that paper's original 13-run analysis. `viral_sequence_runs.json` is a run-level manifest, not a subject list. Challenge participants, inoculum, passage controls, natural infection and technical/amplicon replicates still require exact sample-level assignment.

## Scope decisions

- GSE73072 contains four eligible influenza arms (H3N2 DEE2, H1N1 DEE3, H1N1 DEE4, H3N2 DEE5): 81 participant assignments and 1,700 arrays within the repository's 148-subject / 2,886-array mixed-virus series. RSV and rhinovirus arms are separate. These numbers do not deduplicate participants against older Duke accessions.
- GSE17156 also mixes influenza, RSV and rhinovirus. GSE52428 mixes deliberate challenge with natural respiratory illness validation.
- GSE61754 includes vaccinated and unvaccinated volunteers who were all challenged; vaccination status remains an analysis covariate.
- GSE111368 (MOSAIC) and GSE68310 are natural infection cohorts. GSE194378 is influenza vaccination after prior COVID-19. GSE117580 is LAIV/TIV vaccination followed by pneumococcal challenge, not wild-type influenza challenge. These are retained as adjacent exclusions, including the ambiguous HR-VILAGE rows.
- E-MTAB-15137 contains blood collected during human influenza challenge and then infected with BCG **ex vivo**. It does not describe human BCG inoculation.

## Meaning of raw and available

Each record distinguishes raw measurement availability from processed data and from catalogue metadata. Public declarations are marked with the level actually verified. A publicly listed accession is not proof that every clinical measurement or original instrument file is downloadable.

- Affymetrix CEL and Illumina IDAT files, where declared in GEO, are instrument-level array measurements. GEO RAW archives may also contain submitter-exported unnormalized feature tables, so archive members need inspection before assigning a more precise level.
- A file named `Raw_gene_counts_matrix` or an unlogged count table remains a derived sequencing count matrix, not FASTQ reads. GSE299820 has a separately verified representative SRA experiment; the GSE175551 representative sample lacks an experiment/run link despite being labelled SRA, so its raw reads remain unresolved.
- EGA raw sequencing is controlled access. No controlled data or access applications were submitted.
- FlowRepository FR-FCM-Z2NZ is declared public by the primary JCI paper. Its certificate was expired during direct retrieval; current file inventory and deposited raw/normalized FCS status remain unverified. This is a transport limitation, not evidence that the dataset is unavailable.
- The 2021 oral-vaccine/challenge mass-cytometry paper explicitly offers raw data on reasonable request. Public XLSX supplements are not a substitute for raw FCS.
- The 2026 Imperial multimodal study restricts participant-data requests to individual-participant meta-analysis, from 12 months until five years after its 2026-07-01 publication. That request window begins 2027-07-01; it is not currently open. Blood RNA is separately available under managed EGA access, and nasal counts are public.
- Walters 2025 Olink NPX values are normalized protein expression, not absolute concentrations or original instrument outputs. Its immuneACCESS landing page was retrieved, but original read files versus processed clonotype tables remain to be enumerated.
- Nasal-lavage mass spectrometry (Burke 2017) and serum 25-plex cytokines (McClain 2016) are verified challenge measurements with unresolved complete raw-data deposits. They remain visible gaps instead of being silently excluded.

## Remaining data-inventory work

Expand GEO archive members, SDRF sample relationships, immuneACCESS exports and paper supplementary workbooks into field-level entries; resolve original cytometry/proteomics/cytokine files; verify the complete GSE175551 raw-read route; locate the single-cell RNA/ATAC/methylation data reported by the 2025 GSE299820-linked multiomics paper; extend repository-level searches for human challenge metabolomics, viral genomes and interventional challenge trials. Preserve trial, participant, arm, specimen, timepoint and assay identifiers so reused cohorts cannot inflate apparent sample size.

No large raw matrices, FASTQ/SRA reads, instrument files, or controlled participant data were downloaded. Saved files are repository metadata and primary-article evidence snapshots. No signed credential URLs were retained. Only `data_dictionary/sources/influenza/` was modified by this lane; the atlas was not changed or reviewed.

## Validation

All 30 catalogue IDs are unique, all declared source paths exist, and every source hash matched. All 278 run IDs are unique. A targeted scan found no AWS access-key IDs or signed AWS credential query parameters in this lane. Source-curation status remains pending review; resource-public status is not scientific review approval.

The source records can be regenerated offline in sequence with `build_records.py`, `add_extended_records.py`, and `add_final_records.py`, from the saved snapshots. The root project compiler is the intended user-facing entry point.

A final bounded catalogue consistency pass corrected the GSE68310 subject phenotype file to `clinical_subject_metadata`, separated `unnormalized_feature_intensity_table` exports from `raw_submitter_archive` containers, and made representative versus complete run metadata coverage explicit. The Imperial participant-data request is marked `currently_requestable: false` as of 2026-09-14. The three offline generators now preserve all PRJNA528931 cohort counts and keep search IDs unique on regeneration. All four catalogue outputs reproduced byte-for-byte and all primary snapshot hashes remained unchanged; see `consistency_check.json`.
