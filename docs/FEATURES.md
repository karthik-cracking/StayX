# StayX optional features

Installable update: **StayX-v1.0.0.apk** from [Releases](https://github.com/karthik-cracking/StayX/releases). The app is named StayX and uses the original YouTube launcher icon. StayX branding remains inside the app; upstream attribution is preserved in the About page.

Open **You > Settings > StayX > Settings** to find these controls. Controls are grouped by feature; some require restarting the app after a change.

| Feature | Settings location | How to enable |
|---|---|---|
| Background playback | Miscellaneous | Turn on Remove background play restrictions; restart when prompted. Shorts background playback has a separate control under Shorts. |
| SponsorBlock | SponsorBlock | Turn on Enable SponsorBlock, then choose the segment categories and actions you want. |
| Remember quality | Video | Turn on Remember video quality; choose network defaults if desired. |
| Remember speed | Video | Turn on Remember playback speed. |
| Volume/brightness gestures | Swipe controls | Set Left swipe gesture to Brightness and Right swipe gesture to Volume, or choose your preferred arrangement. |
| Floating player button | Player > Overlay buttons | Turn on Show Picture-in-Picture button. Android's PiP permission must be allowed. |
| Cleaner home screen | Shorts, Feed, General, and Player | Choose the individual hiding controls you want. They are not one global switch. |
| Queue | Feed | Enable Override feed flyout queue button or the available local queue option. |
| StayX colors | General and Seekbar | In General choose Custom under Dark theme background to use the StayX #080810 background. Under Seekbar, enable custom colors to use cyan #00D7FF and violet #A83BFF. All colors can be edited. |

New optional Boolean controls default to off; swipe zones also start Off. Ad hiding, stream compatibility patches, and downloads remain from the previous build. Existing user choices can override defaults on an update. Theme backgrounds use selectors rather than a master on/off switch. Return to Pure black/White or your previous choice to leave the custom StayX palette.

## Checks completed

- All 17 selected patches applied; rebuilding, alignment and signing completed; APK signature verification passed.
- Installed as an update without clearing app data; launched successfully.
- Verified new settings sections: Feed, Shorts, Seekbar, Swipe controls, SponsorBlock, Video, plus expanded General/Player/Miscellaneous.
- SponsorBlock's master switch was verified initially off, switched on and off successfully, and left off.
- Remember video quality was switched on and off successfully and left off.
- Swipe gestures were verified Off; background-play restriction removal was verified Off.
- Custom theme was selected, the app restarted successfully, and its background was measured at RGB (8,8,16), matching #080810. The phone was returned to its previous Pure black choice afterward.
- Original YouTube launcher icon was visually verified on the phone.
- End-to-end behavior for every SponsorBlock category, background-audio scenario, queue mode, PiP mode, and gesture combination was not exhaustively tested. A prior download test completed a 635-second 360p MP4 with H.264 video and AAC audio through YTDLnis.

The app still uses experimental compatibility for YouTube 21.42.243. Source patches explicitly list experimental 21.42.241, and the compatibility version check was overridden, as in the preceding builds.

Downloads use the installed YTDLnis companion and save under Download/YTDLnis/Video.

## Build records

The repository's config directory records the feature selection and optional defaults. The scripts directory contains the branding, icon restoration, and resource compatibility modifications. Each build writes patch-result.json to its private working directory. The theme helper temporarily maps synthetic resource configurations to valid build configurations and restores the original numeric configurations in the compiled resource table before signing.

Source patches: https://github.com/MorpheApp/morphe-patches/tree/v1.48.0-dev.15

Release APK SHA-256: 69b321b39634617f1fe3c7b9d2580031e46893dc26fa6dee14060575279dce10
