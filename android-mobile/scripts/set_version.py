"""Keep the base version label while assigning an update-safe test build code.
SPDX-License-Identifier: GPL-3.0-only
"""
import argparse
from pathlib import Path
import re
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('decoded', type=Path)
parser.add_argument('--version-code', type=int, default=1561304942)
parser.add_argument('--version-name', default='21.30.216')
args = parser.parse_args()
if args.version_code < 1561304942 or args.version_code > 2147483647:
    parser.error('version code must be between 1561304942 and 2147483647')
android = 'http://schemas.android.com/apk/res/android'
ET.register_namespace('android', android)
path = args.decoded / 'AndroidManifest.xml'
tree = ET.parse(path)
manifest = tree.getroot()
assert manifest.get('package') == 'com.tubemod.android.youtube'
manifest.set('{'+android+'}versionCode', str(args.version_code))
manifest.set('{'+android+'}versionName', args.version_name)
tree.write(path, encoding='utf-8', xml_declaration=True)
path = args.decoded / 'apktool.yml'
text = path.read_text(encoding='utf-8')
for key, value in [('versionCode', str(args.version_code)), ('versionName', args.version_name)]:
    text, count = re.subn(r'(?m)^(\s{2}'+key+r':)\s*.*$', lambda m: m[1]+' '+value, text)
    assert count == 1, 'Expected exactly one '+key+' in apktool.yml'
path.write_text(text, encoding='utf-8')
print('Version:', args.version_code, args.version_name)
