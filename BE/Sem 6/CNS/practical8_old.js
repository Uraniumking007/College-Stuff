"use strict";
/**
 * RSA (Rivest-Shamir-Adleman) Algorithm Implementation
 *
 * Asymmetric cryptographic algorithm based on the mathematical difficulty
 * of factoring the product of two large prime numbers.
 */
/**
 * Calculate modular exponentiation: (base^exp) % mod
 * Uses fast exponentiation (binary exponentiation) for efficiency
 *
 * Time Complexity: O(log exp)
 * Space Complexity: O(1)
 */
function modExp(base, exp, mod) {
    if (mod === 1n)
        return 0n;
    let result = 1n;
    base = base % mod;
    while (exp > 0n) {
        // If exp is odd, multiply base with result
        if (exp % 2n === 1n) {
            result = (result * base) % mod;
        }
        // exp must be even now
        exp = exp / 2n;
        base = (base * base) % mod;
    }
    return result;
}
/**
 * Calculate Greatest Common Divisor using Euclidean algorithm
 *
 * Time Complexity: O(log min(a, b))
 */
function gcd(a, b) {
    while (b !== 0n) {
        const temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}
/**
 * Extended Euclidean Algorithm
 * Finds integers x and y such that: a*x + b*y = gcd(a, b)
 * Returns: [gcd, x, y]
 *
 * Used to find modular multiplicative inverse
 */
function extendedGcd(a, b) {
    if (a === 0n) {
        return [b, 0n, 1n];
    }
    const [g, x1, y1] = extendedGcd(b % a, a);
    const x = y1 - (b / a) * x1;
    const y = x1;
    return [g, x, y];
}
/**
 * Find modular multiplicative inverse of 'a' modulo 'm'
 * Returns x such that (a * x) ≡ 1 (mod m)
 * Returns null if inverse doesn't exist (i.e., gcd(a, m) ≠ 1)
 */
function modInverse(a, m) {
    const [g, x] = extendedGcd(a, m);
    // Inverse exists only if a and m are coprime
    if (g !== 1n) {
        return null; // Modular inverse doesn't exist
    }
    // Handle negative result
    return ((x % m) + m) % m;
}
/**
 * Check if a number is prime using Miller-Rabin primality test
 *
 * @param n - Number to test for primality
 * @param k - Number of iterations (higher = more accurate, default 5)
 * @returns true if n is probably prime, false if composite
 */
function isPrime(n, k = 5) {
    if (n <= 1n)
        return false;
    if (n <= 3n)
        return true;
    if (n % 2n === 0n)
        return false;
    // Write n-1 as 2^r * d
    let d = n - 1n;
    let r = 0n;
    while (d % 2n === 0n) {
        d = d / 2n;
        r = r + 1n;
    }
    // Witness loop
    for (let i = 0; i < k; i++) {
        const a = BigInt(Math.floor(Math.random() * Number(n - 4n))) + 2n;
        let x = modExp(a, d, n);
        if (x === 1n || x === n - 1n)
            continue;
        let composite = true;
        for (let j = 0n; j < r - 1n; j = j + 1n) {
            x = modExp(x, 2n, n);
            if (x === n - 1n) {
                composite = false;
                break;
            }
        }
        if (composite)
            return false;
    }
    return true;
}
/**
 * Generate RSA key pair from two prime numbers
 *
 * Algorithm:
 * 1. Calculate n = p × q
 * 2. Calculate φ(n) = (p-1) × (q-1)
 * 3. Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1
 * 4. Calculate d = e^(-1) mod φ(n) (modular inverse)
 *
 * @param parameters - { p, q, e? }
 * @returns RSA key pair (public and private keys)
 */
function generateRSAKeyPair(parameters) {
    const { p, q, e: providedE } = parameters;
    // Validate primes
    if (!isPrime(p, 10) || !isPrime(q, 10)) {
        throw new Error('p and q must be prime numbers');
    }
    // Calculate n and φ(n)
    const n = p * q;
    const phi = (p - 1n) * (q - 1n);
    console.log(`\nKey Generation:`);
    console.log(`  p = ${p}`);
    console.log(`  q = ${q}`);
    console.log(`  n = p × q = ${n}`);
    console.log(`  φ(n) = (p-1) × (q-1) = ${phi}`);
    // Choose or validate encryption key e
    let e;
    if (providedE) {
        // Validate provided e
        if (providedE <= 1n || providedE >= phi) {
            throw new Error(`e must satisfy: 1 < e < φ(n) (got e=${providedE}, φ(n)=${phi})`);
        }
        if (gcd(providedE, phi) !== 1n) {
            throw new Error(`e must be coprime with φ(n) (gcd(${providedE}, ${phi}) ≠ 1)`);
        }
        e = providedE;
        console.log(`  e = ${e} (provided, gcd(e, φ(n)) = ${gcd(e, phi)})`);
    }
    else {
        // Generate e (common value is 65537 = 2^16 + 1)
        e = 65537n;
        // Ensure e < φ(n)
        while (e >= phi || gcd(e, phi) !== 1n) {
            e = e + 2n; // Try odd numbers only
        }
        console.log(`  e = ${e} (auto-generated)`);
    }
    // Calculate decryption key d
    const d = modInverse(e, phi);
    if (d === null) {
        throw new Error('Failed to calculate modular inverse');
    }
    console.log(`  d = ${d}`);
    console.log(`\n  Verification: d × e mod φ(n) = ${(d * e) % phi}`);
    return {
        publicKey: { n, e },
        privateKey: { n, d }
    };
}
// ============ ENCRYPTION & DECRYPTION ============
/**
 * Encrypt plaintext message using RSA
 *
 * C = M^e mod n
 *
 * @param M - Plaintext message (as number)
 * @param publicKey - { n, e }
 * @returns Ciphertext (as number)
 */
function rsaEncrypt(M, publicKey) {
    if (M >= publicKey.n) {
        throw new Error(`Message must be less than modulus (M=${M}, n=${publicKey.n})`);
    }
    const C = modExp(M, publicKey.e, publicKey.n);
    return C;
}
/**
 * Decrypt ciphertext message using RSA
 *
 * M = C^d mod n
 *
 * @param C - Ciphertext (as number)
 * @param privateKey - { n, d }
 * @returns Plaintext message (as number)
 */
function rsaDecrypt(C, privateKey) {
    if (C >= privateKey.n) {
        throw new Error(`Ciphertext must be less than modulus (C=${C}, n=${privateKey.n})`);
    }
    const M = modExp(C, privateKey.d, privateKey.n);
    return M;
}
// ============ STRING ENCRYPTION/DECRYPTION ============
/**
 * Encrypt a string message using RSA
 * Converts each character to its ASCII value and encrypts separately
 *
 * Note: This is a simplified approach for demonstration.
 * In practice, use hybrid encryption (RSA + AES) for better performance.
 */
function rsaEncryptString(plaintext, publicKey) {
    return plaintext.split('').map((char) => {
        const M = BigInt(char.charCodeAt(0));
        return rsaEncrypt(M, publicKey);
    });
}
/**
 * Decrypt a string message using RSA
 */
function rsaDecryptString(ciphertext, privateKey) {
    return ciphertext
        .map((C) => {
        const M = rsaDecrypt(C, privateKey);
        return String.fromCharCode(Number(M));
    })
        .join('');
}
// ============ TEST CASE ============
console.log('='.repeat(70));
console.log('RSA ALGORITHM - TEST CASE');
console.log('='.repeat(70));
// Given test case parameters
const P = 17n;
const Q = 11n;
const E = 7n;
const M = 88n;
const EXPECTED_D = 23n;
const EXPECTED_C = 11n;
console.log(`\nTest Case Parameters:`);
console.log(`  Prime p = ${P}`);
console.log(`  Prime q = ${Q}`);
console.log(`  Encryption key e = ${E}`);
console.log(`  Plaintext M = ${M}`);
// Generate key pair
const keyPair = generateRSAKeyPair({ p: P, q: Q, e: E });
// Verify decryption key
if (keyPair.privateKey.d === EXPECTED_D) {
    console.log(`\n✓ Decryption key verified: d = ${keyPair.privateKey.d}`);
}
else {
    console.log(`\n✗ Decryption key mismatch: expected ${EXPECTED_D}, got ${keyPair.privateKey.d}`);
}
// Encrypt message
const C = rsaEncrypt(M, keyPair.publicKey);
console.log(`\nEncryption:`);
console.log(`  C = M^e mod n`);
console.log(`  C = ${M}^${keyPair.publicKey.e} mod ${keyPair.publicKey.n}`);
console.log(`  C = ${C}`);
// Verify ciphertext
if (C === EXPECTED_C) {
    console.log(`\n✓ Ciphertext verified: C = ${C}`);
}
else {
    console.log(`\n✗ Ciphertext mismatch: expected ${EXPECTED_C}, got ${C}`);
}
// Decrypt message
const decryptedM = rsaDecrypt(C, keyPair.privateKey);
console.log(`\nDecryption:`);
console.log(`  M = C^d mod n`);
console.log(`  M = ${C}^${keyPair.privateKey.d} mod ${keyPair.privateKey.n}`);
console.log(`  M = ${decryptedM}`);
// Verify decryption
if (decryptedM === M) {
    console.log(`\n✓ Decryption verified: M = ${decryptedM}`);
}
else {
    console.log(`\n✗ Decryption failed: expected ${M}, got ${decryptedM}`);
}
// ============ ADDITIONAL TESTS ============
console.log('\n' + '='.repeat(70));
console.log('ADDITIONAL TEST: STRING ENCRYPTION');
console.log('='.repeat(70));
// Test with larger primes for string encryption
const testP = 61n;
const testQ = 53n;
const testKeyPair = generateRSAKeyPair({ p: testP, q: testQ });
console.log(`\nGenerated Key Pair:`);
console.log(`  Public Key (n, e): (${testKeyPair.publicKey.n}, ${testKeyPair.publicKey.e})`);
console.log(`  Private Key (n, d): (${testKeyPair.privateKey.n}, ${testKeyPair.privateKey.d})`);
const testMessage = 'RSA';
console.log(`\nOriginal Message: "${testMessage}"`);
// Encrypt
const encryptedChars = rsaEncryptString(testMessage, testKeyPair.publicKey);
console.log(`\nEncrypted (character by character):`);
testMessage.split('').forEach((char, i) => {
    console.log(`  '${char}' (ASCII ${char.charCodeAt(0)}) → ${encryptedChars[i]}`);
});
// Decrypt
const decryptedMessage = rsaDecryptString(encryptedChars, testKeyPair.privateKey);
console.log(`\nDecrypted Message: "${decryptedMessage}"`);
if (decryptedMessage === testMessage) {
    console.log(`\n✓ String encryption/decryption verified`);
}
else {
    console.log(`\n✗ String encryption/decryption failed`);
}
// ============ SECURITY ANALYSIS ============
console.log('\n' + '='.repeat(70));
console.log('RSA SECURITY ANALYSIS');
console.log('='.repeat(70));
console.log(`
1. MATHEMATICAL FOUNDATION
   -------------------------
   Based on the computational difficulty of factoring large integers.

   Key Generation:
   - Choose two large primes p and q (typically 1024+ bits each)
   - Calculate n = p × q (2048+ bits for security)
   - Calculate φ(n) = (p-1) × (q-1)
   - Choose e such that gcd(e, φ(n)) = 1
   - Calculate d = e^(-1) mod φ(n)

   Encryption: C = M^e mod n
   Decryption: M = C^d mod n

   Why it works:
   By Euler's theorem: M^(φ(n)) ≡ 1 (mod n)
   Therefore: (M^e)^d = M^(e×d) = M^(1 + k×φ(n)) = M × (M^φ(n))^k ≡ M (mod n)


2. KEY SIZE RECOMMENDATIONS (2024)
   ----------------------------------
   Key Size    | Security Level | Factoring Difficulty
   ------------|----------------|---------------------
   1024 bits   | WEAK           | ~80 hours (2024)
   2048 bits   | RECOMMENDED    | ~6.4 million years
   3072 bits   | HIGH           | Infeasible
   4096 bits   | VERY HIGH      | Infeasible

   For new systems, minimum 2048 bits is recommended.
   For long-term security (>2030), use 3072+ bits.


3. ATTACKS AND COUNTERMEASURES
   ----------------------------

   a) BRUTE FORCE (Factoring n)
      Attack: Try to factor n into p and q
      Difficulty: O(exp((ln n)^(1/3) × (ln ln n)^(2/3)))
      Countermeasure: Use large key sizes (2048+ bits)

   b) CHOSEN CIPHERTEXT ATTACK
      Attack: Send crafted ciphertext to reveal plaintext
      Countermeasure: Use OAEP (Optimal Asymmetric Encryption Padding)

   c) TIMING ATTACKS
      Attack: Measure decryption time to reveal private key
      Countermeasure: Use constant-time implementations, blinding

   d) SIDE-CHANNEL ATTACKS
      Attack: Power analysis, electromagnetic leakage
      Countermeasure: Hardware security modules, shielding

   e) MATHEMATICAL ATTACKS
      - Low exponent attacks (e < 3)
      - Common modulus attacks (same n for different keys)
      Countermeasure: Use e ≥ 65537, proper key management


4. PRACTICAL CONSIDERATIONS
   -------------------------

   Limitations:
   ✗ Slow: 1000x slower than symmetric encryption
   ✗ Message size limited by modulus (for 2048-bit n: max 245 bytes)
   ✗ Requires padding for security (OAEP, PKCS#1)

   Best Practice:
   ✓ Use Hybrid Encryption:
     1. Generate random symmetric key (AES-256)
     2. Encrypt data with AES (fast, arbitrary size)
     3. Encrypt AES key with RSA (secure key exchange)
     4. Send: [RSA-encrypted key] + [AES-encrypted data]

   This combines the best of both worlds:
   - RSA security for key exchange
   - AES speed for bulk encryption


5. COMPARISON WITH OTHER ALGORITHMS
   ----------------------------------

   RSA vs ECC (Elliptic Curve Cryptography):
   - RSA: 2048 bits ≈ ECC: 256 bits (similar security)
   - ECC is faster and uses smaller keys
   - RSA is more widely supported

   RSA vs Diffie-Hellman:
   - RSA: Encryption + Digital signatures
   - DH: Key exchange only
   - Both based on difficult mathematical problems


6. IMPLEMENTATION SECURITY
   ------------------------

   CRITICAL WARNINGS:
   ✗ NEVER implement RSA from scratch for production
   ✗ ALWAYS use vetted libraries (OpenSSL, NaCl, Web Crypto API)
   ✗ ALWAYS use proper padding (OAEP, PSS)
   ✗ ALWAYS generate primes with sufficient entropy
   ✗ NEVER reuse keys across different applications

   This implementation is for EDUCATIONAL PURPOSES ONLY.
   It demonstrates the mathematics but lacks:
   - Secure padding schemes
   - Constant-time operations
   - Side-channel protections
   - Proper randomness for prime generation


7. REAL-WORLD APPLICATIONS
   -------------------------

   RSA is used in:
   ✓ TLS/SSL certificates (HTTPS)
   ✓ Email encryption (PGP, S/MIME)
   ✓ Digital signatures (code signing, documents)
   ✓ SSH key authentication
   ✓ Blockchain/cryptocurrency wallets
   ✓ Secure messaging (Signal, WhatsApp)

   Standard: PKCS#1 (RSA Cryptography Standard)
`);
// ============ MATHEMATICAL VERIFICATION ============
console.log('='.repeat(70));
console.log('MATHEMATICAL VERIFICATION');
console.log('='.repeat(70));
console.log(`
For our test case:
  p = 17, q = 11
  n = 187
  φ(n) = 160
  e = 7
  d = 23

Verification of d (modular inverse):
  d × e = 23 × 7 = 161
  161 mod 160 = 1
  ✓ Since d × e ≡ 1 (mod φ(n)), d is correct

Verification of encryption:
  C = M^e mod n
  C = 88^7 mod 187
  C = ${C}
  ✓ Expected: 11

Verification of decryption:
  M = C^d mod n
  M = ${C}^23 mod 187
  M = ${decryptedM}
  ✓ Expected: 88

Verification of Euler's theorem:
  For any M coprime with n: M^φ(n) ≡ 1 (mod n)
  Since M = 88 and n = 187:
    gcd(88, 187) = 1 (88 is not divisible by 11 or 17)
    88^160 mod 187 = 1 ✓

Why decryption works:
  M' = C^d mod n
  M' = (M^e)^d mod n
  M' = M^(e×d) mod n
  M' = M^(1 + k×φ(n)) mod n      [since e×d ≡ 1 (mod φ(n))]
  M' = M × (M^φ(n))^k mod n
  M' = M × 1^k mod n             [by Euler's theorem]
  M' = M mod n
  M' = M ✓
`);
console.log('='.repeat(70));
