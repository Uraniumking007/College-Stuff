"""
Test 3 — Memory Usage
Measures peak memory allocation for both implementations.
"""

import sys
import os
import tracemalloc
import statistics
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from standard_rsa.rsa import (
    generate_keypair as std_gen,
    encrypt_bytes as std_encrypt_bytes,
    decrypt_bytes as std_decrypt_bytes,
    mod_exp as std_mod_exp,
)

from optimized_rsa.rsa import (
    generate_keypair as opt_gen,
    encrypt_bytes as opt_encrypt_bytes,
    decrypt_bytes as opt_decrypt_bytes,
    mod_exp_sliding_window as opt_mod_exp,
    KeyCache,
)

SEP = "=" * 70
SUBSEP = "-" * 70


def _measure_memory(fn, repeats: int = 20) -> tuple:
    """Return (mean_kb, peak_kb, stdev_kb)."""
    peaks = []
    for _ in range(repeats):
        tracemalloc.start()
        fn()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peaks.append(peak / 1024)
    return statistics.mean(peaks), max(peaks), statistics.stdev(peaks) if len(peaks) > 1 else 0


def _print_mem(label, std_stats, opt_stats):
    std_mean, std_peak, std_sd = std_stats
    opt_mean, opt_peak, opt_sd = opt_stats

    if std_mean > 0:
        reduction = (1 - opt_mean / std_mean) * 100
    else:
        reduction = 0

    print(f"\n  {label}")
    print(f"  {'':30s} {'Standard':>12s}  {'Optimized':>12s}  {'Reduction':>10s}")
    print(f"  {'':30s} {'─'*12}  {'─'*12}  {'─'*10}")
    print(f"  {'Mean alloc (KB)':30s} {std_mean:12.2f}  {opt_mean:12.2f}  {reduction:9.1f}%")
    print(f"  {'Peak alloc (KB)':30s} {std_peak:12.2f}  {opt_peak:12.2f}")
    print(f"  {'Std Dev (KB)':30s} {std_sd:12.2f}  {opt_sd:12.2f}")


def test_keygen_memory():
    print(f"\n{SUBSEP}")
    print("Key Generation Memory")
    print(SUBSEP)

    for bits in (1024, 2048):
        std_mem = _measure_memory(lambda: std_gen(bits), 10)
        opt_mem = _measure_memory(lambda: opt_gen(bits), 10)
        _print_mem(f"Key gen ({bits}-bit)", std_mem, opt_mem)


def test_encrypt_memory():
    print(f"\n{SUBSEP}")
    print("Encryption Memory")
    print(SUBSEP)

    for bits in (1024,):
        std_priv, std_pub = std_gen(bits)
        opt_priv, opt_pub = opt_gen(bits)
        msg = os.urandom((bits // 8) - 11)

        std_mem = _measure_memory(lambda: std_encrypt_bytes(std_pub, msg))
        opt_mem = _measure_memory(lambda: opt_encrypt_bytes(opt_pub, msg))
        _print_mem(f"Encrypt ({bits}-bit)", std_mem, opt_mem)


def test_decrypt_memory():
    print(f"\n{SUBSEP}")
    print("Decryption Memory")
    print(SUBSEP)

    for bits in (1024,):
        std_priv, std_pub = std_gen(bits)
        opt_priv, opt_pub = opt_gen(bits)
        msg = os.urandom((bits // 8) - 11)

        std_ct = std_encrypt_bytes(std_pub, msg)
        opt_ct = opt_encrypt_bytes(opt_pub, msg)

        std_mem = _measure_memory(lambda: std_decrypt_bytes(std_priv, std_ct))
        opt_mem = _measure_memory(lambda: opt_decrypt_bytes(opt_priv, opt_ct))
        _print_mem(f"Decrypt ({bits}-bit)", std_mem, opt_mem)


def test_mod_exp_memory():
    print(f"\n{SUBSEP}")
    print("Modular Exponentiation Memory (2048-bit)")
    print(SUBSEP)

    base = random.getrandbits(2048)
    exp = random.getrandbits(2048)
    mod = random.getrandbits(2048) | (1 << 2047) | 1

    std_mem = _measure_memory(lambda: std_mod_exp(base, exp, mod))
    opt_mem = _measure_memory(lambda: opt_mod_exp(base, exp, mod))
    _print_mem("mod_exp (2048-bit)", std_mem, opt_mem)


def test_batch_memory():
    print(f"\n{SUBSEP}")
    print("Batch Operations Memory (10 messages)")
    print(SUBSEP)

    batch_size = 10
    std_priv, std_pub = std_gen(1024)
    opt_priv, opt_pub = opt_gen(1024)
    msgs = [os.urandom(100) for _ in range(batch_size)]

    def std_batch():
        cts = [std_encrypt_bytes(std_pub, m) for m in msgs]
        for ct in cts:
            std_decrypt_bytes(std_priv, ct)

    def opt_batch():
        cts = [opt_encrypt_bytes(opt_pub, m) for m in msgs]
        for ct in cts:
            opt_decrypt_bytes(opt_priv, ct)

    std_mem = _measure_memory(std_batch, 5)
    opt_mem = _measure_memory(opt_batch, 5)
    _print_mem("Batch encrypt+decrypt x10", std_mem, opt_mem)


def main():
    print(SEP)
    print("TEST 3 — MEMORY USAGE")
    print(SEP)

    test_keygen_memory()
    test_encrypt_memory()
    test_decrypt_memory()
    test_mod_exp_memory()
    test_batch_memory()

    print(f"\n{SEP}")
    print("MEMORY BENCHMARK COMPLETE")
    print(SEP)


if __name__ == "__main__":
    main()
