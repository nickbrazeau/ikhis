#!/usr/bin/env python3
"""Retrieve public full-text alternatives for four pending pilot assertions."""
import datetime,hashlib,json,urllib.request,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'research/fulltext_followup'
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    records=[]
    for pmc in ('PMC1810496','PMC534504'):
        url='https://www.ebi.ac.uk/europepmc/webservices/rest/'+pmc+'/fullTextXML'
        rec={'pmcid':pmc,'url':url,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'access_level':'unavailable'}
        try:
            with urllib.request.urlopen(url,timeout=45) as response: raw=response.read()
            path=OUT/(pmc+'.xml');path.write_bytes(raw)
            tree=ET.fromstring(raw)
            if tree.find('.//body') is None: raise ValueError('No article body in payload')
            text='\n'.join(' '.join(node.itertext()).strip() for node in tree.iter() if node.tag in ('article-title','title','p','caption'))
            (OUT/(pmc+'.txt')).write_text(text)
            rec.update(access_level='full_text_XML',snapshot_path=str(path.relative_to(ROOT)),sha256=hashlib.sha256(raw).hexdigest())
        except Exception as exc: rec['error']=str(exc)
        records.append(rec);print(pmc,rec['access_level'],rec.get('error',''),flush=True)
    (OUT/'retrieval.json').write_text(json.dumps(records,indent=2)+'\n')
if __name__=='__main__':main()
