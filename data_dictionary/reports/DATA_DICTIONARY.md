# IKHIS data dictionary · 0.1.0

## Human checklist

Preparation is complete. Human review items remain unchecked until someone has completed and documented them.

**Completed preparation**

- [x] Move the existing project into `atlas/` and verify that its contents were preserved.
- [x] Build the initial data dictionary, searchable catalog, source links and downloadable inventories.
- [x] Check the data inventory, reproducibility, browser functionality and credential scan.

**For human review**

- [ ] Review the included influenza challenge records and the reasons for excluding adjacent studies.
- [ ] Confirm which original raw files are available; decide which controlled or request-only datasets to pursue.
- [ ] Review the open data gaps and assign an owner and next action to each follow-up being pursued.
- [ ] Resolve unmatched participant IDs and unexplained participant-count differences before combining data.
- [ ] Confirm specimen types, assay definitions, units, detection limits and sampling times in the original sources.
- [ ] Check which records reuse the same participants so people are not counted more than once.
- [ ] Record the review decision below, including any remaining limitations, before using the dictionary to assemble an analysis dataset.

Reviewer: _not yet assigned_  
Review date: _not yet reviewed_  
Decision and remaining limitations: _pending_

The atlas's separate scientific review remains pending.

[Update the human checklist](../HUMAN_CHECKLIST.md). Its checkboxes and review notes are preserved when the report is rebuilt.

---

Checked 14 September 2026. [Browse the catalog](catalog.html) · [Project guide](../README.md) · [Database](../catalog/data_dictionary.sqlite)

## What is covered

The local atlas inventory contains **2,059 files**, representing 724 distinct byte-identical assets after deduplication. It excludes Python environments, caches and operating-system files. The migration ledger separately binds all 2,751 moved files, including the old nested environment. Every atlas file has a path, content hash, format and storage/data classification. All 123 registered sources are accounted for, including 15 explicit cohort-data accessions; 55 primary-study/preprint records still have no explicit raw-data route in their cohort records. Those gaps are visible in the source-coverage table. Literature and repository snapshots are documentary inputs, not participant measurement files.

The pinned HR-VILAGE inventory covers **66 study/cohort rows and all 175 listed files**. All 59 bulk-study metadata tables and 37 antibody tables were inspected, together with three root metadata tables: 3,668 per-table field entries. The author common bulk feature list contains 41,667 labels; it is not an independently validated gene ontology. Full expression matrices and H5AD layers were not downloaded. Six HR rows are verified influenza challenge subsets; four belong to GSE73072, so these are three original GEO series, not six independent deposits.

The expanded influenza search contains **26 eligible challenge-related records**, four adjacent exclusions, and **278 public viral-sequencing run identifiers**. Records include accessions, modalities and reanalyses of shared trials. They are not a count of independent cohorts. The 258 current SRP091397 runs exceed the 13 named in the original 2016 paper; the run manifest preserves the expanded repository, with sample-level challenge/control assignment still required.

## Raw data and access

