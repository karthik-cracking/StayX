"""Use the existing StayX settings logo in both Lottie startup resources.
SPDX-License-Identifier: GPL-3.0-only
"""
from pathlib import Path
import base64,json,sys
ROOT=Path(__file__).resolve().parents[1]
def animation():
    image=base64.b64encode((ROOT/'assets/stayx-logo.png').read_bytes()).decode('ascii')
    return {'v':'5.12.1','fr':60,'ip':0,'op':42,'w':432,'h':432,'nm':'StayX startup',
      'assets':[{'id':'stayx','w':512,'h':512,'u':'','p':'data:image/png;base64,'+image,'e':1}],
      'layers':[{'ddd':0,'ind':1,'ty':2,'nm':'StayX settings logo','refId':'stayx','sr':1,
       'ks':{'o':{'a':0,'k':100},'r':{'a':0,'k':0},'p':{'a':0,'k':[216,216,0]},
        'a':{'a':0,'k':[256,256,0]},'s':{'a':0,'k':[32,32,100]}},
       'ao':0,'ip':0,'op':42,'st':0,'bm':0}]}
if __name__=='__main__':
    raw=Path(sys.argv[1])/'res/raw'
    for name in ['morphe_startup_animation.json','morphe_startup_animation_play.json']:
        p=raw/name
        if not p.exists():raise FileNotFoundError(p)
        p.write_text(json.dumps(animation(),separators=(',',':')),encoding='utf-8')
    print('Replaced both startup animations with the existing StayX settings logo')
