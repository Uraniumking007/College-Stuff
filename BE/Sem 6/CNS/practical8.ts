/**
 * Practical 8: RSA Algorithm Implementation
 * 
 * This implementation demonstrates the RSA (Rivest-Shamir-Adleman) algorithm,
 * an asymmetric cryptographic algorithm based on the mathematical properties
 * of large prime numbers.
 */

interface RSAKeyPair {
   p: number      // First prime number
   q: number      // Second prime number
   n: number      // Modulus (n = p × q)
   phi: number    // Euler's totient function φ(n) = (p-1) × (q-1)
   e: number      // Public exponent (encryption key)
   d: number      // Private exponent (decryption key)
}

interface RSAEncryptParameters {
   message: number
   e: number
   n: number
}

interface RSADecryptParameters {
   ciphertext: number
   d: number
   n: number
}

/**
 * Calculates the greatest common divisor using Euclid's algorithm
 * @param a - First number
 * @param b - Second number
 * @returns GCD of a and b
 */
function gcd(a: number, b: number): number {
   a = Math.abs(a)
   b = Math.abs(b)
   while (b !== 0) {
      const temp = b
      b = a % b
      a = temp
   }
   return a
}

/**
 * Calculates modular exponentiation (base^exp mod mod) efficiently
 * Uses the binary exponentiation method to avoid overflow
 * @param base - The base number
 * @param exp - The exponent
 * @param mod - The modulus
 * @returns (base^exp) mod mod
 */
function modPow(base: number, exp: number, mod: number): number {
   if (mod === 1) return 0

   let result = 1
   base = base % mod

   while (exp > 0) {
      // If exp is odd, multiply result with base
      if (exp % 2 === 1) {
         result = (result * base) % mod
      }

      // Square the base
      base = (base * base) % mod

      // Divide exp by 2
      exp = Math.floor(exp / 2)
   }

   return result
}

/**
 * Uses Extended Euclidean Algorithm to find modular multiplicative inverse
 * Finds d such that (e * d) ≡ 1 (mod phi)
 * @param e - The number to find inverse for
 * @param phi - The modulus
 * @returns The modular multiplicative inverse of e mod phi
 */
function modInverse(e: number, phi: number): number {
   let m0 = phi
   let y = 0
   let x = 1

   if (phi === 1) return 0

   let a = e
   let b = phi

   while (a > 1) {
      // q is quotient
      const q = Math.floor(a / b)

      let t = b
      b = a % b
      a = t

      t = y
      y = x - q * y
      x = t
   }

   // Make x positive
   if (x < 0) x += m0

   return x
}

/**
 * Checks if a number is prime using trial division
 * @param num - Number to check
 * @returns true if prime, false otherwise
 */
function isPrime(num: number): boolean {
   if (num <= 1) return false
   if (num <= 3) return true
   if (num % 2 === 0 || num % 3 === 0) return false

   for (let i = 5; i * i <= num; i += 6) {
      if (num % i === 0 || num % (i + 2) === 0) {
         return false
      }
   }
   return true
}

/**
 * Generates RSA key pair from two prime numbers
 * @param p - First prime number
 * @param q - Second prime number
 * @param e - Public exponent (must be coprime with φ(n))
 * @returns RSA key pair with all parameters
 */
function generateRSAKeyPair(p: number, q: number, e: number): RSAKeyPair {
   // Validate inputs
   if (!isPrime(p)) {
      throw new Error(`p must be prime: ${p} is not prime`)
   }
   if (!isPrime(q)) {
      throw new Error(`q must be prime: ${q} is not prime`)
   }
   if (p === q) {
      throw new Error("p and q must be different primes")
   }

   // Calculate n and φ(n)
   const n = p * q
   const phi = (p - 1) * (q - 1)

   // Validate e
   if (e <= 1 || e >= phi) {
      throw new Error(`e must satisfy 1 < e < φ(n): 1 < ${e} < ${phi}`)
   }

   if (gcd(e, phi) !== 1) {
      throw new Error(`e must be coprime with φ(n): gcd(${e}, ${phi}) = ${gcd(e, phi)}`)
   }

   // Calculate d (decryption key)
   const d = modInverse(e, phi)

   return { p, q, n, phi, e, d }
}

/**
 * Encrypts a message using RSA
 * @param message - The plaintext message (as number)
 * @param e - Public exponent
 * @param n - Modulus
 * @returns The ciphertext
 */
