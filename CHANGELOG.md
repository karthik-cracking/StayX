# Changelog

## 1.1.0 — 2026-11-17

- Moved mobile to supported YouTube 21.30.216 and Morphe 2.3.0-dev.8 without the compatibility override.
- Enabled background playback defaults, including Shorts; existing saved preferences take precedence.
- Restored a legacy Cast initialization guard for the existing MicroG setup; casting is disabled.
- Replaced the M startup animation with the SX logo from StayX settings, preserving the YouTube launcher icon.
- Added updated mobile build source, installation notes and pinned checksums under `android-mobile/`.
- Installed as an update on one Android 16 phone; playback/background audio confirmed, final startup visually checked.


## 1.0.0 — 2026-10-21

- Added StayX in-app branding, About page, and local logo assets.
- Retained the original YouTube launcher icon and separate StayX package.
- Added ad-hiding controls and YTDLnis download-button integration.
- Added optional background playback, SponsorBlock, remembered quality/speed, swipe gestures, PiP button, feed cleanup, queue controls and editable theme colors.
- Kept new feature switches optional and preserved existing user settings during updates.
- Fixed the settings logo's opaque-background tinting bug.
- Published local build tooling, pinned dependency checksums, documentation and upstream attribution.
