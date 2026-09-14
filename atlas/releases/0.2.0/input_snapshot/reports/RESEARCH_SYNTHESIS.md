# Greenfield multi-omic immune-system evidence synthesis

The initial evidence release establishes a traceable starting point for immune-system biological priors. Its strongest feature is the preservation of experimental context and measurement identity. Its principal scientific limitation is coverage: the corpus is a deliberately bounded collection of anchor resources and primary experiments, rather than a completed systematic enumeration of immune biology. A statement absent from this release is an evidence gap, not a biological negative.

The corpus contains 72 assertions extracted from 27 publication/resource records across cytokine signaling, genomics, transcription and proteomics. Two records describe the same Human Cytokine Dictionary experiment, so there are 26 distinct publication families; that count is not a count of independent cohorts. The cohort registry contains 38 records for datasets, subsets and experimental contexts. Most independence assessments remain unresolved, with known reuse retained explicitly. Thirty original cytokine assay labels have identity records, including separate ambiguous IL-12 and VEGF assay concepts.

## Biological conclusions

### Cytokine responses are cell- and system-dependent

The mouse Immune Dictionary and the Human Cytokine Dictionary provide complementary perturbation resources. The mouse study’s in-vivo lymph-node responses and the human study’s ex-vivo blood responses differ in species, tissue, exposure and experimental system. Their records must therefore remain distinct. The extracted IL-4 transcriptional responses support narrow RNA-level assertions and do not identify the cytokine’s natural producing cell, demonstrate functional receptor abundance, or establish a cellular phenotype. [1,2]

The Human Cytokine Dictionary has two public preprint records corresponding to the same 12-donor experiment. Its bioRxiv API record had no linked published article at retrieval. This is evidence of the observed repository status, rather than proof that no unindexed journal version exists. The two records are registered as one biological dataset and must not double its prior weight. A journal-version check is required at the next literature refresh. [2,3]

CytoSig links perturbation signatures with inferred signaling activity, but signature inference and measured cytokine response are different evidence classes. The pilot extracts an experimental validation involving BMP6 and extracellular CXCL8/CCL2 measurements in A549 cells. That experiment supports its cancer-cell culture context; it does not establish the same response in immune cells or physiological cytokine-producing tissues. Such model-system evidence remains useful when its transportability is explicit. [4]

### IL-10 autoregulation illustrates the importance of time

The human monocyte IL-10 study supports several distinct observations: endogenous IL-10 secretion after stimulation, suppression of TNF production, and a later decrease in IL-10 RNA. Independent review corrected the RNA-decrease record from seven to 24 hours and retained the earlier no/minimal inhibition separately. The two records differ in observation time and need not represent contradictory biology. Neither result justifies an unqualified, timeless “IL-10 inhibits IL-10” relationship. [5]

A separate STAT3 study contributes a functional null observation concerning TNF regulation. This record does not establish that STAT3 signaling is absent, and it does not erase IL-10’s effects through other mechanisms. Its accessible source detail is insufficient for a complete mechanistic chain, so the record remains excluded from numerical prior updates pending full-text curation. [6]

### Source manipulation can establish communication without proving every intermediate

Engineering human dendritic cells with IL15 and IL15RA mRNA provides stronger source-to-target evidence than ligand–receptor expression matching. The extracted study distinguishes soluble IL-15, surface-associated IL-15, intracellular IFNG and target-cell killing. Contact and neutralization experiments support a P4 source-to-target assertion in the engineered culture system. They do not establish every proximal signaling and transcriptional intermediate or equivalence to unmodified dendritic cells. [7]

Another dendritic-cell/NK-cell study differentiates IL-12- and IL-15-dependent responses. Some accessible passages describe IFNG “secretion” without enough assay detail to establish the measured compartment. The corresponding assertion now records protein production with compartment unavailable and remains flagged for full-text review. The source’s terminology is retained in the evidence narrative without turning it into a more specific measurement claim. [8]

