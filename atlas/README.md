# Greenfield Multi-Omic Immune-System Prior Review

## Current work and preserved release

The current 0.3.0 candidate includes all cytokines and broader immune genetic, transcriptional, proteomic and cellular mechanisms. The fixed cytokine priority coverage set has been removed from active scope. The candidate adds source-linked mechanism dossiers, an expandable cytokine discovery inventory and typed connection proposals. Independent review will be triggered separately by the user; no new candidate evidence enters production priors or approved pathways.

Start with [the candidate review packet](candidates/0.3.0/REVIEW_PACKET.md), [the product scope](protocol/PRODUCT_SCOPE.md), [RUNNING.md](RUNNING.md), and [the project status](reports/PROJECT_STATUS.md). Release 0.2.0 remains the preserved 140-assertion baseline with normalized tables, source snapshots, independent agent review, uncalibrated prior interfaces and reproducible lineage; see [its release report](reports/RELEASE_0.2.0.md). Human adjudication, empirical calibration and broader systematic corpus completion remain open. The original specification is preserved as historical provenance in [protocol/README.original.md](protocol/README.original.md); its former assay list does not govern current scope. The first-release narrative remains in [the initial research synthesis](reports/RESEARCH_SYNTHESIS.md).

## Project status

**Protocol concept:** Greenfield, multi-omic systematic evidence review
**Current protocol version:** v0.3.0 candidate (all-cytokine scope and multi-omic mechanism preparation; review pending)
**Biological-prior lineage:** Required
**Evidence lineage:** Required
**Adversarial review:** Required
**Primary objective:** Construct a source-backed, probabilistic, context-dependent representation of the human immune system that can provide biological priors to future mechanistic/statistical models.

------

# 1. Project objective

This project is a **greenfield systematic review, evidence atlas, and knowledge-base construction effort** covering immune-system biology across four major evidence domains:

1. **Genomic**
2. **Transcriptional**
3. **Proteomic**
4. **Cellular/intercellular signaling**

The project should answer questions such as:

- Which immune cells produce a mediator?
- Which cells can respond to it?
- Which receptors and signaling pathways mediate the response?
- Which transcriptional programs result?
- Which proteins, phosphorylation states, or secreted mediators change?
- Which cellular processes result?
- Which genomic variants alter any of these relationships?
- How do these relationships depend on cell type, cell state, tissue, disease, ancestry, dose, time, and experimental system?
- How certain are each of these assertions?

------

# 2. Core philosophy

The objective is to represent:

> what is supported, under which conditions, by which evidence, with what uncertainty.

Canonical immunology is useful evidence but not ground truth.

New studies may:

- strengthen an interaction;
- weaken an interaction;
- reverse an apparent direction;
- expose a secondary mediator;
- identify a new receptor branch;
- reveal cell-state dependence;
- identify tissue-specific behavior;
- identify genetic modification of an interaction;
- split one interaction into several context-specific interactions;
- increase uncertainty rather than resolve it.

Contradictory observations should therefore remain visible.

The knowledge base should **move with the literature rather than becoming dogmatic**.

------

# 3. Multi-layer immune-system representation

The knowledge base should support several linked biological layers.

## Layer G — Genomic/regulatory

Examples:

- germline variants;
- somatic variants when immunologically relevant;
- GWAS associations;
- fine-mapped variants;
- HLA variation;
- KIR variation;
- structural variants/CNVs;
- cis-eQTLs;
- trans-eQTLs;
- response eQTLs;
- sQTLs;
- pQTLs;
- cytokine QTLs;
- allele-specific expression;
- regulatory-element activity;
- experimentally validated enhancer/promoter effects.

Supporting epigenomic information such as ATAC-seq, ChIP-seq and chromatin-contact data may be included when it helps bridge genomic variation to transcriptional regulation.

------

## Layer T — Transcriptional

Examples:

