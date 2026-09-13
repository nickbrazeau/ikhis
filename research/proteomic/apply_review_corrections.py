#!/usr/bin/env python3
"""Idempotently apply the source-verified proteomic review corrections.

pack.json is the authoritative manually extracted input; there is no separate
proteomic pack generator. This script preserves the exact reviewed changes for
replay without replacing the immutable critic review or its response audit.
"""

import hashlib
import json
from pathlib import Path

CHANGES = {
    "P_A01": {
        "direction": ["mixed", "association"],
        "uncertainty": [
            "Caption reports FDR <5%; effect sizes unavailable.",
            "Caption reports FDR <5%; effect sizes and signed protein-level changes unavailable. Total-profile differences do not establish both increase and decrease."
        ]
    },
    "P_A06": {
        "source_locator": [
            "Fig. 5B legend",
            "Fig. 5C as cited in the main-text STAT5 paragraph; bendall_fulltext.txt:181. Saved Fig. 5 legend at line 175 instead labels this STAT5 result B."
        ],
        "limitations": [
            "PTM site, antibody clone, dose and duration unavailable in extracted main text. Two donors; phosphorylation is not measured cell function.",
            "PTM site, antibody clone, dose and duration unavailable in extracted main text. Two donors; phosphorylation is not measured cell function. The saved source has a panel-label discrepancy: main text cites Fig. 5C for STAT5, while the Fig. 5 legend labels STAT5 B and PLC-gamma-2 C; use the specific STAT5 passage."
        ]
    },
    "P_A07": {
        "direction": ["mixed", "association"],
        "source_locator": [
            "Supplementary Fig. 6b caption; extract in open3.json",
            "Supplementary Fig. 6b caption; cite_publisher_page.txt:257 (also captured in open3.json)"
        ]
    },
    "P_A15": {
        "direction": ["mixed", "association"],
        "source_locator": [
            "Protein–phenotype associations paragraph; Supplementary Table 18",
            "Protein-phenotype associations paragraph; extract2.json source line 148, referring to Supplementary Table 18 (table not independently extracted)"
        ]
    },
    "P_A16": {
        "direction": ["mixed", "association"],
        "source_locator": [
            "Protein–phenotype associations paragraph; Supplementary Table 18",
            "Protein-phenotype associations paragraph; extract2.json source line 149, referring to Supplementary Table 18 (table not independently extracted)"
        ]
    }
}


def main():
    target = Path(__file__).resolve().with_name("pack.json")
    original = target.read_bytes()
    pack = json.loads(original)
    records = {item["assertion_id"]: item for item in pack["assertions"]}
    edits = 0
    for assertion_id, fields in CHANGES.items():
        for field, (old, new) in fields.items():
            current = records[assertion_id][field]
            if current not in (old, new):
                raise ValueError(f"Unexpected value for {assertion_id}.{field}: {current!r}")
            if current == old:
                records[assertion_id][field] = new
                edits += 1
    if edits:
        target.write_text(json.dumps(pack, indent=2, ensure_ascii=True) + "\n")
    print(json.dumps({"field_edits": edits, "pack_sha256": hashlib.sha256(target.read_bytes()).hexdigest()}))


if __name__ == "__main__":
    main()
