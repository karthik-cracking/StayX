// SPDX-License-Identifier: GPL-3.0-only
// StayX personal iOS app, using the GPL-3.0 SmartTubeIOS library.
import SwiftUI
import SmartTubeIOS
import SmartTubeIOSCore

@main
@MainActor
struct StayXApp: App {
    @UIApplicationDelegateAdaptor(StayXAppDelegate.self) var appDelegate
    @State private var api: InnerTubeAPI
    @State private var auth: AuthService
    @State private var browse: BrowseViewModel
    @State private var settings: SettingsStore
    @State private var player: PlayerStateStore
    @State private var embedded: TOSPlayerStateStore
    @State private var router: PlayerRouter
    @State private var downloads: VideoDownloadService
    @Environment(\.scenePhase) private var phase

    init() {
        let settings = SettingsStore()
        let api = InnerTubeAPI(authToken: nil, poTokenProvider: BotGuardClient())
        let player = PlayerStateStore(api: api)
        let embedded = TOSPlayerStateStore()
        _api = State(initialValue: api)
        _auth = State(initialValue: AuthService())
        _browse = State(initialValue: BrowseViewModel(api: api))
        _settings = State(initialValue: settings)
        _player = State(initialValue: player)
        _embedded = State(initialValue: embedded)
        _router = State(initialValue: PlayerRouter(playerState: player, tosState: embedded, settingsStore: settings))
        _downloads = State(initialValue: VideoDownloadService(api: api))
    }
    var body: some Scene {
        WindowGroup {
            RootView()
                .environment(auth).environment(browse).environment(settings)
                .environment(player).environment(embedded).environment(router)
                .environment(downloads).environment(DownloadStore.shared)
                .environment(\.innerTubeAPI, api)
                .onChange(of: auth.accessToken, initial: true) { _, token in
                    player.vm.updateAuthToken(token)
                    Task { await api.setAuthToken(token); await browse.updateAuthToken(token) }
                }
                .onChange(of: auth.sapisid, initial: true) { _, value in
                    player.vm.updateSAPISID(value)
                    Task { await api.setSAPISID(value) }
                }
                .onChange(of: settings.settings.enabledSections) { _, value in browse.configureSections(value) }
                .onChange(of: settings.settings.historyState, initial: true) { _, value in
                    browse.updateHistoryEnabled(value == .enabled)
                }
                .onChange(of: phase, initial: true) { _, value in
                    if value == .active {
                        auth.handleForeground(); browse.refreshIfStale()
                        if player.presentation == .miniPlayer { player.vm.handleForeground() }
                    } else if value == .background && player.presentation == .miniPlayer {
                        player.vm.handleBackground()
                    }
                }
                .onOpenURL { url in
                    let videoID = YouTubeLinkHandler.videoID(from: url)
                    if let videoID { browse.deepLinkedVideo = Video(id: videoID, title: "", channelTitle: "") }
                }
        }
    }
}