- bulk RNA-seq;
- microarrays where historically important;
- single-cell RNA-seq;
- single-nucleus RNA-seq;
- spatial transcriptomics;
- Perturb-seq;
- transcription-factor programs;
- gene-set activity;
- alternative splicing;
- isoform expression;
- temporal transcriptional trajectories;
- cytokine-induced transcriptional programs;
- disease-associated transcriptional states.

------

## Layer P — Proteomic

Examples:

- mass-spectrometry proteomics;
- secretome measurements;
- plasma/serum proteomics;
- intracellular proteomics;
- surface proteomics;
- phosphoproteomics;
- other post-translational modifications;
- immunopeptidomics;
- antibody-based protein measurements;
- multiplex cytokine assays;
- CyTOF;
- flow cytometry;
- CITE-seq protein measurements;
- affinity-platform proteomics;
- receptor abundance;
- protein-complex measurements.

------

## Layer C — Cellular and cytokine communication

The presumed core network:

**source cell → cytokine → target cell → receptor complex → proximal signaling pathway → transcriptional response → immediate cellular process**

The target cell may equal the source cell.

Autocrine, paracrine and systemic interactions should be distinguished whenever possible.

------

## Layer F — Immune function and phenotype

Examples:

- activation;
- inhibition;
- migration;
- chemotaxis;
- survival;
- proliferation;
- differentiation;
- cell death;
- cytotoxicity;
- phagocytosis;
- antigen presentation;
- cytokine production;
- antibody production;
- degranulation;
- exhaustion;
- memory formation;
- tolerance;
- tissue trafficking.

------

# 4. Integrated mechanistic representation

The expanded framework should be capable of representing paths such as:

```text
genomic variant
    ↓
regulatory element
    ↓
gene transcription / alternative splicing
    ↓
protein abundance / isoform
    ↓
receptor or signaling activity
    ↓
transcriptional program
    ↓
immune-cell phenotype
```

as well as:

```text
source immune cell
    ↓
secreted cytokine
    ↓
target immune cell
    ↓
receptor complex
    ↓
proximal signaling
    ↓
transcriptional program
    ↓
protein / secretome change
    ↓
cellular process
```

and combinations such as:

```text
genetic variant
    ↓
receptor expression
    ↓
altered cytokine responsiveness
    ↓
altered transcriptional program
    ↓
altered immune phenotype
```

These paths must only be materialized when their component evidence is compatible.

------

# 5. Fundamental evidence principle

The fundamental unit is an **evidence-backed assertion**, not a complete network path.

Examples:

```text
monocyte → secretes → IL-1β

IL-1β → binds → IL1R1/IL1RAP

IL1R1/IL1RAP → activates → MyD88/IRAK signaling

STAT1 → induces → CXCL10 transcription

variant X → increases → IL7R expression

variant Y → alters → cytokine responsiveness
```

Complete paths are assembled from compatible assertions.

Every edge retains its own:

- evidence;
- species;
- context;
- uncertainty;
- direction;
- effect size;
- provenance.

------

# 6. Critical rule: do not collapse molecular layers

The following are **not equivalent**:

```text
DNA variation
≠
RNA abundance
≠
protein abundance
≠
secreted protein
≠
protein activity
≠
functional phenotype
```

Likewise:

**RNA expression of a cytokine does not prove secretion.**

**RNA expression of a receptor does not prove functional receptor availability.**

**Protein abundance does not necessarily prove activation.**

**Phosphorylation does not necessarily prove downstream cellular function.**

**A transcriptional apoptosis signature does not equal measured apoptosis.**

Every transition between biological layers requires its own evidence.

------

# 7. Genomic evidence hierarchy

Genetic evidence should be explicitly graded.

A useful initial hierarchy is:

## G4 — Experimentally validated causal variant

Examples:

- CRISPR editing of allele;
- reporter or enhancer perturbation;
- allele replacement;
- demonstrated effect on molecular phenotype.

## G3 — Strong statistical-genetic mechanism

Examples:

- fine-mapped association;
- colocalized GWAS/eQTL or GWAS/pQTL signal;
- credible target gene;
- supporting cell-specific functional evidence.

## G2 — Molecular QTL

Examples:

