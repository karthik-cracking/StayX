# StayX TV runtime

Based on TizenTube userscript commit f99945a84ff767bf14ad8c1146e8e3fd49a3d628 (1.15.2), GPL-3.0-only. Upstream: https://github.com/reisxd/TizenTube

Build with Node.js and npm: run `npm ci --ignore-scripts` and `npm run build` in mods/. The output is dist/userScript.js. The root tv.js prepends the license/provenance header.

StayX adds an optional remote-player download button, a validated native download-helper action, settings branding, optional-feature defaults, a Menu-key settings entry, and disables the incompatible upstream APK updater. Downloading uses the separately installed YTDLnis helper; it is not a built-in downloader engine.

The app includes a local copy and also requests this same script from the immutable tv5 tag over the existing jsDelivr host allowed by the Cobalt runtime. The runtime itself does not load a second upstream userscript.

ARM32 testing on Fire OS 7.7.1.7 confirmed fullscreen playback, StayX settings, and a completed local video/audio download through YTDLnis. See ../README.md for scope and limits. ARM64 is not device-tested.
