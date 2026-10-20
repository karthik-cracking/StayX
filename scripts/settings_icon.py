from pathlib import Path
import sys
from PIL import Image
r=Path(sys.argv[1])/'res/drawable'
im=Image.open(r/'morphe_notification_icon_custom.png').convert('RGBA')
glyph=im.crop(im.getchannel('A').getbbox())
scale=176/max(glyph.size)
glyph=glyph.resize((round(glyph.width*scale),round(glyph.height*scale)),Image.Resampling.LANCZOS)
icon=Image.new('RGBA',(192,192),(0,0,0,0))
icon.alpha_composite(glyph,((192-glyph.width)//2,(192-glyph.height)//2))
assert icon.getpixel((0,0))[3]==0
icon.save(r/'stayx_brand_logo.png',optimize=True)
