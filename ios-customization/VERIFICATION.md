# Verification record

Date: 21 October 2026. Test device: one iPhone 12 running iOS 26.5. Personal account details, device identifiers, signed recovery copies, and raw logs remain private.

## Static package checks

- Exact input SHA-256 and ZIP CRC checks passed.
- Main app version: YouTube 21.13.6; ARM64, physical iOS, minimum iOS 16.0. The executable reports `cryptid=0`; this script does not decrypt it.
- Input review identified the YouTube Plus/YTLite 5.2b4 library and other injected libraries. They were not fully audited. Matching the selected release digest establishes identity, not safety or source equivalence.
- Corrected output changes 80 app-name plist files and one extension replication manifest. All 11,842 other ZIP entries, including directory entries, match the input byte for byte.
- The six removed manifest targets refer to absent AppMigrationExtension, IntentsExtension, NotificationContentExtension, NotificationServiceExtension, ShareExtension, and WidgetKitExtension bundles. Existing main-app and framework replication targets remain.

## Phone checks

| Check | Result |
|---|---|
| Installation of initial upstream test package | Passed after restoring USB connection |
| YouTube interface, Shorts/fullscreen/switching checklist | User reported it opens and works like YouTube |
| Ad behavior and downloaded video | User reported no ads seen and downloaded video plays |
| Name-only StayX update | Failed with an installation-journal error |
| Restart and retry | Same installation error |
| Scoped installer diagnostics | Missing extension Info.plist paths matched stale replication targets |
| Corrected package installed through AltServer | Passed |
| Existing personal bundle updated | Verified by before/after installation-proxy inventory |
| Original App Store YouTube coexistence | Verified; original app remained installed |
| Corrected StayX launch/interface/icon/fullscreen/saved-download checklist | User reported StayX opens and everything still works |

App behavior tests were user-reported sampled use. PiP, background playback, every ad format, all settings, and other devices were not validated. The earlier SmartTubeIOS-based prototype is a separate implementation and did not satisfy the requested interface/playback behavior.
