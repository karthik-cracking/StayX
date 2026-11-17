# StayX Android 1.1.0 installation

This is a test update using YouTube 21.30.216 with Morphe patches 2.3.0-dev.8. Device playback testing determines whether it fixes the reported stalls. The app keeps the StayX name, original YouTube launcher icon and existing application package. Its Android version name stays exactly `21.30.216` for upstream compatibility checks; the StayX 1.1 test label appears in About text and file names.

Update the existing app using the signed `StayX-v1.1.0.apk`. Keep the current app installed so Android can attempt to retain its settings and downloads. The package has a higher update code and uses the existing mobile signing certificate.

This test build includes a legacy Cast compatibility guard to skip the Cast initialization path associated with the startup crash. **Casting is unavailable in this variant.** The initial device observation passed settings use, normal video playback and picture-in-picture for three minutes. That result does not establish that every stream or background playback scenario works.

APK SHA-256: `47f1a1f0e189fdce8daeed5a284caa6ff682141138c57db1c9cae58da4b94397`.

**Existing settings are preserved.** The new build defaults allow normal and Shorts background playback, but previously saved values override those defaults. After updating, open the app's StayX settings, find the background playback controls and:

1. Turn **Remove background playback restrictions** on.
2. Turn **Disable Shorts background playback** off.
3. Leave other optional features at your preferred values.

If an older saved setting has a different label, use the StayX settings search for “background.” Check normal videos and Shorts with the screen on, then while another app is in front or the screen is locked. Also check that your chosen spoof stream client loads several videos without repeated stalls. A successful installation alone does not establish that playback is fixed.

The source ZIP contains the build recipe, branding/default modifications, selected patch settings, upstream source links and license notices. It excludes Google's APK, downloaded build tools, signing keys, passwords and phone logs. Build output is unsigned; anyone rebuilding must provide the pinned base/tools and sign with their own private key. A different signing key cannot replace the existing installation as an update.


## Device test result

Installed as an update on the existing Realme RMX3853 running Android 16, preserving app data and sign-in. Normal video playback and Home picture-in-picture were observed. Android reported playback continuing with the screen off; the user confirmed “Playback and background audio work” after being asked to test videos and scrolling Shorts. These finite tests do not guarantee every video or network condition. Casting initialization remains disabled for compatibility with the existing MicroG.


The 1.1.0 release also replaces the M startup animation with the StayX SX logo used in settings. Its signed APK was installed and the centered SX startup screen was visually checked.
