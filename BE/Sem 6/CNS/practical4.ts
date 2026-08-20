/**
 * Rail Fence Cipher Implementation
 * 
 * A transposition cipher that writes plaintext in a zigzag pattern across multiple rails,
 * then reads off each rail sequentially to form the ciphertext.
 */
interface RailFenceParameters {
  plainText: string
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
function railFenceEncrypt({ plainText, rails }: RailFenceParameters): string {
  if (rails < 2) {
    throw new Error("Number of rails must be at least 2")
  }

  // Create rails array
  const railArray: string[] = Array(rails).fill('')
  
  // Current rail position and direction
  let currentRail = 0
  let direction = 1 // 1 for down, -1 for up
  
  // Write characters in zigzag pattern
  for (const char of plainText) {
    railArray[currentRail] += char
    
    // Change direction at top or bottom rail
    if (currentRail === 0) {
      direction = 1
    } else if (currentRail === rails - 1) {
      direction = -1
    }
    
    currentRail += direction
  }
  
  // Combine all rails to form ciphertext
  return railArray.join('')
}

/**
 * Decrypt ciphertext using Rail Fence cipher
 * 
 * Algorithm:
 * 1. Determine the length of each rail by simulating the zigzag pattern
 * 2. Distribute ciphertext characters to each rail
 * 3. Read characters in zigzag pattern to reconstruct plaintext
 */
function railFenceDecrypt({ cipherText, rails }: RailFenceParameters): string {
  if (rails < 2) {
    throw new Error("Number of rails must be at least 2")
  }
  
  const textLength = cipherText.length
  const railArray: string[] = Array(rails).fill('')
  
  // Step 1: Determine length of each rail
  let currentRail = 0
  let direction = 1
  const railLengths: number[] = Array(rails).fill(0)
  
  for (let i = 0; i < textLength; i++) {
    railLengths[currentRail]++
    
    if (currentRail === 0) {
      direction = 1
    } else if (currentRail === rails - 1) {
      direction = -1
    }
    
    currentRail += direction
  }
  
  // Step 2: Distribute ciphertext to rails
  let currentIndex = 0
  for (let rail = 0; rail < rails; rail++) {
    railArray[rail] = cipherText.substring(currentIndex, currentIndex + railLengths[rail])
    currentIndex += railLengths[rail]
  }
  
  // Step 3: Read characters in zigzag pattern
  let decryptedText = ''
  currentRail = 0
  direction = 1
  const railPositions: number[] = Array(rails).fill(0)
  
  for (let i = 0; i < textLength; i++) {
    decryptedText += railArray[currentRail][railPositions[currentRail]]
    railPositions[currentRail]++
    
    if (currentRail === 0) {
      direction = 1
    } else if (currentRail === rails - 1) {
      direction = -1
    }
    
    currentRail += direction
  }
  
  return decryptedText
}

// ============ TEST CASE ============
console.log("=" .repeat(60))
console.log("RAIL FENCE CIPHER - ENCRYPTION AND DECRYPTION")
console.log("=" .repeat(60))

const PLAIN_TEXT = "HELLO WORLD"
const RAILS = 3

console.log(`\nOriginal Text: "${PLAIN_TEXT}"`)
console.log(`Number of Rails: ${RAILS}`)

try {
  // Encrypt
  const encrypted = railFenceEncrypt({ plainText: PLAIN_TEXT, rails: RAILS })
  console.log(`\nEncrypted: "${encrypted}"`)
  
  // Decrypt
  const decrypted = railFenceDecrypt({ cipherText: encrypted, rails: RAILS })
  console.log(`Decrypted: "${decrypted}"`)
  
  console.log("\n✓ Rail Fence cipher test completed successfully")
  console.log(`Encryption successful: ${decrypted === PLAIN_TEXT}`)
  
} catch (error) {
  console.log(`\n✗ Error: ${error.message}`)
}

// Additional test cases
console.log("\n" + "=".repeat(60))
console.log("ADDITIONAL TEST CASES")
console.log("=".repeat(60))

const testCases = [
  { text: "CRYPTOGRAPHY", rails: 4 },
  { text: "NETWORK SECURITY", rails: 3 },
  { text: "RAIL FENCE CIPHER", rails: 2 }
]

testCases.forEach(({ text, rails }, index) => {
  try {
    const encrypted = railFenceEncrypt({ plainText: text, rails })
    const decrypted = railFenceDecrypt({ cipherText: encrypted, rails })
    console.log(`\nTest ${index + 1}: "${text}" (Rails: ${rails})`)
    console.log(`  Encrypted: "${encrypted}"`)
    console.log(`  Decrypted: "${decrypted}"`)
    console.log(`  Success: ${decrypted === text}`)
  } catch (error) {
    console.log(`\n✗ Test ${index + 1} failed: ${error.message}`)
  }
})