HR-VILAGE V3 (28 August 2026) removed `bulk_gene_expr_raw/`. Its May 2026 paper predates this change. The remaining legacy `raw_data` flags do not establish present-day raw-file availability. The [pinned dataset card](https://huggingface.co/datasets/xuejun72/HR-VILAGE-3K3M/blob/c68349578b97af04d1102eac5ad9f30f85362c53/README.md) and [study citations](../sources/hr_vilage/study_citations.csv) provide the current context and original repository routes.

Instrument files, submitter measurement tables, quantified counts, normalized expression, antibody measurements, derived outcomes and metadata are separate levels. A gene-count matrix is not a sequencing-read file. H5AD `.X` is not universally raw counts. Olink NPX is normalized protein expression, not absolute concentration. Antibody tables combine measurements with derived response fields.

Public access means the stated evidence supports a public route; each file records whether this was a repository listing, a primary-paper declaration or inspected table content. EGA requires managed access. The Imperial participant-data request window begins 1 July 2027 and is not currently open. A failed repository fetch does not establish data absence. File-level source evidence and restrictions remain in [influenza_studies.json](../catalog/influenza_studies.json).

## Influenza challenge records

| Record | Measurements / specimen | Raw access as checked | Source |
|---|---|---|---|
| GSE17156 | Expression profiling by array / whole blood | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17156) |
| GSE30550 | Expression profiling by array / whole blood | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE30550) |
| GSE52428 | Expression profiling by array / whole blood | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE52428) |
| GSE61754 | Expression profiling by array / whole blood | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE61754) |
| GSE73072 | Expression profiling by array / whole blood | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE73072) |
| GSE90732 | Expression profiling by array / whole blood | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE90732) |
| GSE118223 | Expression profiling by array / whole blood | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE118223) |
| GSE175551 | Expression profiling by high throughput sequencing / BAL and blood T cells (CD4/CD8 targeted) | unverified | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE175551) |
| GSE299820 | Expression profiling by high throughput sequencing / whole blood | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE299820) |
| E-MTAB-13038 | bulk RNA-seq / nasal scrape | unverified | [record](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-13038) |
| E-MTAB-13041 | bulk RNA-seq / whole blood | controlled | [record](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-13041) |
| EGAD50000000956 | bulk RNA-seq / whole blood | controlled | [record](https://ega-archive.org/datasets/EGAD50000000956) |
| FR-FCM-Z2NZ | mass cytometry; CBC; viral qRT-PCR; HA/stalk antibody ELISA; symptom scores / peripheral blood / nasopharyngeal swabs | public | [record](https://flowrepository.org/id/FR-FCM-Z2NZ) |
| MCILWAIN2021_CHALLENGE | mass cytometry; HAI; microneutralization; ELISPOT; viral qRT-PCR; Flu-PRO symptoms / whole blood; serum; nasopharyngeal swabs | request_only | [record](https://doi.org/10.1016/j.chom.2021.10.009) |
| BURKE2017_NPL | 2D-LC-MS/MS discovery proteomics; targeted MRM proteomics / nasopharyngeal lavage | unverified | [record](https://doi.org/10.1016/j.ebiom.2017.02.015) |
| FLU_DAY_PREDICTION2026 | mass cytometry derived cell populations; viral shedding; challenge day / whole blood | unverified | [record](https://doi.org/10.3389/fimmu.2026.1787198) |
| IMPERIAL_H3N2_MULTIMODAL2026 | flow cytometry; functional immune assays; antibody assays; viral qRT-PCR; symptom diaries; bulk RNA-seq / blood; nasal samples; respiratory immune samples | request_window_not_yet_open | [record](https://doi.org/10.1038/s41591-026-04483-7) |
| GSE253685 | expression microarray / PBMC | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253685) |
| GSE253686 | expression microarray / nasal epithelium | public | [record](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE253686) |
| KAW2025STM | BCR sequencing; TCR sequencing / blood immune repertoire | unverified | [record](https://doi.org/10.21417/KAW2025STM) |
| WALTERS2025_IMMUNE | Olink inflammation proteins; antibody HAI/neutralization; viral shedding; symptoms; BCR/TCR repertoire / nasal mucosa, blood and serum | unverified | [record](https://pmc.ncbi.nlm.nih.gov/articles/PMC12375958/) |
| SRP091397 | viral RNA sequencing / nasal wash and challenge-virus stock | public | [record](https://www.ncbi.nlm.nih.gov/sra?term=SRP091397) |
| PRJNA528931 | viral RNA sequencing / nasal wash and challenge-virus stock | public | [record](https://www.ncbi.nlm.nih.gov/sra?term=PRJNA528931) |
| E-MTAB-15137 | bulk RNA-seq; mycobacterial growth inhibition; cytokines; cellular assays / whole blood aliquots with/without ex vivo BCG lux | controlled | [record](https://www.ebi.ac.uk/biostudies/arrayexpress/studies/E-MTAB-15137) |
| EGAD50000002407 | bulk RNA-seq / whole blood aliquots with/without ex vivo BCG lux | controlled | [record](https://ega-archive.org/datasets/EGAD50000002407) |
| MCCLAIN2016_CYTOKINES | 25-plex cytokine assay; viral shedding; symptom scores / serum / peripheral blood | unverified | [record](https://pmc.ncbi.nlm.nih.gov/articles/PMC4750592/) |

## Joining and interpreting observations

Qualify participant IDs with `study_ID`. Repeated visits, tissues, assays and cells are not independent people. Join sample rows using preserved source row identifiers; subject-ID agreement does not establish antigen/visit alignment. Full metadata-to-expression row alignment still needs matrix inspection. All antibody subjects match the metadata in 24 tables; 8 tables have unmatched IDs; 5 require another mapping or metadata inspection. Of the author counts compared with inspected tables, 114 match, 2 differ and 2 cannot be assessed because subject IDs are unavailable. Differences are retained in [count checks](../catalog/hr_count_checks.csv), not silently reconciled.

Preserve original visit labels, baseline origin, specimen, antigen, assay units and detection limits. Author processing can turn pooled `d28+d35` into 31.5; this does not establish an exact collection day. Blank/NA values are unavailable, not zeros or negative outcomes. Misspelled source headers remain literal.

## Coverage limits and next acquisition work

The exact GEO query returned 200 records; all 200 titles plus two known leads were screened. Thirty search/lookup records and citation chasing extend the search. The broad query missed known challenge studies, so the influenza inventory is expandable and **cannot yet establish that every existing dataset has been found**. See [search log](../catalog/search_log.json), [screening decisions](../catalog/geo_screening.json) and [source research notes](../sources/influenza/notes.md).

The remaining work is enumerated in 109 [open gap records](../catalog/open_gaps.csv): expand archive members and sample manifests; inspect supplementary workbook fields and immuneACCESS exports; resolve incomplete cytometry, proteomics, cytokine and raw-read routes; obtain subject/arm/time crosswalks; and continue screening repositories beyond the initial discovery set. Unknown raw-file fields and unavailable assay units remain explicitly unknown. No large raw biological files or controlled participant data were downloaded.

The atlas's original migration receipt is preserved. Later security maintenance redacted publisher credential metadata and rebuilt the unreviewed candidate, with changes documented in the [post-migration change log](../provenance/post_migration_changes.json). Frozen releases and scientific records remain unchanged. Independent scientific review remains pending.
