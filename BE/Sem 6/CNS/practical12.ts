import * as fs from 'fs'

interface FileSizeResult {
    originalSize: number
    newSize: number
    sizeIncrease: number
}

function getFileSize(filePath: string): number {
    if (!fs.existsSync(filePath)) {
        throw new Error(`File not found: ${filePath}`)
    }
    const stats = fs.statSync(filePath)
    return stats.size
}

function formatSize(sizeBytes: number): string {
    const units = ['B', 'KB', 'MB', 'GB']
    let size = sizeBytes
    for (const unit of units) {
        if (size < 1024) {
            return `${size.toFixed(2)} ${unit}`
        }
        size /= 1024
    }
    return `${size.toFixed(2)} TB`
}

function increaseByBytes(filePath: string, bytesToAdd: number): FileSizeResult {
    const originalSize = getFileSize(filePath)
    const buffer = Buffer.alloc(bytesToAdd, 0)
    fs.appendFileSync(filePath, buffer)
    const newSize = getFileSize(filePath)

    return {
        originalSize,
        newSize,
        sizeIncrease: newSize - originalSize
    }
}

function increaseByPercentage(filePath: string, percentage: number): FileSizeResult {
    const originalSize = getFileSize(filePath)
    let bytesToAdd = Math.floor(originalSize * (percentage / 100.0))
    bytesToAdd = Math.max(1, bytesToAdd)

    const buffer = Buffer.alloc(bytesToAdd, 0)
    fs.appendFileSync(filePath, buffer)
    const newSize = getFileSize(filePath)

    return {
        originalSize,
        newSize,
        sizeIncrease: newSize - originalSize
    }
}

function increaseByMultiplier(filePath: string, multiplier: number): FileSizeResult {
    const originalSize = getFileSize(filePath)
    const targetSize = Math.floor(originalSize * multiplier)
    let bytesToAdd = targetSize - originalSize
    bytesToAdd = Math.max(1, bytesToAdd)

    const buffer = Buffer.alloc(bytesToAdd, 0)
    fs.appendFileSync(filePath, buffer)
    const newSize = getFileSize(filePath)

    return {
        originalSize,
        newSize,
        sizeIncrease: newSize - originalSize
    }
}

function displayResult(result: FileSizeResult, method: string): void {
    console.log(`\nMethod: ${method}`)
    console.log(`Original size: ${result.originalSize} bytes (${formatSize(result.originalSize)})`)
    console.log(`New size:      ${result.newSize} bytes (${formatSize(result.newSize)})`)
    console.log(`Size increase: ${result.sizeIncrease} bytes (${formatSize(result.sizeIncrease)})`)
}

const testFile = 'test_file.txt'
fs.writeFileSync(testFile, 'Hello, World!\n')

console.log('FILE SIZE INCREASE PROGRAM')
console.log(`\nCreated test file: ${testFile}`)
console.log(`Initial size: ${formatSize(getFileSize(testFile))}`)

const result1 = increaseByBytes(testFile, 10)
displayResult(result1, 'Add 10 bytes')

const result2 = increaseByPercentage(testFile, 10)
displayResult(result2, 'Increase by 10%')

const result3 = increaseByMultiplier(testFile, 2)
displayResult(result3, 'Multiply by 2')

fs.unlinkSync(testFile)
console.log(`\nCleaned up test file: ${testFile}`)
