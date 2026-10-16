import copy
import plistlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from freeband_release import make_source


class ReleaseManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ipa = Path(self.temp.name) / "FreeBand-ios-v11.8.1.ipa"
        self.app = {
            "CFBundleIdentifier": "app.freeband.noop", "CFBundleShortVersionString": "11.8.1",
            "CFBundleVersion": "416", "MinimumOSVersion": "17.0",
            "CFBundleDisplayName": "FreeBand", "CFBundleName": "FreeBand",
            "AppGroupIdentifier": "group.app.freeband.noop.staging",
            "NSBluetoothAlwaysUsageDescription": "Connect to a strap.",
            "NSMicrophoneUsageDescription": "Ask the coach by voice.",
            "NSSpeechRecognitionUsageDescription": "Transcribe on-device.",
        }
        self.widget = copy.deepcopy(self.app)
        self.widget["CFBundleIdentifier"] += ".widgets"

    def generate(self, *, tag="freeband-v11.8.1-b416", extra=None, widget=True):
        with zipfile.ZipFile(self.ipa, "w") as archive:
            archive.writestr("Payload/FreeBand.app/Info.plist", plistlib.dumps(self.app, fmt=plistlib.FMT_BINARY))
            if widget:
                archive.writestr("Payload/FreeBand.app/PlugIns/NOOPWidgets.appex/Info.plist", plistlib.dumps(self.widget))
            for path, content in (extra or {}).items():
                archive.writestr(path, content)
        return make_source(self.ipa, tag, date="2026-10-16")

    def test_manifest_matches_binary_and_legacy_fields(self):
        source = self.generate()
        app = source["apps"][0]
        version = app["versions"][0]
        self.assertEqual(version["downloadURL"], "https://github.com/austin17022/freeband/releases/download/freeband-v11.8.1-b416/FreeBand-ios-v11.8.1.ipa")
        self.assertEqual(version["size"], self.ipa.stat().st_size)
        for key in ("version", "buildVersion", "downloadURL", "size", "minOSVersion"):
            self.assertEqual(app[key], version[key])
        self.assertEqual(app["bundleIdentifier"], "app.freeband.noop")
        self.assertIn(app["category"], {"developer", "entertainment", "games", "lifestyle", "other", "photo-video", "social", "utilities"})
        self.assertEqual(source["sourceURL"], "https://raw.githubusercontent.com/austin17022/freeband/main/altstore-source.json")

    def test_all_privacy_permissions_come_from_the_binary(self):
        privacy = self.generate()["apps"][0]["appPermissions"]["privacy"]
        self.assertEqual(len(privacy), 3)
        self.assertEqual(privacy["NSSpeechRecognitionUsageDescription"], "Transcribe on-device.")
        self.assertIn("NSMicrophoneUsageDescription", privacy)

    def test_rejects_upstream_app(self):
        self.app["CFBundleIdentifier"] = "com.noopapp.noop"
        with self.assertRaisesRegex(ValueError, "not the FreeBand"):
            self.generate()

    def test_rejects_wrong_widget(self):
        self.widget["CFBundleIdentifier"] = "com.noopapp.noop.widgets"
        with self.assertRaisesRegex(ValueError, "Widget identity"):
            self.generate()

    def test_rejects_an_upstream_display_name(self):
        self.app["CFBundleName"] = "NOOP Staging"
        with self.assertRaisesRegex(ValueError, "display the FreeBand name"):
            self.generate()

    def test_rejects_different_app_groups(self):
        self.widget["AppGroupIdentifier"] = "group.someone.else"
        with self.assertRaisesRegex(ValueError, "App Group"):
            self.generate()

    def test_rejects_widget_version_mismatch(self):
        self.widget["CFBundleVersion"] = "415"
        with self.assertRaisesRegex(ValueError, "versions differ"):
            self.generate()

    def test_rejects_mutable_or_mismatched_tags(self):
        for tag in ("testing-latest", "freeband-v11.8.1-b415", "freeband-v11.8.0-b416"):
            with self.subTest(tag=tag), self.assertRaisesRegex(ValueError, "Tag must match"):
                self.generate(tag=tag)

    def test_rejects_missing_widget(self):
        with self.assertRaises(KeyError):
            self.generate(widget=False)

    def test_rejects_watch_payload(self):
        with self.assertRaisesRegex(ValueError, "Watch"):
            self.generate(extra={"Payload/FreeBand.app/Watch/App.app/Info.plist": b"x"})

    def test_rejects_multiple_apps(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            self.generate(extra={"Payload/Other.app/Info.plist": plistlib.dumps(self.app)})

    def test_rejects_missing_bluetooth_permission(self):
        del self.app["NSBluetoothAlwaysUsageDescription"]
        with self.assertRaisesRegex(ValueError, "Bluetooth"):
            self.generate()

    def test_rejects_invalid_version(self):
        self.app["CFBundleShortVersionString"] = "11.8.1-beta"
        with self.assertRaisesRegex(ValueError, "marketing version"):
            self.generate()


if __name__ == "__main__":
    unittest.main()
