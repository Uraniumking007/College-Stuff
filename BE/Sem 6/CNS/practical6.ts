/**
 * Practical 6: Columnar Transposition Cipher Implementation
 * 
 * This implementation demonstrates the Columnar Transposition cipher,
 * a permutation cipher that rearranges plaintext characters based on
 * a numeric key.
 */

interface ColumnarTranspositionEncryptParameters {
   plainText: string
   key: string // Numeric key as string, e.g., "4312567"
}

interface ColumnarTranspositionDecryptParameters {
   cipherText: string
   key: string
}

/**
 * Validates the key format
 * @param key - The numeric key string
 * @throws Error if key is invalid
 */
function validateKey(key: string): void {
   if (!key || key.length === 0) {
      throw new Error("Key cannot be empty")
   }

   // Check if key contains only digits
   if (!/^\d+$/.test(key)) {
      throw new Error("Key must contain only digits")
   }

   // Check if key is a valid permutation (1 to key.length)
   const keyDigits = key.split('').map(Number)
   const expected = Array.from({ length: key.length }, (_, i) => i + 1)
   const sorted = [...keyDigits].sort((a, b) => a - b)

   for (let i = 0; i < sorted.length; i++) {
      if (sorted[i] !== expected[i]) {
         throw new Error(`Key must be a permutation of 1 to ${key.length}`)
      }
   }
}

/**
 * Gets the column reading order based on the key
 * @param key - The numeric key string
 * @returns Array of column indices in reading order
 */
function getReadingOrder(key: string): number[] {
   const keyDigits = key.split('').map(Number)
   const order: number[] = []

   // Create pairs of [position, value] and sort by value
   const pairs = keyDigits.map((value, index) => ({ value, index }))
   pairs.sort((a, b) => a.value - b.value)

   // Extract the sorted indices (reading order)
   for (const pair of pairs) {
      order.push(pair.index)
   }

   return order
}

/**
 * Encrypts plaintext using Columnar Transposition cipher
 * @param plainText - The message to encrypt
 * @param key - Numeric key as string (e.g., "4312567")
 * @returns The encrypted ciphertext
 */
function columnarTranspositionEncrypt({
   plainText,
   key
}: ColumnarTranspositionEncryptParameters): string {
   validateKey(key)

   // Normalize to uppercase and remove spaces
   const normalizedText = plainText.toUpperCase().replace(/\s+/g, '')
   const numCols = key.length
   const numRows = Math.ceil(normalizedText.length / numCols)

   // Create the grid
   const grid: string[][] = Array.from({ length: numRows }, () =>
      Array(numCols).fill('')
   )

   // Fill the grid row by row
   let index = 0
   for (let row = 0; row < numRows; row++) {
      for (let col = 0; col < numCols; col++) {
         if (index < normalizedText.length) {
            grid[row][col] = normalizedText[index++]
         }
      }
   }

   // Get the reading order from the key
   const readingOrder = getReadingOrder(key)

   // Read off columns according to the key order
   let result = ''
   for (const col of readingOrder) {
      for (let row = 0; row < numRows; row++) {
         result += grid[row][col]
      }
   }

   return result
}

/**
 * Decrypts ciphertext using Columnar Transposition cipher
 * @param cipherText - The message to decrypt
 * @param key - Numeric key as string
 * @returns The decrypted plaintext
 */
function columnarTranspositionDecrypt({
   cipherText,
   key
}: ColumnarTranspositionDecryptParameters): string {
   validateKey(key)

   const normalizedText = cipherText.toUpperCase().replace(/\s+/g, '')
   const numCols = key.length
   const numRows = Math.ceil(normalizedText.length / numCols)

   // Calculate how many characters are in each column
   const totalChars = normalizedText.length
   const fullRows = Math.floor(totalChars / numCols)
   const remainder = totalChars % numCols

   const colLengths: number[] = []
   for (let i = 0; i < numCols; i++) {
      // Columns that come first in the grid get an extra character if there's a remainder
      colLengths.push(fullRows + (i < remainder ? 1 : 0))
   }

   // Get the reading order from the key
   const readingOrder = getReadingOrder(key)

   // Reconstruct the grid by distributing ciphertext according to column lengths
   const grid: string[][] = Array.from({ length: numRows }, () =>
      Array(numCols).fill('')
   )

   let textIndex = 0
   for (const col of readingOrder) {
      const colLength = colLengths[col]
      for (let row = 0; row < colLength; row++) {
         grid[row][col] = normalizedText[textIndex++]
      }
   }

   // Read off the grid row by row
   let result = ''
   for (let row = 0; row < numRows; row++) {
      for (let col = 0; col < numCols; col++) {
         result += grid[row][col]
      }
   }

   return result
}

/**
 * Analyzes the cryptographic strength of the transposition cipher
 */
