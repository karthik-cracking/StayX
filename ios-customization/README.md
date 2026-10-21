# StayX for personal iPhone use

This folder contains the reproducible StayX name customization and packaging correction for a separately supplied YouTube Plus IPA. It preserves YouTube's icon, interface, player, and upstream feature code. It is not a native recreation of YouTube or the complete source code of the app.

**Verified on one iPhone 12 running iOS 26.5:** installation, launch, the retained YouTube interface, fullscreen playback, and an existing saved download. The tester also reported no ads during sampled playback and a playable downloaded video before renaming. These are sampled user tests, not a guarantee for every video, iPhone, account, or future server change. PiP and background playback were not validated.

The `ios` branch contains an earlier, separate native client. That prototype did not meet the requested interface and playback behavior. The working original-interface customization is documented here on `main`.

## Get started

1. Supply the exact reviewed input: `YouTubePlus_5.2b4.ipa`, from the [user-selected upstream release, tag ytp-7](https://github.com/shreybaviskar/YouTube-Premium-IPA/releases/tag/ytp-7). Review upstream software independently; matching a hash establishes file identity, not safety or correspondence to published source.
2. Install Python 3.11 or later. This script uses only Python's standard library and was run with Python 3.12 on Windows.
3. Run from the repository root, choosing an output path that does not exist:

```powershell
python ios-customization/build.py "C:\inputs\YouTubePlus_5.2b4.ipa" "C:\outputs\StayX-YouTube-21.13.6-fixed.ipa" --repair-extension-metadata
```

The parent output folder must already exist. Run Python without optimization flags so the validation checks remain enabled. The script preserves the input, verifies its SHA-256 and ZIP integrity, updates the name in the main bundle and 79 localizations, fixes the stale extension replication entries, and compares every other archive entry. It emits a `.verification.json` next to the output.

4. Personally sign and install the generated IPA through AltServer. It cannot be installed by simply tapping it in Files or a messaging app. See the [installation and friend-sharing guide](SHARING.md).

## What changes

| Item | Result |
|---|---|
| App display name | StayX, including all 79 localized name files |
| Launcher icon | Original YouTube icon preserved |
| Executable, libraries, player resources | Byte-identical to the reviewed input |
| App extension metadata | Six replication targets removed for extensions absent from the supplied IPA |
| Main app and existing framework replication targets | Preserved |
| Bundle identifier | Unchanged by this script; the signing tool applies the personal identifier |
| Internal YouTube and upstream tweak names/credits | Preserved |
| Signing | Must be performed again after customization |

The input already supplies the upstream playback and download features. This script does not implement those features, remove binary encryption, reconstruct missing extensions, or audit the injected libraries.

The metadata correction addresses an observed installation failure: iOS reported missing extension Info.plist files and an installation-journal decoding error. Removing the six stale replication targets allowed the update to complete on the test phone. See [verification notes](VERIFICATION.md).

## Pinned package identity

| Package | SHA-256 |
|---|---|
| Reviewed input | `d5aab0da9f45adb1a643b6852a1bd5c0a62824cbf3800e78427091d380e9225f` |
| Corrected output before personal re-signing | `f721e97d9e05211c40a8aa639559eb837e7feef65e18b3617fc6f3063055d38d` |

Re-signing changes the output hash. A different upstream version needs new inspection and compatibility testing; do not bypass the input checksum to force a newer release.

## Source and credits

The public repository and source release contain the customization script and documentation. They contain no YouTube IPA, personally signed app, Apple credentials, provisioning profiles, device identifiers, or private logs.

This project's script is covered by the repository's [GPL-3.0 license](../LICENSE). This does not relicense Google's application, the YouTube Plus/YTLite binaries, other injected libraries, or trademarks. Preserve applicable upstream credits and terms. The project is unofficial and is not affiliated with Google, YouTube, Apple, AltStore, or the upstream tweak authors.

- [YouTube Plus input release](https://github.com/shreybaviskar/YouTube-Premium-IPA/releases/tag/ytp-7)
- [YTLite upstream](https://github.com/dayanch96/YTLite)
- [AltServer official documentation](https://faq.altstore.io/release-notes/altserver)
- [REA](https://github.com/morluto/rea): archive inventory evidence during the input review; plist/Mach-O checks were also performed with local tools.
