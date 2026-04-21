"""
Test 5 — Key Size Scaling
Benchmarks how both implementations scale across 512, 1024, 2048, 3072, 4096-bit keys.
Shows encryption time, decryption time, and key generation time.
"""

import sys
import os
import time
import statistics
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from standard_rsa.rsa import (
    generate_keypair as std_gen,
    encrypt as std_encrypt,
    decrypt as std_decrypt,
    mod_exp as std_mod_exp,
)

from optimized_rsa.rsa import (
    generate_keypair as opt_gen,
    encrypt as opt_encrypt,
    decrypt as opt_decrypt,
    mod_exp_sliding_window as opt_mod_exp,
)

SEP = "=" * 70
SUBSEP = "-" * 70
KEY_SIZES = [512, 1024, 2048]  # 3072/4096 removed — keygen is very slow for from-scratch
SAMPLES = 20


def _bench(fn, repeats: int = SAMPLES) -> float:
    """Return mean time in ms."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)
    return statistics.mean(times)


def test_keygen_scaling():
    print(f"\n{SUBSEP}")
    print("Key Generation Time vs Key Size")
    print(SUBSEP)

    print(f"  {'Bits':>6s}  {'Standard (ms)':>14s}  {'Optimized (ms)':>15s}  {'Ratio':>7s}")
    print(f"  {'─'*6}  {'─'*14}  {'─'*15}  {'─'*7}")

    for bits in KEY_SIZES:
        std_t = _bench(lambda: std_gen(bits), 5)
        opt_t = _bench(lambda: opt_gen(bits), 5)
        ratio = std_t / opt_t if opt_t > 0 else float("inf")
        print(f"  {bits:>6d}  {std_t:>14.3f}  {opt_t:>15.3f}  {ratio:>6.2f}x")


def test_encrypt_scaling():
    print(f"\n{SUBSEP}")
    print("Encryption Time vs Key Size")
    print(SUBSEP)

    print(f"  {'Bits':>6s}  {'Standard (ms)':>14s}  {'Optimized (ms)':>15s}  {'Speedup':>8s}")
    print(f"  {'─'*6}  {'─'*14}  {'─'*15}  {'─'*8}")

    for bits in KEY_SIZES:
        std_priv, std_pub = std_gen(bits)
        opt_priv, opt_pub = opt_gen(bits)
        msg = random.getrandbits(bits // 2)

        std_t = _bench(lambda: std_encrypt(std_pub, msg))
        opt_t = _bench(lambda: opt_encrypt(opt_pub, msg))
        speedup = std_t / opt_t if opt_t > 0 else float("inf")
        print(f"  {bits:>6d}  {std_t:>14.4f}  {opt_t:>15.4f}  {speedup:>7.2f}x")


def test_decrypt_scaling():
    print(f"\n{SUBSEP}")
    print("Decryption Time vs Key Size (CRT advantage)")
    print(SUBSEP)

    print(f"  {'Bits':>6s}  {'Standard (ms)':>14s}  {'Optimized (ms)':>15s}  {'Speedup':>8s}")
    print(f"  {'─'*6}  {'─'*14}  {'─'*15}  {'─'*8}")

    for bits in KEY_SIZES:
        std_priv, std_pub = std_gen(bits)
        opt_priv, opt_pub = opt_gen(bits)
        msg = random.getrandbits(bits // 2)

        std_ct = std_encrypt(std_pub, msg)
        opt_ct = opt_encrypt(opt_pub, msg)

        std_t = _bench(lambda: std_decrypt(std_priv, std_ct))
        opt_t = _bench(lambda: opt_decrypt(opt_priv, opt_ct))
        speedup = std_t / opt_t if opt_t > 0 else float("inf")
        print(f"  {bits:>6d}  {std_t:>14.4f}  {opt_t:>15.4f}  {speedup:>7.2f}x")


def test_modexp_scaling():
    print(f"\n{SUBSEP}")
    print("Modular Exponentiation Time vs Operand Size")
    print(SUBSEP)

    print(f"  {'Bits':>6s}  {'Standard (ms)':>14s}  {'Optimized (ms)':>15s}  {'Speedup':>8s}")
    print(f"  {'─'*6}  {'─'*14}  {'─'*15}  {'─'*8}")

    for bits in [512, 1024, 2048]:
        base = random.getrandbits(bits)
        exp = random.getrandbits(bits)
        mod = random.getrandbits(bits) | (1 << (bits - 1)) | 1

        std_t = _bench(lambda: std_mod_exp(base, exp, mod))
        opt_t = _bench(lambda: opt_mod_exp(base, exp, mod))
        speedup = std_t / opt_t if opt_t > 0 else float("inf")
        print(f"  {bits:>6d}  {std_t:>14.4f}  {opt_t:>15.4f}  {speedup:>7.2f}x")


def test_rsa_operation_growth():
    print(f"\n{SUBSEP}")
    print("Growth Factor: how much slower is 2x key size?")
    print(SUBSEP)

    results = {}
    for bits in KEY_SIZES:
        priv, pub = opt_gen(bits)
        msg = random.getrandbits(bits // 2)
        ct = opt_encrypt(pub, msg)

        enc_t = _bench(lambda: opt_encrypt(pub, msg), SAMPLES)
        dec_t = _bench(lambda: opt_decrypt(priv, ct), SAMPLES)
        results[bits] = {"encrypt": enc_t, "decrypt": dec_t}

    sizes = sorted(results.keys())
    print(f"  {'From → To':>15s}  {'Encrypt Growth':>16s}  {'Decrypt Growth':>16s}")
    print(f"  {'─'*15}  {'─'*16}  {'─'*16}")
    for i in range(1, len(sizes)):
        prev, curr = sizes[i - 1], sizes[i]
        enc_growth = results[curr]["encrypt"] / results[prev]["encrypt"]
        dec_growth = results[curr]["decrypt"] / results[prev]["decrypt"]
        print(f"  {prev}→{curr}         {enc_growth:>15.2f}x  {dec_growth:>15.2f}x")


def main():
    print(SEP)
    print("TEST 5 — KEY SIZE SCALING")
    print(SEP)

    test_keygen_scaling()
    test_encrypt_scaling()
    test_decrypt_scaling()
    test_modexp_scaling()
    test_rsa_operation_growth()

    print(f"\n{SEP}")
    print("KEY SIZE SCALING COMPLETE")
    print(SEP)


if __name__ == "__main__":
    main()
