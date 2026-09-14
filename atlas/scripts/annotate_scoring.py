#!/usr/bin/env python3
"""Write the coordinating review's explicit pilot scoring annotations.

The positive hypothesis set is enumerated, not inferred from a signed direction.
New assertions require another review and explicit addition before weighting.
"""
import json
from pathlib import Path
import kb

ROOT=Path(__file__).resolve().parents[1]
from scoring_rules import legacy_annotation, explicit_annotation
def main():
    annotations={}
    curations=kb.approved_curations()
    for lane in ('cytokine','genomic','proteomic'):
        for a in json.loads((ROOT/'research'/lane/'pack.json').read_text())['assertions']:
            a={**a,**curations.get('assertions',{}).get(a['assertion_id'],{})}
            aid=a['assertion_id']
            annotations[aid]=legacy_annotation(a,curations.get('assertions',{}).get(aid))
    approvals=json.loads((ROOT/'data/reviewed_expansion_packs.json').read_text()) if (ROOT/'data/reviewed_expansion_packs.json').exists() else {}
    for lane in ('cytokine_expansion','chemokine_expansion','receptor_expansion'):
        path=ROOT/'research'/lane/'pack.json'
        if not path.exists(): continue
        pack=json.loads(path.read_text())
        approved=kb.review_inputs_approved(path,approvals.get(lane,{}),kb.source_snapshot_paths(pack['sources']))
        for a in pack['assertions']:
            ann=a.get('scoring_annotation',{})
            annotations[a['assertion_id']]={
              'tested_hypothesis':ann.get('tested_hypothesis','unavailable'),
              'evidence_relation':ann.get('evidence_relation','unavailable') if approved else 'unavailable',
              'null_adequacy':ann.get('null_adequacy','unavailable'),
              'annotation_role':'extractor_and_independent_agent_review' if approved else 'pending_independent_review',
              'rationale':ann.get('rationale','unavailable'),
              'review_basis':approvals.get(lane,{}) if approved else 'Expansion pack hash has not been approved following independent review.'}
    (ROOT/'data/scoring_annotations.json').write_text(json.dumps(annotations,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