The IL12RB1-deficiency study separates expanded T-cell clone responses from activated-blast STAT4 DNA-binding results. A receptor-deficient response in a selected clone system does not imply that receptor dependence is irrelevant in ordinary human immune cells. Conversely, an absent response under a thresholded assay is not a formal demonstration of biological impossibility. Participant overlap between experiments is now machine-readable while clone and blast contexts remain separate. [9]

### Genetic relationships depend on cell state and assay

Fairfax and colleagues show why response-QTL observations require stimulation and time in their identity. The pilot retains context-specific HIP1 and GDPD5 observations and a late-LPS TNF locus-level eQTL. The TNF observation is not converted into a named causal variant because the extracted assertion does not supply one. A broad statement that an allele “regulates an immune gene” would discard the experimental condition that makes the relationship interpretable. [10]

The IL2RA enhancer work contributes three different levels of evidence: a human reporter effect, a human genotype–RNA association and a separate mouse knock-in surface-protein effect. G4 grading applies to the specific validated experimental outcome. It is not evidence that a complete native human allele-to-disease mechanism has been established. Independent review recovered an ancestry restriction in the human association analysis, which is retained using the source’s population labels. The reported author correction is registered, but its complete content remains a specific curation gap. [11]

The IL7R/DDX39B evidence is similarly layered. Minigene splicing, a 5′-UTR reporter, gene depletion and soluble-protein measurements are different experiments. Heterogeneity between depletion reagents is retained as an unsigned combined result rather than forced into opposing effect directions. Antibody detection of soluble material cannot establish a specific isoform when the assay does not distinguish it. [12]

The original IL7R multiple-sclerosis association is represented as G1 association evidence within the accessible source limits. Follow-up monocyte work separates surface IL7R from supernatant soluble IL7R and retains a reported failure to detect the proposed genotype interaction in that context. The soluble-protein analysis reuses a subset of Fairfax donors; it must not count as an independent cohort merely because it appears in a later paper. [13,14]

DICE contributes an example in which the same genotype is associated with lower GAB2 RNA in one cellular context and higher RNA in another. Those are separate context-specific assertions. Its surface 4-1BB follow-up also illustrates the danger of abbreviated methods extraction: IL-7 was part of the co-stimulation alongside CD3/CD28, and was restored after review. The candidate protein association remains distinct from receptor activity and downstream function. [15]

BLUEPRINT supports a statistical link between a disease signal and splicing regulation, while the CD4 activation study supplies state-dependent locus-level eQTL observations. The OneK1K study is retained as a source anchor without fabricating molecule-level edges that were not extracted. Dendritic-cell response-QTL results preserve pathogen and interferon contexts. Collectively these sources support context-specific genetic hypotheses, not universal regulatory arrows. [16–19]

### Protein measurement is an additional evidence layer

The human immune-cell proteomic atlas is an important source for total and secreted proteomes. Its pilot IL34 assertion is an unsigned aggregate proteome difference based on accessible supplementary information; it is not a set of individual protein effects and remains awaiting deeper extraction. Unresolved isoforms and absent main-matrix extraction are explicit limitations. [20]

Mass cytometry supplies a particularly useful receptor–response contrast. A B-cell population can display a receptor-associated marker without the expected cytokine-induced phospho-response under the tested conditions. The positive IFNα comparator and the IL7–STAT5 observations remain separate records. These results do not equate phosphorylation with downstream cellular function. A Figure 5 panel-label inconsistency in the saved source is documented instead of silently “corrected” into an unsupported citation. [21]

CITE-seq provides paired surface-protein and transcript measurements, but the pilot’s NK-subset comparisons come from accessible supplementary captions and remain limited. REAP-seq provides a clearer perturbational contrast: CD27 costimulation increases ICOS protein without a corresponding RNA increase, while IL7R decreases in both measured layers. The observations do not establish receptor functionality or a cellular outcome merely from changes in marker abundance. [22,23]

### Plasma protein signals retain platform and cohort ambiguity

UK Biobank plasma analyses and cross-platform comparisons show why a protein-assay value needs platform and reagent provenance. A coding variant can alter a measured affinity signal through epitope effects, protein abundance, or both; the assay association alone does not settle the mechanism. IL6 and CXCL9 disease-association discrepancies are encoded as unsigned platform/reagent differences, not opposing biological effect directions. [24,25]

