import { execFile } from "node:child_process"
import { promisify } from "node:util"
const execFileAsync = promisify(execFile)

interface ShortcutOptions {
    targetFilePath: string
    shortcutPath: string
}

async function createFileShortcut({ targetFilePath, shortcutPath }: ShortcutOptions): Promise<void> {
    const escapedTarget = targetFilePath.replace(/'/g, "''")
    const escapedShortcut = shortcutPath.replace(/'/g, "''")

    const command = [
        "$shell = New-Object -ComObject WScript.Shell",
        `$shortcut = $shell.CreateShortcut('${escapedShortcut}')`,
        `$shortcut.TargetPath = '${escapedTarget}'`,
        "$shortcut.Save()"
    ].join("; ")

    await execFileAsync("powershell.exe", [
        "-NoProfile",
        "-NonInteractive",
        "-ExecutionPolicy",
        "Bypass",
        "-Command",
        command
    ])
}

async function main(): Promise<void> {
    const targetFilePath = "C:\\Users\\Public\\Documents\\sample.txt"
    const desktopPath = process.env.USERPROFILE
        ? `${process.env.USERPROFILE}\\Desktop`
        : "C:\\Users\\Public\\Desktop"
    const shortcutPath = `${desktopPath}\\sample-file-shortcut.lnk`

    await createFileShortcut({ targetFilePath, shortcutPath })
    console.log(`Shortcut created at: ${shortcutPath}`)
}

main().catch((error: unknown) => {
    const message = error instanceof Error ? error.message : "Unknown error"
    console.error(`Failed to create shortcut: ${message}`)
    process.exit(1)
})
