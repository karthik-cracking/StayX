# SPDX-License-Identifier: GPL-3.0-only
from pathlib import Path
import sys
from common import ROOT, font_for
DECODED=Path(sys.argv[1]).resolve()
import re
R=(DECODED/'res')
p=(DECODED/'AndroidManifest.xml');s=p.read_text()
s=re.sub(r'android:(icon|roundIcon)="@mipmap/[^"]+"',r'android:\1="@mipmap/ringo2_ic_launcher"',s);p.write_text(s)
# Offer StayX colors without applying a theme at build time.
for p in R.glob('values*/strings.xml'):
 s=p.read_text(encoding='utf-8')
 s=re.sub(r'(<string name="morphe_theme_color_dark_custom_title">).*?(</string>)',r'\g<1>StayX custom dark background\2',s)
 s=re.sub(r'(<string name="morphe_theme_color_dark_custom_summary">).*?(</string>)',r'\g<1>Choose Custom above to use the StayX dark preset, or pick another color\2',s)
 p.write_text(s,encoding='utf-8')
print('Launcher icons restored to original YouTube artwork')
