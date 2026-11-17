from pathlib import Path
import os
from PIL import ImageFont
ROOT=Path(__file__).resolve().parents[1]
def font_for(size):
    candidates=[os.environ.get('STAYX_FONT',''),'C:/Windows/Fonts/arialbd.ttf','DejaVuSans-Bold.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
    for candidate in candidates:
        if not candidate:continue
        try:return ImageFont.truetype(candidate,size)
        except OSError:pass
    raise RuntimeError('Set STAYX_FONT to a bold TTF font file')
