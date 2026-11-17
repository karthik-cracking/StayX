# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import sys
from common import ROOT, font_for
DECODED=Path(sys.argv[1]).resolve()
from PIL import Image
R=(DECODED/'res')
im=Image.open(ROOT/'assets/stayx-logo.png').convert('RGBA')
alpha=im.convert('RGB').point(lambda v: v)
mask=Image.new('L',im.size)
mask.putdata([255 if max(r,g,b)>90 else 0 for r,g,b in alpha.getdata()])
white=Image.new('RGBA',im.size,'white');white.putalpha(mask)
count=0
for p in list(R.glob('drawable*/morphe_notification_icon*.xml'))+list(R.glob('drawable*/morphe_adaptive_monochrome*.xml')):
 p.unlink();white.resize((96,96),Image.Resampling.LANCZOS).save(p.with_suffix('.png'));count+=1
for p in R.glob('drawable*/ic_stat_yt_notification_logo.png'):
 size=Image.open(p).size;white.resize(size,Image.Resampling.LANCZOS).save(p);count+=1
print('Replaced notification and monochrome branding:',count)