function analyzeCryptanalysis(): void {
   console.log("\n=== CRYPTANALYSIS OF TRANSPOSITION CIPHER ===\n")

   console.log("Strengths:")
   console.log("  1. Simple to implement and understand")
   console.log("  2. No character substitution - only permutation")
   console.log("  3. Can be combined with substitution ciphers for strength")
   console.log("  4. Key space = n! where n is key length")
   console.log("     - For key length 7: 7! = 5,040 possible keys")
   console.log("     - For key length 10: 10! = 3,628,800 possible keys")

   console.log("\nWeaknesses:")
   console.log("  1. Preserves letter frequency distribution")
   console.log("  2. Vulnerable to known-plaintext attacks")
   console.log("  3. Susceptible to anagramming attacks")
   console.log("  4. Short messages with short keys are easily broken")
   console.log("  5. Pattern analysis can reveal column boundaries")

   console.log("\nCommon Attacks:")
   console.log("  1. Brute Force: Try all n! permutations")
   console.log("  2. Frequency Analysis: Letter frequencies remain intact")
   console.log("  3. Anagramming: Rearrange columns until meaningful text appears")
   console.log("  4. Known-plaintext: Deduce key patterns from known pairs")

   console.log("\nComparison: Rail Fence vs Columnar Transposition")
   console.log("  Rail Fence:")
   console.log("    - Fixed zigzag pattern")
   console.log("    - Limited key space (just number of rails)")
   console.log("    - Easier to break due to predictable structure")
   console.log("  Columnar Transposition:")
   console.log("    - Flexible key ordering")
   console.log("    - Larger key space (n! permutations)")
   console.log("    - More complex pattern analysis required")

   console.log("\nRecommendations for Stronger Security:")
   console.log("  1. Use longer keys (10+ digits)")
   console.log("  2. Combine with substitution ciphers (e.g., AES + transposition)")
   console.log("  3. Multiple rounds of transposition")
   console.log("  4. Use modern ciphers instead (AES, ChaCha20)")
}

/**
 * Visualizes the encryption process
 */
function visualizeEncryption(plainText: string, key: string): void {
   console.log("\n=== ENCRYPTION VISUALIZATION ===\n")

   const normalizedText = plainText.toUpperCase().replace(/\s+/g, '')
   const numCols = key.length
   const numRows = Math.ceil(normalizedText.length / numCols)

   console.log(`Plaintext: ${plainText}`)
   console.log(`Normalized: ${normalizedText}`)
   console.log(`Key: ${key}`)
   console.log(`Key length: ${numCols} columns`)
   console.log(`Rows: ${numRows}`)

   // Create and display the grid
   const grid: string[][] = Array.from({ length: numRows }, () =>
      Array(numCols).fill('')
   )

   let index = 0
   for (let row = 0; row < numRows; row++) {
      for (let col = 0; col < numCols; col++) {
         if (index < normalizedText.length) {
            grid[row][col] = normalizedText[index++]
         }
      }
   }

   // Display column headers (key digits)
   console.log("\nGrid (filled row by row):")
   console.log("  " + key.split('').join(' '))
   console.log("  " + "-".repeat(numCols * 2 - 1))

   for (let row = 0; row < numRows; row++) {
      console.log(`| ${grid[row].join(' ')} |`)
   }

   // Display reading order
   const readingOrder = getReadingOrder(key)
   console.log(`\nReading order (by key value): ${readingOrder.map(i => i + 1).join(', ')}`)

   // Display how columns are read
   console.log("\nReading columns in key order:")
   for (const col of readingOrder) {
      let columnText = ''
      for (let row = 0; row < numRows; row++) {
         if (grid[row][col]) {
            columnText += grid[row][col]
         }
      }
      console.log(`  Column ${col + 1} (key value ${key[col]}): ${columnText}`)
   }
}

/**
 * Demonstrates Columnar Transposition cipher with test cases
 */
function demonstrateColumnarTranspositionCipher(): void {
   console.log("=== COLUMNAR TRANSPOSITION CIPHER DEMONSTRATION ===\n")

   // Test case with key "4312567"
   const key = "4312567"
   const plainText = "attackpostponeduntiltwoam"

   console.log("Test Case 1: Key 4312567")
   console.log("Plaintext:", plainText)
   console.log("Key:", key)

   const encrypted = columnarTranspositionEncrypt({ plainText, key })
   console.log("Ciphertext:", encrypted)

   const decrypted = columnarTranspositionDecrypt({ cipherText: encrypted, key })
   console.log("Decrypted:", decrypted)
   console.log("Match:", decrypted.toLowerCase() === plainText.toLowerCase() ? "✓" : "✗")

   console.log("\n" + "-".repeat(50) + "\n")

   // Visual demonstration
   visualizeEncryption(plainText, key)

   console.log("\n" + "-".repeat(50) + "\n")

   // Test case 2: Simple example with key "3142"
   const plainText2 = "Enemyattackstonight"
   const key2 = "3142"

   console.log("\nTest Case 2: Key 3142")
   console.log("Plaintext:", plainText2)
   console.log("Key:", key2)

   const encrypted2 = columnarTranspositionEncrypt({ plainText: plainText2, key: key2 })
   console.log("Ciphertext:", encrypted2)

   const decrypted2 = columnarTranspositionDecrypt({ cipherText: encrypted2, key: key2 })
   console.log("Decrypted:", decrypted2)
   console.log("Match:", decrypted2.toLowerCase() === plainText2.toLowerCase() ? "✓" : "✗")

   // Cryptanalysis
   analyzeCryptanalysis()
}

// Run the demonstration
demonstrateColumnarTranspositionCipher()