function rsaEncrypt({ message, e, n }: RSAEncryptParameters): number {
   if (message >= n) {
      throw new Error(`Message must be less than n: ${message} >= ${n}`)
   }
   if (message < 0) {
      throw new Error(`Message must be non-negative: ${message}`)
   }

   return modPow(message, e, n)
}

/**
 * Decrypts a ciphertext using RSA
 * @param ciphertext - The ciphertext (as number)
 * @param d - Private exponent
 * @param n - Modulus
 * @returns The decrypted plaintext message
 */
function rsaDecrypt({ ciphertext, d, n }: RSADecryptParameters): number {
   if (ciphertext >= n) {
      throw new Error(`Ciphertext must be less than n: ${ciphertext} >= ${n}`)
   }
   if (ciphertext < 0) {
      throw new Error(`Ciphertext must be non-negative: ${ciphertext}`)
   }

   return modPow(ciphertext, d, n)
}

/**
 * Visualizes the RSA key generation process
 */
function visualizeKeyGeneration(keyPair: RSAKeyPair): void {
   console.log("\n=== RSA KEY GENERATION ===\n")

   console.log("Step 1: Choose two distinct prime numbers p and q")
   console.log(`  p = ${keyPair.p}`)
   console.log(`  q = ${keyPair.q}`)

   console.log("\nStep 2: Calculate n = p × q")
   console.log(`  n = ${keyPair.p} × ${keyPair.q} = ${keyPair.n}`)

   console.log("\nStep 3: Calculate φ(n) = (p-1) × (q-1)")
   console.log(`  φ(n) = (${keyPair.p}-1) × (${keyPair.q}-1)`)
   console.log(`  φ(n) = ${keyPair.p - 1} × ${keyPair.q - 1} = ${keyPair.phi}`)

   console.log("\nStep 4: Choose encryption key e")
   console.log(`  e = ${keyPair.e}`)
   console.log(`  Conditions:`)
   console.log(`    1 < e < φ(n): 1 < ${keyPair.e} < ${keyPair.phi} ✓`)
   console.log(`    gcd(e, φ(n)) = 1: gcd(${keyPair.e}, ${keyPair.phi}) = ${gcd(keyPair.e, keyPair.phi)} ✓`)

   console.log("\nStep 5: Calculate decryption key d")
   console.log(`  d × e ≡ 1 (mod φ(n))`)
   console.log(`  d × ${keyPair.e} ≡ 1 (mod ${keyPair.phi})`)
   console.log(`  d = ${keyPair.d}`)
   console.log(`  Verification: ${keyPair.d} × ${keyPair.e} = ${keyPair.d * keyPair.e}`)
   console.log(`  ${keyPair.d * keyPair.e} mod ${keyPair.phi} = ${(keyPair.d * keyPair.e) % keyPair.phi} ✓`)

   console.log("\nPublic Key: (e, n) = (" + keyPair.e + ", " + keyPair.n + ")")
   console.log("Private Key: (d, n) = (" + keyPair.d + ", " + keyPair.n + ")")
}

/**
 * Visualizes the encryption/decryption process
 */
function visualizeEncryptionDecryption(
   message: number,
   ciphertext: number,
   decrypted: number,
   keyPair: RSAKeyPair
): void {
   console.log("\n=== RSA ENCRYPTION/DECRYPTION ===\n")

   console.log("Encryption:")
   console.log(`  C = M^e mod n`)
   console.log(`  C = ${message}^${keyPair.e} mod ${keyPair.n}`)
   console.log(`  C = ${ciphertext}`)

   console.log("\nDecryption:")
   console.log(`  M = C^d mod n`)
   console.log(`  M = ${ciphertext}^${keyPair.d} mod ${keyPair.n}`)
   console.log(`  M = ${decrypted}`)

   console.log("\nVerification:")
   console.log(`  Original:  ${message}`)
   console.log(`  Decrypted: ${decrypted}`)
   console.log(`  Match: ${message === decrypted ? "✓" : "✗"}`)
}

/**
 * Analyzes the cryptographic strength of RSA
 */
