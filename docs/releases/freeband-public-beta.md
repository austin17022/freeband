# FreeBand 11.8.1 public beta

An iPhone companion for WHOOP straps, with Traditional Chinese screens and Taiwanese food presets. This beta is distributed as an IPA for sideloading; it is not an App Store or TestFlight release.

## Changes

- Keep manually entered profile weight when opening Weight loss. Projected weight remains available inside the weight-loss plan; an explicit weigh-in updates the profile.
- Check FreeBand's own published beta releases for updates, and open FreeBand's repository from Settings.
- Provide an AltStore source generated from the packaged app's version, bundle identity, size and permission descriptions.
- Retain the restored Today, Trends, Sleep and More screens, with Weight loss in its own tab.

## Install or update

Download `FreeBand-ios-v11.8.1.ipa` below and import it into AltStore Classic or a compatible sideloader. iOS 17 or later is required. The IPA must be signed by your sideloader before it can run; downloading it in Safari does not install it.

[Installation and pairing guide](https://github.com/austin17022/freeband/blob/main/docs/FREEBAND_INSTALL.md) · [Report a problem](https://github.com/austin17022/freeband/issues)

For an existing FreeBand install, update in place with the same signing account and sideloader. Export a backup first. **The inherited `.noopbak` backup does not include Weight loss food logs, weigh-ins or goals. Do not delete the app to update it.** Other companion apps use different identities; this release does not import their data automatically.

## Beta limits

- The maintainer reports successful strap connection and data sync on the preceding build. That is not validation of every strap, iPhone, or health estimate; hardware retesting is still needed after installing this build.
- Apple Health, App Groups and widgets depend on the signing method and available entitlements. Apple Watch is not included in this IPA.
- Android and macOS code remain in the repository, but this public beta contains only the iPhone app. Old staging downloads are development builds.
- Core tracking is local. Automatic update checks contact GitHub; optional Coach and export features can contact a service the user configures. See the installation guide before enabling those features.
- Recovery, strain, sleep and calorie estimates are not WHOOP's official scores and are not medical measurements.

[PolyForm Noncommercial 1.0.0](https://github.com/austin17022/freeband/blob/main/LICENSE). Original author credits and required notices remain in the [attribution file](https://github.com/austin17022/freeband/blob/main/ATTRIBUTION.md) and [third-party notices](https://github.com/austin17022/freeband/blob/main/NOTICE). FreeBand is independent of WHOOP, Inc.

## Verification

- [iPhone Release build](https://github.com/austin17022/freeband/actions/runs/38832912873): packaged app identity, ad-hoc signature, widget entitlements and SHA-256 verified. The sideloader must replace the ad-hoc signature before installation.
- [App regression tests](https://github.com/austin17022/freeband/actions/runs/38833739051): 2,149 tests, 0 failures, 2 skipped.
- 145 core Python checks passed.

The IPA was built from `fc6d3f74c9435c2dab2b1b7d18e4137cd4e934ef`. The app validation run passed at `b3f5ff7ea702ae7c6c316d6f58018d41f0cc7b18`. The release source adds the report-form test correction and publication metadata; application sources are identical to the IPA build. New-build hardware testing remains open.
