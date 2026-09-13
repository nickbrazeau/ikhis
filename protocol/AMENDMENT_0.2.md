# Protocol amendment 0.2.0

This amendment extends operational protocol 0.1.0 without changing its biological evidence principles. The continued review prioritizes the cytokines and chemokines with no extracted protein-involving evidence in Release 0.1.0. Original evidence packs are retained. The new corpus is a documented coverage expansion, not exhaustive literature saturation.

## Extraction and screening

New lane packs supply candidate-level screening decisions with exact queries, citations and include/exclude/await-full-text reasons. Relevance-ranked web discovery is not presented as an exhaustive database corpus. Search absence and unreported outcomes do not become biological negatives.

Directly measured biochemical binding has its own measurement class, `binding`. Its endpoint is a protein or protein complex in layer P. Binding alone does not demonstrate signaling, receptor surface availability, or a cellular process. Source-reported quantitative measurements are stored separately from prior distributions; missing precision and heterogeneous assays are not repaired with invented standard errors.

The original IL-12 and VEGF assay labels remain unresolved until platform documentation is available. Literature about an explicitly identified IL12A:IL12B complex or VEGFA protein does not by itself identify a user's assay target. Original assay channels are preserved.

New scoring annotations explicitly describe the tested hypothesis, relation to that hypothesis and null-evidence adequacy. They are reviewed alongside extraction. An unsigned contrast or ordinary null cannot be silently converted into evidence for absence or opposite direction.

## Immutable release lineage

Each release retains its own generated files, manifest and full input snapshot. The snapshot includes the complete verified predecessor dependency, allowing an isolated historical rebuild without reading later working inputs. Release 0.1.0's original 388-entry manifest was verified before all 347 external inputs were copied into its input_snapshot directory; the original manifest and generated outputs are unchanged. A subsequent security redaction removed credential parameters from one archived search result; its original and replacement hashes are recorded in a separate ledger, and verification reports this exception explicitly. Future verification resolves each manifest's external inputs within that release's own snapshot.

A frozen release cannot be rebuilt or refrozen in place. New evidence is compiled under a new semantic release version. Release changes identify added, modified and removed assertions, evidence, sources and priors; unchanged records do not receive spurious prior-change rows. The previous release is opened read-only for comparison. Snapshots and generated outputs are locally versioned; no external publication or human approval is implied.

## Remaining limits

Independent agents perform extraction and adversarial review; coordinating-agent dispositions remain distinct from human adjudication. Heuristic probabilities remain uncalibrated. Source-backed bridge ingestion and complete mechanistic paths are not introduced by this amendment. The human-assay mapping, whole-corpus screening, expanded genomic/omic parameter extraction and quantitative calibration tasks remain on the broader roadmap.
