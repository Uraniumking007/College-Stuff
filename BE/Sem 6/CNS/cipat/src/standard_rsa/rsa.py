"""
Standard RSA Implementation — No Optimizations

Implements RSA from scratch using Python's built-in integers:
  - Key generation (random prime selection via Miller-Rabin)
  - Textbook RSA encrypt / decrypt (m^e mod n, c^d mod n)
  - Naive square-and-multiply modular exponentiation
  - PKCS#1 v1.5–style padding (simplified)
  - Hybrid mode: RSA for key-wrap + AES-256-CBC for bulk data

No CRT, no pre-computation, no key caching, no batch shortcuts.
"""

import random
import math
import os
import time
from typing import Tuple

# ---------------------------------------------------------------------------
# Primality testing
# ---------------------------------------------------------------------------

def is_probable_prime(n: int, k: int = 20) -> bool:
    """Miller-Rabin primality test with *k* rounds."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # write n-1 as 2^r * d
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
    """Generate a random prime of the specified bit length."""
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1  # ensure high bit and odd
        if is_probable_prime(candidate):
            return candidate


# ---------------------------------------------------------------------------
# Modular exponentiation — naive square-and-multiply
# ---------------------------------------------------------------------------

def mod_exp(base: int, exp: int, mod: int) -> int:
    """Square-and-multiply (left-to-right binary method).

    This is the *unoptimised* version: processes one bit at a time,
    no windowing, no Montgomery reduction.
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        exp >>= 1
        base = (base * base) % mod
    return result


# ---------------------------------------------------------------------------
# Key generation
# ---------------------------------------------------------------------------

def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return a


def generate_keypair(key_size: int = 2048) -> Tuple[dict, dict]:
    """Return (private_key, public_key) dicts.

    Each call generates fresh primes — no caching.
    """
    half = key_size // 2
    p = generate_prime(half)
    q = generate_prime(half)
    while q == p:
        q = generate_prime(half)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537
    while gcd(e, phi) != 1:
        e += 2

    d = pow(e, -1, phi)  # modular inverse

    pub = {"e": e, "n": n}
    priv = {"d": d, "n": n, "p": p, "q": q}
    return priv, pub


# ---------------------------------------------------------------------------
# Encrypt / Decrypt
# ---------------------------------------------------------------------------

def encrypt(pub: dict, plaintext: int) -> int:
    """Textbook RSA encryption: c = m^e mod n."""
    return mod_exp(plaintext, pub["e"], pub["n"])


def decrypt(priv: dict, ciphertext: int) -> int:
    """Textbook RSA decryption: m = c^d mod n (full-size exponent, no CRT)."""
    return mod_exp(ciphertext, priv["d"], priv["n"])


# ---------------------------------------------------------------------------
# Byte-level helpers (padding)
# ---------------------------------------------------------------------------

def pkcs1_pad(data: bytes, n_bytes: int) -> int:
    """Simplified PKCS#1 v1.5–style padding → integer."""
    pad_len = n_bytes - len(data) - 3
    if pad_len < 8:
        raise ValueError("Data too long for key size")
    padding = bytes(random.randint(1, 255) for _ in range(pad_len))
    padded = b"\x00\x02" + padding + b"\x00" + data
    return int.from_bytes(padded, "big")


def pkcs1_unpad(padded_int: int) -> bytes:
    """Strip PKCS#1 v1.5 padding."""
    data = padded_int.to_bytes((padded_int.bit_length() + 7) // 8, "big")
    # skip 0x00 0x02 padding... 0x00
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
# Hybrid RSA + AES-256-GCM (for bulk data tests)
# Uses the cryptography library for AES — RSA itself is from scratch.
# This matches real-world practice where hybrid = custom RSA + library AES.
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
