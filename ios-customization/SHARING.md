# Install StayX on a friend's iPhone

Your friend needs an IPA that can be personally re-signed, access to a Windows PC or Mac, their iPhone, a data cable, and their own Apple account. Their phone does not inherit authorization from the app installed on your phone. Sending a file by AirDrop, chat, or a cloud link transfers it but does not perform signing or installation.

You can privately transfer the corrected `StayX-YouTube-21.13.6-fixed.ipa` input package to their computer, subject to the upstream application's applicable rights and terms, or they can reproduce it using [build.py](build.py) and their separately obtained input. The public StayX release provides customization source and this guide, not the third-party YouTube application.

## Windows installation

1. Follow the [official AltServer Windows setup guide](https://faq.altstore.io/altstore-classic/how-to-install-altstore-windows) for AltServer and its Apple software requirements. A friend can also connect to your already configured PC instead of setting up another computer.
2. Connect the friend's iPhone by USB, unlock it, and let them approve Trust This Computer on the phone. Check that Apple Devices or iTunes can see it consistently.
3. Close any open AltServer menu. Hold **Shift before clicking** the AltServer diamond icon near the Windows clock. Choose **Sideload .ipa...**, then the friend's iPhone. The normal **Install AltStore** item is a different action.
4. Select `StayX-YouTube-21.13.6-fixed.ipa`.
5. The friend enters **their own Apple account** and any verification directly in AltServer. Never exchange passwords, codes, certificates, or provisioning files. Your own personally signed recovery copy is not the file to distribute.
6. Keep the phone connected and unlocked until the success notification appears. Check that StayX appears and launches.
7. If prompted for developer trust, follow the instructions under Settings > General > VPN & Device Management for the signing account. If Developer Mode is required, the friend enables it under Settings > Privacy & Security > Developer Mode, restarts, and confirms on the phone. These are personal decisions the phone owner completes themselves.
8. Test Home/Shorts, fullscreen video playback, and a short download. The friend should verify their own phone; the current device result is not universal compatibility evidence.

## Mac

Use the [official Mac setup guide](https://faq.altstore.io/altstore-classic/how-to-install-altstore-macos). AltServer's direct IPA menu is revealed by holding **Option** when clicking its menu-bar icon, rather than Shift. The friend still signs with their own account.

## Keeping it working

With a free Apple account, directly sideloaded apps must be re-signed and reinstalled every **7 days**. Renew before expiry using the same account and package identifier; updating in place is intended to preserve app data, so do not delete the working app just to refresh it. This weekly renewal also applies to the original personal StayX installation.

Direct AltServer sideloading does not set up automatic refresh by itself. Installing and managing apps through AltStore Classic is a separate workflow that supports automatic refresh when its requirements are met. Free accounts are limited to **3 active sideloaded apps**, including AltStore if installed. See [AltServer release notes](https://faq.altstore.io/release-notes/altserver) and [AltStore's getting-started guide](https://faq.altstore.io/altstore-classic/your-altstore).

If the friend has no computer, they can use your PC for installation, but they will also need access to a suitable computer for this direct-sideload renewal workflow. A GitHub release link alone does not provide tap-to-install access.

## Troubleshooting

- **Only Install AltStore appears:** close the menu, hold Shift first, then click the tray icon again. Use Option on Mac.
- **Session expired:** repeat the sign-in locally in AltServer.
- **Server connection error:** check connectivity and retry after reviewing [AltStore's troubleshooting guide](https://faq.altstore.io/altstore-classic/troubleshooting-guide). A server error does not establish a bad IPA or an incorrect password.
- **Phone disappears during transfer:** restore a stable USB connection before retrying; the initial test encountered intermittent USB disconnection.
- **Installation-journal / missing extension Info.plist error:** use the corrected package built with `--repair-extension-metadata`, not the earlier name-only candidate. The correction was verified on the test phone.
- **A new error persists:** retain its exact text without account details. Do not repeatedly uninstall apps, revoke certificates, change security software, or reset the phone as a first response.
