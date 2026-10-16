"""Guard the iOS-only weight-loss view's shared-profile boundary.

StrandTests hosts the macOS target, which excludes this view. These source checks
cover the regression until an iOS UI test target can exercise the Settings flow.
"""

from pathlib import Path
import re
import unittest


SOURCE = (Path(__file__).resolve().parents[1]
          / "StrandiOS/Cut/CutTodayView.swift").read_text(encoding="utf-8")


class FreeBandWeightTests(unittest.TestCase):
    def test_refresh_cannot_replace_the_shared_profile_weight(self):
        view = SOURCE.split("// MARK: - Sheets", 1)[0]
        self.assertEqual([], re.findall(r"profile\.weightKg\s*=(?!=)", view),
                         "A background refresh must not replace measured profile weight")

    def test_explicit_measurement_still_updates_plan_and_profile(self):
        sheet = SOURCE.split("private struct LogWeightSheet", 1)[1]
        sheet = sheet.split("private struct CutPlanSheet", 1)[0]
        self.assertRegex(sheet, r"plan\.logWeight\(v\)\s+profile\.weightKg\s*=\s*v")


if __name__ == "__main__":
    unittest.main()
