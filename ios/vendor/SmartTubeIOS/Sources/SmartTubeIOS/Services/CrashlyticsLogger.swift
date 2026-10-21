// StayX modification: device-local OS logging only. No Firebase SDK or remote reports.
import Foundation
import SmartTubeIOSCore
import os

public struct CrashlyticsLogger: Sendable {
    public nonisolated(unsafe) static var isEnabled = false
    static let sessionReportID = String(UUID().uuidString.prefix(8))
    private let logger: Logger
    init(subsystem: String = appSubsystem, category: String) {
        logger = Logger(subsystem: subsystem, category: category)
    }
    func notice(_ message: @autoclosure () -> String) { logger.notice("\(message(), privacy: .private)") }
    func error(_ message: @autoclosure () -> String) { logger.error("\(message(), privacy: .private)") }
    func debug(_ message: @autoclosure () -> String) { logger.debug("\(message(), privacy: .private)") }
    func recordNonFatal(_ error: Error, userInfo: [String: String] = [:]) {
        logger.error("\(error.localizedDescription, privacy: .private)")
    }
    static func setVideoContext(id: String, title: String) {}
    static func setIntendedVideo(id: String, title: String) {}
    static func sendDiagnosticReport() {}
    static func sendAutoPlaybackDiagnostic() {}
    static func recordSlowVideoLoad(videoId: String, elapsedMs: Int, streamType: String, hasError: Bool, errorDescription: String? = nil) {}
    static func sendWrongVideoReport(intendedId: String, intendedTitle: String, activeId: String, activeTitle: String) {}
}
