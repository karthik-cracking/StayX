# StayX settings icon fix

Included in StayX v1.0.0. Visually verified on the development phone: the settings row shows an SX silhouette instead of a solid square.

The settings row applies a monochrome tint to its icon. The previous bitmap had an opaque background, so its entire rectangle was tinted white. The replacement uses a transparent background and a white SX silhouette sized for the existing 24dp icon wrapper.

The original fix changed only res/drawable/stayx_brand_logo.png compared with the preceding feature build (besides signing metadata). The consolidated build script reproduces this artwork alongside the other customizations. Signature verification passed.

The [feature guide](FEATURES.md) describes the available controls. Existing app data was preserved during the tested update.
