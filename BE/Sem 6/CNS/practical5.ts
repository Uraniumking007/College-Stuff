/**
 * Rail Fence Cipher Implementation
 *
 * A transposition cipher that writes the message in a zigzag pattern
 * across multiple rails, then reads off each rail sequentially.
 */

interface EncryptParameters {
  plainText: string
  rails: number
}

interface DecryptParameters {
  cipherText: string
  rails: number
}

/**
 * Encrypt plaintext using Rail Fence cipher
 *
 * Algorithm:
 * 1. Create 'rails' number of empty strings
 * 2. Write each character in zigzag pattern across rails
 * 3. Read all rails sequentially to form ciphertext
 */
function railFenceEncrypt({ plainText, rails }: EncryptParameters): string {
  if (rails < 2) {
    throw new Error("Number of rails must be at least 2")
  }

  // Create rails array
  const railStrings: string[] = Array.from({ length: rails }, () => "")

  // Write characters in zigzag pattern
  let currentRail = 0
  let direction = 1 // going down

  for (const char of plainText) {
    railStrings[currentRail] += char

    // Change direction at top or bottom rail
    if (currentRail === 0) {
      direction = 1
    } else if (currentRail === rails - 1) {
      direction = -1
    }

    currentRail += direction
  }

  // Read all rails sequentially
  return railStrings.join("")
}

/**
 * Decrypt ciphertext using Rail Fence cipher
 *
 * Algorithm:
 * 1. Determine length of each rail
 * 2. Fill rails with ciphertext characters
 * 3. Read in zigzag pattern to recover plaintext
 */
function railFenceDecrypt({ cipherText, rails }: DecryptParameters): string {
  if (rails < 2) {
    throw new Error("Number of rails must be at least 2")
  }

  const len = cipherText.length

  // Step 1: Determine length of each rail
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

  // Step 2: Fill rails with ciphertext characters
  const railStrings: string[] = []
  let index = 0

  for (let r = 0; r < rails; r++) {
    railStrings.push(cipherText.slice(index, index + railLengths[r]))
    index += railLengths[r]
  }

  // Step 3: Create position array to track indices in each rail
  const railPositions: number[] = new Array(rails).fill(0)

  // Step 4: Read in zigzag pattern
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

// ============ TEST CASE ============

console.log("=" .repeat(60))
console.log("RAIL FENCE CIPHER - TEST CASE")
console.log("=" .repeat(60))

const PLAINTEXT = "Meetme"
const RAILS = 2

console.log(`\nPlaintext: ${PLAINTEXT}`)
console.log(`Number of rails: ${RAILS}`)

// Show the rail pattern for 2 rails
console.log("\nRail Pattern (2 rails):")
console.log("  Rail 0: M . e . m . e  → 'Meme'")
console.log("  Rail 1: . e . e . t .  → 'eet'")

const encrypted = railFenceEncrypt({ plainText: PLAINTEXT, rails: RAILS })
console.log(`\nCiphertext: ${encrypted}`)

const decrypted = railFenceDecrypt({ cipherText: encrypted, rails: RAILS })
console.log(`Decrypted: ${decrypted}`)

// Verification
if (encrypted === "MEMEET") {
  console.log("\n✓ ENCRYPTION VERIFIED: 'Meetme' → 'MEMEET'")
} else {
  console.log(`\n✗ Expected 'MEMEET', got '${encrypted}'`)
}

if (decrypted === PLAINTEXT) {
  console.log("✓ DECRYPTION VERIFIED: Successfully recovered original plaintext")
} else {
  console.log(`✗ Decryption failed: expected '${PLAINTEXT}', got '${decrypted}'`)
}

// Additional test with 3 rails
console.log("\n" + "=".repeat(60))
console.log("ADDITIONAL TEST: 3 Rails")
console.log("=".repeat(60))

const plaintext3 = "WEAREDISCOVEREDFLEEATONCE"
const rails3 = 3

console.log(`\nPlaintext: ${plaintext3}`)
console.log(`Number of rails: ${rails3}`)

const encrypted3 = railFenceEncrypt({ plainText: plaintext3, rails: rails3 })
console.log(`Ciphertext: ${encrypted3}`)

const decrypted3 = railFenceDecrypt({ cipherText: encrypted3, rails: rails3 })
console.log(`Decrypted: ${decrypted3}`)

if (decrypted3 === plaintext3) {
  console.log("\n✓ VERIFIED: 3-rail encryption/decryption works correctly")
} else {
  console.log(`\n✗ Failed: expected '${plaintext3}', got '${decrypted3}'`)
}
