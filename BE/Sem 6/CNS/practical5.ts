interface ColumnarEncryptParameters {
    plainText: string
    key: string
}

interface ColumnarDecryptParameters {
    cipherText: string
    key: string
}

function columnarParseKey(key: string): number[] {
    const keyDigits = key.split('').map(Number)
    const order = keyDigits.map((_, index) => index)
    order.sort((a, b) => keyDigits[a] - keyDigits[b])
    return order
}

function columnarTranspositionEncrypt({
    plainText,
    key
}: ColumnarEncryptParameters): string {
    const keyLength = key.length

    if (keyLength < 2) {
        throw new Error("Key must have at least 2 digits")
    }

    if (!/^\d+$/.test(key)) {
        throw new Error("Key must contain only digits")
    }

    const numCols = keyLength
    const numRows = Math.ceil(plainText.length / numCols)

    const grid: string[][] = []
    for (let row = 0; row < numRows; row++) {
        grid.push([])
        for (let col = 0; col < numCols; col++) {
            const index = row * numCols + col
            grid[row].push(index < plainText.length ? plainText[index] : '')
        }
    }

    const colOrder = columnarParseKey(key)

    let ciphertext = ''
    for (const colIndex of colOrder) {
        for (let row = 0; row < numRows; row++) {
            if (grid[row][colIndex]) {
                ciphertext += grid[row][colIndex]
            }
        }
    }

    return ciphertext
}

function columnarTranspositionDecrypt({
    cipherText,
    key
}: ColumnarDecryptParameters): string {
    const keyLength = key.length

    if (keyLength < 2) {
        throw new Error("Key must have at least 2 digits")
    }

    if (!/^\d+$/.test(key)) {
        throw new Error("Key must contain only digits")
    }

    const numCols = keyLength
    const numRows = Math.ceil(cipherText.length / numCols)

    const colLengths: number[] = []
    for (let col = 0; col < numCols; col++) {
        const fullRows = Math.floor(cipherText.length / numCols)
        const extra = col < (cipherText.length % numCols) ? 1 : 0
        colLengths.push(fullRows + extra)
    }

    const colOrder = columnarParseKey(key)

    const grid: string[][] = Array.from({ length: numRows }, () =>
        new Array(numCols).fill('')
    )

    let textIndex = 0
    for (const colIndex of colOrder) {
        for (let row = 0; row < colLengths[colIndex]; row++) {
            grid[row][colIndex] = cipherText[textIndex++]
        }
    }

    let plaintext = ''
    for (let row = 0; row < numRows; row++) {
        for (let col = 0; col < numCols; col++) {
            if (grid[row][col]) {
                plaintext += grid[row][col]
            }
        }
    }

    return plaintext
}

const plainText5 = "hello world"
const key5 = "312"

const encrypted5 = columnarTranspositionEncrypt({ plainText: plainText5, key: key5 })
console.log("Plaintext:", plainText5)
console.log("Key:", key5)
console.log("Ciphertext:", encrypted5)

const decrypted5 = columnarTranspositionDecrypt({ cipherText: encrypted5, key: key5 })
console.log("Decrypted:", decrypted5)
