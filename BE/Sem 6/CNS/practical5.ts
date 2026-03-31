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
        throw new Error("Rails must be at least 2")
    }

    const normalizedText = plainText.toUpperCase().replace(/\s+/g, '')
    const fence: string[][] = Array.from({ length: rails }, () => [])

    let rail = 0
    let direction = 1

    for (const char of normalizedText) {
        fence[rail].push(char)

        if (rail === 0) {
            direction = 1
        } else if (rail === rails - 1) {
            direction = -1
        }

        rail += direction
    }

    return fence.map((r) => r.join('')).join('')
}

function railFenceDecrypt({ cipherText, rails }: RailFenceDecryptParameters): string {
    if (rails < 2) {
        throw new Error("Rails must be at least 2")
    }

    const n = cipherText.length
    const railLengths: number[] = Array(rails).fill(0)

    let rail = 0
    let direction = 1

    for (let i = 0; i < n; i++) {
        railLengths[rail]++

        if (rail === 0) {
            direction = 1
        } else if (rail === rails - 1) {
            direction = -1
        }

        rail += direction
    }

    const fence: string[][] = Array.from({ length: rails }, () => [])

    let index = 0
    for (let i = 0; i < rails; i++) {
        for (let j = 0; j < railLengths[i]; j++) {
            fence[i].push(cipherText[index++])
        }
    }

    const result: string[] = []
    rail = 0
    direction = 1
    const railIndices: number[] = Array(rails).fill(0)

    for (let i = 0; i < n; i++) {
        result.push(fence[rail][railIndices[rail]++])

        if (rail === 0) {
            direction = 1
        } else if (rail === rails - 1) {
            direction = -1
        }

        rail += direction
    }

    return result.join('')
}

const plainText5 = "Meetme"
const rails5 = 2

const encrypted5 = railFenceEncrypt({ plainText: plainText5, rails: rails5 })
console.log(encrypted5)

const decrypted5 = railFenceDecrypt({ cipherText: encrypted5, rails: rails5 })
console.log(decrypted5)
