# StayX TV Android packaging source

This folder contains the Java bridge, package/resource patch and build driver used for StayX TV `1.0.0-tv` (`com.stayx.tv`). The TV player uses TizenTube Cobalt and YouTube's TV web interface. StayX supplies the name, launcher artwork selection, optional download actions, remote Menu-key settings entry and bundled runtime fallback. It preserves upstream attribution and disables the upstream arbitrary APK installer/updater route.

## Upstream inputs

Use these exact Cobalt **v2.0.3** release artifacts; the build checks their SHA-256 before decoding.

| Target | Official upstream artifact | SHA-256 |
| --- | --- | --- |
| ARMv7 / 32-bit Fire TV | [cobalt-arm.apk](https://github.com/reisxd/TizenTubeCobalt/releases/download/v2.0.3/cobalt-arm.apk) | `72a3527f520db3a1b414916ad96481244e451c41e272ae33344ae5e79abb37dd` |
| ARM64 Android TV | [cobalt-arm64.apk](https://github.com/reisxd/TizenTubeCobalt/releases/download/v2.0.3/cobalt-arm64.apk) | `4e3df211abb243cb06b06ba3676fe62c3d5b59baa47c1a0050cb180b3493e539` |

Cobalt corresponding source: [TizenTubeCobalt commit 9809b5aae6d820c852bc6cf7095304fb1c92f31a](https://github.com/reisxd/TizenTubeCobalt/tree/9809b5aae6d820c852bc6cf7095304fb1c92f31a). Cobalt includes Chromium and third-party components with their own notices; keep those notices in any rebuilt APK. This packaging recipe customizes the pinned release binary rather than compiling the entire Cobalt/Chromium toolchain.

StayX's complete modified userscript source is in [../runtime/mods](../runtime/mods), based on [TizenTube commit f99945a84ff767bf14ad8c1146e8e3fd49a3d628](https://github.com/reisxd/TizenTube/tree/f99945a84ff767bf14ad8c1146e8e3fd49a3d628). Its GPL-3.0-only license is retained in [../runtime/LICENSE](../runtime/LICENSE). The checked-in root [tv.js](../../tv.js) is the packaged runtime. Rebuild the userscript in `tv/runtime/mods` using `npm ci --ignore-scripts` followed by `npm run build`; preserve the root bundle's provenance header and initialization guard when replacing its generated body.

Launcher icon/banner bytes come from the separately supplied YouTube TV **7.29.300 base APK**, SHA-256 `b4db25f33c95c131a1d1016c24c5a07c2d8829d04442d36305c1f89be62e3b0a`. If starting with an APKM archive, extract its `base.apk` first. The package patch reads `res/o-.png` (icon) and `res/dN.png` (TV banner). This repository does not supply Google's APK; YouTube's artwork and service remain Google's property. Supplying a different APK requires reviewing and updating this pinned artwork recipe.

## Build requirements

- Python 3.11 or later.
- A JDK with `java` and `javac`; the project was built with Android Studio's bundled JDK 25 using `javac --release 8`.
- Android SDK platform `android-34` and build-tools `36.0.0` (D8, zipalign, apksigner).
- [APKtool 3.0.3](https://github.com/iBotPeaches/Apktool/releases/tag/v3.0.3).
- An existing signing keystore kept outside the repository, its alias and password. The build does not create or publish keys.

Example from the repository root (replace all paths locally):

```powershell
# Enter the password locally; it is passed to apksigner by environment variable.
$signingSecret = Read-Host 'Keystore password' -AsSecureString
$env:STAYX_TV_KEY_PASSWORD = [System.Net.NetworkCredential]::new('', $signingSecret).Password
python tv/android/build.py --abi arm `
  --apk "D:/inputs/cobalt-arm.apk" `
  --artwork-apk "D:/inputs/youtube-tv-base.apk" `
  --jdk "D:/tools/jdk" `
  --sdk "D:/tools/android-sdk" `
  --apktool "D:/tools/apktool_3.0.3.jar" `
  --build-dir "D:/build/stayx-tv-arm-new" `
  --output "D:/build/StayX-TV-arm.apk" `
  --keystore "D:/private/stayx-tv.p12" --key-alias stayx-tv
Remove-Item Env:STAYX_TV_KEY_PASSWORD
```

For ARM64, change `--abi arm64`, supply `cobalt-arm64.apk` and use new output/build paths. Choose the architecture supported by the device's operating system, not only its CPU. The tested Fire TV has a 32-bit OS and needs ARMv7. Both packages require Android API 24 or later, but that declaration alone does not establish compatibility with every television.

The script rejects mismatched upstream/artwork hashes and existing build/output paths. It performs a fresh APKtool decode, applies pinned modifications, compiles **all** Java classes (including anonymous classes), runs D8, appends the bridge as `classes4.dex`, builds/aligns/signs the APK, then verifies its signature and alignment. It writes a SHA-256 sidecar and a build report. Use the same private signing key for future updates to your installed build; a different key does not update an existing installation. APK output need not be byte-for-byte reproducible across signing keys or tool versions.

The native loader URL is an equal-length replacement pinned to the immutable `tv5` runtime tag. A guarded copy of that runtime is also bundled as `assets/stayx-runtime.js` and injected after the TV interface initializes, so an unavailable script CDN does not leave the StayX menu missing. To change the hosted runtime version, review the pinned URL in `patch_tv_apk.py`, keep its native-string length constraint and build/test a new APK. Do not silently move an existing runtime tag.

## Optional download helper

The Java bridge accepts only `stayx://download` with an 11-character YouTube video ID, or `stayx://downloads`. It uses explicit Android intents to the separately installed [YTDLnis](https://github.com/deniscerri/ytdlnis) app; no shell command or arbitrary installer is exposed. YTDLnis must be set up and allowed to save files on the device. StayX does not embed the helper or its download engine. Download success depends on the helper, network and video's availability; a queued request is not a completed file.

## Validation scope

The ARM build has been installed on an Amazon AFTSSS running Fire OS **7.7.1.7**, Android 9/API 28. YouTube TV fullscreen playback and the remote-accessible StayX settings menu were observed. ARM64 packaging/signatures were checked, but Android TV 12+ device testing is still required. Download completion and other optional feature checks are documented separately as testing progresses; their presence in source is not evidence of successful playback/downloads on every device.

## Licenses

StayX Java/patch/build modifications and the TizenTube userscript are GPL-3.0-only; see [LICENSE](LICENSE). Cobalt/Chromium retain their [upstream BSD license](LICENSE-Cobalt) and third-party licenses. The native binary is supplied by the separately linked upstream project, not relicensed wholesale by this folder. Keep upstream license resources and contributor credits when distributing a customized package. YouTube is not affiliated with StayX.
