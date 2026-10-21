# StayX for iPhone — personal build

Native iOS customization based on [SmartTubeIOS](https://github.com/milika/SmartTubeIOS), pinned to commit `e659ce9268c02857fb3769cc2aa2e0efc516e36e`. This is a separate Swift app, not a conversion or patch of the Android APK. The Android release on `main` is unaffected.

Target device: iPhone 12 on iOS 26.5. Minimum deployment target: iOS 17. Hardware playback and download success still require testing on the phone; a successful build is not proof that every YouTube stream works.

## Included

- Native AVPlayer stream playback with quality/speed controls, queue, mini-player, optional background audio, and PiP.
- Download actions in video menus/player. Downloads save to Photos and the app's Library → Downloads. Photos add permission is requested at download time.
- Optional SponsorBlock, DeArrow, appearance/feed controls, captions and audio tracks.
- StayX app name, YouTube-style launcher artwork, GPL credits in Settings, dark theme default.
- Native player default. Settings → StayX → Use official embedded player provides a fallback; the embedded player can show ads and has different controls.
- SponsorBlock/background audio/autoplay start off. Existing upstream settings allow individual control of optional features.
- Firebase removed from the package. Logs remain on device; there is no remote crash-reporting SDK.
- No Apple credentials, private signing keys, GoogleService configuration, or personal device identifiers in the project.

## Build on a hosted Mac

The `StayX iOS` GitHub workflow uses a standard macOS runner. It builds an unsigned arm64 IPA and runs a simulator settings/control smoke test. It does not request an Apple ID or upload signing credentials.

For a local Mac with Xcode, `brew install xcodegen just`, then run `just ci` from this directory. XcodeGen generates a separate project; the upstream Xcode project is not hand-edited. The vendored Swift package has no external Swift package dependencies.

The build's downloadable `StayX-iOS-build` artifact contains the unsigned IPA, logs, checksums, and simulator test results. Unsigned IPA files cannot launch on a real iPhone until signed.

## Install using Windows

Use [AltServer/AltStore Classic](https://faq.altstore.io/altstore-classic/how-to-install-altstore-windows) from the official vendor. Install Apple's required desktop components, connect/unlock the iPhone and trust the PC. Enter your Apple account directly into the local signing tool, never into chat or GitHub. Install the generated IPA through AltStore. A free personal account requires periodic refresh, generally every seven days.

This personal target includes no app extensions, App Groups, push, or iCloud entitlements, which simplifies free-account signing. Widgets, Safari/share extensions, iCloud sync, and Live Activity progress are not included. Background audio and PiP still depend on iOS permissions and actual stream support.

## Investigation

YouTube tweak bundles such as uYouEnhanced/YTLite require a separately supplied decrypted YouTube IPA. YTLite also moved newer versions to a subscription. The source-based native client can be compiled without an original Google IPA. See `UPSTREAM.json` for the pinned source and modifications, and `UPSTREAM-README.md` for the original project's description. Native playback does not request video-ad segments; this is not a guarantee against all future ad formats, server changes, account restrictions, or unavailable streams.

## License

GPL-3.0, preserving the original authors' rights and source attribution. See `LICENSE`. This is an independent derivative called StayX, not an official SmartTube/Google/YouTube product. The logo shape and names of third-party services retain their respective rights. Modified source is vendored here so the exact personal build can be reviewed and rebuilt.
