"""
Test 6 — Concurrency & Throughput
Simulates multiple concurrent sessions encrypting/decrypting with both
implementations. Measures throughput, latency, and thread scaling.
"""

import sys
import os
import time
import statistics
import threading
import random
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from standard_rsa.rsa import (
    generate_keypair as std_gen,
    encrypt_bytes as std_encrypt_bytes,
    decrypt_bytes as std_decrypt_bytes,
)

from optimized_rsa.rsa import (
    generate_keypair as opt_gen,
    encrypt_bytes as opt_encrypt_bytes,
    decrypt_bytes as opt_decrypt_bytes,
    KeyCache,
)

SEP = "=" * 70
SUBSEP = "-" * 70


def _run_sessions(gen_fn, enc_fn, dec_fn, concurrency: int, total: int) -> dict:
    """Run total sessions across concurrency threads. Return stats."""
    priv, pub = gen_fn(1024)
    msg = os.urandom(100)
    latencies = []
    lock = threading.Lock()
    errors = []

    def session(_):
        t0 = time.perf_counter()
        try:
            ct = enc_fn(pub, msg)
            pt = dec_fn(priv, ct)
            if pt != msg:
                with lock:
                    errors.append("mismatch")
        except Exception as e:
            with lock:
                errors.append(str(e))
        elapsed = (time.perf_counter() - t0) * 1000
        with lock:
            latencies.append(elapsed)

    t_start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        list(pool.map(session, range(total)))
    total_time = time.perf_counter() - t_start

    return {
        "concurrency": concurrency,
        "total": total,
        "time_s": total_time,
        "throughput": total / total_time,
        "avg_latency_ms": statistics.mean(latencies),
        "p50_ms": statistics.median(latencies),
        "p99_ms": sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0,
        "errors": len(errors),
    }


def test_concurrency_scaling():
    print(f"\n{SUBSEP}")
    print("Throughput vs Concurrency (50 sessions)")
    print(SUBSEP)

    session_counts = 50

    print(f"\n  {'Implementation':>15s}  {'Threads':>8s}  {'Time (s)':>10s}  {'TP (sess/s)':>12s}  {'Avg Lat (ms)':>13s}  {'P99 (ms)':>10s}  {'Errors':>7s}")
    print(f"  {'─'*15}  {'─'*8}  {'─'*10}  {'─'*12}  {'─'*13}  {'─'*10}  {'─'*7}")

    for conc in (1, 2, 5, 10):
        # Standard
        std_r = _run_sessions(std_gen, std_encrypt_bytes, std_decrypt_bytes, conc, session_counts)
        print(f"  {'Standard':>15s}  {conc:>8d}  {std_r['time_s']:>10.3f}  {std_r['throughput']:>12.1f}  {std_r['avg_latency_ms']:>13.3f}  {std_r['p99_ms']:>10.3f}  {std_r['errors']:>7d}")

        # Optimized
        opt_r = _run_sessions(opt_gen, opt_encrypt_bytes, opt_decrypt_bytes, conc, session_counts)
        print(f"  {'Optimized':>15s}  {conc:>8d}  {opt_r['time_s']:>10.3f}  {opt_r['throughput']:>12.1f}  {opt_r['avg_latency_ms']:>13.3f}  {opt_r['p99_ms']:>10.3f}  {opt_r['errors']:>7d}")

        # Speedup
        if opt_r["avg_latency_ms"] > 0:
            lat_speedup = std_r["avg_latency_ms"] / opt_r["avg_latency_ms"]
        else:
            lat_speedup = float("inf")
        tp_speedup = opt_r["throughput"] / std_r["throughput"] if std_r["throughput"] > 0 else float("inf")
        print(f"  {'':>15s}  {'':>8s}  {'':>10s}  {'TP speedup:':>12s}  {f'{lat_speedup:.2f}x latency':>13s}  {f'{tp_speedup:.2f}x TP':>10s}")
        print()


def test_high_volume():
    print(f"\n{SUBSEP}")
    print("High Volume: 200 sessions, 10 threads")
    print(SUBSEP)

    std_r = _run_sessions(std_gen, std_encrypt_bytes, std_decrypt_bytes, 10, 200)
    opt_r = _run_sessions(opt_gen, opt_encrypt_bytes, opt_decrypt_bytes, 10, 200)

    print(f"  {'':20s} {'Standard':>12s}  {'Optimized':>12s}")
    print(f"  {'─'*20} {'─'*12}  {'─'*12}")
    print(f"  {'Total time (s)':20s} {std_r['time_s']:>12.3f}  {opt_r['time_s']:>12.3f}")
    print(f"  {'Throughput (sess/s)':20s} {std_r['throughput']:>12.1f}  {opt_r['throughput']:>12.1f}")
    print(f"  {'Avg latency (ms)':20s} {std_r['avg_latency_ms']:>12.3f}  {opt_r['avg_latency_ms']:>12.3f}")
    print(f"  {'P99 latency (ms)':20s} {std_r['p99_ms']:>12.3f}  {opt_r['p99_ms']:>12.3f}")
    print(f"  {'Errors':20s} {std_r['errors']:>12d}  {opt_r['errors']:>12d}")


def test_cached_vs_uncached_concurrent():
    print(f"\n{SUBSEP}")
    print("Cached Key vs Fresh Key per Session (concurrent)")
    print(SUBSEP)

    cache = KeyCache(1024)
    msg = os.urandom(100)
    sessions = 100

    def cached_session(_):
        priv, pub = cache.get()
        ct = opt_encrypt_bytes(pub, msg)
        opt_decrypt_bytes(priv, ct)

    def uncached_session(_):
        priv, pub = std_gen(1024)
        ct = std_encrypt_bytes(pub, msg)
        std_decrypt_bytes(priv, ct)

    for conc in (1, 5):
        t0 = time.perf_counter()
        with ThreadPoolExecutor(max_workers=conc) as pool:
            list(pool.map(uncached_session, range(sessions)))
        uncached_time = time.perf_counter() - t0

        t0 = time.perf_counter()
        with ThreadPoolExecutor(max_workers=conc) as pool:
            list(pool.map(cached_session, range(sessions)))
        cached_time = time.perf_counter() - t0

        speedup = uncached_time / cached_time if cached_time > 0 else float("inf")
        print(f"  Threads={conc}: Uncached={uncached_time:.3f}s  Cached={cached_time:.3f}s  Speedup={speedup:.1f}x")


def main():
    print(SEP)
    print("TEST 6 — CONCURRENCY & THROUGHPUT")
    print(SEP)

    test_concurrency_scaling()
    test_high_volume()
    test_cached_vs_uncached_concurrent()

    print(f"\n{SEP}")
    print("CONCURRENCY BENCHMARK COMPLETE")
    print(SEP)


if __name__ == "__main__":
    main()
