/**
 * Columnar Transposition Cipher Implementation
 *
 * A permutation cipher that rearranges plaintext by writing it in rows
 * and reading columns in the order specified by a numeric key.
 */

interface EncryptParameters {
  plainText: string
  key: string
}

interface DecryptParameters {
  cipherText: string
  key: string
}

/**
 * Parse numeric key into array of 0-indexed column positions
 * Key "4312567" means: read column in order 3, 2, 0, 1, 4, 5, 6
 * (col 1 is 4th, col 2 is 3rd, col 3 is 1st, col 4 is 2nd, etc.)
 */
function parseKey(key: string): number[] {
  const keyDigits = key.split('').map(Number)

  // Create array of column indices sorted by key value
  // Example: key=[4,3,1,2,5,6,7] → order=[2,3,1,0,4,5,6]
  const order = keyDigits.map((_, index) => index)
  order.sort((a, b) => keyDigits[a] - keyDigits[b])

  return order
}

/**
 * Encrypt plaintext using Columnar Transposition cipher
 *
 * Algorithm:
 * 1. Write plaintext in rows of length = key length
 * 2. Read each column in order determined by key
 * 3. Concatenate columns to form ciphertext
 */
function columnarTranspositionEncrypt({
  plainText,
  key
}: EncryptParameters): string {
  const keyLength = key.length

  if (keyLength < 2) {
    throw new Error("Key must have at least 2 digits")
  }

  // Validate key is numeric
  if (!/^\d+$/.test(key)) {
    throw new Error("Key must contain only digits")
  }

  const numCols = keyLength
  const numRows = Math.ceil(plainText.length / numCols)

  // Create grid
  const grid: string[][] = []
  for (let row = 0; row < numRows; row++) {
    grid.push([])
    for (let col = 0; col < numCols; col++) {
      const index = row * numCols + col
      grid[row].push(index < plainText.length ? plainText[index] : '')
    }
  }

  // Parse key to get column reading order
  const colOrder = parseKey(key)

  // Read columns in order specified by key
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

/**
 * Decrypt ciphertext using Columnar Transposition cipher
 *
 * Algorithm:
 * 1. Calculate grid dimensions
 * 2. Determine column lengths (last column may be shorter)
 * 3. Distribute ciphertext across columns in key order
 * 4. Read row by row to recover plaintext
 */
function columnarTranspositionDecrypt({
  cipherText,
  key
}: DecryptParameters): string {
  const keyLength = key.length

  if (keyLength < 2) {
    throw new Error("Key must have at least 2 digits")
  }

  if (!/^\d+$/.test(key)) {
    throw new Error("Key must contain only digits")
  }

  const numCols = keyLength
  const numRows = Math.ceil(cipherText.length / numCols)

  // Calculate column lengths
  const colLengths: number[] = []
  for (let col = 0; col < numCols; col++) {
    const fullRows = Math.floor(cipherText.length / numCols)
    const extra = col < (cipherText.length % numCols) ? 1 : 0
    colLengths.push(fullRows + extra)
  }

  // Parse key to get column reading order
  const colOrder = parseKey(key)

  // Build grid by distributing ciphertext
  const grid: string[][] = Array.from({ length: numRows }, () =>
    new Array(numCols).fill('')
  )

  let textIndex = 0
  for (const colIndex of colOrder) {
    for (let row = 0; row < colLengths[colIndex]; row++) {
      grid[row][colIndex] = cipherText[textIndex++]
    }
  }

  // Read row by row
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

/**
 * Analyze the strength of Columnar Transposition cipher against cryptanalysis
 */
function cryptanalysis() {
  console.log('\n' + '='.repeat(70))
  console.log('CRYPTANALYSIS OF COLUMNAR TRANSPOSITION CIPHER')
  console.log('='.repeat(70))

  console.log(`
1. BRUTE FORCE ATTACK
   -------------------
   Key Space Analysis:
   - For key length L, number of possible keys = L! (L factorial)
   - Key length 7: 7! = 5,040 possible keys
   - Key length 10: 10! ≈ 3.6 million keys
   - Key length 15: 15! ≈ 1.3 trillion keys

   Strength Assessment: WEAK TO MODERATE
   ✓ Better than Rail Fence (limited rail options)
   ✗ Still feasible with modern computing power
   ✗ Key length often limited by message length

   Time estimates (assuming 10^6 key trials/second):
   - Length 5: 120 keys (~0.0001 seconds) - TRIVIAL
   - Length 7: 5,040 keys (~0.005 seconds) - TRIVIAL
   - Length 10: 3.6M keys (~3.6 seconds) - WEAK
   - Length 15: 1.3T keys (~15 days) - MODERATE


2. FREQUENCY ANALYSIS ATTACK
   ---------------------------
   Character Distribution:
   ✓ Letter frequencies are preserved (no substitution)
   ✓ Single-letter frequencies reveal language patterns

   Attack Method:
   - Count character frequencies in ciphertext
   - Compare with known language frequencies (e.g., English)
   - Confirm it's a transposition cipher (not substitution)
   - Use anagramming techniques to reconstruct columns

   Strength Assessment: VERY WEAK
   ✗ Frequencies directly exposed
   ✗ Reveals cipher type immediately
   ✓ But doesn't directly reveal key


3. ANAGRAMMING ATTACK (THE CRITICAL WEAKNESS)
   ------------------------------------------
   Known Plaintext or Ciphertext-Only Approach:

   Step 1: Determine key length
   - Try various lengths (e.g., 5, 6, 7, 8...)
   - Look for reasonable digrams/trigrams when read in columns

   Step 2: Anagramming
   - For each key length, rearrange columns to form meaningful text
   - Use common digrams (TH, HE, IN, ER) and trigrams (THE, ING)
   - Validate with dictionary lookup

   Step 3: Backtracking search
   - Start with most promising column orderings
   - Use depth-first search with pruning
   - Rapidly converges to correct key

   Strength Assessment: WEAK
   ✗ Anagramming breaks short keys (<8) in minutes
   ✗ Dictionary lookup automates validation
   ✗ No specialized knowledge needed


4. KNOWN PLAINTEXT ATTACK
   -----------------------
   With a small known plaintext-ciphertext pair:

   Recovery Process:
   1. Write known plaintext in grid rows
   2. Find where ciphertext segments appear in columns
   3. Directly read off the key order

   Requirements:
   - Need only one plaintext-ciphertext pair
   - Plaintext length ≥ key length

   Strength Assessment: TRIVIAL
   ✗ Single pair breaks entire system
   ✗ Key recovered in O(n) time


5. CHOSEN PLAINTEXT ATTACK
   -------------------------
   Attacker chooses specific plaintext:

   Strategy: Use sequential plaintext (ABCDE... or AAAA...)
   - Creates clear column patterns
   - Directly reveals column ordering
   - Instant key recovery

   Strength Assessment: TRIVIAL
   ✗ One chosen message breaks system completely
   ✗ No computation needed


6. COMPARATIVE ANALYSIS
   ---------------------
   Columnar Transposition vs Rail Fence:

   Similarities:
   + Both are permutation ciphers (preserve letter frequencies)
   + Both rely on position rearrangement only
   + Both vulnerable to anagramming

   Columnar Advantages:
   + Larger key space (L! vs L possible rails)
   + More complex permutation pattern

   Rail Fence Advantages:
   + Simpler implementation
   + Fixed zigzag pattern

   Both suffer from:
   - No confusion (substitution)
   - No diffusion (local changes stay local)
   - Deterministic (same plaintext → same ciphertext)


7. KEY WEAKNESSES SUMMARY
   -----------------------
   CRITICAL VULNERABILITIES:

   a) LINEAR STRUCTURE
      - Permutation is linear transformation
      - Algebraic attacks possible
      - No non-linear mixing

   b) PRESERVED STATISTICS
      - Single-letter frequencies unchanged
      - Reveals language immediately
      - Aids all cryptanalysis methods

   c) SMALL KEY SPACE
      - Practical keys: 6-10 digits
      - 6! = 720, 10! = 3.6M
      - Enumerated quickly

   d) ANAGRAMMING
      - Most effective attack
      - Works with ciphertext-only
      - Automated with dictionaries

   e) NO DIFFUSION
      - Each letter stays in same column
      - Pattern preserved in columns
      - No avalanche effect


8. MODERN CRYPTOGRAPHY CONTEXT
   ----------------------------
   Why Columnar Transposition is obsolete:

   ✓ Historical interest (WWI, WWII era)
   ✓ Educational tool for understanding permutations
   ✓ Component in more complex ciphers (e.g., AES uses permutation)

   ✗ Not secure by modern standards
   ✗ Broken by basic statistical analysis
   ✗ No resistance to known-plaintext attacks
   ✗ Fails all modern design principles:

   Modern Requirements:
   - Confusion (relationship key↔ciphertext complex)
   - Diffusion (plaintext change → widespread ciphertext change)
   - Resistance to known/chosen plaintext
   - Large key space (2^128+ operations)
   - Proven security reduction


9. RECOMMENDATIONS
   ----------------
   If used today (NOT RECOMMENDED):

   Minimum Security Enhancements:
   1. Use with substitution cipher (confusion + diffusion)
   2. Double transposition (two different keys)
   3. Very long keys (12+ digits)
   4. Add padding to obscure column lengths
   5. Multiple rounds with different keys

   Better Alternative:
   - Use modern ciphers: AES, ChaCha20
   - Proven security, standardized
   - Resistant to all known attacks
  `)
}

// ============ TEST CASE ============

console.log('='.repeat(70))
console.log('COLUMNAR TRANSPOSITION CIPHER - TEST CASE')
console.log('='.repeat(70))

const KEY = '4312567'
const PLAINTEXT = 'attackpostponeduntiltwoam'

console.log(`\nKey: ${KEY}`)
console.log(`Plaintext: ${PLAINTEXT}`)
console.log(`Key length: ${KEY.length} columns`)

// Show the grid layout
const numCols = KEY.length
const numRows = Math.ceil(PLAINTEXT.length / numCols)

console.log(`\nGrid Layout (${numRows} rows × ${numCols} columns):`)
console.log('─'.repeat(70))

const grid: string[][] = []
for (let row = 0; row < numRows; row++) {
  const rowData: string[] = []
  for (let col = 0; col < numCols; col++) {
    const index = row * numCols + col
    rowData.push(index < PLAINTEXT.length ? PLAINTEXT[index] : ' ')
  }
  grid.push(rowData)
  console.log(`Row ${row + 1}: ${rowData.join('  ')}`)
}

// Show column reading order
const colOrder = parseKey(KEY)
console.log('\nColumn Reading Order (by key):')
console.log('─'.repeat(70))
for (let i = 0; i < colOrder.length; i++) {
  const col = colOrder[i]
  const colData = grid.map((row) => row[col]).join('')
  console.log(`Position ${i + 1}: Column ${col + 1} → "${colData}"`)
}

const encrypted = columnarTranspositionEncrypt({ plainText: PLAINTEXT, key: KEY })
console.log('\n' + '─'.repeat(70))
console.log(`Ciphertext: ${encrypted}`)

const decrypted = columnarTranspositionDecrypt({
  cipherText: encrypted,
  key: KEY
})
console.log(`Decrypted: ${decrypted}`)

// Verification
console.log('\n' + '='.repeat(70))
console.log('VERIFICATION')
console.log('='.repeat(70))

if (decrypted === PLAINTEXT) {
  console.log('✓ DECRYPTION VERIFIED: Successfully recovered original plaintext')
} else {
  console.log(`✗ Decryption failed: expected '${PLAINTEXT}', got '${decrypted}'`)
}

// Run cryptanalysis
cryptanalysis()

console.log('\n' + '='.repeat(70))
