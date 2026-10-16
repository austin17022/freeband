#!/usr/bin/env python3
"""Generate the FreeBand AltStore source from the packaged IPA, without extracting it."""

import argparse
import datetime
import json
import plistlib
import re
import zipfile
from pathlib import Path

REPOSITORY = "austin17022/freeband"
BUNDLE_ID = "app.freeband.noop"
SOURCE_URL = f"https://raw.githubusercontent.com/{REPOSITORY}/main/altstore-source.json"


def make_source(ipa: Path, tag: str, date: str | None = None) -> dict:
    with zipfile.ZipFile(ipa) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise ValueError("Duplicate ZIP entries")
        if archive.testzip() is not None:
            raise ValueError("Corrupt IPA")
        roots = [name for name in names if re.fullmatch(r"Payload/[^/]+\.app/Info.plist", name)]
        if len(roots) != 1:
            raise ValueError("Expected exactly one Payload app")
        root = roots[0].removesuffix("Info.plist")
        if any(name.startswith(root + "Watch/") for name in names):
            raise ValueError("Remove the Watch app before sideload packaging")
        plists = [roots[0], root + "PlugIns/NOOPWidgets.appex/Info.plist"]
        infos = []
        for name in plists:
            if archive.getinfo(name).file_size > 1024 * 1024:
                raise ValueError("Unexpectedly large Info.plist")
            infos.append(plistlib.loads(archive.read(name)))
        app, widget = infos
        if app.get("CFBundleIdentifier") != BUNDLE_ID:
            raise ValueError("IPA is not the FreeBand app")
        if widget.get("CFBundleIdentifier") != BUNDLE_ID + ".widgets":
            raise ValueError("Widget identity does not match FreeBand")
        group = "group.app.freeband.noop.staging"
        if app.get("AppGroupIdentifier") != group or widget.get("AppGroupIdentifier") != group:
            raise ValueError("App and widget must share the FreeBand App Group")
        version = app.get("CFBundleShortVersionString", "")
        build = app.get("CFBundleVersion", "")
        if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", version):
            raise ValueError("Invalid marketing version")
        if not re.fullmatch(r"[0-9]+", build):
            raise ValueError("Invalid build number")
        if tag != f"freeband-v{version}-b{build}":
            raise ValueError("Tag must match the packaged version and build")
        if ipa.name != f"FreeBand-ios-v{version}.ipa":
            raise ValueError("IPA filename must match its packaged version")
        for key in ("CFBundleShortVersionString", "CFBundleVersion"):
            if widget.get(key) != app[key]:
                raise ValueError("App and widget versions differ")
        minimum = app.get("MinimumOSVersion", "")
        if not re.fullmatch(r"[0-9]+(?:\.[0-9]+){1,2}", minimum):
            raise ValueError("Missing or invalid minimum iOS version")
        privacy = {key: value for key, value in app.items()
                   if key.startswith("NS") and key.endswith("UsageDescription") and isinstance(value, str)}
        if not privacy.get("NSBluetoothAlwaysUsageDescription"):
            raise ValueError("Missing Bluetooth permission description")

    release_url = f"https://github.com/{REPOSITORY}/releases/download/{tag}/{ipa.name}"
    description = (f"FreeBand {version}, public beta (build {build}). "
                   "Install with AltStore Classic or another compatible sideloader. "
                   "Back up before updating; weight-loss logs are not included in .noopbak backups.")
    entry = {
        "version": version, "buildVersion": build,
        "date": date or datetime.datetime.now(datetime.timezone.utc).date().isoformat(),
        "localizedDescription": description, "downloadURL": release_url,
        "size": ipa.stat().st_size, "minOSVersion": minimum,
    }
    icon = f"https://raw.githubusercontent.com/{REPOSITORY}/main/docs/assets/zhoop-icon.png"
    return {
        "name": "FreeBand", "identifier": "app.freeband.altstore", "sourceURL": SOURCE_URL,
        "subtitle": "An on-device WHOOP companion, with Traditional Chinese support.",
        "description": "FreeBand public iOS beta. Based on Zhoop and NOOP; independent of WHOOP. Noncommercial use.",
        "iconURL": icon, "website": f"https://github.com/{REPOSITORY}", "tintColor": "44E2B0",
        "apps": [{
            "name": "FreeBand", "bundleIdentifier": BUNDLE_ID, "developerName": "austin17022",
            "subtitle": "Your WHOOP strap, your iPhone, your data.",
            "localizedDescription": "Connect a WHOOP strap over Bluetooth. View heart rate, sleep, recovery and trends, and keep a food log with Taiwanese presets. Core tracking works on-device without a FreeBand account. Optional network features are described in the installation guide.",
            "iconURL": icon, "tintColor": "44E2B0", "category": "lifestyle",
            "versions": [entry],
            "appPermissions": {
                "entitlements": ["com.apple.developer.healthkit", "com.apple.developer.healthkit.access",
                                 "com.apple.security.application-groups"],
                "privacy": privacy,
            },
            "version": version, "buildVersion": build, "versionDate": entry["date"],
            "versionDescription": description, "downloadURL": release_url,
            "size": entry["size"], "minOSVersion": minimum,
        }], "news": [],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ipa", type=Path, required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = make_source(args.ipa, args.tag)
    args.output.write_text(json.dumps(source, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Validated FreeBand IPA; wrote {args.output}")


if __name__ == "__main__":
    main()
