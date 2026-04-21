"""
Optimized RSA Implementation

Optimisations over standard RSA:
  1. CRT (Chinese Remainder Theorem) for decryption — ~4x speedup
  2. Sliding-window modular exponentiation (4-bit window)
  3. Montgomery multiplication for modular arithmetic
  4. Key caching — generate once, reuse across operations
  5. Batch encrypt/decrypt with amortised overhead
  6. Pre-computed CRT parameters (dp, dq, qInv) stored in private key
  7. Hybrid RSA+AES-256-CBC using library-accelerated AES
  8. Fault-attack protection — verify decryption result before returning
"""

import random
import math
import os
import time
from typing import Tuple, List

# ---------------------------------------------------------------------------
# Primality testing (same Miller-Rabin, but with deterministic witnesses
# for small sizes for speed)
# ---------------------------------------------------------------------------

_SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53,
                 59, 61, 67, 71, 73, 79, 83, 89, 97]


def is_probable_prime(n: int, k: int = 20) -> bool:
    if n < 2:
        return False
    for p in _SMALL_PRIMES:
        if n % p == 0:
            return n == p
    if n < 2:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits: int) -> int:
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1
        if is_probable_prime(candidate):
            return candidate


# ---------------------------------------------------------------------------
# Montgomery Multiplication
# ---------------------------------------------------------------------------

class MontgomeryContext:
    """Pre-computed Montgomery parameters for a given modulus."""

    def __init__(self, n: int):
        self.n = n
        self.r = 1 << (n.bit_length())  # R = 2^k where k = bit_length(n)
        self.r_inv = pow(self.r, -1, n)
        self.n_prime = (-pow(n, -1, self.r)) % self.r  # n' such that n*n' ≡ -1 (mod R)
        self.r2 = (self.r * self.r) % n

    def to_mont(self, x: int) -> int:
        return (x * self.r) % self.n

    def from_mont(self, x: int) -> int:
        return (x * self.r_inv) % self.n

    def reduce(self, t: int) -> int:
        """Montgomery reduction (REDC)."""
        n, r, n_prime = self.n, self.r, self.n_prime
        m = (t * n_prime) % r
        t = (t + m * n) // r
        if t >= n:
            t -= n
        return t

    def mul(self, a: int, b: int) -> int:
        """Montgomery multiplication: a*b*R^-1 mod n."""
        return self.reduce(a * b)


# ---------------------------------------------------------------------------
# Sliding-window modular exponentiation (4-bit window)
# ---------------------------------------------------------------------------

def _sliding_window_no_mont(base: int, exp: int, mod: int) -> int:
    """Sliding-window exponentiation without Montgomery (fallback for even moduli)."""
    w = 4 if exp.bit_length() > 64 else 2

    # Pre-compute odd powers
    g = base % mod
    g2 = (g * g) % mod
    table = {}
    table[1] = g
    for i in range(3, 1 << w, 2):
        table[i] = (table[i - 2] * g2) % mod

    result = 1
    i = exp.bit_length() - 1
    while i >= 0:
        if not (exp >> i) & 1:
            result = (result * result) % mod
            i -= 1
        else:
            best_j, best_val = i, 1
            j = i
            while j >= 0 and (i - j + 1) <= w:
                val = (exp >> j) & ((1 << (i - j + 1)) - 1)
                if val & 1:
                    best_j = j
                    best_val = val
                j -= 1
            for _ in range(i - best_j + 1):
                result = (result * result) % mod
            result = (result * table[best_val]) % mod
            i = best_j - 1
    return result


def _build_window_table(base: int, exp_bits: int, mont: MontgomeryContext) -> list:
    """Pre-compute g^(2k+1) for window size k, in Montgomery form."""
    window_size = 4 if exp_bits > 64 else 2
    table_size = 1 << window_size
    g = mont.to_mont(base)
    g2 = mont.mul(g, g)  # g^2 in Montgomery

    table = [0] * table_size
    table[1] = g
    for i in range(3, table_size, 2):
        table[i] = mont.mul(table[i - 2], g2)
    return table, window_size


def mod_exp_sliding_window(base: int, exp: int, mod: int) -> int:
    """Sliding-window modular exponentiation using Montgomery multiplication.

    Falls back to built-in pow() for small/even moduli where Montgomery
    isn't applicable (R must be coprime to n).
    """
    if exp == 0:
        return 1 % mod
    if mod == 1:
        return 0
    # Montgomery requires gcd(R, n) == 1, i.e., n must be odd.
    # Fall back to sliding-window without Montgomery for even moduli.
    if mod % 2 == 0:
        return _sliding_window_no_mont(base, exp, mod)

    mont = MontgomeryContext(mod)
    table, w = _build_window_table(base, exp.bit_length(), mont)

    result = mont.to_mont(1)  # 1 in Montgomery
    i = exp.bit_length() - 1

    while i >= 0:
        if not (exp >> i) & 1:
            result = mont.mul(result, result)
            i -= 1
        else:
            # Find the longest window of at most w bits starting at i
            j_start = i
            while j_start >= 0 and (i - j_start + 1) <= w:
                # Check if bit at j_start is 1 (window must end with 1)
                val = (exp >> j_start) & ((1 << (i - j_start + 1)) - 1)
                if val & 1:
                    best_j = j_start
                    best_val = val
                j_start -= 1

            window_len = i - best_j + 1
            # Square for each bit in window
            for _ in range(window_len):
                result = mont.mul(result, result)

            result = mont.mul(result, table[best_val])
            i = best_j - 1

    return mont.from_mont(result)


# ---------------------------------------------------------------------------
# Key generation with CRT parameter pre-computation
# ---------------------------------------------------------------------------

