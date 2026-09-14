# HR-VILAGE documentation and schema audit

Inspected on 14 September 2026. This audit describes the supplied resource using its paper, authors' documentation/code, and small tables. It does not download full expression matrices or instrument files and does not establish a complete census of influenza challenge studies.

- [schema.json](schema.json): 49 published metadata variables, study/citation tables, expression and antibody structures, units, grain and safe joins.
- [transformations.json](transformations.json): six processing paths with source locators and distinctions between instrument files, count/intensity measurements, normalized data and derived outcomes.
- [version_notes.json](version_notes.json): release differences, source-reported duplicate/pair relationships and influenza leads.
- [sources.json](sources.json): original URLs, revisions, snapshot hashes and derived reading-text bindings.

## Version and raw-data status

The [current HF card](https://huggingface.co/datasets/xuejun72/HR-VILAGE-3K3M/blob/c68349578b97af04d1102eac5ad9f30f85362c53/README.md) and [GitHub README](https://github.com/XuejunSun98/HR-VILAGE-3K3M/blob/716c27dccba847875f85be63103e2245acaa3320/README.md) identify V3, released 28 August 2026: `bulk_gene_expr_raw/` was removed, while `study_citations.csv` now directs readers to the original records. The [paper v2](https://arxiv.org/html/2505.14725v2), dated 31 May 2026, predates that change. Its raw-file availability wording must not be treated as the current inventory.

The HF study table has 66 rows and 16 columns; the GitHub copy has 66 rows and 13 columns. The former adds gene and time summaries. The legacy `raw_data` flag is not sufficient evidence that a particular raw file is presently downloadable. Original repositories can contain both processed matrices and instrument-level files.

The HF card labels antibody files as raw measurements. That label does not mean plate-reader or other instrument output: the inspected example also contains derived MFC and responder columns. Assay, units and censoring remain endpoint-specific.

## Directly inspected checks

The current HF GSE194378 **example** metadata contains 387 unique sample rows, 73 distinct within-study subject IDs and 50 columns. Each row index equals `geo_accession`. The antibody example contains 73 unique subject IDs and 17 columns; every ID occurs in the metadata. The card describes 386 rows/72 subjects. The full study summary reports 75 subjects and 412 observations; example counts do not establish an error in those full-cohort totals. Root integration should check the full files independently.

The author demos are illustrative and not an execution ledger for each current matrix. The [RNA-seq demo](https://github.com/XuejunSun98/HR-VILAGE-3K3M/blob/716c27dccba847875f85be63103e2245acaa3320/docs/RNAseq_Process.qmd) uses CPM after gene aggregation, with log transformation shown in a plot. The [Illumina demo](https://github.com/XuejunSun98/HR-VILAGE-3K3M/blob/716c27dccba847875f85be63103e2245acaa3320/docs/Illumina_microarray_process.qmd) likewise separates QN from a plot-only log transform. Generic Methods wording cannot establish exact units for all exported matrices.

The [single-cell merger](https://github.com/XuejunSun98/HR-VILAGE-3K3M/blob/716c27dccba847875f85be63103e2245acaa3320/code/Merge_Plot_Demo.py) can populate an absent `.X` from `log_norm` or `.raw.X`, after checking count layers. Consequently `.X`, `.raw` and a directory named raw cannot independently establish count-scale data. Each H5AD artifact and layer needs separate inspection before assigning its processing level.

The [metadata demo](https://github.com/XuejunSun98/HR-VILAGE-3K3M/blob/716c27dccba847875f85be63103e2245acaa3320/docs/Meta_preprocess_demo.qmd) changes pooled `d28+d35` into day 31.5. Preserve that original label and representative-time rule; 31.5 does not establish an exact collection time. Missing values can also become literal `nan` or `<NA>` strings after metadata coercion.

## Influenza leads and deduplication

The current author study table supplies six influenza-inoculation cohort rows: GSE61754, GSE90732 and four GSE73072 cohorts (H1N1 DEE3/DEE4 and H3N2 DEE2/DEE5). These are leads for source-level trial/arm confirmation, not six distinct repository series. Three influenza-related mixed-exposure rows—GSE68310, GSE194378 and GSE117580—must retain their original study-design context. A mixed-exposure or influenza label alone does not establish an influenza challenge.

The README reports overlapping cohorts in GSE52428, GSE30550 and GSE17156 that are excluded in favor of corresponding GSE73072 cohorts. It also identifies paired bulk/single-cell subjects in GSE201533/GSE201534 and GSE246525/GSE246937. These are author-reported links, not independently reconstructed participant equivalences. Repeated samples, tissues, modalities, challenge episodes and cells cannot be summed as independent people. Similar laboratory provenance likewise does not prove negligible batch effects.

Use `(study_ID, source_row_name)` for sample joins and `(study_ID, ID)` for participant joins unless source-backed cross-cohort mappings exist. Preserve original antigen, assay, specimen and visit labels. Missing expression and missing clinical outcomes must not become zeros or negative outcomes.
