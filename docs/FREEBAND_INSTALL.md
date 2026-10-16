# Install FreeBand on iPhone

This guide covers **FreeBand 11.8.1, build 416**, the public iOS beta. The [release page](https://github.com/austin17022/freeband/releases/tag/freeband-v11.8.1-b416) contains `FreeBand-ios-v11.8.1.ipa` and the release notes.

## Before installing

- An iPhone running iOS 17 or later and a charged WHOOP strap are required for tracking. The inherited code supports WHOOP 4.0 and 5.0/MG, but this beta has not been tested across every model.
- A sideloader must sign the IPA with an Apple account before iOS can run it. AltStore Classic, SideStore, and Sideloadly are installation options; their setup requirements differ.
- For AltStore Classic, follow the official [macOS or Windows installation instructions](https://faq.altstore.io/altstore-classic). Initial setup uses a computer and AltServer. Follow its prompts for device trust and Developer Mode where required.

FreeBand is not on the App Store or TestFlight. The release IPA has no distribution signature that allows direct installation from Safari; a replaceable ad-hoc signature is not a substitute for signing through a sideloader.

## Install with AltStore Classic

1. Finish the [official AltStore Classic setup](https://faq.altstore.io/altstore-classic) and confirm that AltStore opens on the iPhone.
2. Download `FreeBand-ios-v11.8.1.ipa` from the [FreeBand release](https://github.com/austin17022/freeband/releases/tag/freeband-v11.8.1-b416).
3. Import the IPA through AltStore Classic's **My Apps** screen using its add button, or share the downloaded file to AltStore. Let AltStore sign and install it.
4. Complete any iOS trust or Developer Mode prompts described in AltStore's guide, then open FreeBand.

The FreeBand source can also be added through AltStore Classic's source management screen:

```text
https://raw.githubusercontent.com/austin17022/freeband/main/altstore-source.json
```

Use that raw URL, not the GitHub file-view page. Look for FreeBand in Browse after adding it. AltStore's [source documentation](https://faq.altstore.io/altstore-classic/trusted-sources) explains source discovery; FreeBand is a third-party source, not an AltStore-reviewed Trusted Source. This IPA is intended for **AltStore Classic**, not AltStore PAL. If adding a source fails, use the direct IPA import above.

With a free Apple account, signed apps expire after **7 days** unless refreshed. AltStore attempts background refresh, but it is not guaranteed; check the remaining time in My Apps and refresh manually when needed. See [AltStore's refresh guide](https://faq.altstore.io/altstore-classic/your-altstore) and [Classic's limits](https://github.com/altstoreio/FAQ/blob/main/altstore-pal-v.-altstore-classic.md).

For [SideStore](https://sidestore.io) or [Sideloadly](https://sideloadly.io), follow that tool's current official setup and IPA-import instructions. Signing success and supported capabilities depend on the tool, Apple account, and provisioning profile.

## First launch and pairing

1. Complete FreeBand's introduction and enter height, age, and measured weight. Allow Bluetooth access when prompted.
2. Keep the charged strap near the phone. Close the official WHOOP app so it does not hold the connection. For WHOOP 5.0/MG, release its pairing in the official app if it is still attached there, then fully close that app.
3. Follow FreeBand's setup prompts to select the strap model and scan. A 5.0/MG must be in pairing mode; tap the band until its LEDs flash blue, then select it in FreeBand and accept any iOS pairing request.
4. Keep FreeBand open during the first sync. Confirm that both live heart rate and stored history appear; a live heart-rate reading alone does not prove that history sync is working.

If no strap appears, check Bluetooth permission, battery, distance, and whether another app or phone still holds the connection. Retry through FreeBand's Devices screen and follow the specific message it displays. Do not factory-reset the strap or delete the app as a first troubleshooting step. [FreeBand support](../SUPPORT.md) explains how to report a persistent problem without posting private data.

The maintainer confirmed connection and sync on the preceding build. That report does not validate every strap, this build's behavior on hardware, or the accuracy of health estimates.

## Update an existing install

Install the new IPA over the existing FreeBand app with the **same signing account and sideloader**, preserving its app identity. Export an available `.noopbak` backup first, but do not treat it as a complete copy of the app.

**Weight loss food logs, weigh-ins, and goals are not included in `.noopbak`.** These records are stored separately on the phone. Keep the installed app and separately record any essential weight-loss entries before updating. Uninstalling can lose those records; a backup restore cannot recover omitted data.

If the installer offers to replace the app by deleting it, or creates a second app instead of updating it, stop and resolve the signing or app-identity mismatch. Refresh an expired signature through the existing sideloader rather than uninstalling. NOOP and Zhoop use different app identities; this beta does not automatically migrate their data.

Weight-loss projections now stay inside the plan instead of overwriting measured profile weight. To reset the plan's estimate from a scale reading, record a weigh-in **inside Weight loss**. Editing the general profile alone does not reset the plan's anchor.

## Network access and permissions

Core Bluetooth tracking, storage, and calculations run on the phone. FreeBand has no required account or hosted tracking service.

Automatic update checks are on by default and contact GitHub. Disable **Check automatically** in Settings to stop those automatic checks. Manual update checks, release downloads, and sideloader refreshes still require their respective network connections; checking for a FreeBand update does not install it.

Optional Coach and export features can send data to a user-configured provider or endpoint. Review their settings and the destination before enabling them. They are not required for strap sync.

Apple Health, widgets, and shared App Groups require capabilities allowed by the signing account and provisioning profile. They may be unavailable with a particular sideloading setup, even if Bluetooth tracking works. Removing the widget extension removes widget functionality. Apple Watch is not included in this beta IPA.

## Source builds and upstream documentation

Developers can use the inherited [iOS build guide](IOS.md) and [build documentation](BUILD.md). Those documents describe upstream NOOP and may name its downloads, sources, or historical limitations. Use this guide's FreeBand release and source URLs for the public beta. Android and macOS code remain in the repository but are not validated FreeBand beta releases.