function analyzeCryptanalysis(): void {
   console.log("\n=== CRYPTANALYSIS OF RSA ===\n")

   console.log("Mathematical Foundation:")
   console.log("  RSA is based on the practical difficulty of factoring the product")
   console.log("  of two large prime numbers (the factoring problem)")

   console.log("\nKey Generation Requirements:")
   console.log("  1. p and q must be large primes (typically 1024+ bits each)")
   console.log("  2. p and q must be kept secret")
   console.log("  3. n = p × q is public (modulus)")
   console.log("  4. φ(n) = (p-1)(q-1) must not be easily derivable from n")
   console.log("  5. e must be coprime with φ(n)")
   console.log("  6. d is the modular multiplicative inverse of e mod φ(n)")

   console.log("\nSecurity Strengths:")
   console.log("  1. Asymmetric: Public key can encrypt, private key decrypts")
   console.log("  2. Strong mathematical foundation (factoring problem)")
   console.log("  3. Key size can be increased as computing power grows")
   console.log("  4. Widely studied and standardized")

   console.log("\nSecurity Weaknesses:")
   console.log("  1. Vulnerable to brute force if keys are too small")
   console.log("  2. Vulnerable to factoring attacks (improved algorithms)")
   console.log("  3. Poor padding can lead to attacks")
   console.log("  4. Side-channel attacks (timing, power analysis)")
   console.log("  5. Key generation must use truly random primes")

   console.log("\nCommon Attacks:")
   console.log("  1. Brute Force: Try all possible private keys")
   console.log("  2. Integer Factorization: Factor n into p and q")
   console.log("     - Trial division (inefficient for large n)")
   console.log("     - Quadratic sieve")
   console.log("     - General number field sieve (GNFS)")
   console.log("  3. Timing Attacks: Measure decryption time")
   console.log("  4. Chosen Ciphertext Attacks:")
   console.log("     - Send modified ciphertexts to learn about plaintext")
   console.log("  5. Mathematical Attacks on Poor Implementation:")
   console.log("     - Small p and q")
   console.log("     - p and q too close together")
   console.log("     - Small encryption exponent e with small message")

   console.log("\nRecommended Key Sizes (as of 2024):")
   console.log("  - 2048 bits: Minimum recommended for new systems")
   console.log("  - 3072 bits: For long-term security")
   console.log("  - 4096 bits: For high-security applications")
   console.log("  - 8192 bits: Future-proofing (very slow)")

   console.log("\nBest Practices:")
   console.log("  1. Use proper padding (OAEP, PKCS#1 v2.2)")
   console.log("  2. Use sufficiently large key sizes (2048+ bits)")
   console.log("  3. Don't roll your own crypto - use established libraries")
   console.log("  4. Protect private key from unauthorized access")
   console.log("  5. Use RSA for key exchange, AES for data encryption")
   console.log("  6. Verify certificates when using public keys")
}

/**
 * Demonstrates RSA algorithm with test cases
 */
function demonstrateRSAAlgorithm(): void {
   console.log("=== RSA ALGORITHM DEMONSTRATION ===\n")

   // Test case from practical: p=17, q=11, e=7
   console.log("Test Case 1: p=17, q=11, e=7, M=88")
   console.log("-".repeat(50))

   const keyPair = generateRSAKeyPair(17, 11, 7)

   // Verify d = 23 as given
   console.log("\nVerification of decryption key:")
   console.log(`  Expected d = 23`)
   console.log(`  Calculated d = ${keyPair.d}`)
   console.log(`  Match: ${keyPair.d === 23 ? "✓" : "✗"}`)

   visualizeKeyGeneration(keyPair)

   const message = 88
   console.log("\nOriginal Message (M):", message)

   // Encrypt
   const ciphertext = rsaEncrypt({ message, e: keyPair.e, n: keyPair.n })
   console.log("\nCiphertext (C):", ciphertext)
   console.log("Expected C:      11")
   console.log("Match:", ciphertext === 11 ? "✓" : "✗")

   // Decrypt
   const decrypted = rsaDecrypt({ ciphertext, d: keyPair.d, n: keyPair.n })
   console.log("\nDecrypted Message:", decrypted)

   visualizeEncryptionDecryption(message, ciphertext, decrypted, keyPair)

   console.log("\n" + "=".repeat(50) + "\n")

   // Test case 2: Different example
   console.log("Test Case 2: p=61, q=53, e=17")
   console.log("-".repeat(50))

   const keyPair2 = generateRSAKeyPair(61, 53, 17)
   visualizeKeyGeneration(keyPair2)

   const message2 = 123
   console.log("\nOriginal Message (M):", message2)

   const ciphertext2 = rsaEncrypt({ message: message2, e: keyPair2.e, n: keyPair2.n })
   console.log("Ciphertext (C):", ciphertext2)

   const decrypted2 = rsaDecrypt({ ciphertext: ciphertext2, d: keyPair2.d, n: keyPair2.n })
   console.log("Decrypted Message:", decrypted2)

   visualizeEncryptionDecryption(message2, ciphertext2, decrypted2, keyPair2)

   // Cryptanalysis
   analyzeCryptanalysis()
}

// Run the demonstration
demonstrateRSAAlgorithm()
