import { appendFile, stat } from "node:fs/promises"

const BYTES_TO_ADD = 10

async function increaseFileSizeByTenBytes(filePath: string): Promise<void> {
    const sizeBefore = await stat(filePath).then((stats) => stats.size).catch(() => 0)
    const padding = Buffer.alloc(BYTES_TO_ADD, "0")

    await appendFile(filePath, padding)

    const sizeAfter = (await stat(filePath)).size
    console.log(`File updated: ${filePath}`)
    console.log(`Size before: ${sizeBefore} bytes`)
    console.log(`Size after : ${sizeAfter} bytes`)
}

async function main(): Promise<void> {
    const filePath = process.argv[2] ?? "sample.txt"
    await increaseFileSizeByTenBytes(filePath)
}

main().catch((error: unknown) => {
    const message = error instanceof Error ? error.message : "Unknown error"
    console.error(`Failed to increase file size: ${message}`)
    process.exit(1)
})
