# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import re,json,sys,struct,zipfile
base=Path(sys.argv[2]).resolve();root=(base/'decoded/res').resolve()
mappingfile=base/'theme-config-map.json'
if sys.argv[1]=="prepare":
 mapping={}
 used={int(m[1]) for p in root.glob('values-mcc*') if (m:=re.fullmatch(r'values-mcc(\d{1,3})(.*)',p.name))}
 available=iter(x for x in range(1,1000) if x not in used)
 for p in sorted(root.glob('values-mcc*')):
  m=re.fullmatch(r'values-mcc(\d{4,})(.*)',p.name)
  if not m:continue
  old=int(m[1]);new=next(available)
  dest=root/f'values-mcc{new:03d}{m[2]}'
  if not p.resolve().is_relative_to(root) or not dest.resolve().is_relative_to(root):raise ValueError('Unsafe path')
  if dest.exists():raise ValueError('Configuration collision')
  p.rename(dest);mapping[new]=old
 mappingfile.write_text(json.dumps(mapping));print('Prepared theme configs:',len(mapping))
else:
 mapping={int(k):v for k,v in json.loads(mappingfile.read_text()).items()};count=[0]
 z=zipfile.ZipFile(base/'unsigned.apk');data=bytearray(z.read('resources.arsc'))
 def walk(start,end):
  pos=start
  while pos<end:
   typ,hs,size=struct.unpack_from('<HHI',data,pos)
   if size<hs or size<8 or pos+size>end:raise ValueError('Invalid resource chunk')
   if typ==0x0201:
    configsize=struct.unpack_from('<I',data,pos+20)[0]
    if configsize<8:raise ValueError('Invalid configuration')
    mcc=struct.unpack_from('<H',data,pos+24)[0]
    if mcc in mapping:struct.pack_into('<H',data,pos+24,mapping[mcc]);count[0]+=1
   if typ in (0x0002,0x0200):walk(pos+hs,pos+size)
   pos+=size
  if pos!=end:raise ValueError('Chunk alignment mismatch')
 walk(0,len(data))
 if count[0]<len(mapping):raise ValueError('Missing theme configurations')
 with zipfile.ZipFile(base/'theme-restored.apk','w') as out:
  for info in z.infolist():
   content=data if info.filename=='resources.arsc' else (base/'decoded'/info.filename).read_bytes() if info.filename.endswith('.dex') and '/' not in info.filename else z.read(info.filename)
   out.writestr(info,content)
 print('Restored original theme resource configurations:',count[0])
