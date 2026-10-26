# StayX TV

StayX TV keeps YouTube's TV interface, search, Shorts shelves and fullscreen remote controls using [TizenTube Cobalt](https://github.com/reisxd/TizenTubeCobalt). It uses the StayX name and original YouTube launcher artwork. It is a separate TV application, package `com.stayx.tv`, and can coexist with the official app.

## Install

Download the APKs and source backup from the [StayX TV 1.0.0 experimental release](https://github.com/karthik-cracking/StayX/releases/tag/tv-v1.0.0).

Choose the APK for the device's **Android ABI**, not just its processor hardware:

| APK | Device |
| --- | --- |
| `StayX-TV-1.0.0-arm.apk` | 32-bit ARM Android/Fire OS, including the tested Fire TV Stick Lite AFTSSS |
| `StayX-TV-1.0.0-arm64.apk` | Android TV with 64-bit ARM app support; built and signature-checked, not tested on a physical ARM64 TV |

The runtime requires Android 7/API 24 or later. Android TV 12+ is an intended target, but was not available for device testing. The supplied Google YouTube TV 7.29.300 APKM requires API 29 and cannot run on the tested Fire OS 7 device, so this build uses the user-selected Cobalt route instead.

Sideload the matching APK and open **StayX**. First launch may take around 20–30 seconds on the tested low-end Fire TV. Choose **Watch as guest**, or sign in yourself if desired. Google sign-in was not tested.

Press the remote's **Menu (three lines)** button to open **StayX Settings**. Ad Block starts enabled. Downloads, SponsorBlock, DeArrow and the mini-player button can be enabled from their settings. Some player changes require closing and reopening the app.

## Save videos locally

1. Install the official [YTDLnis 1.9.1.1 companion](https://github.com/deniscerri/ytdlnis/releases/tag/v1.9.1.1). Match its ABI to the TV: **armeabi-v7a** for the tested Fire TV, **arm64-v8a** for a 64-bit Android TV. Open it once and complete its setup and storage permission.
2. In StayX, press **Menu → Downloads → Show download button**.
3. Open a video and use **Download video** in the player controls/settings, or **Menu → Downloads → Download current video**.
4. Open **Menu → Downloads → Open downloaded videos** to see YTDLnis. If an item waits in its queue, choose **Resume all**.
5. For offline playback, install a compatible local video player such as [official VLC for Android TV](https://www.videolan.org/vlc/download-android.html), open it once and complete its setup. Open the saved item from YTDLnis or VLC.

The default folder in this test was `Download/YTDLnis/Video`. Download processing is separate from streaming playback. The first ARM32 extraction took several minutes, even for a short video. The helper's own setup/preferences can require a mouse or Android remote-pointer app. Save videos you are permitted to download.

## Features and test scope

| Area | Status |
| --- | --- |
| Home, search and fullscreen TV playback | Observed on AFTSSS / Fire OS 7.7.1.7 / Android 9 API 28 |
| StayX Menu-key settings and download settings | Observed; download enable state persisted after restart |
| Ad-block setting | Enabled; no ad seen in the sampled playback sessions; this does not guarantee all videos remain ad-free |
| Local download handoff | Actual video ID passed from StayX to YTDLnis |
| Completed saved file | 19.028-second video with AV1 video and Opus audio; full decode passed on the PC; local playback observed in VLC on the Fire TV |
| SponsorBlock, DeArrow, speed, quality, queue, mini-player/PiP, captions, interface preferences | Upstream features retained with settings; not all individually exercised |
| ARM64, Android TV 12+, Google login, casting, HDR/DRM and long-session reliability | Not device-verified |

Phone-only swipe/brightness controls are not carried over as TV remote features. This is an experimental independent client; YouTube website changes can affect its interface and patches.

## Source and rebuilding

- [Android packaging, Java bridge and build driver](android/README.md)
- [Complete modified userscript source](runtime/README.md)
- [Validation records](validation/)

The APK includes the runtime locally. Its native loader also requests the same pinned `tv5` script from this repository through jsDelivr; the guard prevents duplicate initialization. It does not automatically fetch the latest upstream userscript or install upstream APK updates.

## Credits and licenses

[TizenTube](https://github.com/reisxd/TizenTube), by Reis Can and contributors, provides the TV modifications (GPL-3.0-only). [TizenTube Cobalt](https://github.com/reisxd/TizenTubeCobalt) provides the Cobalt/Chromium runtime, with BSD and third-party notices preserved. StayX modifications and bridge source are GPL-3.0-only. [YTDLnis](https://github.com/deniscerri/ytdlnis) and [VLC](https://code.videolan.org/videolan/vlc-android) are separate projects and are not bundled inside StayX. YouTube's artwork and service belong to Google. StayX is not affiliated with those projects or Google.
