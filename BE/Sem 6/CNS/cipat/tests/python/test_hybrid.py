"""
Test 4 — Hybrid RSA+AES vs Pure RSA
Benchmarks bulk-data encryption time for hybrid (RSA wrapping AES key + AES-CBC)
vs pure RSA (chunked encryption of entire payload).
"""

import sys
import os
import time
import statistics
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from standard_rsa.rsa import (
    generate_keypair as std_gen,
    encrypt_bytes as std_enc_bytes,
    hybrid_encrypt as std_hybrid_enc,
    hybrid_decrypt as std_hybrid_dec,
)

from optimized_rsa.rsa import (
    generate_keypair as opt_gen,
    encrypt_bytes as opt_enc_bytes,
    hybrid_encrypt as opt_hybrid_enc,
    hybrid_decrypt as opt_hybrid_dec,
)

SEP = "=" * 70
SUBSEP = "-" * 70


def _bench(fn, repeats: int = 10) -> tuple:
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)
    return statistics.mean(times), statistics.median(times), min(times), max(times)


def _print_comparison(label, std_mean, opt_mean, unit="ms"):
    if std_mean > 0:
        speedup = std_mean / opt_mean
    else:
        speedup = float("inf")
    print(f"  {label:40s}  Std: {std_mean:10.3f} {unit}  Opt: {opt_mean:10.3f} {unit}  Speedup: {speedup:.1f}x")
    return speedup


def test_hybrid_vs_pure_standard():
    print(f"\n{SUBSEP}")
    print("STANDARD RSA: Hybrid (RSA+AES-CBC) vs Pure RSA (chunked)")
    print(SUBSEP)

    priv, pub = std_gen(1024)
    chunk_size = (1024 // 8) - 11  # max bytes per RSA block

    for data_kb in (1, 10, 50):
        data = os.urandom(data_kb * 1024)

        # Hybrid
        hy_mean, hy_med, hy_min, hy_max = _bench(lambda: std_hybrid_enc(pub, data), 5)
        # Verify
        env = std_hybrid_enc(pub, data)
        assert std_hybrid_dec(priv, env) == data, "Hybrid decrypt failed"

        # Pure RSA chunked
        def pure_rsa():
            for i in range(0, len(data), chunk_size):
                std_enc_bytes(pub, data[i:i+chunk_size])

        pure_mean, pure_med, pure_min, pure_max = _bench(pure_rsa, min(5, max(1, data_kb)))

        _print_comparison(f"Standard — {data_kb}KB", pure_mean, hy_mean)


def test_hybrid_vs_pure_optimized():
    print(f"\n{SUBSEP}")
    print("OPTIMIZED RSA: Hybrid (RSA+AES-CBC) vs Pure RSA (chunked)")
    print(SUBSEP)

    priv, pub = opt_gen(1024)
    chunk_size = (1024 // 8) - 11

    for data_kb in (1, 10, 50):
        data = os.urandom(data_kb * 1024)

        # Hybrid
        hy_mean, hy_med, hy_min, hy_max = _bench(lambda: opt_hybrid_enc(pub, data), 5)
        env = opt_hybrid_enc(pub, data)
        assert opt_hybrid_dec(priv, env) == data, "Hybrid decrypt failed"

        # Pure RSA chunked
        def pure_rsa():
            for i in range(0, len(data), chunk_size):
                opt_enc_bytes(pub, data[i:i+chunk_size])

        pure_mean, pure_med, pure_min, pure_max = _bench(pure_rsa, min(5, max(1, data_kb)))

        _print_comparison(f"Optimized — {data_kb}KB", pure_mean, hy_mean)


def test_hybrid_std_vs_opt():
    print(f"\n{SUBSEP}")
    print("HYBRID COMPARISON: Standard RSA+AES vs Optimized RSA+AES")
    print(SUBSEP)

    std_priv, std_pub = std_gen(1024)
    opt_priv, opt_pub = opt_gen(1024)

    for data_kb in (1, 10, 50):
        data = os.urandom(data_kb * 1024)

        std_stats = _bench(lambda: std_hybrid_enc(std_pub, data), 5)
        opt_stats = _bench(lambda: opt_hybrid_enc(opt_pub, data), 5)

        _print_comparison(f"Hybrid encrypt {data_kb}KB", std_stats[0], opt_stats[0])


def test_hybrid_correctness_large():
    print(f"\n{SUBSEP}")
    print("HYBRID Correctness — large payloads")
    print(SUBSEP)

    for label, gen, hy_enc, hy_dec in [
        ("Standard", std_gen, std_hybrid_enc, std_hybrid_dec),
        ("Optimized", opt_gen, opt_hybrid_enc, opt_hybrid_dec),
    ]:
        priv, pub = gen(1024)
        for size in [256, 1024, 5120]:  # 0.25KB, 1KB, 5KB
            data = os.urandom(size)
            env = hy_enc(pub, data)
            recovered = hy_dec(priv, env)
            status = "PASS" if recovered == data else "FAIL"
            print(f"  [{status}] {label} hybrid {size}B roundtrip")
            assert recovered == data, f"{label} hybrid failed for {size}B"


def main():
    print(SEP)
    print("TEST 4 — HYBRID RSA+AES vs PURE RSA")
    print(SEP)

    test_hybrid_vs_pure_standard()
    test_hybrid_vs_pure_optimized()
    test_hybrid_std_vs_opt()
    test_hybrid_correctness_large()

    print(f"\n{SEP}")
    print("HYBRID BENCHMARK COMPLETE")
    print(SEP)


if __name__ == "__main__":
    main()
