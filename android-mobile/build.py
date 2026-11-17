"""Build an unsigned StayX 1.1 playback-test candidate from pinned compatible inputs.
SPDX-License-Identifier: GPL-3.0-only
"""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    'input': '3775a15129dcc4e5b80fc17b7e0841b7fdd1ca89a6e72baa798806f666c74d02',
    'morphe': '5ca0320ee05481df1ae3afd2f003bba3ff994d11d1f66ae48811ced71355e4fe',
    'patches': '1282547ca7cdfd5352119e73b31cf7c051dbf8d3ae9bd3c5319edb1c246d3331',
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['input','morphe','patches','apktool','work']:
        parser.add_argument('--'+key, type=Path, required=True)
    parser.add_argument('--java', default='java')
    parser.add_argument('--version-code',type=int,default=1561304942)
    args=parser.parse_args()
    for key,expected in EXPECTED.items():
        with getattr(args,key).open('rb') as stream:
            digest=hashlib.file_digest(stream,'sha256').hexdigest()
        if digest!=expected:parser.error('Pinned SHA-256 mismatch for '+key)
    work=args.work.resolve()
    if work.exists():parser.error('Use a fresh, non-existing --work directory')
    work.mkdir(parents=True)
    def run(*command):
        with (work/'build.log').open('a',encoding='utf-8') as log:
            subprocess.run([str(arg) for arg in command],stdout=log,stderr=subprocess.STDOUT,check=True)
    run(args.java,'-Xmx8G','-jar',args.morphe.resolve(),'patch',args.input.resolve(),
        '-p',args.patches.resolve(),'--options-file',ROOT/'config/patch-options.json',
        '--unsigned','--out',work/'patched.apk','--result-file',work/'patch-result.json',
        '-t',work/'scratch')
    result=json.loads((work/'patch-result.json').read_text(encoding='utf-8-sig'))
    if not result.get('success') or result.get('failedPatches') or not all(s.get('success') for s in result['stepResults']):
        raise RuntimeError('A patch step failed; see patch-result.json and build.log')
    run(args.java,'-jar',args.apktool.resolve(),'d',work/'patched.apk','-s','-o',work/'decoded')
    for script in ['rebrand.py','notification_icons.py','polish.py','restore_icon.py','settings_icon.py','startup_logo.py']:
        run(sys.executable,ROOT/'scripts'/script,work/'decoded')
    run(args.java,'-cp',args.morphe.resolve(),ROOT/'scripts/java/StayXBranding.java',work/'decoded',work/'about.html')
    run(args.java,'-cp',args.morphe.resolve(),ROOT/'scripts/java/OptionalDefaults.java',work/'decoded',ROOT/'config/optional-switches.txt')
    run(args.java,'-cp',args.morphe.resolve(),ROOT/'scripts/java/LegacyCastCompatibility.java',work/'decoded')
    run(args.java,'-cp',args.morphe.resolve(),ROOT/'scripts/java/StayXStartupCompatibility.java',work/'decoded')
    run(sys.executable,ROOT/'scripts/set_version.py',work/'decoded','--version-code',args.version_code)
    run(sys.executable,ROOT/'scripts/theme_configs.py','prepare',work)
    run(args.java,'-jar',args.apktool.resolve(),'b',work/'decoded','-o',work/'unsigned.apk')
    run(sys.executable,ROOT/'scripts/theme_configs.py','restore',work)
    output=work/'theme-restored.apk'
    with output.open('rb') as stream:digest=hashlib.file_digest(stream,'sha256').hexdigest()
    report={'output':output.name,'sha256':digest,'versionCode':args.version_code,
            'versionName':'21.30.216','package':'com.tubemod.android.youtube',
            'signed':False,'device_tested':False}
    (work/'unsigned-build.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
