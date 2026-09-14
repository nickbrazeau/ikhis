import importlib.util
from pathlib import Path
import unittest
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))

spec=importlib.util.spec_from_file_location('kb',Path(__file__).resolve().parents[1]/'scripts/kb.py')
kb=importlib.util.module_from_spec(spec);spec.loader.exec_module(kb)

class EvidenceSafetyTests(unittest.TestCase):
    def record(self,**changes):
        return dict(status='reviewed',qc_status='reviewed_extraction',evidence_tier='P3',direction='increase',independence_group='cohort_A',independence_status='resolved',access_level='full_text',qualitative_confidence='moderate',evidence_relation='supports',tested_hypothesis='A increases B in explicit context',null_adequacy='unavailable',**changes)

    def test_duplicate_publication_cannot_increase_weight(self):
        r=self.record()
        self.assertEqual(kb.summarize_evidence([r]),kb.summarize_evidence([r,r,r]))

    def test_unresolved_cohorts_are_not_replication(self):
        a=self.record();b=self.record()
        a.update(independence_status='unresolved',independence_group='a')
        b.update(independence_status='unresolved',independence_group='b')
        self.assertEqual(kb.summarize_evidence([a,b])['independent_groups'],1)

    def test_true_replication_adds_weight(self):
        a=self.record();b=self.record();b['independence_group']='b'
        self.assertGreater(kb.summarize_evidence([a,b])['alpha'],kb.summarize_evidence([a])['alpha'])

    def test_null_and_opposing_results_reduce_support(self):
        a=self.record();b=self.record();b.update(direction='null',independence_group='b',evidence_relation='opposes',null_adequacy='adequate')
        self.assertLess(kb.summarize_evidence([a,b])['estimate'],kb.summarize_evidence([a])['estimate'])

    def test_conflict_within_cohort_is_retained_under_cap(self):
        a=self.record();b=self.record();b['direction']='decrease';b['evidence_relation']='opposes'
        result=kb.summarize_evidence([a,b])
        self.assertGreater(result['beta'],1)
        self.assertLessEqual(result['alpha']+result['beta']-2,1.5)

    def test_null_without_adequacy_does_not_refute_negative_predicate(self):
        a=self.record();a.update(direction='null',evidence_relation='opposes',null_adequacy='unavailable')
        self.assertEqual(kb.summarize_evidence([a])['independent_groups'],0)

    def test_unsigned_heterogeneity_does_not_create_opposing_evidence(self):
        a=self.record();a['direction']='mixed'
        self.assertEqual(kb.summarize_evidence([a])['beta'],1)

    def test_contested_and_full_text_pending_are_withheld(self):
        a=self.record();a['status']='contested'
        b=self.record();b['qc_status']='needs_full_text'
        self.assertEqual(kb.summarize_evidence([a,b])['estimate'],.5)
        self.assertEqual(kb.summarize_evidence([a,b])['independent_groups'],0)

    def test_missing_and_unverified_journal_metrics_are_neutral(self):
        self.assertEqual(kb.journal_multiplier(),1)
        self.assertEqual(kb.journal_multiplier(200,False),1)
        for jif in (0,1,100,1e20):
            self.assertTrue(1<=kb.journal_multiplier(jif,True)<=1.05)
        with self.assertRaises(ValueError): kb.journal_multiplier(float('nan'),True)

    def path_fixture(self):
        c={f:'explicit_same_context' for f in kb.CRITICAL_CONTEXT}
        a={'assertion_id':'a','subject_id':'x','object_id':'y','context_id':'c1','status':'reviewed','evidence_tier':'P3','direction':'increase','evidence_relation':'supports'}
        b={'assertion_id':'b','subject_id':'y','object_id':'z','context_id':'c2','status':'reviewed','evidence_tier':'P3','direction':'increase','evidence_relation':'supports'}
        return [a,b],{'c1':dict(c),'c2':dict(c)}

    def bridge(self):
        return {('a','b'):{'status':'reviewed','temporal_compatibility':'verified','measurement_bridge':'verified','context_compatibility':'verified','evidence_id':'EV_bridge'}}

    def test_endpoint_matching_does_not_make_mechanistic_path(self):
        edges,contexts=self.path_fixture()
        ok,reasons=kb.compatible_path(edges,contexts)
        self.assertFalse(ok)
        self.assertIn('missing_reviewed_transition_and_temporal_bridge',reasons)

    def test_unknown_context_is_not_a_match(self):
        edges,contexts=self.path_fixture();contexts['c1']['species']='unavailable';contexts['c2']['species']='unavailable'
        self.assertFalse(kb.compatible_path(edges,contexts,{('a','b')})[0])

    def test_cross_species_path_blocked(self):
        edges,contexts=self.path_fixture();contexts['c1']['species']='human';contexts['c2']['species']='mouse'
        self.assertFalse(kb.compatible_path(edges,contexts,{('a','b')})[0])

    def test_explicit_compatible_bridge_can_pass(self):
        edges,contexts=self.path_fixture()
        self.assertTrue(kb.compatible_path(edges,contexts,self.bridge())[0])

    def test_inferred_edge_cannot_become_causal_path(self):
        edges,contexts=self.path_fixture();edges[0]['evidence_tier']='P0'
        self.assertFalse(kb.compatible_path(edges,contexts,{('a','b')})[0])

    def test_gene_and_protein_identity_are_distinct(self):
        import sqlite3
        db=sqlite3.connect(':memory:');db.execute('CREATE TABLE entities ('+kb.TABLES['entities']+')')
        gene=kb.ensure_entity(db,'IL7R','gene','G','human')
        protein=kb.ensure_entity(db,'IL7R','protein','P','human')
        self.assertNotEqual(gene,protein)

    def test_no_fixed_panel_required_and_partial_historical_aliases_are_valid(self):
        import sqlite3
        db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
        for table,definition in kb.TABLES.items():
            db.execute('CREATE TABLE '+table+' ('+definition+')')
        self.assertEqual(kb.validate(db),[])
        entity=kb.ensure_entity(db,'CXCL8','protein','P','Homo sapiens')
        kb.insert(db,'entity_aliases',dict(alias_id='one',entity_id=entity,original_label='IL-8'))
        self.assertEqual(kb.validate(db),[])

    def test_nested_cohort_reuse_and_unresolved_parent(self):
        cohorts={'parent':{'parent_cohort':'unavailable','independence_status':'resolved'},'child':{'parent_cohort':'parent','independence_status':'resolved'},'grandchild':{'parent_cohort':'child','independence_status':'resolved'}}
        self.assertEqual(kb.cohort_group('grandchild',cohorts),('parent',True))
        cohorts['parent']['independence_status']='unresolved'
        self.assertEqual(kb.cohort_group('grandchild',cohorts),('parent',False))
        cohorts['parent']['parent_cohort']='grandchild'
        self.assertFalse(kb.cohort_group('grandchild',cohorts)[1])

    def test_unknown_hypothesis_cannot_update_prior(self):
        r=self.record();r['tested_hypothesis']='unavailable'
        self.assertEqual(kb.summarize_evidence([r])['independent_groups'],0)

    def test_null_edge_and_changed_treatment_cannot_form_path(self):
        edges,contexts=self.path_fixture();edges[0]['direction']='null'
        self.assertFalse(kb.compatible_path(edges,contexts,self.bridge())[0])
        edges[0]['direction']='increase';contexts['c2']['treatment_status']='different'
        self.assertFalse(kb.compatible_path(edges,contexts,self.bridge())[0])

    def test_tuple_is_not_a_verified_bridge(self):
        edges,contexts=self.path_fixture()
        self.assertFalse(kb.compatible_path(edges,contexts,{('a','b')})[0])

    def test_high_source_and_parent_cohort_findings_propagate(self):
        a={'assertion_id':'a','source_id':'s','cohort_id':'child'}
        cohorts={'child':{'parent_cohort':'parent'}}
        self.assertTrue(kb.is_contested(a,'ctx',{'source':{'s'}},cohorts))
        self.assertTrue(kb.is_contested(a,'ctx',{'cohort':{'parent'}},cohorts))
        self.assertTrue(kb.is_contested(a,'ctx',{'context':{'ctx'}},cohorts))

    def compiled_fixture(self,relation2='opposes'):
        import sqlite3
        db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
        for t,d in kb.TABLES.items(): db.execute('CREATE TABLE '+t+' ('+d+')')
        for i in (1,2):
            kb.insert(db,'source_registry',dict(source_id='s'+str(i),title='source',url='https://example.org',access_level='full_text'))
            kb.insert(db,'cohorts',dict(cohort_id='c'+str(i),independence_status='resolved',parent_cohort='unavailable'))
            kb.insert(db,'edge_assertions',dict(assertion_id='a'+str(i),subject_id='x',object_id='y',predicate='increases' if i==1 else 'does_not_increase',context_id='ctx',measurement='protein_abundance',direction='increase' if i==1 else 'decrease',evidence_tier='P3',status='reviewed',qualitative_confidence='moderate'))
            kb.insert(db,'evidence_instances',dict(evidence_id='e'+str(i),assertion_id='a'+str(i),source_id='s'+str(i),cohort_id='c'+str(i),source_locator='Fig1',evidence_summary='fixture',qc_status='reviewed_extraction',tested_hypothesis='X increases Y in context',evidence_relation='supports' if i==1 else relation2,null_adequacy='unavailable'))
        return db

    def test_raw_negative_predicate_does_not_split_shared_hypothesis(self):
        import json
        db=self.compiled_fixture();kb.compile_priors(db)
        rows=db.execute("SELECT parameters FROM prior_parameters WHERE parameter_family='existence' ORDER BY assertion_id").fetchall()
        self.assertEqual(rows[0][0],rows[1][0]);self.assertEqual(json.loads(rows[0][0]),{'alpha':2.5,'beta':2.5})

    def test_inconclusive_record_cannot_inherit_numeric_prior(self):
        db=self.compiled_fixture('inconclusive');kb.compile_priors(db)
        row=db.execute("SELECT estimate,availability FROM prior_parameters WHERE assertion_id='a2' AND parameter_family='existence'").fetchone()
        self.assertIsNone(row[0]);self.assertNotEqual(row[1],'available')

    def test_inadequate_null_cannot_contribute_via_another_record(self):
        import json
        db=self.compiled_fixture('supports')
        db.execute("UPDATE edge_assertions SET direction='null' WHERE assertion_id='a2'")
        kb.compile_priors(db)
        row=db.execute("SELECT parameters FROM prior_parameters WHERE assertion_id='a1' AND parameter_family='existence'").fetchone()
        self.assertEqual(json.loads(row[0]),{'alpha':2.5,'beta':1.0})

if __name__=='__main__': unittest.main()
