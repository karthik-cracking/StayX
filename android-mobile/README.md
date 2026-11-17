# StayX Android mobile 1.1.0

This prerelease rebuild uses the explicitly compatible YouTube **21.30.216** base and Morphe patches **2.3.0-dev.8** with Morphe Desktop **2.2.0**. It keeps package `com.tubemod.android.youtube`, StayX display branding, the original YouTube launcher icon and upstream GPL credits. It does not use the CLI compatibility override.

The selected patches provide ad controls, downloads through YTDLnis, SponsorBlock, speed, quality, swipe, picture-in-picture, queue and optional appearance/Shorts controls. Existing optional defaults remain off. Normal background playback is now enabled by default and Shorts background playback is allowed (`morphe_remove_background_playback_restrictions=true`, `morphe_shorts_disable_background_playback=false`). Existing saved user preferences take precedence over defaults; an installed app with explicit old values must change these settings locally.

The app's update code is **1561304942**, greater than the older installed build. Its Android version name stays exactly `21.30.216` because upstream compatibility checks require the original version string. The StayX 1.1 test label appears only in About text and artifact names. `scripts/set_version.py` updates both the manifest and APKtool version fields. A higher code only enables an update attempt; the signing certificate must also match the installed application.

This compatibility variant restores the legacy Morphe Cast-context early-return guard. `LegacyCastCompatibility.java` locates exactly one void method containing `Error fetching CastContext.` and replaces its body with `return-void`. On this pinned base it matches `Lamvm;->a(Lurz;)V` in `classes2.dex`. **Casting is unavailable in this variant.** The guard avoids the Cast initialization path that crashed on the test setup; it does not establish a universal fix for every playback problem. After this change, the test phone remained running through settings, a normal playing video and picture-in-picture for an initial three-minute observation. Screen-off and broader playback checks remain separate runtime tests.

## Pinned inputs

| Input | SHA-256 |
| --- | --- |
| Operator-supplied YouTube 21.30.216 universal APK | `3775a15129dcc4e5b80fc17b7e0841b7fdd1ca89a6e72baa798806f666c74d02` |
| [Morphe Desktop 2.2.0](https://github.com/MorpheApp/morphe-desktop/releases/tag/v2.2.0) | `5ca0320ee05481df1ae3afd2f003bba3ff994d11d1f66ae48811ced71355e4fe` |
| [Morphe patches 2.3.0-dev.8](https://github.com/MorpheApp/morphe-patches/releases/tag/v2.3.0-dev.8) | `1282547ca7cdfd5352119e73b31cf7c051dbf8d3ae9bd3c5319edb1c246d3331` |

Use Python 3.11+, Pillow, Java (tested with Android Studio JDK 25) and APKtool 3.0.3. The generated `upstream-options.json` and `upstream-patches.txt` record the current CLI patch names/options. `config/patch-options.json` deliberately selects the prior StayX feature set rather than enabling every newly added upstream patch.

```powershell
python build.py --input "D:/inputs/youtube-21.30.216.apk" `
  --morphe "D:/tools/morphe-desktop-2.2.0-all.jar" `
  --patches "D:/tools/patches-2.3.0-dev.8.mpp" `
  --apktool "D:/tools/apktool_3.0.3.jar" `
  --java "D:/tools/jdk/bin/java.exe" `
  --work "D:/build/stayx-1.1-test-new"
```

The build rejects mismatched hashes and an existing work directory. It patches unsigned, checks the new CLI `success`/`stepResults` report, decodes resources without disassembling DEX, applies StayX branding/default edits and the legacy Cast guard, updates both version fields, rebuilds and restores Morphe theme resource configurations and edited DEX. Its output is **`theme-restored.apk`**, still unsigned. `unsigned.apk` precedes theme restoration and is not the final input for signing.

Align and sign `theme-restored.apk` separately with the original private mobile signing key, then verify its APK signature and final manifest. Keep that key and passwords outside this folder. The source/build process does not install the app or erase app data. A successful build is not evidence that device playback/background playback is fixed; test those behaviors on the target phone before release.

Source modifications are GPL-3.0-only; preserve [LICENSE](LICENSE), [NOTICE](NOTICE), Morphe contributor links and notices. Google's APK is an operator input and is not included here.


## Release 1.1.0 validation and startup branding

The published APK is the phone-tested startup-logo update. Its two branded Lottie resources embed the same SX image as Settings/About. `StayXStartupCompatibility.java` routes Rive-capable startup through Lottie by disabling the two Rive-selection predicates, so the upstream M glow animation is no longer selected. The original YouTube launcher icon is preserved. A fresh launch was visually verified on the test phone.

Installed as an update on a Realme RMX3853 running Android 16 using the existing mobile signing certificate. Normal playback, picture-in-picture and screen-off playback were observed for the preceding playback build; the owner confirmed playback/background audio work after testing videos and Shorts. The final branding update was installed and its installed hash matched the published APK. These are limited single-device checks. Casting remains disabled in this compatibility variant.

The release label is **1.1.0**, while Android Settings still reports **21.30.216** for compatibility with upstream checks. Existing preferences override new background defaults. See [INSTALL.md](INSTALL.md) for updating and background settings.
