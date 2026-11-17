# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import sys
from common import ROOT, font_for
DECODED=Path(sys.argv[1]).resolve()
from PIL import Image,ImageDraw,ImageFont
import re
R=(DECODED/'res')
logo=Image.open(ROOT/'assets/stayx-logo.png').convert('RGBA')
logo.resize((192,192),Image.Resampling.LANCZOS).save(R/'drawable/stayx_brand_logo.png')
for p in R.glob('drawable*/morphe_settings_icon*.png'):
 p.unlink()
 p.with_suffix('.xml').write_text('<layer-list xmlns:android="http://schemas.android.com/apk/res/android"><item android:width="24dp" android:height="24dp" android:drawable="@drawable/stayx_brand_logo" /></layer-list>',encoding='utf-8')
for p in R.glob('drawable*/*'):
 if p.suffix not in ('.png','.webp'):continue
 if not any(s in p.stem for s in ['wordmark_header','yt_logo_text','ringo2_action_bar_logo']):continue
 w,h=Image.open(p).size
 canvas=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(canvas)
 font=font_for(max(12,int(h*.85)))
 d.text((0,-int(h*.08)),'StayX',font=font,fill='#F5F8FF' if 'dark' in p.stem else '#111827')
 canvas.save(p,**({'lossless':True} if p.suffix=='.webp' else {}))
for p in R.glob('values*/strings.xml'):
 s=p.read_text(encoding='utf-8')
 s=re.sub(r'(<string\b[^>]*>)(YouTube)(</string>)',r'\g<1>StayX\3',s)
 p.write_text(s,encoding='utf-8')
print('Polished settings icon sizes, header assets, and app accessibility labels')