- cis-eQTL;
- sQTL;
- pQTL;
- response-QTL.

## G1 — Association

Examples:

- GWAS locus;
- candidate association;
- variant-expression correlation without strong causal localization.

Nearest-gene assignment alone should never be treated as causal gene identification.

------

# 8. Cytokine evidence hierarchy

Retain the previously agreed intercellular hierarchy.

## P4 — Source-to-target causality

Source manipulation demonstrates cytokine-dependent effects on the target.

## P3 — Receptor-dependent target response

Cytokine changes the target and receptor/pathway dependence is demonstrated.

## P2 — Direct target perturbation

Purified cytokine changes target phenotype without receptor confirmation.

## P1 — Observational/curated mechanism

Protein measurements, biochemical relationships or curated pathways.

## P0 — Inferred communication

Ligand–receptor expression, spatial inference, LIANA/CellPhoneDB/NicheNet-type predictions.

P0 evidence is hypothesis-generating and must not automatically become causal evidence.

------

# 9. Transcriptomic evidence interpretation

Transcriptomic studies should distinguish:

- baseline expression;
- differential expression;
- transcription-factor activity inference;
- gene-set activity;
- trajectory;
- perturbational response;
- cell-state association;
- direct transcriptional regulation.

Differential expression alone should generally not imply causal regulation.

Special attention must be paid to:

- cell composition effects;
- pseudoreplication;
- donor effects;
- batch effects;
- disease severity;
- treatment exposure;
- cell-state annotation;
- single-cell multiple testing;
- sparse expression;
- ambient RNA;
- doublets;
- temporal sampling.

------

# 10. Proteomic evidence interpretation

Proteomic measurements require modality-specific QC.

Track:

- measurement platform;
- antibody or affinity reagent;
- mass-spec methodology;
- peptide uniqueness;
- protein isoform;
- limit of detection;
- batch;
- normalization;
- extracellular versus intracellular measurement;
- phosphorylation/PTM site;
- receptor surface localization;
- biological matrix.

Affinity proteomics and antibody measurements should retain information about potential cross-reactivity.

A plasma protein level should not automatically be interpreted as:

- its source cell;
- tissue of origin;
- receptor activity;
- intracellular pathway activation.

------

# 11. Cytokine coverage

All cytokines are in scope, including chemokines, interleukins, interferons, tumor-necrosis-factor families, colony-stimulating factors and other proteins or complexes with supported cytokine activity. There is no fixed assay panel or priority coverage set.

The cytokine inventory will be maintained from versioned, authoritative resources and primary literature. Inclusion in the inventory identifies an entity for investigation; biological relationships require separately extracted evidence. Family membership, aliases, subunits, active complexes, isoforms and species must remain distinguishable.

Cytokines are one part of the broader genomic, transcriptional, proteomic, signaling and cellular-function scope. Antigen processing and presentation, receptor and transcription-factor regulation, immune-cell differentiation and other immune mechanisms remain in scope even when they are unrelated to cytokines.

Historical assay labels remain available as provenance in earlier releases. They do not define current scope, determine research priority or supply a denominator for project completion.

------

# 12. Anchor data resources

The review should systematically evaluate and version relevant sources, including but not limited to:

## Cytokine/signaling

- Immune Dictionary
- Human Cytokine Dictionary
- CytoSig
- LIANA+
- CellPhoneDB
- OmniPath
- Reactome
- SIGNOR

## Genomic / genetic

- NHGRI-EBI GWAS Catalog
- eQTL Catalogue
- GTEx
- immune-cell-specific QTL studies
- stimulated/response-QTL studies
- HLA/KIR resources where applicable
- fine-mapping and colocalization studies

## Transcriptomic

- Human Cell Atlas
- CELLxGENE
- Human Protein Atlas immune transcriptome
- GEO
- ArrayExpress / BioStudies
- ImmPort
- BLUEPRINT
- DICE and related immune-cell transcriptomic resources
- disease-specific single-cell atlases

## Proteomic

