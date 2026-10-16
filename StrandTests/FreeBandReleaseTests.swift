import XCTest
@testable import Strand

@MainActor
final class FreeBandReleaseTests: XCTestCase {
    private func entry(_ version: String = "11.8.1", platform: String = "ios", draft: Bool = false) -> [String: Any] {
        let tag = "freeband-v\(version)-b416"
        let base = "https://github.com/austin17022/freeband"
        let filename = "FreeBand-\(platform)-v\(version).\(platform == "ios" ? "ipa" : "zip")"
        return ["tag_name": tag, "draft": draft, "prerelease": true,
                "html_url": "\(base)/releases/tag/\(tag)", "body": "Public beta.",
                "assets": [["name": filename, "browser_download_url": "\(base)/releases/download/\(tag)/\(filename)"]]]
    }

    private func parse(_ entries: [[String: Any]], platform: String = "ios") throws -> UpdateChecker.Release? {
        UpdateChecker.release(from: try JSONSerialization.data(withJSONObject: entries), platform: platform)
    }

    func testPublicPrereleaseIsOffered() throws {
        let release = try XCTUnwrap(parse([entry()]))
        XCTAssertEqual(release.version, "11.8.1")
        XCTAssertEqual(release.url.absoluteString, "https://github.com/austin17022/freeband/releases/tag/freeband-v11.8.1-b416")
    }

    func testDraftOrIncompleteReleaseIsNotOffered() throws {
        XCTAssertNil(try parse([entry(draft: true)]))
        var release = entry()
        release["assets"] = []
        XCTAssertNil(try parse([release]))
    }

    func testRollingAndUpstreamTagsAreIgnored() throws {
        for tag in ["testing-latest", "v11.8.1", "freeband-vgarbage-b416"] {
            var release = entry()
            release["tag_name"] = tag
            XCTAssertNil(try parse([release]))
        }
    }

    func testAnotherProjectsDownloadIsRejected() throws {
        var release = entry()
        release["assets"] = [["name": "FreeBand-ios-v11.8.1.ipa",
                              "browser_download_url": "https://github.com/ryanbr/noop/releases/download/v11.8.1/app.ipa"]]
        XCTAssertNil(try parse([release]))
        release = entry()
        release["html_url"] = "https://example.com"
        XCTAssertNil(try parse([release]))
    }

    func testMacDoesNotOfferAnIOSOnlyBeta() throws {
        XCTAssertNil(try parse([entry()], platform: "macos"))
        XCTAssertEqual(try parse([entry(platform: "macos")], platform: "macos")?.version, "11.8.1")
    }

    func testHighestVersionWinsRegardlessOfReleaseOrder() throws {
        XCTAssertEqual(try parse([entry("11.8.1"), entry("11.10.0"), entry("11.9.0")])?.version, "11.10.0")
    }

    func testMalformedResponseFailsQuietly() {
        XCTAssertNil(UpdateChecker.release(from: Data("not JSON".utf8), platform: "ios"))
        XCTAssertNil(UpdateChecker.release(from: Data("{}".utf8), platform: "ios"))
    }
}
