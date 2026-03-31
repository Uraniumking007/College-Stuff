interface HillEncryptParameters {
    plainText: string
    keyMatrix: number[][]
}

interface HillDecryptParameters {
    cipherText: string
    keyMatrix: number[][]
}

const HILL_MODULUS = 26

function hillCharToNum(char: string): number {
    return char.toLowerCase().charCodeAt(0) - 97
}

function hillNumToChar(num: number): string {
    return String.fromCharCode((((num % HILL_MODULUS) + HILL_MODULUS) % HILL_MODULUS) + 65)
}

function hillTextToVector(text: string): number[] {
    return text.toLowerCase().split("").map(hillCharToNum)
}

function hillVectorToText(vector: number[]): string {
    return vector.map(hillNumToChar).join("")
}

function hillMatrixVectorMultiply(matrix: number[][], vector: number[]): number[] {
    const n = matrix.length
    const result: number[] = Array(n).fill(0)

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            result[i] += matrix[i][j] * vector[j]
        }
        result[i] = ((result[i] % HILL_MODULUS) + HILL_MODULUS) % HILL_MODULUS
    }

    return result
}

function hillEncrypt({ plainText, keyMatrix }: HillEncryptParameters): string {
    plainText = plainText.toUpperCase().replace(/[^A-Z]/g, "")
    const n = keyMatrix.length
    let ciphertext = ""

    for (let i = 0; i < plainText.length; i += n) {
        const block = plainText.substring(i, i + n).padEnd(n, "X")
        const vector = hillTextToVector(block)
        const encryptedVector = hillMatrixVectorMultiply(keyMatrix, vector)
        ciphertext += hillVectorToText(encryptedVector)
    }

    return ciphertext
}

function hillCalculateDeterminant(matrix: number[][]): number {
    const n = matrix.length
    if (n === 1) return matrix[0][0]
    if (n === 2) return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    let det = 0
    for (let j = 0; j < n; j++) {
        const minor = hillGetMinor(matrix, 0, j)
        det += Math.pow(-1, j) * matrix[0][j] * hillCalculateDeterminant(minor)
    }
    return det
}

function hillGetMinor(matrix: number[][], row: number, col: number): number[][] {
    return matrix
        .filter((_, i) => i !== row)
        .map(row => row.filter((_, j) => j !== col))
}

function hillGcd(a: number, b: number): number {
    while (b !== 0) {
        ;[a, b] = [b, a % b]
    }
    return Math.abs(a)
}

function hillModInverse(a: number, m: number): number {
    a = ((a % m) + m) % m
    if (hillGcd(a, m) !== 1) {
        throw new Error("Inverse does not exist")
    }

    let [oldR, r] = [a, m]
    let [oldS, s] = [1, 0]

    while (r !== 0) {
        const quotient = Math.floor(oldR / r)
        ;[oldR, r] = [r, oldR - quotient * r]
        ;[oldS, s] = [s, oldS - quotient * s]
    }

    return ((oldS % m) + m) % m
}

function hillCalculateAdjugate(matrix: number[][]): number[][] {
    const n = matrix.length
    const adjugate: number[][] = Array(n).fill(0).map(() => Array(n).fill(0))

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            const minor = hillGetMinor(matrix, i, j)
            const det = hillCalculateDeterminant(minor)
            adjugate[j][i] = Math.pow(-1, i + j) * det
        }
    }

    return adjugate
}

function hillCalculateInverseMatrix(matrix: number[][]): number[][] {
    const det = hillCalculateDeterminant(matrix)
    const detInv = hillModInverse(det, HILL_MODULUS)
    const adjugate = hillCalculateAdjugate(matrix)

    const n = matrix.length
    const inverse: number[][] = Array(n).fill(0).map(() => Array(n).fill(0))

    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            inverse[i][j] = (((adjugate[i][j] * detInv) % HILL_MODULUS) + HILL_MODULUS) % HILL_MODULUS
        }
    }

    return inverse
}

function hillDecrypt({ cipherText, keyMatrix }: HillDecryptParameters): string {
    cipherText = cipherText.toUpperCase().replace(/[^A-Z]/g, "")
    const inverseMatrix = hillCalculateInverseMatrix(keyMatrix)
    const n = inverseMatrix.length
    let plaintext = ""

    for (let i = 0; i < cipherText.length; i += n) {
        const block = cipherText.substring(i, i + n)
        const vector = hillTextToVector(block)
        const decryptedVector = hillMatrixVectorMultiply(inverseMatrix, vector)
        plaintext += hillVectorToText(decryptedVector)
    }

    return plaintext
}

const keyMatrix3 = [
    [17, 17, 5],
    [21, 18, 21],
    [2, 2, 19]
]

const plainText3 = "pay"
const encrypted3 = hillEncrypt({ plainText: plainText3, keyMatrix: keyMatrix3 })
console.log("Plaintext:", plainText3)
console.log("Ciphertext:", encrypted3)
const decrypted3 = hillDecrypt({ cipherText: encrypted3, keyMatrix: keyMatrix3 })
console.log("Decrypted:", decrypted3)
