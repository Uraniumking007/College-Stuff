/**
 * Standard RSA Implementation — No Optimizations
 *
 * Implements RSA from scratch using BigInt:
 *   - Key generation (random prime selection via Miller-Rabin)
 *   - Textbook RSA encrypt / decrypt (m^e mod n, c^d mod n)
 *   - Naive square-and-multiply modular exponentiation
 *   - PKCS#1 v1.5–style padding (simplified)
 *   - Hybrid mode: RSA for key-wrap + AES-256-GCM for bulk data
 *
 * No CRT, no pre-computation, no key caching, no batch shortcuts.
 */

import { randomBytes, createCipheriv, createDecipheriv } from "node:crypto";

// ---------------------------------------------------------------------------
// Modular exponentiation — naive square-and-multiply
// ---------------------------------------------------------------------------

/**
 * Square-and-multiply (left-to-right binary method).
 *
 * The *unoptimised* version: processes one bit at a time,
 * no windowing, no Montgomery reduction.
 */
export function modExp(base: bigint, exp: bigint, mod: bigint): bigint {
  let result = 1n;
  base = base % mod;
  while (exp > 0n) {
    if (exp & 1n) {
      result = (result * base) % mod;
    }
    exp >>= 1n;
    base = (base * base) % mod;
  }
  return result;
}

// ---------------------------------------------------------------------------
// Primality testing
// ---------------------------------------------------------------------------

/**
 * Miller-Rabin primality test with k rounds.
 */
export function isProbablePrime(n: bigint, k: number = 20): boolean {
  if (n < 2n) return false;
  if (n === 2n || n === 3n) return true;
  if (n % 2n === 0n) return false;

  // Write n-1 as 2^r * d
  let r = 0;
  let d = n - 1n;
  while (d % 2n === 0n) {
    d /= 2n;
    r++;
  }

  for (let round = 0; round < k; round++) {
    const a = randomBigIntInRange(2n, n - 2n);
    let x = modExp(a, d, n);
    if (x === 1n || x === n - 1n) continue;
    let found = false;
    for (let i = 0; i < r - 1; i++) {
      x = (x * x) % n;
      if (x === n - 1n) {
        found = true;
        break;
      }
    }
    if (!found) return false;
  }
  return true;
}

/**
 * Generate a random BigInt with the specified number of bits.
 */
function randomBigIntBits(bits: number): bigint {
  const bytes = Math.ceil(bits / 8);
  const buf = randomBytes(bytes);
  // Trim to exact bit length
  let result = bufToBigInt(buf);
  const mask = (1n << BigInt(bits)) - 1n;
  return result & mask;
}

/**
 * Generate a random BigInt in [min, max].
 */
function randomBigIntInRange(min: bigint, max: bigint): bigint {
  const range = max - min + 1n;
  const bits = range.toString(2).length;
  let result: bigint;
  do {
    result = randomBigIntBits(bits);
  } while (result > range);
  return result + min;
}

/**
 * Convert a Buffer to BigInt (big-endian).
 */
function bufToBigInt(buf: Buffer): bigint {
  let result = 0n;
  for (const b of buf) {
    result = (result << 8n) | BigInt(b);
  }
  return result;
}

/**
 * Generate a random prime of the specified bit length.
 */
export function generatePrime(bits: number): bigint {
  while (true) {
    let candidate = randomBigIntBits(bits);
    // Ensure high bit and odd
    candidate |= (1n << BigInt(bits - 1)) | 1n;
    if (isProbablePrime(candidate)) return candidate;
  }
}

// ---------------------------------------------------------------------------
// Key generation
// ---------------------------------------------------------------------------

function gcd(a: bigint, b: bigint): bigint {
  while (b) {
    [a, b] = [b, a % b];
  }
  return a;
}

/**
 * Modular inverse using extended Euclidean algorithm.
 */
function modInverse(e: bigint, phi: bigint): bigint {
  let [old_r, r] = [e, phi];
  let [old_s, s] = [1n, 0n];
  while (r !== 0n) {
    const q = old_r / r;
    [old_r, r] = [r, old_r - q * r];
    [old_s, s] = [s, old_s - q * s];
  }
  return ((old_s % phi) + phi) % phi;
}

export interface PublicKey {
  e: bigint;
  n: bigint;
}

export interface PrivateKey {
  d: bigint;
  n: bigint;
  p: bigint;
  q: bigint;
}

export type KeyPair = { priv: PrivateKey; pub: PublicKey };

