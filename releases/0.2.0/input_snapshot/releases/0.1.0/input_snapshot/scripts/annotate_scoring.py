#!/usr/bin/env python3
"""Write the coordinating review's explicit pilot scoring annotations.

The positive hypothesis set is enumerated, not inferred from a signed direction.
New assertions require another review and explicit addition before weighting.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SUPPORTS=set('''
C-A01 C-A02 C-A03 C-A04 C-A05 C-A06 C-A07 C-A08 C-A09 C-A10 C-A11
C-A13 C-A15 C-A16 C-A17 C-A18 C-A19 C-A21 C-A24
G-A001 G-A002 G-A004 G-A005 G-A006 G-A007 G-A008 G-A009 G-A011 G-A012
G-A013 G-A014 G-A015 G-A016 G-A017 G-A018 G-A019 G-A020 G-A021 G-A022 G-A023 G-A024
P_A01 P_A02 P_A04 P_A05 P_A07 P_A09 P_A10 P_A11 P_A13 P_A14 P_A15 P_A16 P_A17 P_A18 P_A19 P_A20 P_A21
'''.split())
INCONCLUSIVE=set('C-A12 C-A14 C-A20 C-A22 C-A23 C-A25 G-A003 G-A010 G-A025 P_A03 P_A06 P_A08 P_A12 P_A22'.split())
def main():
    annotations={}
    for lane in ('cytokine','genomic','proteomic'):
        for a in json.loads((ROOT/'research'/lane/'pack.json').read_text())['assertions']:
            aid=a['assertion_id']
            annotations[aid]={
              'tested_hypothesis':a['subject']+' '+a['predicate']+' '+a['object']+'; measurement='+a['measurement']+'; context='+json.dumps({k:a.get(k,'unavailable') for k in 'species ancestry age sex tissue disease disease_severity treatment_status cell_type cell_state developmental_state stimulation dose duration assay genomic_background time_point'.split()},sort_keys=True),
              'evidence_relation':'supports' if aid in SUPPORTS else 'inconclusive' if aid in INCONCLUSIVE else 'unavailable',
              'null_adequacy':'unavailable',
              'annotation_role':'coordinating_agent',
              'rationale':'Supports only the stated narrow extracted relationship; no causal or cross-context upgrade.' if aid in SUPPORTS else 'Observed null/threshold/nonsignificance does not establish relationship absence. Retained descriptively; no numerical prior update.',
              'review_basis':'Independent critic findings plus corrected extraction; human adjudication pending.'}
    (ROOT/'data/scoring_annotations.json').write_text(json.dumps(annotations,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
