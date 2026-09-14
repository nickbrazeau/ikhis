from html.parser import HTMLParser
from pathlib import Path
import re,json
class P(HTMLParser):
 def __init__(self):super().__init__();self.skip=0;self.out=[];self.meta={}
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='meta' and a.get('name','').startswith('citation_'):self.meta.setdefault(a['name'],[]).append(a.get('content',''))
  if t in ['script','style']:self.skip+=1
  if t in ['p','h1','h2','h3','h4','li','caption','tr','div']:self.out.append('\n')
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip-=1
 def handle_data(self,d):
  if not self.skip:self.out.append(d)
for path in Path('research/mechanisms_activation/snapshots').glob('*_full.html'):
 p=P();p.feed(path.read_text());s='\n'.join(x.strip() for x in ''.join(p.out).splitlines() if x.strip());path.with_suffix('.txt').write_text(s)
 path.with_name(path.stem+'_metadata.json').write_text(json.dumps(p.meta,indent=2));print(path.name,len(s),p.meta)
