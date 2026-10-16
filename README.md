<p align="center">
  <img src="docs/assets/zhoop-icon.png" alt="FreeBand" width="96">
</p>

<h1 align="center">FreeBand</h1>

<p align="center"><b>不用訂閱的 WHOOP 手環 App，台灣繁中版。</b></p>

FreeBand is an independent iPhone companion for WHOOP straps, with Traditional Chinese screens and Taiwanese food presets. It connects over Bluetooth and stores tracking data on the phone. No FreeBand account or subscription is required.

## Public iOS beta

**[Download FreeBand 11.8.1 (build 416)](https://github.com/austin17022/freeband/releases/tag/freeband-v11.8.1-b416)** · **[Install and pair](docs/FREEBAND_INSTALL.md)** · [Release notes](docs/releases/freeband-public-beta.md) · [Get help](SUPPORT.md)

Requires iOS 17 or later. Download `FreeBand-ios-v11.8.1.ipa` from the release and sign it with AltStore Classic, SideStore, or Sideloadly. This is a sideloaded beta, not an App Store or TestFlight release; opening the download in Safari does not install it. Free Apple accounts need periodic signing refreshes. The installation guide covers setup and signing limits.

**Existing users: update in place with the same signing account and sideloader. Do not delete the app.** The inherited `.noopbak` backup does **not** include Weight loss food logs, weigh-ins, or goals. See the [upgrade notes](docs/FREEBAND_INSTALL.md#update-an-existing-install).

## What FreeBand adds

- Traditional Chinese weight-loss and sleep screens, plus 16 Taiwanese food presets with estimated portions.
- A first-run profile for height, age, and weight.
- Today, Trends, Sleep, and More, with Weight loss in a separate tab. Recovery, strain, workouts, stress, and health views remain available.
- Weight-loss projections kept separate from measured profile weight. A weigh-in entered in Weight loss resets the plan's estimate and updates the profile.

Connection and data sync were confirmed by the maintainer on the preceding build. This does not establish compatibility with every WHOOP model or iPhone. The code includes WHOOP 4.0 and 5.0/MG support; this beta still needs broader device testing. Apple Health and widgets depend on signing entitlements. Apple Watch is not included. Inherited Android and macOS code is outside this public beta and has not been validated for FreeBand.

## Data and estimates

Core tracking and calculations run locally. Automatic update checks are on by default and contact GitHub; they can be switched off in Settings. Optional Coach and export features may send data to the endpoint configured by the user. See [network access and permissions](docs/FREEBAND_INSTALL.md#network-access-and-permissions).

Recovery, strain, sleep, calorie, and weight projections are estimates derived from the app's own methods, not WHOOP's official scores. FreeBand is not a medical device.

## Credits and license

FreeBand builds on [Zhoop by @hackyguru](https://github.com/hackyguru/zhoop) and [NOOP](https://github.com/ryanbr/noop). The [original Zhoop README](https://github.com/hackyguru/zhoop#readme) describes that fork's design. NOOP and its contributors provide the Bluetooth protocol, storage, and analytics foundation, with prior work from [johnmiddleton12/my-whoop](https://github.com/johnmiddleton12/my-whoop) and [b-nnett/goose](https://github.com/b-nnett/goose). See [ATTRIBUTION.md](ATTRIBUTION.md) and [NOTICE](NOTICE).

Most inherited documents, including [docs/IOS.md](docs/IOS.md) and [CHANGELOG.md](CHANGELOG.md), describe upstream NOOP. Use the FreeBand installation guide and release notes above for this beta.

Licensed under [PolyForm Noncommercial 1.0.0](LICENSE), permitting noncommercial use.

Required Notice: Copyright 2026 NoopApp

FreeBand is not affiliated with or endorsed by WHOOP, Inc., Zhoop, or the NOOP project. “WHOOP” identifies the hardware the app works with.