/**
 * Generate RSA keypair. Each call generates fresh primes — no caching.
 */
export function generateKeypair(keySize: number = 2048): KeyPair {
  const half = keySize >> 1;
  let p = generatePrime(half);
  let q = generatePrime(half);
  while (q === p) {
    q = generatePrime(half);
  }

  const n = p * q;
  const phi = (p - 1n) * (q - 1n);
  let e = 65537n;
  while (gcd(e, phi) !== 1n) {
    e += 2n;
  }
  const d = modInverse(e, phi);

  return {
    priv: { d, n, p, q },
    pub: { e, n },
  };
}

// ---------------------------------------------------------------------------
// Encrypt / Decrypt
// ---------------------------------------------------------------------------

/** Textbook RSA encryption: c = m^e mod n. */
export function encrypt(pub: PublicKey, plaintext: bigint): bigint {
  return modExp(plaintext, pub.e, pub.n);
}

/** Textbook RSA decryption: m = c^d mod n (full-size exponent, no CRT). */
export function decrypt(priv: PrivateKey, ciphertext: bigint): bigint {
  return modExp(ciphertext, priv.d, priv.n);
}

// ---------------------------------------------------------------------------
// Byte-level helpers (padding)
// ---------------------------------------------------------------------------

/** Simplified PKCS#1 v1.5–style padding → BigInt. */
export function pkcs1Pad(data: Buffer, nBytes: number): bigint {
  const padLen = nBytes - data.length - 3;
  if (padLen < 8) throw new Error("Data too long for key size");
  const padding = randomBytes(padLen);
  // Ensure no zero bytes in padding
  for (let i = 0; i < padding.length; i++) {
    if (padding[i] === 0) padding[i] = 1;
  }
  const padded = Buffer.concat([
    Buffer.from([0x00, 0x02]),
    padding,
    Buffer.from([0x00]),
    data,
  ]);
  return bufToBigInt(padded);
}

/** Strip PKCS#1 v1.5 padding. */
export function pkcs1Unpad(paddedInt: bigint): Buffer {
  const hex = paddedInt.toString(16);
  const byteLen = Math.ceil(hex.length / 2);
  const data = Buffer.alloc(byteLen);
  // Write hex into buffer (big-endian)
  const paddedHex = hex.padStart(byteLen * 2, "0");
  for (let i = 0; i < byteLen; i++) {
    data[i] = parseInt(paddedHex.substring(i * 2, i * 2 + 2), 16);
  }
  // Skip 0x00 0x02 padding... 0x00
  let idx = 2;
  while (idx < data.length && data[idx] !== 0x00) idx++;
  idx++; // skip the 0x00 separator
  return data.subarray(idx);
}

export function encryptBytes(pub: PublicKey, data: Buffer): bigint {
  const nBytes = Math.ceil(pub.n.toString(2).length / 8);
  const m = pkcs1Pad(data, nBytes);
  return encrypt(pub, m);
}

export function decryptBytes(priv: PrivateKey, ciphertext: bigint): Buffer {
  const m = decrypt(priv, ciphertext);
  return pkcs1Unpad(m);
}

// ---------------------------------------------------------------------------
// Hybrid RSA + AES-256-GCM (for bulk data tests)
// Uses Node crypto for AES — RSA itself is from scratch.
// ---------------------------------------------------------------------------

export interface HybridEnvelope {
  wrappedKey: bigint;
  iv: Buffer;
  ct: Buffer;
  tag: Buffer;
}

export function hybridEncrypt(pub: PublicKey, data: Buffer): HybridEnvelope {
  const aesKey = randomBytes(32);
  const iv = randomBytes(12);

  const cipher = createCipheriv("aes-256-gcm", aesKey, iv);
  const ct = Buffer.concat([cipher.update(data), cipher.final()]);
  const tag = cipher.getAuthTag();

  const wrappedKey = encryptBytes(pub, aesKey);

  return { wrappedKey, iv, ct, tag };
}

export function hybridDecrypt(
  priv: PrivateKey,
  envelope: HybridEnvelope,
): Buffer {
  const aesKey = decryptBytes(priv, envelope.wrappedKey);

  const decipher = createDecipheriv(
    "aes-256-gcm",
    aesKey,
    envelope.iv,
  );
  decipher.setAuthTag(envelope.tag);
  return Buffer.concat([
    decipher.update(envelope.ct),
    decipher.final(),
  ]);
}
