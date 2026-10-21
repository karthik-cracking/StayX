// StayX modifications, 2026. SPDX-License-Identifier: GPL-3.0-only
import SwiftUI

struct StayXLicenseView: View {
    private var license: String {
        guard let url = Bundle.module.url(forResource: "StayX-LICENSE", withExtension: "txt") else { return "License unavailable" }
        return (try? String(contentsOf: url, encoding: .utf8)) ?? "License unavailable"
    }
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("StayX").font(.largeTitle.bold())
                Text("Independent personal customization of SmartTubeIOS. Original authors retain their copyright.")
                Link("SmartTubeIOS source and contributors", destination: URL(string: "https://github.com/milika/SmartTubeIOS")!)
                Link("StayX source", destination: URL(string: "https://github.com/karthik-cracking/StayX/tree/ios/ios")!)
                Text(license).font(.caption.monospaced()).textSelection(.enabled)
            }.padding()
        }.navigationTitle("Credits and license")
    }
}
