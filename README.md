# IKHIS

IKHIS contains two related projects:

| Project | Purpose | Start here |
|---|---|---|
| [atlas](atlas/) | Source-backed immune-system evidence atlas, including all cytokines and broader immune mechanisms. | [Atlas README](atlas/README.md) · [Current candidate](atlas/reports/CANDIDATE_0.3.0.md) |
| [data_dictionary](data_dictionary/) | Data inventory, provenance and variable dictionary for atlas inputs and human influenza challenge studies. | [Dictionary README](data_dictionary/README.md) |

The atlas was nested under `atlas/` on September 14, 2026. Its frozen releases, candidate snapshots and existing working changes were preserved. Git history remains at the IKHIS root. The shared local Python environment remains in `.venv/`; `atlas/.venv` links to it for existing research commands. Run atlas commands from `atlas/` as described in [its instructions](atlas/RUNNING.md).

The dictionary builds on the [HR-VILAGE paper](https://doi.org/10.48550/arXiv.2505.14725), [dataset](https://huggingface.co/datasets/xuejun72/HR-VILAGE-3K3M) and [author repository](https://github.com/XuejunSun98/HR-VILAGE-3K3M), tracing original repositories rather than equating harmonized expression matrices with instrument-level raw data.

The atlas candidate's independent review remains pending; this organizational and data-inventory work does not constitute that review.
