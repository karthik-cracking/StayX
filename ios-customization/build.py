# SPDX-License-Identifier: GPL-3.0-only
"""Apply the StayX name and optional metadata repair to the reviewed IPA.

Input is supplied separately; this script does not fetch or distribute YouTube.
The output must be signed again before installation.
"""
from pathlib import Path
import argparse
import hashlib
import json
import plistlib
import zipfile

SOURCE_SHA256 = 'd5aab0da9f45adb1a643b6852a1bd5c0a62824cbf3800e78427091d380e9225f'
APP = 'Payload/YouTube.app/'

def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def main():
    if not __debug__:
        raise SystemExit("Run without Python optimization flags so validation remains enabled")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--repair-extension-metadata', action='store_true',
                        help='Remove replication targets for absent app extensions')
    args = parser.parse_args()
    assert args.input.resolve() != args.output.resolve(), 'Preserve the input IPA'
    assert sha256(args.input) == SOURCE_SHA256, 'Input differs from the inspected release'
    assert not args.output.exists(), 'Output already exists; choose a new path'
    changed = []
    removed_extension_targets = []
    with zipfile.ZipFile(args.input) as source, zipfile.ZipFile(args.output, 'w') as target:
        assert source.testzip() is None, 'Input CRC failure'
        archive_names = set(source.namelist())
        for entry in source.infolist():
            data = source.read(entry.filename)
            main_info = entry.filename == APP + 'Info.plist'
            localized_info = (entry.filename.startswith(APP) and
                              entry.filename.count('/') == 3 and
                              entry.filename.endswith('.lproj/InfoPlist.strings'))
            if args.repair_extension_metadata and entry.filename == APP + 'SC_Info/Manifest.plist':
                manifest = plistlib.loads(data)
                remaining = []
                for path in manifest['SinfReplicationPaths']:
                    extension = path.split('.appex/', 1)[0] + '.appex/' if '.appex/' in path else None
                    if extension and APP + extension + 'Info.plist' not in archive_names:
                        removed_extension_targets.append(path)
                    else:
                        remaining.append(path)
                assert len(removed_extension_targets) == 6, 'Unexpected extension metadata layout'
                manifest['SinfReplicationPaths'] = remaining
                fmt = plistlib.FMT_BINARY if data.startswith(b'bplist') else plistlib.FMT_XML
                data = plistlib.dumps(manifest, fmt=fmt, sort_keys=False)
                changed.append(entry.filename)
            if main_info or localized_info:
                info = plistlib.loads(data)
                before = dict(info)
                for key in ('CFBundleDisplayName', 'CFBundleName'):
                    if key in info:
                        info[key] = 'StayX'
                if info != before:
                    fmt = plistlib.FMT_BINARY if data.startswith(b'bplist') else plistlib.FMT_XML
                    data = plistlib.dumps(info, fmt=fmt, sort_keys=False)
                    changed.append(entry.filename)
            target.writestr(entry, data)
    with zipfile.ZipFile(args.input) as source, zipfile.ZipFile(args.output) as target:
        assert target.testzip() is None, 'Output CRC failure'
        assert source.namelist() == target.namelist(), 'Archive membership changed'
        verified_unchanged = 0
        for name in source.namelist():
            original, result = source.read(name), target.read(name)
            if name in changed:
                before, after = plistlib.loads(original), plistlib.loads(result)
                changed_keys = {key for key in before.keys() | after.keys() if before.get(key) != after.get(key)}
                if name == APP + 'SC_Info/Manifest.plist':
                    assert changed_keys == {'SinfReplicationPaths'}
                    assert before['SinfPaths'] == after['SinfPaths']
                    assert after['SinfReplicationPaths'] == [p for p in before['SinfReplicationPaths'] if p not in removed_extension_targets]
                    assert len(after['SinfReplicationPaths']) == 2
                else:
                    assert changed_keys <= {'CFBundleDisplayName', 'CFBundleName'}
                    assert after['CFBundleDisplayName'] == 'StayX'
            else:
                assert original == result, f'Unexpected change: {name}'
                verified_unchanged += 1
        assert len(changed) == (81 if args.repair_extension_metadata else 80), 'Unexpected changed file count'
    report = {
        'input_sha256': SOURCE_SHA256,
        'output_sha256': sha256(args.output),
        'output_filename': args.output.name,
        'changed_files': changed,
        'name_keys_changed_only': ['CFBundleDisplayName', 'CFBundleName'],
        'extension_metadata_repair': {'enabled': args.repair_extension_metadata,
            'manifest_key_changed': 'SinfReplicationPaths' if args.repair_extension_metadata else None,
            'removed_targets_for_absent_extensions': removed_extension_targets,
            'existing_framework_and_main_app_targets': 'preserved'},
        'byte_identical_other_archive_entries': verified_unchanged,
        'icon_executable_libraries_and_player_resources': 'unchanged byte for byte',
        'bundle_identifier': 'unchanged; personal signing is required',
        'signature_status': 'Package edits invalidate existing signatures; re-sign with AltServer',
        'modified_build_phone_validation': 'pending installation and launch',
    }
    args.output.with_suffix('.verification.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key != 'changed_files'}, indent=2))

if __name__ == '__main__':
    main()
