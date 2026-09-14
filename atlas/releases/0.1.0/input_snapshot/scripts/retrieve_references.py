#!/usr/bin/env python3
"""Retrieve public reference snapshots; no biological assertions are auto-created."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'research' / 'references'
SKILLS = Path('/Users/nfb9/.codex/plugins/cache/openai-curated-remote/life-science-research/1.0.3/skills')
SKILL_PYTHON = ROOT / '.venv' / 'bin' / 'python3'
ALIASES = [('GM-CSF','CSF2'),('IL-12',None),('IL-15','IL15'),('IL-16','IL16'),('IL-17A','IL17A'),('IL-1α','IL1A'),('IL-5','IL5'),('IL-7','IL7'),('TNF-β','LTA'),('VEGF',None),('IFN-γ','IFNG'),('IL-10','IL10'),('IL-12p70','IL12A:IL12B'),('IL-13','IL13'),('IL-1β','IL1B'),('IL-2','IL2'),('IL-4','IL4'),('IL-6','IL6'),('IL-8','CXCL8'),('TNF-α','TNF'),('Eotaxin','CCL11'),('Eotaxin-3','CCL26'),('IL-8 high range','CXCL8'),('IP-10','CXCL10'),('MCP-1','CCL2'),('MCP-4','CCL13'),('MDC','CCL22'),('MIP-1α','CCL3'),('MIP-1β','CCL4'),('TARC','CCL17')]
RESOURCES = [
('LIANA+','C','https://liana-py.readthedocs.io/en/latest/','Inference; P0 outputs; imported resource overlap'),
('CellPhoneDB','C','https://www.cellphonedb.org/','Multimeric ligand/receptor knowledge; inferred communication is P0'),
('OmniPath','C','https://omnipathdb.org/','Aggregated interactions; original source deduplication required'),
('Reactome','C','https://reactome.org/','Curated pathways; verify species and original experiment'),
('SIGNOR','C','https://signor.uniroma2.it/','Signed causal relationships; extract original evidence and context'),
('GWAS Catalog','G','https://www.ebi.ac.uk/gwas/','Association/fine-mapping; locus does not establish target gene'),
('eQTL Catalogue','G','https://www.ebi.ac.uk/eqtl/','Study-specific molecular QTL; datasets may overlap original papers'),
('GTEx','G','https://gtexportal.org/home/','Bulk tissue QTL; cellular composition and ancestry limit transfer'),
('IPD-IMGT/HLA','G','https://www.ebi.ac.uk/ipd/imgt/hla/','Allele nomenclature; not direct functional effect evidence'),
('IPD-KIR','G','https://www.ebi.ac.uk/ipd/kir/','KIR allele/structural variation nomenclature'),
('ENCODE','G','https://www.encodeproject.org/','Regulatory measurements; activity does not identify causal variant alone'),
('Human Cell Atlas','T','https://data.humancellatlas.org/','Cellular transcriptomic atlas; ontology and donor QC'),
('CELLxGENE','T','https://cellxgene.cziscience.com/','Atlas aggregation; preserve collection/dataset versions'),
('Human Protein Atlas','T/P','https://www.proteinatlas.org/','RNA/protein evidence and antibody validation must remain distinct'),
('GEO','T','https://www.ncbi.nlm.nih.gov/geo/','Study accessions, platform and sample provenance'),
('BioStudies/ArrayExpress','T','https://www.ebi.ac.uk/biostudies/arrayexpress','Original and reprocessed transcriptomics; accession deduplication'),
('ImmPort','T/P','https://www.immport.org/','Immune cohorts and assays; controlled metadata review'),
('BLUEPRINT','G/T','https://www.blueprint-epigenome.eu/','Immune epigenome/QTL study reuse must be tracked'),
('DICE','G/T','https://dice-database.org/','Immune-cell eQTL/transcriptomes; cell-specific context'),
('ProteomeXchange','P','https://www.proteomexchange.org/','Repository consortium; PRIDE deposits are not independent studies'),
('PRIDE','P','https://www.ebi.ac.uk/pride/','Peptide/reagent/protein inference QC and dataset accession'),
('UniProt','G/P','https://www.uniprot.org/','Identity normalization only; gene and protein remain separate'),
('IUPHAR IL-12','C','https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=4977','IL12A/IL12B heterodimer identity; assay label remains separate')]

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def snapshot_time(path):
    return datetime.datetime.fromtimestamp(path.stat().st_mtime,datetime.timezone.utc).isoformat()

def write(path, obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def call_skill(script, request, name):
    req_path = OUT / (name+'.request.json')
    write(req_path, request)
    p = subprocess.run([str(SKILL_PYTHON) if SKILL_PYTHON.exists() else sys.executable,str(SKILLS / script)], input=json.dumps(request),text=True,capture_output=True,timeout=90)
    (OUT / (name+'.response.json')).write_text(p.stdout or p.stderr)
    try:
        return json.loads(p.stdout)
    except ValueError:
        return {'ok':False,'error':p.stderr[:500]}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=[]
    genes = sorted(set(g for _,g in ALIASES if g and ':' not in g) | {'IL12A','IL12B','VEGFA'})
    for gene in genes:
        name='uniprot_'+gene
        raw=OUT/(name+'.json')
        if raw.exists():
            continue
        r=call_skill('uniprot-skill/scripts/rest_request.py',{'base_url':'https://rest.uniprot.org','path':'uniprotkb/search','params':{'query':'gene_exact:'+gene+' AND organism_id:9606 AND reviewed:true','size':10,'format':'json'},'max_items':10,'save_raw':True,'raw_output_path':str(raw)},name)
        if not r.get('ok'):
            # Preserve the helper error. The native HTTP client is a documented
            # transport fallback when this host's requests TLS transport fails.
            import urllib.parse
            url='https://rest.uniprot.org/uniprotkb/Q9Y258.json' if gene=='CCL26' else 'https://rest.uniprot.org/uniprotkb/search?'+urllib.parse.urlencode({'query':'gene_exact:'+gene+' AND organism_id:9606 AND reviewed:true','size':10,'format':'json'})
            try:
                with urllib.request.urlopen(url,timeout=30) as response:
                    raw.write_bytes(response.read())
                write(OUT/(name+'.fallback.json'),{'transport':'urllib.request','url':url,'retrieved_at':now(),'reason':'primary skill helper transport failed; exact error preserved'})
                r={'ok':True}
            except Exception as exc:
                write(OUT/(name+'.fallback.json'),{'transport':'urllib.request','url':url,'retrieved_at':now(),'error':str(exc)})
        print(gene,r.get('ok'),flush=True)
        time.sleep(.35)
    for i,(name,lane,url,caution) in enumerate(RESOURCES,1):
        path=OUT/('resource_%02d.html'%i)
        rec={'source_id':'R%03d'%i,'title':name,'lane':lane,'url':url,'version':'unavailable','retrieved_at':now(),'source_type':'resource','notes':caution,'access_level':'resource_landing_page','ingestion_status':'registry_only'}
        try:
            if not path.exists():
                request=urllib.request.Request(url,headers={'User-Agent':'ImmuneEvidenceReview/0.1 (public research)'})
                with urllib.request.urlopen(request,timeout=25) as response:
                    path.write_bytes(response.read(3000000))
                    rec['resolved_url']=response.url
            rec['snapshot_path']=str(path.relative_to(ROOT));rec['snapshot_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            rec['retrieved_at']=snapshot_time(path)
        except Exception as exc:
            rec['access_level']='retrieval_failed';rec['snapshot_path']='unavailable';rec['notes']+='; '+str(exc)
        manifest.append(rec)
        print(name,rec['access_level'],flush=True)
        write(OUT/'resource_registry.json',manifest)
    lanes={
      'A':'(cytokine OR chemokine) AND (immune OR leukocyte) AND (perturbation OR receptor OR signaling)',
      'B':'(immune OR leukocyte) AND (eQTL OR sQTL OR pQTL OR fine-mapping OR colocalization OR response-QTL)',
      'C':'(immune OR leukocyte) AND (single-cell OR RNA-seq OR transcriptomic OR Perturb-seq)',
      'D':'(immune OR leukocyte) AND (proteomic OR phosphoproteomic OR secretome OR CITE-seq OR CyTOF)'}
    searches=[]
    queries=list(lanes.items())+[('entity_'+g, '"'+g+'" AND (cytokine OR chemokine) AND (human OR humans) AND (receptor OR perturbation)') for g in genes]
    for lane,base in queries:
        query='('+base+') AND ("1900/01/01"[Date - Publication] : "2026/09/12"[Date - Publication])'
        name='pubmed_'+lane
        raw=OUT/(name+'.json')
        searched_at=now()
        if not raw.exists():
            r=call_skill('ncbi-entrez-skill/scripts/ncbi_entrez.py',{'endpoint':'esearch','params':{'db':'pubmed','term':query,'retmode':'json','retmax':10,'sort':'relevance'},'max_items':10,'save_raw':True,'raw_output_path':str(raw)},name)
        rec={'search_id':'RSEARCH_'+lane,'lane':lane,'query':query,'database':'PubMed E-utilities','searched_at':searched_at,'retrieval_limit':10,'sort':'relevance','screening_notes':'Bounded discovery index. Returned hits are not screened or automatically included as evidence. Full systematic enumeration remains outstanding.','snapshot_path':str(raw.relative_to(ROOT)) if raw.exists() else 'unavailable'}
        if raw.exists():
            rec['searched_at']=snapshot_time(raw)
            payload=json.loads(raw.read_text()).get('esearchresult',{})
            rec.update(total_hits=payload.get('count','unavailable'),returned_pmids=payload.get('idlist',[]))
        searches.append(rec);write(OUT/'search_registry.json',searches)
        print(name,rec.get('total_hits','failed'),flush=True)
        time.sleep(.4)
    write(OUT/'alias_plan.json',[{'assay_label':a,'canonical_symbol':g or 'unavailable'} for a,g in ALIASES])

if __name__=='__main__':
    main()
