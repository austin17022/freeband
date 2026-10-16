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

For an existing FreeBand install, update in place with the same signing account and sideloader. Export a backup first. **The inherited `.noopbak` backup does not include Weight loss food logs, weigh-ins or goals. Do not delete the app to update it.** NOOP and Zhoop use different identities; this release does not import their data automatically.

## Beta limits

- The maintainer reports successful strap connection and data sync on the preceding build. That is not validation of every strap, iPhone, or health estimate; hardware retesting is still needed after installing this build.
- Apple Health, App Groups and widgets depend on the signing method and available entitlements. Apple Watch is not included in this IPA.
- Android and macOS code remain in the repository, but this public beta contains only the iPhone app. Old NOOP-named staging downloads are development builds.
- Core tracking is local. Automatic update checks contact GitHub; optional Coach and export features can contact a service the user configures. See the installation guide before enabling those features.
- Recovery, strain, sleep and calorie estimates are not WHOOP's official scores and are not medical measurements.

Based on [Zhoop](https://github.com/hackyguru/zhoop) and [NOOP](https://github.com/ryanbr/noop). [PolyForm Noncommercial 1.0.0](https://github.com/austin17022/freeband/blob/main/LICENSE); upstream notices are retained. FreeBand is independent of WHOOP, Inc.
