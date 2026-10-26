#!/usr/bin/env python3
"""Build a StayX TV customization from verified Cobalt v2.0.3 inputs.

SPDX-License-Identifier: GPL-3.0-only
Requires Python 3.11+, a JDK, Android SDK tools and APKtool 3.0.3.
Signing keys remain outside this source tree and are supplied by the operator.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUTS = {
    "arm": "72a3527f520db3a1b414916ad96481244e451c41e272ae33344ae5e79abb37dd",
    "arm64": "4e3df211abb243cb06b06ba3676fe62c3d5b59baa47c1a0050cb180b3493e539",
}
ARTWORK_SHA256 = "b4db25f33c95c131a1d1016c24c5a07c2d8829d04442d36305c1f89be62e3b0a"


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def run(*args: object) -> None:
    subprocess.run([str(arg) for arg in args], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--abi", choices=INPUTS, required=True)
    parser.add_argument("--apk", type=Path, required=True, help="Pinned upstream release APK")
    parser.add_argument("--artwork-apk", type=Path, required=True, help="Original YouTube TV base.apk")
    parser.add_argument("--sdk", type=Path, required=True, help="Android SDK directory")
    parser.add_argument("--jdk", type=Path, required=True, help="JDK directory containing bin/")
    parser.add_argument("--apktool", type=Path, required=True, help="APKtool 3.0.3 JAR")
    parser.add_argument("--runtime", type=Path, default=ROOT / "tv.js")
    parser.add_argument("--platform", default="android-34")
    parser.add_argument("--build-tools", default="36.0.0")
    parser.add_argument("--build-dir", type=Path, required=True, help="New directory; existing directories are rejected")
    parser.add_argument("--output", type=Path, required=True, help="New signed APK path")
    parser.add_argument("--keystore", type=Path, required=True, help="Existing external signing keystore")
    parser.add_argument("--key-alias", required=True)
    parser.add_argument("--password-env", default="STAYX_TV_KEY_PASSWORD", help="Name of environment variable holding the keystore password")
    args = parser.parse_args()

    if not os.environ.get(args.password_env):
        parser.error(f"Set the {args.password_env} environment variable locally before building")
    suffix = ".exe" if os.name == "nt" else ""
    java = args.jdk / "bin" / ("java" + suffix)
    javac = args.jdk / "bin" / ("javac" + suffix)
    android_jar = args.sdk / "platforms" / args.platform / "android.jar"
    tools = args.sdk / "build-tools" / args.build_tools
    zipalign = tools / ("zipalign" + suffix)
    r8 = tools / "lib" / "d8.jar"
    # Android SDK packages use d8.jar; some distributions call the same driver r8.jar.
    if not r8.is_file():
        r8 = tools / "lib" / "r8.jar"
    apksigner = tools / "lib" / "apksigner.jar"
    for path in [args.apk, args.artwork_apk, args.runtime, args.apktool, args.keystore,
                 java, javac, android_jar, zipalign, r8, apksigner]:
        if not path.is_file():
            parser.error(f"Required file does not exist: {path}")
    if sha256(args.apk) != INPUTS[args.abi]:
        parser.error("Upstream APK SHA-256 does not match the pinned Cobalt v2.0.3 release")
    if sha256(args.artwork_apk) != ARTWORK_SHA256:
        parser.error("Artwork APK SHA-256 does not match the supplied YouTube TV 7.29.300 base APK")
    if args.build_dir.exists() or args.output.exists():
        parser.error("Use a new build directory and output path; no existing files will be replaced")

    work = args.build_dir.resolve()
    work.mkdir(parents=True)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    decoded = work / "decoded"
    classes = work / "helper-classes"
    dex = work / "helper-dex"
    classes.mkdir()
    dex.mkdir()
    run(java, "-jar", args.apktool.resolve(), "d", args.apk.resolve(), "-o", decoded)
    run(sys.executable, HERE / "patch_tv_apk.py", decoded,
        "--artwork-apk", args.artwork_apk.resolve(), "--runtime", args.runtime.resolve())
    sources = sorted((HERE / "java").rglob("*.java"))
    run(javac, "--release", "8", "-cp", android_jar.resolve(), "-d", classes, *sources)
    # Include anonymous/nested classes, not only StayXBridge.class.
    run(java, "-cp", r8.resolve(), "com.android.tools.r8.D8", "--lib", android_jar.resolve(),
        "--min-api", "24", "--output", dex, *sorted(classes.rglob("*.class")))
    unsigned = work / "unsigned.apk"
    run(java, "-jar", args.apktool.resolve(), "b", decoded, "-o", unsigned)
    with zipfile.ZipFile(unsigned, "a", compression=zipfile.ZIP_DEFLATED) as archive:
        expected = {"classes.dex", "classes2.dex", "classes3.dex"}
        observed = {name for name in archive.namelist() if "/" not in name and name.endswith(".dex")}
        if observed != expected:
            raise RuntimeError(f"Unexpected upstream DEX layout: {sorted(observed)}")
        archive.write(dex / "classes.dex", "classes4.dex")
    aligned = work / "aligned.apk"
    run(zipalign, "-P", "16", "-f", "4", unsigned, aligned)
    run(java, "-jar", apksigner.resolve(), "sign", "--ks", args.keystore.resolve(),
        "--ks-key-alias", args.key_alias, "--ks-pass", "env:" + args.password_env,
        "--out", output, aligned)
    run(java, "-jar", apksigner.resolve(), "verify", "--verbose", output)
    run(zipalign, "-c", "-P", "16", "4", output)
    digest = sha256(output)
    output.with_suffix(output.suffix + ".sha256").write_text(
        digest + "  " + output.name + "\n", encoding="utf-8")
    report = {"abi": args.abi, "input_sha256": INPUTS[args.abi],
              "runtime_sha256": sha256(args.runtime), "output_sha256": digest,
              "bytes": output.stat().st_size, "package": "com.stayx.tv", "version": "1.0.0-tv",
              "device_tested_by_this_command": False}
    output.with_suffix(output.suffix + ".build.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
