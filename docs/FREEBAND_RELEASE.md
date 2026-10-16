# Publishing a FreeBand iOS beta

Public beta downloads use immutable tags such as `freeband-v11.8.1-b416`. The mutable `testing-latest` release is a build staging area, not the public update source.

## Before building

1. Increase `MARKETING_VERSION` and `CURRENT_PROJECT_VERSION` in `project.yml`, and keep the Android version name in sync as required by AGENTS.md. **Every public beta needs a higher marketing version.** The in-app update notification compares marketing versions; a build-number-only change will not notify installed users.
2. Update `docs/releases/freeband-public-beta.md` and the installation/README links.
3. Run `python3 -m unittest discover -s Tools -p 'test_freeband*.py'`, the core Python suite, doc-comment lint, and the app build/test workflow for changed Apple source.
4. Confirm the current source commit is pushed and no previous release uses the intended tag. Never replace an existing public release's IPA.

## Build with the existing workflows

Dispatch `app-build.yml` and `fork-testing-build.yml` against the same branch. Require the iOS Release build and relevant app tests to succeed. Confirm each run's `headSha` matches the intended source commit before downloading its output.

The testing workflow replaces `testing-latest` and publishes NOOP-named staging assets for all inherited platforms. For the iOS public beta, download only its IPA, rename it to `FreeBand-ios-v<VERSION>.ipa`, and generate the source from the actual file:

```sh
python3 Tools/freeband_release.py \
  --ipa dist/FreeBand-ios-v<VERSION>.ipa \
  --tag freeband-v<VERSION>-b<BUILD> \
  --output dist/altstore-source.json
```

The validator checks the app/widget identity, App Group, version, minimum iOS version, Bluetooth permission description and absence of Watch. It derives all privacy descriptions from the app's Info.plist. Verify the packaged app's ad-hoc signature with `codesign --verify --deep --strict` after extracting it locally, and compare its SHA-256 with the build asset's GitHub digest. Record hardware testing separately from compilation.

## Publish and verify

Create a **draft prerelease** at the built source SHA, with the immutable tag and maintained notes. Upload the IPA, generated `altstore-source.json`, and `SHA256SUMS.txt` covering both files. Download the draft assets again and verify the checksums and sizes. Publish only after those checks pass; keep it marked as a prerelease, not latest stable.

Copy the generated manifest to the repository-root `altstore-source.json` and publish it on `main` after the immutable download exists. Confirm its public raw URL, bundle ID, version, build, size and download URL match the release. Update the README's release link in the same publication pass. Never copy upstream NOOP versions into the FreeBand source.

The inactive template at `Tools/workflows/freeband-beta.yml` automates the iOS packaging and draft verification steps. Installing it under `.github/workflows/` requires GitHub workflow-write permission, which the current login does not have. It deliberately stays inactive. Even with that template, update the root AltStore manifest after publication and run the app test workflow before releasing app changes.

## Release limits to carry forward

The inherited `.noopbak` format omits Weight loss records. Preserve the warning to update in place until a tested backup implementation covers them. Keep upstream license notices and attribution. Android and macOS staging builds are not part of the public iOS beta.
