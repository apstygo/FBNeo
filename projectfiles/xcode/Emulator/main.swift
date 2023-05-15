import AppKit
import ArgumentParser

struct FBNeo: ParsableCommand {

    @Flag
    var headless = false

    @Flag(inversion: .prefixedEnableDisable)
    var sound = true

    @Option
    var skippedFrames: UInt8 = 0

    func run() throws {
        cli_settings.headless = headless ? 1 : 0
        cli_settings.sound = !headless && sound ? 1 : 0
        cli_settings.skipped_frames = skippedFrames

        print("CLI settings: \(cli_settings)")

        NSApplicationMain(CommandLine.argc, CommandLine.unsafeArgv)
    }

}

var arguments = CommandLine.arguments
arguments.removeFirst() // remove executable path

// remove debug arguments
if let offset = arguments.firstIndex(of: "-NSDocumentRevisionsDebugMode") {
    arguments.removeSubrange(offset..<offset+2)
}

FBNeo.main(arguments)
