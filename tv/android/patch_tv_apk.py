"""StayX TV resource/Java/native-loader patch for pinned Cobalt v2.0.3.
SPDX-License-Identifier: GPL-3.0-only
"""
from pathlib import Path
import argparse, hashlib, json, re, zipfile
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser()
parser.add_argument('decoded',type=Path)
parser.add_argument('--artwork-apk',type=Path,required=True,help='Original YouTube TV base APK used for launcher artwork')
parser.add_argument('--runtime',type=Path,default=ROOT/'tv.js')
args=parser.parse_args()
decoded=args.decoded.resolve()
android='http://schemas.android.com/apk/res/android'
ET.register_namespace('android',android)
tree=ET.parse(decoded/'AndroidManifest.xml');manifest=tree.getroot()
old_package=manifest.get('package')
assert old_package in ('io.gh.reisxd.tizentube.cobalt','com.stayx.tv')
old_package='io.gh.reisxd.tizentube.cobalt'
manifest.set('package','com.stayx.tv')
manifest.set('{'+android+'}versionName','1.0.0-tv')
manifest.set('{'+android+'}versionCode','1000001')
app=manifest.find('application');app.set('{'+android+'}label','StayX')
app.set('{'+android+'}debuggable','false')
for item in list(manifest.findall('uses-permission')):
    if item.get('{'+android+'}name')=='android.permission.REQUEST_INSTALL_PACKAGES':manifest.remove(item)
tree.write(decoded/'AndroidManifest.xml',encoding='utf-8',xml_declaration=True)
for pattern in ['*.xml','*.smali']:
    for path in decoded.rglob(pattern):
        try:text=path.read_text(encoding='utf-8')
        except UnicodeDecodeError:continue
        updated=text.replace(old_package,'com.stayx.tv')
        if path.name=='DIALServer.smali':updated=updated.replace('TizenTube','StayX')
        if updated!=text:path.write_text(updated,encoding='utf-8')

yml=decoded/'apktool.yml'
text=yml.read_text(encoding='utf-8').replace('versionCode: 203','versionCode: 1000001').replace('versionName: 2.0.3','versionName: 1.0.0-tv')
yml.write_text(text,encoding='utf-8')

bridge=decoded/'smali_classes2/dev/cobalt/coat/BaseStarboardBridge.smali'
text=bridge.read_text(encoding='utf-8')
pattern=r'(\.method protected installAppFromURL\(Ljava/lang/String;\)Z[\s\S]*?)(    \.line 1040)'
prefix='''    iget-object v0, p0, Ldev/cobalt/coat/BaseStarboardBridge;->mAppContext:Landroid/content/Context;
    invoke-static {v0, p1}, Lcom/stayx/tv/StayXBridge;->handle(Landroid/content/Context;Ljava/lang/String;)Z
    move-result v0
    return v0
'''
text,n=re.subn(pattern,lambda m:m.group(1)+prefix+m.group(2),text,count=1);assert n==1
bridge.write_text(text,encoding='utf-8')

activity=decoded/'smali_classes2/dev/cobalt/coat/CobaltActivity.smali'
text=activity.read_text(encoding='utf-8')
pattern=r'(\.method public onKeyDown\(ILandroid/view/KeyEvent;\)Z[\s\S]*?)(    \.line 395)'
prefix='''    invoke-static {p0, p1}, Lcom/stayx/tv/StayXBridge;->menuKey(Landroid/app/Activity;I)Z
    move-result v0
    if-eqz v0, :stayx_original_key
    const/4 v0, 0x1
    return v0
    :stayx_original_key
'''
text,n=re.subn(pattern,lambda m:m.group(1)+prefix+m.group(2),text,count=1);assert n==1
pattern=r'(\.method protected onResume\(\)V\s+\.locals \d+\s+)'
text,n=re.subn(pattern,lambda m:m.group(1)+'    invoke-static {p0}, Lcom/stayx/tv/StayXBridge;->attach(Landroid/app/Activity;)V\n\n',text,count=1);assert n==1
activity.write_text(text,encoding='utf-8')

with zipfile.ZipFile(args.artwork_apk) as source:
    icon=source.read('res/o-.png')
    banner=source.read('res/dN.png')
for path in decoded.glob('res/mipmap*/ic_app*'):
    if path.is_file():path.write_bytes(icon)
for path in decoded.glob('res/drawable*/app_banner*'):
    if path.is_file():path.write_bytes(banner)
(decoded/'assets/cobalt_logo_1024.png').write_bytes(icon)
(decoded/'assets/stayx-runtime.js').write_bytes(args.runtime.read_bytes())

old=b'https://cdn.jsdelivr.net/npm/@foxreis/tizentube/dist/userScript.js'
new=b'https://cdn.jsdelivr.net/gh/karthik-cracking/StayX@tv2/tv.js?s=tv1'
assert len(old)==len(new)
patched=[]
for path in decoded.glob('lib/*/libchrobalt.so'):
    data=path.read_bytes();assert data.count(old)==2
    output=data.replace(old,new);assert len(data)==len(output)
    path.write_bytes(output)
    patched.append({'abi':path.parent.name,'native_loader_replacements':2,'native_bytes_preserved':len(output),'sha256':hashlib.sha256(output).hexdigest()})
assert patched
(decoded/'assets/StayX-NOTICE.txt').write_text('StayX TV is an independent customization of TizenTube Cobalt v2.0.3 and TizenTube userscript 1.15.2.\nCobalt/Chromium: BSD notices and upstream third-party licenses apply.\nTizenTube and StayX JavaScript/bridge modifications: GPL-3.0-only.\nSource, build details and credits: https://github.com/karthik-cracking/StayX\nYouTube artwork and service belong to their respective owners.\n',encoding='utf-8')
print(json.dumps({'package':'com.stayx.tv','version':'1.0.0-tv','native_patches':patched,'icon_sha256':hashlib.sha256(icon).hexdigest(),'banner_sha256':hashlib.sha256(banner).hexdigest()}))
