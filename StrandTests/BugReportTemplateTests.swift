import XCTest

/// The public beta form collects enough context to reproduce a problem without requiring health logs.
/// TestReportFlow only shares locally; it no longer opens or prefills a GitHub issue.
final class BugReportTemplateTests: XCTestCase {
    private func templateText() throws -> String {
        let repoRoot = URL(fileURLWithPath: #filePath)
            .deletingLastPathComponent().deletingLastPathComponent()
        return try String(contentsOf: repoRoot.appendingPathComponent(".github/ISSUE_TEMPLATE/bug_report.yml"),
                          encoding: .utf8)
    }

    func testCollectsDeviceAndInstallationContext() throws {
        let text = try templateText()
        for field in ["version", "device", "strap", "installation", "reproduction"] {
            XCTAssertTrue(text.contains("id: \(field)\n"), "missing report field: \(field)")
        }
    }

    func testRequiresStepsAndAnActualResult() throws {
        let text = try templateText()
        XCTAssertTrue(text.contains("Steps, expected result, and actual result"))
        XCTAssertTrue(text.contains("exact error message"))
    }

    func testDoesNotRequireHealthDataOrLogUploads() throws {
        let text = try templateText()
        XCTAssertTrue(text.contains("Do not upload health databases, backups, food logs, raw strap logs"))
        XCTAssertFalse(text.contains("Attach your exported"))
        XCTAssertFalse(text.contains("I attached my exported"))
        XCTAssertFalse(text.contains("id: log\n"))
    }

    func testRequiresPublicDataReview() throws {
        let text = try templateText()
        XCTAssertTrue(text.contains("id: privacy\n"))
        let privacy = try XCTUnwrap(text.components(separatedBy: "id: privacy\n").last)
        XCTAssertTrue(privacy.contains("removed personal health data, device identifiers, and credentials"))
        XCTAssertTrue(privacy.contains("required: true"))
    }

    func testRoutesHelpToFreeBand() throws {
        let text = try templateText()
        XCTAssertTrue(text.contains("https://github.com/austin17022/freeband/blob/main/docs/FREEBAND_INSTALL.md"))
        XCTAssertFalse(text.contains("github.com/ryanbr/"))
        XCTAssertFalse(text.contains("discord.com/"))
    }
}
