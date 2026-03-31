interface RailFenceEncryptParameters {
    plainText: string
    rails: number
}

interface RailFenceDecryptParameters {
    cipherText: string
    rails: number
}

function railFenceEncrypt({ plainText, rails }: RailFenceEncryptParameters): string {
    if (rails < 2) {
        throw new Error("Number of rails must be at least 2")
    }

    const railStrings: string[] = Array.from({ length: rails }, () => "")

    let currentRail = 0
    let direction = 1

    for (const char of plainText) {
        railStrings[currentRail] += char

        if (currentRail === 0) {
            direction = 1
        } else if (currentRail === rails - 1) {
            direction = -1
        }

        currentRail += direction
    }

    return railStrings.join("")
}

function railFenceDecrypt({ cipherText, rails }: RailFenceDecryptParameters): string {
    if (rails < 2) {
        throw new Error("Number of rails must be at least 2")
    }

    const len = cipherText.length

    const railLengths: number[] = new Array(rails).fill(0)
    let currentRail = 0
    let direction = 1

    for (let i = 0; i < len; i++) {
        railLengths[currentRail]++

        if (currentRail === 0) {
            direction = 1
        } else if (currentRail === rails - 1) {
            direction = -1
        }

        currentRail += direction
    }

    const railStrings: string[] = []
    let index = 0

    for (let r = 0; r < rails; r++) {
        railStrings.push(cipherText.slice(index, index + railLengths[r]))
        index += railLengths[r]
    }

    const railPositions: number[] = new Array(rails).fill(0)

    let result = ""
    currentRail = 0
    direction = 1

    for (let i = 0; i < len; i++) {
        result += railStrings[currentRail][railPositions[currentRail]]
        railPositions[currentRail]++

        if (currentRail === 0) {
            direction = 1
        } else if (currentRail === rails - 1) {
            direction = -1
        }

        currentRail += direction
    }

    return result
}

const plainText7 = "Meetme"
const rails7 = 2

console.log("RAIL FENCE CIPHER")
console.log(`Plaintext: ${plainText7}`)
console.log(`Rails: ${rails7}`)

const encrypted7 = railFenceEncrypt({ plainText: plainText7, rails: rails7 })
console.log(`Ciphertext: ${encrypted7}`)

const decrypted7 = railFenceDecrypt({ cipherText: encrypted7, rails: rails7 })
console.log(`Decrypted: ${decrypted7}`)

if (encrypted7 === "MEMEET") {
    console.log("\n✓ ENCRYPTION VERIFIED")
}

if (decrypted7 === plainText7) {
    console.log("✓ DECRYPTION VERIFIED")
}