- ProteomeXchange
- PRIDE
- Human Protein Atlas
- immune-cell proteomic atlases
- phosphoproteomic datasets
- secretome datasets
- large plasma-proteomic studies
- CITE-seq/CyTOF datasets where relevant

Resources are evidence sources, not unquestioned authorities.

Every source must retain a release/version and retrieval date.

------

# 13. Knowledge-base architecture

The project should use normalized tables.

Core tables should now include:

```text
entities
entity_aliases
cells
cell_states
contexts
cohorts
samples

genetic_associations
fine_mapping
molecular_qtls
regulatory_evidence

transcriptomic_observations
transcriptional_programs

proteomic_observations
protein_modifications

edge_assertions
evidence_instances

multiomic_links
materialized_paths

prior_parameters
prior_changes

critic_runs
critic_findings
adjudications

journal_metrics
source_registry
agent_runs
instruction_versions
artifact_hashes
```

------

# 14. Cohort and dataset identity

A dedicated cohort/dataset registry is mandatory.

This prevents one biological study from receiving excess weight because the same cohort appears in:

- the original publication;
- a follow-up publication;
- a database;
- a meta-analysis;
- a secondary atlas.

Track:

```text
cohort_id
dataset_id
accession
study_id
participants
ancestry
species
tissue
cell_type
disease
intervention
sample_count
donor_count
parent_cohort
related_publications
```

Evidence weight should reflect **independent biological evidence**, not publication count.

------

# 15. Context dimensions

Every evidence record should capture when available:

- species;
- ancestry;
- age;
- sex;
- tissue;
- disease;
- disease severity;
- treatment status;
- cell type;
- cell state;
- developmental state;
- stimulation;
- dose;
- duration;
- assay;
- genomic background;
- time point.

Context mismatch should reduce transportability, not automatically invalidate evidence.

------

# 16. Journal score

Maintain the agreed bounded journal-level modifier derived from authoritative impact-factor data.

Journal prestige must never dominate:

- experimental design;
- causal directness;
- replication;
- sample quality;
- mechanistic specificity.

The journal multiplier should remain modest, with sensitivity analysis performed with the multiplier removed entirely.

------

# 17. Independent adversarial reviewer

A separate **Adversarial Biological Reviewer** should critique both evidence extraction and integrated network products.

New multi-omic adversarial questions include:

- Is a GWAS locus being incorrectly assigned to the nearest gene?
- Does colocalization actually support a shared causal signal?
- Are ancestry differences being ignored?
- Is an eQTL being treated as a universal regulatory relationship?
- Is bulk differential expression caused by changing cell proportions?
- Is single-cell pseudoreplication inflating confidence?
- Is RNA being treated as protein?
- Is intracellular protein being treated as secreted protein?
- Does the antibody assay distinguish the intended isoform?
- Is phosphorylation being mistaken for pathway output?
- Is the same cohort counted repeatedly across omic resources?
- Are molecular measurements temporally compatible?
- Does a multi-omic path cross incompatible tissues or cell states?

Unresolved high-severity challenges must remain visible as contested evidence.

------

# 18. Provenance

Every run should retain:

```text
run_id
agent_role
timestamp_start
timestamp_end
timezone
LLM_provider
LLM_model
model_snapshot_if_available
reasoning_mode
protocol_version
agent_prompt_version
instruction_bundle_hash
source_versions
retrieval_queries
retrieval_dates
source_hashes
code_commit
environment_hash
output_hash
critic_run_ids
human_edits
```

Unknown information is recorded as `unavailable`, not inferred.

------

# 19. Expanded search strategy

Searches should now operate across four parallel evidence lanes.

## Lane A — Cytokine/signaling

Original cytokine perturbation and receptor/signaling searches.

## Lane B — Genomic

Search for:

- immune GWAS;
- fine mapping;
- eQTL;
- sQTL;
- pQTL;
- response eQTL;
- cytokine QTL;
- HLA/KIR effects;
- functional variant validation.

## Lane C — Transcriptomic

Search for:

- immune bulk RNA-seq;
- single-cell atlases;
- perturbation studies;
- spatial transcriptomics;
- transcriptional trajectories;
- transcription-factor programs;
- disease-associated cell states.

