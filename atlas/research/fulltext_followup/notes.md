# Follow-up source-methods curation

Direct PMC opens produced browser-check pages; Europe PMC fullTextXML returned 404 for PMC1810496 and PMC534504. DOI resolver opens also failed in the browsing tool. These outcomes did not establish that the studies lacked full text elsewhere.

An exact-title search returned extended indexed primary-source passages for [Ferlazzo et al., Distinct roles of IL-12 and IL-15](https://pmc.ncbi.nlm.nih.gov/articles/PMC534504/), including IFNG and CFSE assay methods, Results and Figure4 caption. The snapshot is `source_passages.json`; it is explicitly classified as primary-source excerpts with methods, not a full article.

C-A18 can now be narrowed to intracellular IFNG: monensin, fixation/permeabilization and anti-IFNG flow are specified at six hours. C-A19 has explicit CFSE method details, a 10:1 NK/DC ratio, and blocking antibody at the beginning and day3 of six-day culture. Blocking antibody concentrations and independent donor numbers remain unavailable. These corrections await independent review in `data/curation_overrides_0.2.json` and do not mutate original evidence packs.

C-A12 and C-A20 are not upgraded by this curation. A subsequent narrowly phrased search returned unrelated assay papers and supplies no supporting evidence. All unsuccessful responses are retained for traceability.

Actual queries: “Activated signal transducer” “poor regulator” STAT3 monocytes full text; “Distinct roles of IL-12 and IL-15” “Methods” NK dendritic cells. The method_passages query attempts restricted to the PMC URLs returned irrelevant results; they were excluded from extraction.
