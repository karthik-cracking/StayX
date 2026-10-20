# Build notes

The original working directory was an exploratory APK customization session. These scripts consolidate its final changes into a reusable build workflow; the repository is not a decompilation presented as original source.

Supported input SHA-256: `2d1afe26c399b7c820d862e243d4335a209505f3d7c164f679952a93fcb3aea4`.

The v1.0.0 release APK was rebuilt end to end with the published scripts, including the transparent settings icon and full upstream notices in the About page. Alignment and APK signature verification passed. Its SHA-256 is `69b321b39634617f1fe3c7b9d2580031e46893dc26fa6dee14060575279dce10`.

Rebuilding can produce different bytes due to ZIP timestamps, signing metadata, font rendering, and the consolidated packaging process. A different signing key cannot update a previously installed release. Preserve your private key; it is never part of the public source archive.

## Resource compatibility

The upstream theme patch uses synthetic MCC resource configurations above the range accepted by the standard resource compiler. The helper temporarily assigns unused legal MCC values while compiling and restores the original numeric values in the compiled resource table before signing. It validates chunk boundaries and checks that configurations were restored. Device testing confirmed that selecting the custom dark theme produced RGB (8,8,16).

## Optional defaults

The selected new Boolean preferences default to off without disabling the existing ad/download controls. The negative Shorts background-playback restriction defaults to on so Shorts do not begin playing in the background unexpectedly. Swipe zones start Off. Existing stored user preferences can override defaults after an upgrade.

The Java helper saves and restores constructor argument registers around each default override; the original control flow is maintained through dexlib2's mutable instruction builder.

## Publishing boundaries

The public source tree contains scripts, configuration, assets, licenses and documentation. The separate private recovery archive is not a public release asset: it includes original inputs and signing material. The APK is a modified proprietary application with open-source modifications, not a fully open-source replacement for YouTube. Source licensing must not be represented as permission to relicense third-party code.
