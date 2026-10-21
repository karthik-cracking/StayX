#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p out
SIM_ID=$(xcrun simctl list devices available -j | python3 -c 'import json,sys; d=json.load(sys.stdin); print(next(x["udid"] for k,v in d["devices"].items() if "iOS" in k for x in v if x["name"].startswith("iPhone")))')
xcrun simctl boot "$SIM_ID" || true
collect_diagnostics() {
  local result=$?
  set +e
  xcrun simctl io "$SIM_ID" screenshot out/StayX-simulator.png
  if [ -d out/SmokeTests.xcresult ]; then
    xcrun xcresulttool export attachments --path out/SmokeTests.xcresult --output-path out/attachments
  fi
  rm -rf out/Payload
  exit "$result"
}
trap collect_diagnostics EXIT
xcodebuild -version | tee out/xcode-version.txt
xcodegen generate
set -o pipefail
xcodebuild build -project StayX.xcodeproj -scheme StayX -configuration Release \
  -destination 'generic/platform=iOS' -derivedDataPath build/device \
  CODE_SIGNING_ALLOWED=NO CODE_SIGN_IDENTITY='' DEVELOPMENT_TEAM='' \
  2>&1 | tee out/device-build.log
mkdir -p out/Payload
ditto build/device/Build/Products/Release-iphoneos/StayX.app out/Payload/StayX.app
(cd out && zip -q -r StayX-iOS-unsigned.ipa Payload)
shasum -a 256 out/StayX-iOS-unsigned.ipa > out/SHA256SUMS.txt

# Pick an installed iPhone simulator instead of assuming one particular model exists.
xcrun simctl bootstatus "$SIM_ID" -b
xcodebuild test -project StayX.xcodeproj -scheme StayX -configuration Debug \
  -destination "platform=iOS Simulator,id=$SIM_ID" -derivedDataPath build/simulator \
  -parallel-testing-enabled NO \
  -resultBundlePath out/SmokeTests.xcresult CODE_SIGNING_ALLOWED=NO \
  2>&1 | tee out/simulator-test.log
