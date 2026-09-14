import json,re,hashlib
from pathlib import Path
P=Path('data_dictionary/sources/influenza'); S=P/'snapshots'
gds=json.load(open(S/'gds_summaries.json'))['result'];by={v['accession']:v for k,v in gds.items() if isinstance(v,dict) and 'accession' in v}
inc=['GSE17156','GSE30550','GSE52428','GSE61754','GSE73072','GSE90732','GSE118223','GSE175551','GSE299820']
exc={'GSE111368':'Natural clinical influenza (MOSAIC), not controlled inoculation.','GSE68310':'Prospective natural acute respiratory illness surveillance; baseline before illness does not mean challenge.','GSE194378':'Influenza vaccination following prior COVID-19, not influenza inoculation.','GSE117580':'Pneumococcal challenge after LAIV or inactivated influenza vaccination; not wild-type influenza challenge.'}
records=[]
for a in inc+list(exc):
 text=(S/(a+'.soft.txt')).read_text();fields={}
 for line in text.splitlines():
  if line.startswith('!Series_') and ' = ' in line:
   k,v=line[8:].split(' = ',1);fields.setdefault(k,[]).append(v)
 meta=by.get(a,{})
 files=[]
 for u in fields.get('supplementary_file',[]):
  name=u.rsplit('/',1)[-1]
  if 'phenotype' in name.lower():
   level='clinical_subject_metadata';note='Subject phenotype metadata; not an expression matrix or instrument measurement.'
  elif 'non-normalized' in name.lower():
   level='unnormalized_feature_intensity_table';note='Submitter-exported unnormalized array intensities; not an instrument archive and not sequencing reads.'
  elif 'RAW.tar' in name:
   level='raw_submitter_archive';note='GEO raw archive is listed; member inventory is not expanded and native instrument files versus exported feature tables are not yet distinguished.'
  else:
   level='processed_counts_or_expression';note='Gene counts and normalized expression are derived measurements, including files whose names contain Raw; not sequencing reads.'
  files.append({'url':u.replace('ftp://','https://'),'name':name,'data_level':level,'availability':'public','verification':'listed_in_GEO_series_metadata; file bytes not downloaded','format':name.split('.',1)[-1],'note':note})
 rec={'id':a,'accession':a,'title':fields.get('title',[''])[0],'repository':'NCBI GEO','source_url':'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='+a,'eligibility':'included_human_influenza_challenge' if a in inc else 'adjacent_excluded','eligibility_reason':('Human volunteers deliberately inoculated with influenza; subset restrictions are retained.' if a in inc else exc[a]),'eligibility_evidence':{'snapshot_path':str(S/(a+'.soft.txt')),'locator':'!Series_summary and !Series_overall_design'},'organism':'Homo sapiens','pathogen':'Influenza A virus','strain':None,'study_design':' '.join(fields.get('overall_design',[])),'preparation':'whole blood' if a!='GSE175551' else 'BAL and blood T cells (CD4/CD8 targeted)','modality':[meta.get('gdstype',fields.get('type',['not verified'])[0])],'sample_count_repository':meta.get('n_samples',len(fields.get('sample_id',[]))),'participant_count':None,'raw_data':{'availability':'public' if any(f['data_level'].startswith('raw_') for f in files) else 'unverified','description':'See file-level classification; sequencing count matrices are derived data.'},'processed_data':{'availability':'public','description':'GEO expression/count data and sample metadata; series matrices are derived datasets.'},'files':files,'metadata_access_url':'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc='+a+'&targ=self&view=brief&form=text','file_formats':meta.get('suppfile','').split(', '),'relationships':fields.get('relation',[]),'cohort_reuse':[],'missing_info':['Subject/sample crosswalk and archive member inventory not exhaustively expanded; no raw binary or patient matrix downloads in this catalogue pass.'],'citations':['https://pubmed.ncbi.nlm.nih.gov/'+x+'/' for x in fields.get('pubmed_id',[])],'source_paths':[str(S/(a+'.soft.txt'))],'retrieved_on':'2026-09-14','curation_status':'source_checked_catalogue_pending_review'}
 if a in ['GSE17156','GSE30550','GSE52428','GSE73072']:rec['cohort_reuse']=['Duke/DARPA challenge series may reuse participants or arrays across these accessions. Do not sum independent cohorts without matching original subject/sample identifiers.'];rec['missing_info'].append('Exact cross-accession subject overlap requires primary sample mapping.')
 if a=='GSE73072':
  rec['participant_count']=148;rec['influenza_arm_participants']=81;rec['influenza_arm_arrays']=1700;rec['mixed_study_rule']='Include H3N2 DEE2/DEE5 and H1N1 DEE3/DEE4 only. Exclude RSV DEE1 and HRV UVA/DUKE from influenza analysis.';rec['challenge_arms']=[{'arm':'H3N2 DEE2','participants':17,'arrays':355},{'arm':'H1N1 DEE3','participants':24,'arrays':477},{'arm':'H1N1 DEE4','participants':19,'arrays':386},{'arm':'H3N2 DEE5','participants':21,'arrays':482}]
 if a=='GSE17156':rec['mixed_study_rule']='Include influenza A H3N2 subset; exclude RSV and rhinovirus participants.'
 if a=='GSE52428':rec['mixed_study_rule']='Separate H1N1/H3N2 deliberate challenge participants from naturally acquired emergency-department illness validation.'
 if a=='GSE61754':rec.update(participant_count=22,strain='A/Wisconsin/67/2005 (H3N2)');rec['mixed_study_rule']='11 vaccinated and 11 unvaccinated volunteers were challenged; preserve vaccination arm.'
 if a=='GSE90732':rec['participant_count']=21;rec['strain']='H1N1; exact strain not verified in series metadata'
 if a=='GSE30550':rec['participant_count']=17;rec['strain']='H3N2/Wisconsin'
 if a=='GSE299820':rec['participant_count']=114;rec['strain']='H3N2; exact strain pending primary-paper linkage';rec['mixed_study_rule']='45 placebo and 69 vaccinated participants; preserve arm and challenge time.'
 if a in ['GSE175551','GSE299820']:rec['missing_info'].append('GEO series links a BioProject but no SRA relation; raw sequence-read access must not be inferred from the presence of gene counts.')
 records.append(rec)
json.dump(records,open(P/'studies.json','w'),indent=2)
# The complete bounded GEO hit list is retained; title-screening is not full paper exclusion.
screen=[]
for k in gds['uids']:
 s=gds[k];a=s['accession'];title=s['title'];decision='title_screened_not_selected';reason='No explicit human influenza inoculation cohort in title; further abstract screening may recover additional eligible datasets.'
 if a in inc:decision='include_for_source_verification';reason='Explicit human influenza challenge lead; series metadata inspected.'
 elif a in exc:decision='adjacent_excluded';reason=exc[a]
 elif re.search('vaccin',title,re.I):decision='adjacent_vaccination_title';reason='Vaccination-focused title; not evidence of wild-type human influenza challenge.'
 elif re.search('Calu|A549|BEAS|organoid|epithelial|in vitro|HUVEC|Umbilical',title,re.I):decision='adjacent_cell_or_ex_vivo_title';reason='Cell, tissue, organoid, or in vitro experiment title; not deliberate human participant inoculation.'
 screen.append({'accession':a,'title':title,'decision':decision,'reason':reason,'locator':'snapshots/gds_summaries.json result.'+k})
json.dump(screen,open(P/'geo_screening.json','w'),indent=2)
print('Wrote',len(records),'study/accession records and',len(screen),'title-screening decisions')
