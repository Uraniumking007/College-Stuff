/**
 * Optimized RSA Implementation
 *
 * Optimisations over standard RSA:
 *   1. CRT (Chinese Remainder Theorem) for decryption — ~4x speedup
 *   2. Sliding-window modular exponentiation (4-bit window)
 *   3. Montgomery multiplication for modular arithmetic
 *   4. Key caching — generate once, reuse across operations
 *   5. Batch encrypt/decrypt with amortised overhead
 *   6. Pre-computed CRT parameters (dp, dq, qInv) stored in private key
 *   7. Hybrid RSA+AES-256-GCM using Node crypto for AES
 *   8. Fault-attack protection — verify decryption result before returning
 */

import { randomBytes, createCipheriv, createDecipheriv } from "node:crypto";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Python-style modulo: always returns non-negative result.
 * JS BigInt % can return negatives; this fixes it.
 */
function pymod(a: bigint, b: bigint): bigint {
  return ((a % b) + b) % b;
}

function bufToBigInt(buf: Buffer): bigint {
  let result = 0n;
  for (const b of buf) {
    result = (result << 8n) | BigInt(b);
  }
  return result;
}

function randomBigIntBits(bits: number): bigint {
  const bytes = Math.ceil(bits / 8);
  const buf = randomBytes(bytes);
  let result = bufToBigInt(buf);
  const mask = (1n << BigInt(bits)) - 1n;
  return result & mask;
}

function randomBigIntInRange(min: bigint, max: bigint): bigint {
  const range = max - min + 1n;
  const bits = range.toString(2).length;
  let result: bigint;
  do {
    result = randomBigIntBits(bits);
  } while (result > range);
  return result + min;
}

// ---------------------------------------------------------------------------
// Primality testing (small-prime sieve + Miller-Rabin)
// ---------------------------------------------------------------------------

const SMALL_PRIMES = [
  2n, 3n, 5n, 7n, 11n, 13n, 17n, 19n, 23n, 29n, 31n, 37n, 41n, 43n, 47n,
  53n, 59n, 61n, 67n, 71n, 73n, 79n, 83n, 89n, 97n,
];