The Chinese paired-platform study supplies useful evidence from another population and same-participant measurements. A cis-pQTL replicated across affinity platforms is stronger technical support than a single-platform signal, but paired assays are not independent biological cohorts. Nor does a plasma measurement identify a source cell, tissue of production or intracellular signaling state. [26]

### Platelet secretion and endothelial response require separate assertions

The platelet IL1B study links synthesis and released material with a measured endothelial–neutrophil adhesion response. Fraction transfer and receptor-antagonist experiments support a receptor-dependent component of the response. They do not isolate every active mediator in the fraction or prove that purified IL1B alone explains the result. The source’s eight-hour versus 18-hour collection-time discrepancy is preserved as a path-blocking temporal uncertainty. [27]

## Integration and probability interpretation

The release represents evidence-backed assertions with independent context, source, cohort, assay and uncertainty fields. Gene and transcript entities are distinct from protein entities; protein compartments and measured activity remain observation attributes. Source-only resources and identity snapshots do not become biological assertions through ingestion. Unknown external ontology mappings retain local identifiers rather than guessed ontology accessions.

The prior interface includes existence, direction, effect class, magnitude, temporal, genetic-modifier, expression, protein-availability, human-transportability and context-specific parameter families. Only supported initial families have values. Quantitative magnitude and transportability distributions remain unavailable because an arbitrary numerical distribution would imply precision unsupported by the extraction.

The available Beta and Dirichlet summaries are transparent, uncalibrated weighting devices. Their coefficients are operational proposals; they are not empirically calibrated probabilities of biological truth. Hypothesis identity and evidence relation are explicit, separate from the observed sign. Pilot nulls remain descriptive because their statistical adequacy for absence claims is unavailable. A lack of significance never automatically becomes evidence against an unstated positive hypothesis.

Repeated records from one known cohort are capped before weighting. A transitive parent-cohort relationship remains one group, and unresolved independence is pooled conservatively. Consequently an “effective evidence group” in these summaries is not a declaration that independent replication was established. Direction, magnitude and transportability should be consumed separately by a downstream model.

No complete mechanistic path is materialized in this release. The component assertions remain available, and proposed joins receive explicit reasons for rejection. A shared entity name cannot supply missing temporal order, treatment compatibility, receptor dependence or evidence for a cross-layer transition. Multiplying edge summaries into a path probability is prohibited because it would assume unjustified independence and calibration.

Journal weighting is neutral in the released results. No authoritative impact-factor series was supplied or retrieved. The optional bounded formula is documented as a proposal; it does not reconstruct an absent prior agreement. The no-journal sensitivity values match the main values because the modifier is disabled, not because journal metrics were measured and found irrelevant.

## Review and remaining work

Independent extraction review covered all initial assertions and led to concrete corrections in timing, molecular compartment, direction semantics, ancestry, stimulation and cohort linkage. A separate implementation review checked prior weighting, path gates, source/cohort challenges and release hashing. Original findings and subsequent agent dispositions are both retained. None is labeled human adjudication.

The broad PubMed lanes and entity queries are reproducible discovery searches, capped at ten relevance-ranked results per query. Their total hit counts are stored separately from returned identifiers. They are not an exhaustive corpus, and their hits are not automatically eligible for priors. A defensible full review requires uncapped retrieval with stable pagination, a documented deduplication and screening flow, full-text and supplementary extraction, citation chaining, corrections/retraction checks and an explicit saturation decision.

Additional scientific work includes resolving assay-platform identities; expanding all priority cytokines beyond identity coverage; human validation of high-impact assertions; fine-mapping and colocalization parameter extraction; sample/donor-level provenance where accessible; ontology alignment; calibrated effect and transportability priors; and collection of compatible evidence for complete paths. These are explicitly tracked rather than marked complete by the presence of empty tables.

## Sources

