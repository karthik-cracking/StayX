"""Build StayX from an operator-supplied APK and a private signing key.

SPDX-License-Identifier: GPL-3.0-only
"""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
from fetch_tools import fetch
ROOT=Path(__file__).resolve().parents[1]
EXPECTED='2d1afe26c399b7c820d862e243d4335a209505f3d7c164f679952a93fcb3aea4'
def run(*args):
    print('Running',Path(str(args[0])).name,flush=True)
    subprocess.run([str(x) for x in args],cwd=ROOT,check=True)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',required=True,type=Path)
    p.add_argument('--keystore',required=True,type=Path)
    p.add_argument('--alias',default='stayx')
    p.add_argument('--java',default='java')
    p.add_argument('--build-tools',required=True,type=Path,help='Android SDK build-tools directory containing zipalign and lib/apksigner.jar')
    p.add_argument('--tools',type=Path,default=ROOT/'.tools')
    p.add_argument('--work',type=Path,help='Fresh, non-existing build directory')
    p.add_argument('--out',type=Path,default=ROOT/'dist/StayX.apk')
    a=p.parse_args()
    a.input=a.input.resolve();a.keystore=a.keystore.resolve();a.build_tools=a.build_tools.resolve();a.out=a.out.resolve()
    for key in ['STAYX_KEYSTORE_PASSWORD','STAYX_KEY_PASSWORD']:
        if not os.environ.get(key):raise RuntimeError(f'Set {key} in your environment; never commit it')
    if not a.keystore.is_file():raise FileNotFoundError(a.keystore)
    if hashlib.file_digest(a.input.open('rb'),'sha256').hexdigest()!=EXPECTED:
        raise RuntimeError('Input APK does not match the supported YouTube 21.42.243 build. Do not force a different input.')
    tools=fetch(a.tools);work=(a.work or ROOT/'build/local').resolve()
    if work.exists():raise RuntimeError('Use a fresh --work directory; existing builds are never deleted automatically')
    work.mkdir(parents=True);a.out.parent.mkdir(parents=True,exist_ok=True)
    java=a.java;morphe=tools/'morphe.jar';apktool=tools/'apktool.jar'
    run(java,'-Xmx8G','-jar',morphe,'patch',a.input,'-p',tools/'patches.mpp','--options-file',ROOT/'config/patch-options.json','--force','--unsigned','--out',work/'patched.apk','--result-file',work/'patch-result.json')
    result=json.loads((work/'patch-result.json').read_text(encoding='utf-8-sig'))
    if result.get('failedPatches') or not all(s.get('success') for s in result['patchingSteps']):raise RuntimeError('A patch/build step failed')
    decoded=work/'decoded'
    run(java,'-jar',apktool,'d',work/'patched.apk','-s','-o',decoded)
    for script in ['rebrand.py','notification_icons.py','polish.py','restore_icon.py','settings_icon.py']:
        run(sys.executable,ROOT/'scripts'/script,decoded)
    run(java,'-cp',morphe,ROOT/'scripts/java/StayXBranding.java',decoded,work/'about.html')
    run(java,'-cp',morphe,ROOT/'scripts/java/OptionalDefaults.java',decoded,ROOT/'config/optional-switches.txt')
    run(sys.executable,ROOT/'scripts/theme_configs.py','prepare',work)
    run(java,'-jar',apktool,'b',decoded,'-o',work/'unsigned.apk')
    run(sys.executable,ROOT/'scripts/theme_configs.py','restore',work)
    zipalign=a.build_tools/('zipalign.exe' if os.name=='nt' else 'zipalign')
    signer=a.build_tools/'lib/apksigner.jar'
    run(zipalign,'-P','16','-f','4',work/'theme-restored.apk',work/'aligned.apk')
    run(java,'-jar',signer,'sign','--ks',a.keystore,'--ks-pass','env:STAYX_KEYSTORE_PASSWORD','--key-pass','env:STAYX_KEY_PASSWORD','--ks-key-alias',a.alias,'--out',a.out,work/'aligned.apk')
    run(java,'-jar',signer,'verify','--verbose',a.out)
    digest=hashlib.file_digest(a.out.open('rb'),'sha256').hexdigest()
    (a.out.parent/(a.out.name+'.sha256')).write_text(digest+'  '+a.out.name+'\n')
    print('Built',a.out,'SHA-256',digest)
if __name__=='__main__':main()