export function isProbablePrime(n: bigint, k: number = 20): boolean {
  if (n < 2n) return false;
  for (const p of SMALL_PRIMES) {
    if (n % p === 0n) return n === p;
  }

  let r = 0;
  let d = n - 1n;
  while (d % 2n === 0n) {
    d /= 2n;
    r++;
  }

  for (let round = 0; round < k; round++) {
    const a = randomBigIntInRange(2n, n - 2n);
    let x = modPow(a, d, n); // uses built-in for prime test speed
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
 * Built-in modular exponentiation (used for primality test speed).
 * Inlined here to avoid circular dependency on our custom modExp.
 */
function modPow(base: bigint, exp: bigint, mod: bigint): bigint {
  let result = 1n;
  base = pymod(base, mod);
  while (exp > 0n) {
    if (exp & 1n) result = pymod(result * base, mod);
    exp >>= 1n;
    base = pymod(base * base, mod);
  }
  return result;
}

export function generatePrime(bits: number): bigint {
  while (true) {
    let candidate = randomBigIntBits(bits);
    candidate |= (1n << BigInt(bits - 1)) | 1n;
    if (isProbablePrime(candidate)) return candidate;
  }
}

// ---------------------------------------------------------------------------
// Montgomery Multiplication
// ---------------------------------------------------------------------------

export class MontgomeryContext {
  readonly n: bigint;
  readonly r: bigint;
  readonly rInv: bigint;
  readonly nPrime: bigint;
  readonly r2: bigint;

  constructor(n: bigint) {
    this.n = n;
    this.r = 1n << BigInt(n.toString(2).length); // R = 2^k where k = bit_length(n)
    this.rInv = modInverse(this.r, n);
    this.nPrime = pymod(-modInverse(n, this.r), this.r); // n' such that n*n' ≡ -1 (mod R)
    this.r2 = pymod(this.r * this.r, n);
  }

  toMont(x: bigint): bigint {
    return pymod(x * this.r, this.n);
  }

  fromMont(x: bigint): bigint {
    return pymod(x * this.rInv, this.n);
  }

  /** Montgomery reduction (REDC). */
  reduce(t: bigint): bigint {
    const { n, r, nPrime } = this;
    const m = pymod(t * nPrime, r);
    let result = (t + m * n) / r;
    if (result >= n) result -= n;
    if (result < 0n) result += n;
    return result;
  }

  /** Montgomery multiplication: a*b*R^-1 mod n. */
  mul(a: bigint, b: bigint): bigint {
    return this.reduce(a * b);
  }
}

// ---------------------------------------------------------------------------
// Sliding-window modular exponentiation
// ---------------------------------------------------------------------------

/**
 * Sliding-window exponentiation without Montgomery (public for benchmarking).
 */
export function slidingWindowNoMont(
  base: bigint,
  exp: bigint,
  mod: bigint,
): bigint {
  const w = exp.toString(2).length > 64 ? 4 : 2;

  // Pre-compute odd powers
  const g = pymod(base, mod);
  const g2 = pymod(g * g, mod);
  const table = new Map<bigint, bigint>();
  table.set(1n, g);
  for (let i = 3n; i < BigInt(1 << w); i += 2n) {
    table.set(i, pymod(table.get(i - 2n)! * g2, mod));
  }

  let result = 1n;
  let i = exp.toString(2).length - 1; // bit_length - 1

  while (i >= 0) {
    if (!((exp >> BigInt(i)) & 1n)) {
      result = pymod(result * result, mod);
      i--;
    } else {
      let bestJ = i;
      let bestVal = 1n;
      for (let j = i; j >= 0 && i - j + 1 <= w; j--) {
        const val = (exp >> BigInt(j)) & (BigInt(1) << BigInt(i - j + 1)) - 1n;
        if (val & 1n) {
          bestJ = j;
          bestVal = val;
        }
      }
      for (let s = 0; s < i - bestJ + 1; s++) {
        result = pymod(result * result, mod);
      }
      result = pymod(result * table.get(bestVal)!, mod);
      i = bestJ - 1;
    }
  }
  return result;
}

function buildWindowTable(
  base: bigint,
  expBits: number,
  mont: MontgomeryContext,
): [bigint[], number] {
  const windowSize = expBits > 64 ? 4 : 2;
  const tableSize = 1 << windowSize;
  const g = mont.toMont(base);
  const g2 = mont.mul(g, g);

  const table: bigint[] = new Array(tableSize);
  table[1] = g;
  for (let i = 3; i < tableSize; i += 2) {
    table[i] = mont.mul(table[i - 2], g2);
  }
  return [table, windowSize];
}

/**
 * Sliding-window modular exponentiation using Montgomery multiplication.
 */
export function modExpSlidingWindow(
  base: bigint,
  exp: bigint,
  mod: bigint,
): bigint {
  if (exp === 0n) return 1n % mod;
  if (mod === 1n) return 0n;
  // Montgomery requires odd modulus
  if (mod % 2n === 0n) return slidingWindowNoMont(base, exp, mod);

  const mont = new MontgomeryContext(mod);
  const [table, w] = buildWindowTable(base, exp.toString(2).length, mont);

  let result = mont.toMont(1n); // 1 in Montgomery form
  let i = exp.toString(2).length - 1;

  while (i >= 0) {
    if (!((exp >> BigInt(i)) & 1n)) {
      result = mont.mul(result, result);
      i--;
    } else {
      let bestJ = i;
      let bestVal = 1n;
      for (let j = i; j >= 0 && i - j + 1 <= w; j--) {
        const val =
          (exp >> BigInt(j)) & ((1n << BigInt(i - j + 1)) - 1n);
        if (val & 1n) {
          bestJ = j;
          bestVal = val;
        }
      }
      const windowLen = i - bestJ + 1;
      for (let s = 0; s < windowLen; s++) {
        result = mont.mul(result, result);
      }
      result = mont.mul(result, table[Number(bestVal)]);
      i = bestJ - 1;
    }
  }

  return mont.fromMont(result);
}

// ---------------------------------------------------------------------------
// Key generation with CRT parameter pre-computation
// ---------------------------------------------------------------------------

function modInverse(e: bigint, phi: bigint): bigint {
  let [oldR, r] = [e, phi];
  let [oldS, s] = [1n, 0n];
  while (r !== 0n) {
    const q = oldR / r;
    [oldR, r] = [r, oldR - q * r];
    [oldS, s] = [s, oldS - q * s];
  }
  return ((oldS % phi) + phi) % phi;
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
  dp: bigint;
  dq: bigint;
  qinv: bigint;
}

export type KeyPair = { priv: PrivateKey; pub: PublicKey };

/**
 * Generate RSA keypair with pre-computed CRT parameters.
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
  const e = 65537n;
  const d = modInverse(e, phi);

  // CRT parameters
  const dp = d % (p - 1n);
  const dq = d % (q - 1n);
  const qinv = modInverse(q, p);

  return {
    priv: { d, n, p, q, dp, dq, qinv },
    pub: { e, n },
  };
}

// ---------------------------------------------------------------------------
// Encrypt — sliding-window exponentiation
// ---------------------------------------------------------------------------

export function encrypt(pub: PublicKey, plaintext: bigint): bigint {
  return modExpSlidingWindow(plaintext, pub.e, pub.n);
}

// ---------------------------------------------------------------------------
// Decrypt — CRT + sliding-window
// ---------------------------------------------------------------------------

export function decrypt(priv: PrivateKey, ciphertext: bigint): bigint {
  const { p, q } = priv;

  // CRT half-size exponentiations
  const m1 = modExpSlidingWindow(ciphertext, priv.dp, p);
  const m2 = modExpSlidingWindow(ciphertext, priv.dq, q);

  // Garner's recombination
  let h = pymod(priv.qinv * (m1 - m2), p);
  const m = m2 + h * q;

  // Fault-attack check: verify result
  const n = priv.n;
  const eVal = 65537n;
  if (pymod(modPow(m, eVal, n), n) !== pymod(ciphertext, n)) {
    throw new Error("Fault detected in CRT decryption — result discarded");
  }

  return m;
}

// ---------------------------------------------------------------------------
// PKCS#1 v1.5 padding helpers
// ---------------------------------------------------------------------------

export function pkcs1Pad(data: Buffer, nBytes: number): bigint {
  const padLen = nBytes - data.length - 3;
  if (padLen < 8) throw new Error("Data too long for key size");
  const padding = randomBytes(padLen);
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

export function pkcs1Unpad(paddedInt: bigint): Buffer {
  const hex = paddedInt.toString(16);
  const byteLen = Math.ceil(hex.length / 2);
  const data = Buffer.alloc(byteLen);
  const paddedHex = hex.padStart(byteLen * 2, "0");
  for (let i = 0; i < byteLen; i++) {
    data[i] = parseInt(paddedHex.substring(i * 2, i * 2 + 2), 16);
  }
  let idx = 2;
  while (idx < data.length && data[idx] !== 0x00) idx++;
  idx++;
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
// Key cache — reuse keys across operations
// ---------------------------------------------------------------------------

export class KeyCache {
  private keySize: number;
  private _priv: PrivateKey | null = null;
  private _pub: PublicKey | null = null;

  constructor(keySize: number = 2048) {
    this.keySize = keySize;
  }

  get(): { priv: PrivateKey; pub: PublicKey } {
    if (!this._priv || !this._pub) {
      const kp = generateKeypair(this.keySize);
      this._priv = kp.priv;
      this._pub = kp.pub;
    }
    return { priv: this._priv, pub: this._pub };
  }

  regenerate(): { priv: PrivateKey; pub: PublicKey } {
    const kp = generateKeypair(this.keySize);
    this._priv = kp.priv;
    this._pub = kp.pub;
    return kp;
  }
}

// ---------------------------------------------------------------------------
// Batch operations
// ---------------------------------------------------------------------------

export function batchEncrypt(pub: PublicKey, messages: Buffer[]): bigint[] {
  return messages.map((msg) => encryptBytes(pub, msg));
}

export function batchDecrypt(priv: PrivateKey, ciphertexts: bigint[]): Buffer[] {
  return ciphertexts.map((ct) => decryptBytes(priv, ct));
}

// ---------------------------------------------------------------------------
// Hybrid RSA + AES-256-GCM — uses Node crypto for AES (real-world practice).
// RSA is from scratch.
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

  const decipher = createDecipheriv("aes-256-gcm", aesKey, envelope.iv);
  decipher.setAuthTag(envelope.tag);
  return Buffer.concat([
    decipher.update(envelope.ct),
    decipher.final(),
  ]);
}
