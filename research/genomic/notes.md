# Genomic lane: bounded pilot extraction

The pack contains 10 primary publications, 17 study/assay cohort records, 25 assertions, 18 logged discovery queries and 10 explicit gaps. It is a purposive pilot of immune regulatory mechanisms, not a completed exhaustive systematic review. OneK1K is retained as an evaluated source/cohort anchor without molecule-specific edges because its original full methods and variant-level results were not obtained.

The strongest recurring result is context dependence. [Fairfax et al.](https://doi.org/10.1126/science.1246949) shows stimulus-dependent detection, a HIP1 direction reversal and a later TNF RNA eQTL. [DICE](https://doi.org/10.1016/j.cell.2018.10.022) shows opposing GAB2 RNA associations in B and T cells. A separate genotype-selected surface 4-1BB experiment remains an association, even though protein was measured.

[Simeonov et al.](https://doi.org/10.1038/nature23875) supplies three deliberately separate records: allele-specific reporter activity in Jurkat cells, IL2RA response-eQTL evidence in primary human T cells, and an edited-allele surface-protein phenotype in mice. The [2018 correction](https://doi.org/10.1038/s41586-018-0227-7) is confirmed and archived at metadata/indexed-excerpt level. Its full text was inaccessible. No assertion about EDEL steady-state Treg percentages is extracted from the superseded statement.

[Galarza-Muñoz et al.](https://doi.org/10.1016/j.cell.2017.03.007) provides direct IL7R allele/splicing reporter evidence and a DDX39B UTR translation reporter result. Primary T-cell knockdown supports exon skipping, while supernatant IL7R differs between sh3 and sh5. The authors' antibody-isoform limitation is retained. The PBMC DDX39B RNA association is null; a translation/protein effect must not be recast as an RNA eQTL.

[Al-Mossawi et al.](https://doi.org/10.1038/s41467-019-12393-1) separately measures monocyte surface and soluble IL7R and reports a null DDX39B–IL7R interaction in LPS-stimulated monocytes. Different cellular systems and low minor-allele frequency prevent interpreting that null as a universal refutation. The soluble-protein arm explicitly reuses 161 samples from the Fairfax cohort, so these publications cannot contribute independent donor weights. Published absolute soluble IL7R concentration units require source-data verification before magnitude priors are constructed.

[BLUEPRINT](https://doi.org/10.1016/j.cell.2016.10.026) contributes an IRF5 isoform sQTL and a TNFRSF1A splicing/disease colocalization. The latter is G3 statistical mechanism support, not an experimentally validated variant. [Lee et al.](https://doi.org/10.1126/science.1246980) contributes a stimulated IRF7 association and influenza-specific IFNA13 trans-eQTL. IFNA13 RNA does not prove secreted cytokine. [Soskic et al.](https://doi.org/10.1038/s41588-022-01066-3) contributes target-level VAMP8/AIMP1 cluster-specific eQTL assertions; lead variants are unavailable and must not be invented. The source's sex percentages are inconsistent with its counts; only 67 male/52 female is retained.

The [Gregory 2007 association](https://doi.org/10.1038/ng2103) remains G1 and needs full-text review. [OneK1K](https://doi.org/10.1126/science.abf3041) is an important cohort anchor, but its abstract's Mendelian-randomization causal language is not promoted to G4. Recently indexed 2024–2026 splicing, regulatory-screen and cell-type eQTL studies are explicitly logged for later screening; none is silently treated as reviewed evidence.

## Interpretation and integration rules

- G4 applies only to the experimentally manipulated molecular readout and species. Reporter enzyme activity is recorded as `protein_activity`, with its use as a regulatory/translation readout explained; it is not native RNA or receptor activity.
- G2 molecular QTLs retain LD and state limitations. G3 colocalization is model-dependent. Candidate genotype/phenotype follow-ups remain G1 where formal QTL mapping is not demonstrated.
- Gene depletion is `perturbational`, not an edited causal variant. The DDX39B perturbation and rs2523506 association must not be combined as if the variant were edited in primary T cells.
- Contradiction groups retain cell-state reversals, RNA/protein differences, reagent discordance and nulls. Nondetection is not proof of zero effect.
- Every cohort has unresolved global independence. Known Fairfax/Al-Mossawi reuse is explicitly represented by the parent-cohort link. DICE, ImmVar and BLUEPRINT reanalyses are not assumed independent.
- No complete multiomic pathway is asserted. Variant identities, splice-event coordinates, exact timepoints and compatible biological systems must be established before path assembly.

## Source access and reproducibility

Eight primary papers have actual public PMC HTML snapshots and locally extracted plain-text companions in `snapshots/`. OneK1K and Gregory have actual PubMed tool-response snapshots. Web search responses, failed CAPTCHA/redirect/403 requests and correction-retrieval limitations are also saved. A public Europe PMC XML endpoint returned 404; direct public PMC HTML retrieval succeeded. These are distinct access attempts, not fabricated full-text reviews.

`pack.json` is the machine-readable extraction. `build_pack.py` recreates it from the manually reviewed extraction definitions and saved source metadata. `run.json` records available execution provenance; authoritative source hashing and release registration are handled centrally. Snapshot file modification times are used as retrieval-record timestamps. No participant-level data were downloaded, no source-platform changes were made, and no impact-factor values or calibrated probabilities were fabricated.

Remaining work is explicitly enumerated in the pack: exhaustive searching and screening, supplementary extraction, new-study screening, ancestry and donor-overlap resolution, missing variant/event identities, HLA/KIR and structural/somatic coverage, and source-data verification of quantitative measurements.

## Independent review response

The independent biological reviewer inspected this pack and the supporting full-text passages. Three medium findings were corrected: the combined shRNA record now has an unsigned association direction, the 178-person IL2RA eQTL analysis records its European American/Caucasian restriction, and the DICE surface 4-1BB experiment includes IL7 and the antibody concentrations. `review_response.json` preserves the finding IDs and original/revised hashes. The original review remains unchanged in `research/review_multiomic.json`; final release disposition belongs to the integrating agent. This is not human adjudication or validation of calibrated prior probabilities.
