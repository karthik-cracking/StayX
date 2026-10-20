# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import sys
from common import ROOT, font_for
DECODED=Path(sys.argv[1]).resolve()
import re,shutil,base64,io
from PIL import Image,ImageDraw,ImageFont
R=(DECODED/'res'); A='{http://schemas.android.com/apk/res/android}'
src=(ROOT/'assets/stayx-logo.png')
logo=Image.open(src).convert('RGB')
count=0
for p in R.glob('values*/*.xml'):
 if p.name not in ('strings.xml','arrays.xml'):continue
 s=p.read_text(encoding='utf-8')
 def change(m):
  global count
  head,body,tail=m.groups()
  # Leave machine identifiers and URLs intact; edit only displayed XML text.
  body2=re.sub(r'(?<![\w/])(?:Morphe|TubeMod)(?![\w/])','StayX',body)
  if 'name="application_name"' in head:body2='StayX'
  count+=body!=body2
  return head+body2+tail
 s=re.sub(r'(<string\b[^>]*>)(.*?)(</string>)',change,s,flags=re.S)
 p.write_text(s,encoding='utf-8')
manifest=(DECODED/'AndroidManifest.xml')
s=manifest.read_text(encoding='utf-8').replace('android:label="TubeMod"','android:label="StayX"')
s=re.sub(r'android:(icon|roundIcon)="@mipmap/[^"]+"',r'android:\1="@mipmap/stayx_launcher"',s)
manifest.write_text(s,encoding='utf-8')
(R/'mipmap-xxxhdpi').mkdir(exist_ok=True)
logo.resize((192,192),Image.Resampling.LANCZOS).save(R/'mipmap-xxxhdpi/stayx_launcher.png')
# Replace every switchable Morphe launcher/settings brand icon, preserving resource names/IDs.
replaced=0
for p in list(R.glob('drawable*/morphe_settings_icon*.xml'))+list(R.glob('drawable*/morphe_adaptive_foreground*.xml')):
 p.unlink();logo.resize((108,108),Image.Resampling.LANCZOS).save(p.with_suffix('.png'));replaced+=1
for p in R.glob('mipmap-*/morphe_adaptive_foreground*.png'):
 im=Image.open(p);logo.resize(im.size,Image.Resampling.LANCZOS).save(p)
# Replace header wordmarks at their existing sizes.
for p in R.glob('drawable*/ringo2_action_bar_logo*.webp'):
 old=Image.open(p);w,h=old.size
 im=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(im)
 dark='dark' in p.name
 font=font_for(max(12,int(h*.80)))
 d.text((0,-int(h*.08)),'StayX',font=font,fill='#111827' if dark else '#F5F8FF')
 im.save(p,format='WEBP',lossless=True)
small=logo.resize((160,160),Image.Resampling.LANCZOS);buf=io.BytesIO();small.save(buf,format='PNG',optimize=True)
uri='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
html='''<!doctype html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{margin:0;background:#101017;color:#f3f5ff;font:16px sans-serif;padding:30px 22px;text-align:center}img{width:128px;height:128px;border-radius:28px}h1{font-size:34px;margin:16px 0 6px}h2{font-size:18px;color:#49d5ff}p{line-height:1.6;color:#b8bdd5}.card{padding:18px;margin:22px 0;border:1px solid #303046;border-radius:20px;background:#191923}a{color:#56dcff;text-decoration:none;display:block;padding:14px}small{color:#9298b4}</style></head><body><img src="'''+uri+'''"/><h1>StayX</h1><p>Your videos. Your way.</p><div class="card"><h2>StayX custom build</h2><p>Ad controls &bull; Local video downloads<br>Based on YouTube 21.42.243</p><small>Experimental patches 1.48.0-dev.15</small></div><div class="card"><h2>Open-source credits</h2><p>Built using Morphe patches and REA analysis.<br>Downloads are handled by YTDLnis.<br>This is an independent custom build.</p><a href="https://morphe.software/credits/">Contributors &amp; licenses</a><a href="https://github.com/MorpheApp/morphe-patches/tree/v1.48.0-dev.15">Morphe patch source</a><a href="https://github.com/deniscerri/ytdlnis">YTDLnis source</a></div></body></html>'''
import html as html_lib
legal='<details><summary>License and upstream notice</summary><pre style="white-space:pre-wrap;text-align:left;font-size:11px">'+html_lib.escape((ROOT/'NOTICE').read_text())+'\n\n'+html_lib.escape((ROOT/'LICENSE').read_text())+'</pre></details>'
html=html.replace('</body>',legal+'</body>')
(DECODED.parent/'about.html').write_text(html,encoding='utf-8')
print('Updated',count,'localized brand strings and',replaced,'icon resources')