## Lane D — Proteomic

Search for:

- immune-cell proteomics;
- secretome;
- plasma proteomics;
- cytokine measurements;
- phosphoproteomics;
- surface proteomics;
- CITE-seq;
- CyTOF;
- functional protein assays.

Cross-omic integration should only occur after modality-specific QC.

------

# 20. Revised project checklist

## A. Governance

-  Greenfield review
-  Multi-layer mechanistic framework
-  Adversarial reviewer
-  Prior-only versioning
-  Journal modifier
-  LLM/instruction provenance
-  Expand scope to genomics
-  Expand scope to transcriptomics
-  Expand scope to proteomics
-  Final protocol
-  Hash/register protocol
-  Final adjudication rules
-  Release policy

## B. Ontologies/entities

-  Cytokines/chemokines
-  Genes
-  proteins/isoforms
-  genetic variants
-  regulatory elements
-  immune cells
-  cell states
-  receptor complexes
-  pathways
-  transcription factors
-  cellular processes
-  tissues
-  diseases
-  assay vocabularies

## C. Source registry

-  Cytokine databases
-  signaling databases
-  GWAS sources
-  QTL sources
-  transcriptomic atlases
-  single-cell atlases
-  proteomic repositories
-  functional-genomic resources
-  versions/retrieval dates/hashes

## D. Corpus construction

-  Cytokine search
-  genomic search
-  transcriptomic search
-  proteomic search
-  family/entity-specific searches
-  citation chaining
-  deduplication
-  cohort deduplication
-  frozen initial corpus

## E. Extraction

-  genomic associations
-  molecular QTLs
-  regulatory genomic evidence
-  transcript abundance
-  splicing
-  transcriptional programs
-  protein abundance
-  secretion
-  PTMs/phosphorylation
-  source cell → cytokine
-  cytokine → target
-  receptor
-  signaling
-  cellular process
-  context
-  temporal information
-  null/contradictory evidence
-  exact provenance

## F. Cross-omic integration

-  variant → gene
-  variant → transcript
-  variant → protein
-  transcript → protein
-  protein → signaling
-  signaling → transcript
-  transcript/protein → function
-  genetic modification of cytokine response
-  cell-state-specific integration
-  tissue-specific integration
-  temporal compatibility checks

## G. Adversarial review

-  genomic critique
-  causal-gene critique
-  transcriptomic critique
-  proteomic critique
-  cytokine critique
-  cross-omic compatibility critique
-  duplicate-cohort critique
-  network topology critique
-  human adjudication

## H. Prior construction

-  existence priors
-  direction priors
-  effect-class priors
-  magnitude priors
-  temporal priors
-  genetic-modifier priors
-  expression priors
-  protein-availability priors
-  human-transportability priors
-  context-specific priors
-  journal-modifier sensitivity analysis

## I. Release

-  entity tables
-  genomic evidence tables
-  transcriptomic evidence tables
-  proteomic evidence tables
-  cytokine interaction tables
-  integrated multi-omic paths
-  critic findings
-  prior tables
-  source manifest
-  provenance manifest
-  protocol/instruction manifest
-  QC report
-  freeze/hash Release 0.1

.

# Instructions to a new Agentic Session

Treat this README as the current project specification.

Do not redesign the project unless a substantive methodological flaw is identified.

Continue systematically through the incomplete checklist.

Maintain the distinction between:

- genomic association;
- genomic causality;
- RNA abundance;
- direct transcriptional regulation;
- protein abundance;
- protein activity;
- cytokine secretion;
- receptor signaling;
- cellular phenotype.

Never use one as an undocumented proxy for another.

Prioritize human evidence but retain animal evidence separately.

Prioritize the user's measured cytokines without limiting scope to them.

Use independent adversarial review whenever possible.

Do not inherit assumptions from prior statistical models.

Version only:

- evidence;
- sources;
- instructions;
- biological priors;
- knowledge-base releases.

Preserve contradictory evidence rather than forcing consensus.
