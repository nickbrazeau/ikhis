import concurrent.futures,json,pathlib,requests,sys
base=pathlib.Path('data_dictionary/sources/influenza/snapshots')
def fetch(item):
 name,url=item
 try:
  r=requests.get(url,timeout=25);r.raise_for_status();p=base/name;p.write_bytes(r.content)
  return {'path':str(p),'url':url,'status':r.status_code,'bytes':len(r.content)}
 except Exception as e: return {'path':name,'url':url,'error':str(e)}
items=json.load(open(sys.argv[1]));out=list(concurrent.futures.ThreadPoolExecutor(max_workers=4).map(fetch,items));json.dump(out,open(sys.argv[1]+'.results.json','w'),indent=2);print(json.dumps(out))
