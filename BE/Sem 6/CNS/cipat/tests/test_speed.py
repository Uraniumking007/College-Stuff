"""
Test 2 — Speed Benchmark
Compares encryption/decryption time between Standard and Optimized RSA.
Also tests key-generation time and modular exponentiation speed.
"""

import sys
import os
import time
import statistics
import random
import tracemalloc

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from standard_rsa.rsa import (
    generate_keypair as std_gen,
    encrypt as std_encrypt,
    decrypt as std_decrypt,
    encrypt_bytes as std_encrypt_bytes,
    decrypt_bytes as std_decrypt_bytes,
    mod_exp as std_mod_exp,
)

from optimized_rsa.rsa import (
    generate_keypair as opt_gen,
    encrypt as opt_encrypt,
    decrypt as opt_decrypt,
    encrypt_bytes as opt_encrypt_bytes,
    decrypt_bytes as opt_decrypt_bytes,
    mod_exp_sliding_window as opt_mod_exp,
    KeyCache,
)

SEP = "=" * 70
SUBSEP = "-" * 70
SAMPLES = 50


def _bench(fn, repeats: int = SAMPLES) -> tuple:
    """Return (mean_ms, median_ms, stdev_ms, min_ms, max_ms)."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)
    return (
        statistics.mean(times),
        statistics.median(times),
        statistics.stdev(times) if len(times) > 1 else 0,
        min(times),
        max(times),
    )


def _print_comparison(label, std_stats, opt_stats):
    std_mean, std_med, std_sd, std_min, std_max = std_stats
    opt_mean, opt_med, opt_sd, opt_min, opt_max = opt_stats

    if std_mean > 0:
        speedup = std_mean / opt_mean
    else:
        speedup = float("inf")

    print(f"\n  {label}")
    print(f"  {'':30s} {'Standard':>10s}  {'Optimized':>10s}  {'Speedup':>8s}")
    print(f"  {'':30s} {'─'*10}  {'─'*10}  {'─'*8}")
    print(f"  {'Mean (ms)':30s} {std_mean:10.4f}  {opt_mean:10.4f}  {speedup:7.2f}x")
    print(f"  {'Median (ms)':30s} {std_med:10.4f}  {opt_med:10.4f}")
    print(f"  {'Std Dev (ms)':30s} {std_sd:10.4f}  {opt_sd:10.4f}")
    print(f"  {'Min (ms)':30s} {std_min:10.4f}  {opt_min:10.4f}")
    print(f"  {'Max (ms)':30s} {std_max:10.4f}  {opt_max:10.4f}")
    return speedup


def test_mod_exp_speed():
    print(f"\n{SUBSEP}")
    print("Modular Exponentiation Speed (1024-bit operands)")
    print(SUBSEP)

    base = random.getrandbits(1024)
    exp = random.getrandbits(1024)
    mod = random.getrandbits(1024) | (1 << 1023) | 1

    std_stats = _bench(lambda: std_mod_exp(base, exp, mod), SAMPLES)
    opt_stats = _bench(lambda: opt_mod_exp(base, exp, mod), SAMPLES)
    _print_comparison("mod_exp (1024-bit)", std_stats, opt_stats)

    print("\n  Larger: 2048-bit operands")
    base2 = random.getrandbits(2048)
    exp2 = random.getrandbits(2048)
    mod2 = random.getrandbits(2048) | (1 << 2047) | 1

    std_stats2 = _bench(lambda: std_mod_exp(base2, exp2, mod2), SAMPLES)
    opt_stats2 = _bench(lambda: opt_mod_exp(base2, exp2, mod2), SAMPLES)
    _print_comparison("mod_exp (2048-bit)", std_stats2, opt_stats2)


def test_keygen_speed():
    print(f"\n{SUBSEP}")
    print("Key Generation Speed")
    print(SUBSEP)

    for bits in (1024, 2048):
        std_stats = _bench(lambda: std_gen(bits), 10)
        opt_stats = _bench(lambda: opt_gen(bits), 10)
        _print_comparison(f"Key gen ({bits}-bit)", std_stats, opt_stats)


def test_encrypt_decrypt_speed():
    print(f"\n{SUBSEP}")
    print("Encrypt / Decrypt Speed (integer messages)")
    print(SUBSEP)

    for bits in (1024, 2048):
        std_priv, std_pub = std_gen(bits)
        opt_priv, opt_pub = opt_gen(bits)

        msg = random.getrandbits(bits // 2)

        # Encrypt
        std_enc = _bench(lambda: std_encrypt(std_pub, msg), SAMPLES)
        opt_enc = _bench(lambda: opt_encrypt(opt_pub, msg), SAMPLES)
        speedup = _print_comparison(f"Encrypt ({bits}-bit)", std_enc, opt_enc)

        # Decrypt
        std_ct = std_encrypt(std_pub, msg)
        opt_ct = opt_encrypt(opt_pub, msg)

        std_dec = _bench(lambda: std_decrypt(std_priv, std_ct), SAMPLES)
        opt_dec = _bench(lambda: opt_decrypt(opt_priv, opt_ct), SAMPLES)
        _print_comparison(f"Decrypt ({bits}-bit) — CRT vs no-CRT", std_dec, opt_dec)


def test_bytes_encrypt_decrypt_speed():
    print(f"\n{SUBSEP}")
    print("Byte-level Encrypt / Decrypt Speed (with padding)")
    print(SUBSEP)

    for bits in (1024,):
        std_priv, std_pub = std_gen(bits)
        opt_priv, opt_pub = opt_gen(bits)

        max_msg = (bits // 8) - 11
        msg = os.urandom(max_msg)

        std_enc = _bench(lambda: std_encrypt_bytes(std_pub, msg), SAMPLES)
        opt_enc = _bench(lambda: opt_encrypt_bytes(opt_pub, msg), SAMPLES)
        _print_comparison(f"Bytes encrypt ({bits}-bit)", std_enc, opt_enc)

        std_ct = std_encrypt_bytes(std_pub, msg)
        opt_ct = opt_encrypt_bytes(opt_pub, msg)

        std_dec = _bench(lambda: std_decrypt_bytes(std_priv, std_ct), SAMPLES)
        opt_dec = _bench(lambda: opt_decrypt_bytes(opt_priv, opt_ct), SAMPLES)
        _print_comparison(f"Bytes decrypt ({bits}-bit)", std_dec, opt_dec)


def test_cold_start_vs_cached():
    print(f"\n{SUBSEP}")
    print("Cold Start (new key each time) vs Cached Key")
    print(SUBSEP)

    msg = os.urandom(100)

    def cold_std():
        priv, pub = std_gen(1024)
        std_encrypt_bytes(pub, msg)

    cold_stats = _bench(cold_std, 10)

    cache = KeyCache(1024)
    def cached():
        priv, pub = cache.get()
        opt_encrypt_bytes(pub, msg)

    cached_stats = _bench(cached, SAMPLES)
    _print_comparison("Cold (std, keygen+enc) vs Cached (opt, enc only)", cold_stats, cached_stats)


def main():
    print(SEP)
    print("TEST 2 — SPEED BENCHMARK")
    print(f"Samples per test: {SAMPLES}")
    print(SEP)

    test_mod_exp_speed()
    test_keygen_speed()
    test_encrypt_decrypt_speed()
    test_bytes_encrypt_decrypt_speed()
    test_cold_start_vs_cached()

    print(f"\n{SEP}")
    print("SPEED BENCHMARK COMPLETE")
    print(SEP)


if __name__ == "__main__":
    main()