1. Cui et al. [Dictionary of immune responses to cytokines at single-cell resolution](https://www.nature.com/articles/s41586-023-06816-9). Nature, 2024 issue; online 2023.
2. [A single-cell cytokine dictionary of human peripheral blood](https://pmc.ncbi.nlm.nih.gov/articles/PMC12724453/). Preprint, 2025.
3. [Same Human Cytokine Dictionary experiment, second preprint record](https://pmc.ncbi.nlm.nih.gov/articles/PMC12776526/). Version and duplication retained in source registry.
4. [Systematic investigation of cytokine signaling activity at the tissue and single-cell levels](https://pmc.ncbi.nlm.nih.gov/articles/PMC8493809/). CytoSig primary publication.
5. [Interleukin 10 inhibits cytokine synthesis by human monocytes](https://pubmed.ncbi.nlm.nih.gov/1940799/). Primary human monocyte experiments.
6. [Activated STAT3 is a poor regulator of TNF production by human monocytes](https://pmc.ncbi.nlm.nih.gov/articles/PMC1810496/).
7. [IL-15 transpresentation by engineered human dendritic cells](https://pmc.ncbi.nlm.nih.gov/articles/PMC4792546/).
8. [Distinct roles of IL-12 and IL-15 in human NK-cell activation](https://pmc.ncbi.nlm.nih.gov/articles/PMC534504/).
9. [Residual type 1 immunity in IL12RB1-deficient patients](https://pmc.ncbi.nlm.nih.gov/articles/PMC2193232/).
10. Fairfax et al. [Innate immune activity conditions regulatory variant effects](https://pmc.ncbi.nlm.nih.gov/articles/PMC4064786/).
11. Simeonov et al. [Stimulation-responsive immune enhancers](https://pmc.ncbi.nlm.nih.gov/articles/PMC5675716/).
12. Galarza-Muñoz et al. [Human epistatic interaction controls IL7R splicing](https://pmc.ncbi.nlm.nih.gov/articles/PMC5456452/).
13. Gregory et al. [IL7R allelic and functional association with multiple sclerosis](https://pubmed.ncbi.nlm.nih.gov/17660817/).
14. Al-Mossawi et al. [Context-specific surface and soluble IL7R regulation](https://pmc.ncbi.nlm.nih.gov/articles/PMC6783569/).
15. Schmiedel et al. [Genetic polymorphisms and human immune-cell expression](https://pmc.ncbi.nlm.nih.gov/articles/PMC6289654/). DICE.
16. Chen et al. [Genetic drivers of immune-cell epigenetic and transcriptional variation](https://pmc.ncbi.nlm.nih.gov/articles/PMC5119954/). BLUEPRINT.
17. Yazar et al. [Single-cell eQTL mapping of autoimmune disease regulation](https://pubmed.ncbi.nlm.nih.gov/35389779/). OneK1K.
18. Soskic et al. [Immune risk variants and CD4 activation dynamics](https://pmc.ncbi.nlm.nih.gov/articles/PMC9197762/).
19. Lee et al. [Genetic variants modulate pathogen-sensing responses](https://pmc.ncbi.nlm.nih.gov/articles/PMC4124741/).
20. Rieckmann et al. [Human immune-cell social network by quantitative proteomics](https://www.nature.com/articles/ni.3693).
21. Bendall et al. [Single-cell mass cytometry across a human hematopoietic continuum](https://pmc.ncbi.nlm.nih.gov/articles/PMC3273988/).
22. Stoeckius et al. [Simultaneous epitope and transcriptome measurement](https://www.nature.com/articles/nmeth.4380). CITE-seq.
23. Peterson et al. [Multiplexed protein and transcript quantification](https://www.nature.com/articles/nbt.3973). REAP-seq.
24. Sun et al. [Plasma proteomic associations in UK Biobank](https://www.nature.com/articles/s41586-023-06592-6).
25. Eldjarn et al. [Plasma proteomics comparisons through genetics and disease](https://www.nature.com/articles/s41586-023-06563-x).
26. [Paired plasma-protein platforms in Chinese adults](https://www.nature.com/articles/s41467-025-56935-2). Nature Communications, 2025.
27. Lindemann et al. [Platelet inflammatory signaling by regulated IL1B synthesis](https://pmc.ncbi.nlm.nih.gov/articles/PMC2196422/).