def generate_keypair(key_size: int = 2048) -> Tuple[dict, dict]:
    """Generate RSA keypair with pre-computed CRT parameters.

    Private key includes: d, n, p, q, dp, dq, qinv
    for CRT-accelerated decryption.
    """
    half = key_size // 2
    p = generate_prime(half)
    q = generate_prime(half)
    while q == p:
        q = generate_prime(half)

    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)

    # CRT parameters
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = pow(q, -1, p)

    pub = {"e": e, "n": n}
    priv = {
        "d": d, "n": n,
        "p": p, "q": q,
        "dp": dp, "dq": dq, "qinv": qinv,
    }
    return priv, pub


# ---------------------------------------------------------------------------
# Encrypt — sliding-window exponentiation
# ---------------------------------------------------------------------------

def encrypt(pub: dict, plaintext: int) -> int:
    return mod_exp_sliding_window(plaintext, pub["e"], pub["n"])


# ---------------------------------------------------------------------------
# Decrypt — CRT + sliding-window
# ---------------------------------------------------------------------------

def decrypt(priv: dict, ciphertext: int) -> int:
    """CRT-based RSA decryption with fault-attack verification.

    Steps:
      m1 = c^dp mod p   (half-size exponentiation)
      m2 = c^dq mod q   (half-size exponentiation)
      h  = qinv * (m1 - m2) mod p
      m  = m2 + h * q

    Then verify: encrypt(result) == ciphertext  (fault-attack protection)
    """
    p, q = priv["p"], priv["q"]

    # CRT half-size exponentiations
    m1 = mod_exp_sliding_window(ciphertext, priv["dp"], p)
    m2 = mod_exp_sliding_window(ciphertext, priv["dq"], q)

    # Garner's recombination
    h = (priv["qinv"] * (m1 - m2)) % p
    m = m2 + h * q

    # Fault-attack check: verify result
    n = priv["n"]
    e_val = 65537  # standard public exponent
    if pow(m, e_val, n) != ciphertext % n:
        raise RuntimeError("Fault detected in CRT decryption — result discarded")

    return m


# ---------------------------------------------------------------------------
# PKCS#1 v1.5 padding helpers
# ---------------------------------------------------------------------------

def pkcs1_pad(data: bytes, n_bytes: int) -> int:
    pad_len = n_bytes - len(data) - 3
    if pad_len < 8:
        raise ValueError("Data too long for key size")
    padding = bytes(random.randint(1, 255) for _ in range(pad_len))
    padded = b"\x00\x02" + padding + b"\x00" + data
    return int.from_bytes(padded, "big")


def pkcs1_unpad(padded_int: int) -> bytes:
    data = padded_int.to_bytes((padded_int.bit_length() + 7) // 8, "big")
    idx = data.index(b"\x00", 2)
    return data[idx + 1:]


def encrypt_bytes(pub: dict, data: bytes) -> int:
    n_bytes = (pub["n"].bit_length() + 7) // 8
    m = pkcs1_pad(data, n_bytes)
    return encrypt(pub, m)


def decrypt_bytes(priv: dict, ciphertext: int) -> bytes:
    m = decrypt(priv, ciphertext)
    return pkcs1_unpad(m)


# ---------------------------------------------------------------------------
# Key cache — reuse keys across operations
# ---------------------------------------------------------------------------

class KeyCache:
    """Cache pre-generated keypairs to avoid repeated key generation."""

    def __init__(self, key_size: int = 2048):
        self.key_size = key_size
        self._priv = None
        self._pub = None

    def get(self) -> Tuple[dict, dict]:
        if self._priv is None:
            self._priv, self._pub = generate_keypair(self.key_size)
        return self._priv, self._pub

    def regenerate(self):
        self._priv, self._pub = generate_keypair(self.key_size)
        return self._priv, self._pub


# ---------------------------------------------------------------------------
# Batch operations
# ---------------------------------------------------------------------------

def batch_encrypt(pub: dict, messages: List[bytes]) -> List[int]:
    """Encrypt multiple messages efficiently with key reuse."""
    return [encrypt_bytes(pub, msg) for msg in messages]


def batch_decrypt(priv: dict, ciphertexts: List[int]) -> List[bytes]:
    """Decrypt multiple ciphertexts efficiently with CRT + key reuse."""
    return [decrypt_bytes(priv, ct) for ct in ciphertexts]


# ---------------------------------------------------------------------------
# Hybrid RSA + AES-256-GCM — uses library AES for fair hybrid comparison
# RSA is from scratch; AES uses the cryptography library (real-world practice).
# ---------------------------------------------------------------------------

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def hybrid_encrypt(pub: dict, data: bytes) -> dict:
    """Hybrid: generate AES-256 key, encrypt data with AES-GCM, wrap AES key with RSA."""
    aes_key = os.urandom(32)
    iv = os.urandom(12)
    encryptor = Cipher(algorithms.AES(aes_key), modes.GCM(iv)).encryptor()
    ct = encryptor.update(data) + encryptor.finalize()
    wrapped_key = encrypt_bytes(pub, aes_key)
    return {"wrapped_key": wrapped_key, "iv": iv, "ct": ct, "tag": encryptor.tag}


def hybrid_decrypt(priv: dict, envelope: dict) -> bytes:
    """Hybrid: unwrap AES key via RSA, decrypt data with AES-GCM."""
    aes_key = decrypt_bytes(priv, envelope["wrapped_key"])
    decryptor = Cipher(algorithms.AES(aes_key), modes.GCM(envelope["iv"], envelope["tag"])).decryptor()
    return decryptor.update(envelope["ct"]) + decryptor.finalize()
