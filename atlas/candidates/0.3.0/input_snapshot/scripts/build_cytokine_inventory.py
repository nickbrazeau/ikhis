#!/usr/bin/env python3
"""Normalize the complete saved cytokine annotation queries without adding edges."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def build():
    folder = ROOT / 'research/cytokine_inventory'
    rows, queries, seen = [], [], set()
    for kind in ('reviewed', 'unreviewed'):
        request_path = folder / (kind + '.request.json')
        response_path = folder / (kind + '.response.json')
        request = json.loads(request_path.read_text())
        response = json.loads(response_path.read_text())
        source = folder / 'snapshots' / ('uniprot_' + kind + '.tsv')
        if not response.get('ok') or response.get('status_code') != 200:
            raise ValueError('Incomplete inventory retrieval: ' + kind)
        query_id = 'CYTINV_' + kind.upper()
        result_rows = list(csv.DictReader(source.open(), delimiter='\t'))
        if not result_rows:
            raise ValueError('Empty cytokine annotation response: ' + kind)
        for row in result_rows:
            accession = row['Entry']
            if accession in seen or row['Organism (ID)'] != '9606' or row['Reviewed'] != kind:
                raise ValueError('Duplicate accession or inconsistent taxonomy/review status: ' + accession)
            seen.add(accession)
            rows.append({
                'inventory_id': 'CYT_' + accession,
                'uniprot_accession': accession,
                'entry_name': row['Entry Name'],
                'gene_symbol': row['Gene Names (primary)'] or 'unavailable',
                'gene_aliases': row['Gene Names'],
                'protein_names': row['Protein names'],
                'species': 'Homo sapiens',
                'taxon_id': 9606,
                'resource_annotation_status': kind,
                'inventory_status': 'resource_annotated_candidate' if kind == 'reviewed' else 'unreviewed_discovery_candidate',
                'query_id': query_id,
                'keyword_ids': row['Keyword ID'],
                'go_ids': row['Gene Ontology IDs'],
                'source_url': 'https://www.uniprot.org/uniprotkb/' + accession,
                'snapshot_path': str(source.relative_to(ROOT)),
                'snapshot_sha256': sha(source),
                'biological_evidence_status': 'inventory_only_no_assertion_or_prior',
            })
        queries.append({
            'query_id': query_id,
            'query': request['params']['query'],
            'endpoint': request['base_url'] + '/' + request['path'],
            'retrieved_on': '2026-09-13',
            'retrieval_limit': 'none; complete stream response for the specified query',
            'result_count': len(result_rows),
            'request_path': str(request_path.relative_to(ROOT)),
            'response_path': str(response_path.relative_to(ROOT)),
            'snapshot_path': str(source.relative_to(ROOT)),
            'snapshot_sha256': sha(source),
            'resource_release': 'unavailable; helper response did not preserve release headers',
        })
    rows.sort(key=lambda row: row['uniprot_accession'])
    out = ROOT / 'data/cytokine_inventory.json'
    out.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n')
    with out.with_suffix('.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    metadata = {
        'scope': 'all_cytokines; no fixed panel',
        'queries': queries,
        'reviewed_resource_entries': sum(r['resource_annotation_status'] == 'reviewed' for r in rows),
        'unreviewed_resource_entries': sum(r['resource_annotation_status'] == 'unreviewed' for r in rows),
        'distinct_reported_gene_symbols': len({r['gene_symbol'] for r in rows if r['gene_symbol'] != 'unavailable'}),
        'limitations': [
            'A UniProt reviewed entry is resource curation, not independent review of this project extraction.',
            'Entries include related forms, predicted/unreviewed records and broad cytokine-activity annotations; entry count is not a count of distinct active cytokines.',
            'These two full queries cover their annotation sets, not every possible literature-supported cytokine or every active heteromeric complex.',
            'Registry membership creates no biological edge, source-cell assignment, mechanism or numerical prior.',
            'Source-backed additions and active-complex/isoform curation remain eligible beyond this seed inventory.',
        ],
        'failed_preliminary_attempts': [
            'System Python helper lacked requests.',
            'Local research runtime request failed sandbox DNS; approved public helper calls then succeeded.',
        ],
    }
    (folder / 'inventory_manifest.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps({k: v for k, v in metadata.items() if k not in ('queries', 'limitations', 'failed_preliminary_attempts')}, indent=2))

if __name__ == '__main__':
    build()
