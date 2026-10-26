# TV validation

Validation date: 2026-10-26. Device: Amazon AFTSSS, Fire OS 7.7.1.7, Android 9/API 28, ARMv7. Device identifiers, accounts, private logs and signing keys are excluded.

## Observed on the device

- StayX installs alongside the original Amazon YouTube package.
- YouTube TV home/search and several fullscreen videos rendered, with remote controls.
- Remote Menu opens StayX Settings; the download toggle persists after app restart.
- The ad-block setting was enabled, with no ads seen in the sampled sessions. This does not establish universal or future ad blocking.
- The final tv5 build showed one remote-focusable Download video button. Selecting it handed off the correct video ID; switching downloads off removed the button, and re-enabling restored it.
- StayX passed the currently playing test video ID `jNQXAC9IVRw` to the explicitly selected YTDLnis companion.
- YTDLnis saved the 19-second video in the TV's local Download folder. Extraction took several minutes and required Resume all once during first-run testing.
- The copied test file contained AV1 video and Opus audio. FFmpeg decoded the entire file without errors. VLC then opened and played the actual saved file on the Fire TV.

These are ordinary Android ADB/UI observations and local media checks, not REA runtime captures. Source-level availability of SponsorBlock, DeArrow, queue, PiP and other preferences is not a claim that every feature was exercised.

## Static package analysis

REA inspected the upstream Cobalt ARM v2.0.3 APK, SHA-256 `72a3527f520db3a1b414916ad96481244e451c41e272ae33344ae5e79abb37dd`.

- Parent Evidence: `ev_2e8205cc3244aa90b0f81f1dec879200cc5fdff3b8a300dc73dba5e21a7c754e`
- Summary Evidence: `ev_4c767f4396286416be08c2763ef835615a0bfbebf24d3d1826e5884d48a4cc86`
- Manifest: minimum API 24, target API 36; upstream package `io.gh.reisxd.tizentube.cobalt`, version 2.0.3.

This analysis identifies the artifact and code layout; it does not prove execution or safety. Native Cobalt was reused from the pinned upstream release. The complete customized APK was rebuilt and signed separately.

## Build checks

The published build driver was run from fresh directories for ARM and ARM64. Each build verifies its pinned input SHA-256, compiles all bridge/nested Java classes, adds their DEX, preserves the upstream native ABI, aligns the APK and verifies its v2/v3 signatures. Both compiled manifests declare visibility of `com.deniscerri.ytdl`, required by the bridge's package check on Android 11+.

The runtime inside each APK must match repository `tv.js`. Native loader replacements are equal-length and point to an immutable repository tag. Final artifact digests and runtime identity are recorded in the adjacent JSON files.

ARM64 and Android TV 12+ were not available for physical testing. Google login, casting, HDR/DRM, battery behavior, every settings combination, and long-session stability remain unverified.
