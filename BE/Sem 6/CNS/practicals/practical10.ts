import { execFile } from "node:child_process"
import { promisify } from "node:util"
import path from "node:path"

const execFileAsync = promisify(execFile)

async function createShortcut(targetFilePath: string, shortcutPath: string): Promise<void> {
    const escapedTarget = targetFilePath.replace(/'/g, "''")
    const escapedShortcut = shortcutPath.replace(/'/g, "''")

    const script = [
        "$ws = New-Object -ComObject WScript.Shell",
        `$s = $ws.CreateShortcut('${escapedShortcut}')`,
        `$s.TargetPath = '${escapedTarget}'`,
        "$s.Save()"
    ].join("; ")

    await execFileAsync("powershell.exe", [
        "-NoProfile",
        "-NonInteractive",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        script
    ])
}

async function main(): Promise<void> {
    const targetFilePath = "C:\\Users\\Public\\Documents\\sample.txt"
    const shortcutPath = path.join(process.cwd(), "sample-shortcut.lnk")

    await createShortcut(targetFilePath, shortcutPath)
    console.log(`Shortcut created successfully at: ${shortcutPath}`)
}

main().catch((error: unknown) => {
    const message = error instanceof Error ? error.message : "Unknown error"
    console.error(`Failed to create shortcut: ${message}`)
    process.exit(1)
})
