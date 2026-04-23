"""
RSA Performance & Security Evaluation
Uses the actual from-scratch standard_rsa and optimized_rsa implementations.

Benchmarks:
  1. Standard RSA vs Optimized RSA (encryption/decryption time, memory usage)
  2. Individual optimization breakdown (CRT, Montgomery, sliding-window, key caching)
  3. Hybrid RSA+AES vs Pure RSA for bulk data encryption
  4. Key-size comparison (1024, 2048, 3072, 4096 bits)
  5. Dynamic load simulation (concurrent sessions)

Requirements:
  pip install cryptography matplotlib pandas
"""

import os
import sys
import time
import tracemalloc
import secrets
import statistics
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import pandas as pd

# ---------------------------------------------------------------------------
# Import from-scratch implementations
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..")
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))

from standard_rsa.rsa import (
    generate_keypair as std_gen,
    encrypt as std_encrypt,
    decrypt as std_decrypt,
    encrypt_bytes as std_encrypt_bytes,
    decrypt_bytes as std_decrypt_bytes,
    mod_exp as std_mod_exp,
    hybrid_encrypt as std_hybrid_enc,
    hybrid_decrypt as std_hybrid_dec,
)

from optimized_rsa.rsa import (
    generate_keypair as opt_gen,
    encrypt as opt_encrypt,
    decrypt as opt_decrypt,
    encrypt_bytes as opt_encrypt_bytes,
    decrypt_bytes as opt_decrypt_bytes,
    mod_exp_sliding_window as opt_mod_exp,
    sliding_window_no_mont,
    MontgomeryContext,
    KeyCache,
    hybrid_encrypt as opt_hybrid_enc,
    hybrid_decrypt as opt_hybrid_dec,
)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class BenchmarkResult:
    label: str
    key_size: int
    avg_encrypt_ms: float
    avg_decrypt_ms: float
    avg_encrypt_mem_kb: float
    avg_decrypt_mem_kb: float
    samples: int


@dataclass
class HybridResult:
    label: str
    data_size_kb: int
    avg_time_ms: float
    avg_mem_kb: float
    samples: int


@dataclass
class LoadResult:
    concurrency: int
    total_sessions: int
    total_time_s: float
    throughput_sps: float
    avg_latency_ms: float
    peak_mem_mb: float


@dataclass
class OptBreakdown:
    technique: str
    mean_ms: float
    stdev_ms: float


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _measure(func, *args, repeat: int = 50) -> Tuple[float, float]:
    """Run *func* *repeat* times, return (avg_time_ms, avg_mem_delta_kb)."""
    times: List[float] = []
    mem_deltas: List[float] = []
    for _ in range(repeat):
        tracemalloc.start()
        t0 = time.perf_counter()
        func(*args)
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        times.append((t1 - t0) * 1000)
        mem_deltas.append(peak / 1024)
    return statistics.mean(times), statistics.mean(mem_deltas)


def _bench_ms(func, repeats: int = 50) -> Tuple[float, float]:
    """Return (mean_ms, stdev_ms)."""
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        func()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000)
    return statistics.mean(times), (statistics.stdev(times) if len(times) > 1 else 0)


# ---------------------------------------------------------------------------
# Benchmark 1 — Standard RSA vs Optimized RSA (from-scratch)
# ---------------------------------------------------------------------------

def benchmark_rsa_comparison(key_size: int = 2048, samples: int = 30) -> Tuple[BenchmarkResult, BenchmarkResult]:
    import random
    msg_int = random.getrandbits(key_size // 2)

    # Standard RSA: generate key + encrypt/decrypt per sample (cold start)
    def _std_encrypt_op():
        priv, pub = std_gen(key_size)
        std_encrypt(pub, msg_int)

    def _std_decrypt_op():
        priv, pub = std_gen(key_size)
        ct = std_encrypt(pub, msg_int)
        std_decrypt(priv, ct)

    print("    Measuring standard encrypt (cold start, keygen+encrypt)...")
    enc_t, enc_m = _measure(lambda: _std_encrypt_op(), repeat=min(samples, 10))
    print("    Measuring standard decrypt (cold start, keygen+enc+dec)...")
    dec_t, dec_m = _measure(lambda: _std_decrypt_op(), repeat=min(samples, 10))
    std = BenchmarkResult("Standard RSA (from scratch)", key_size, enc_t, dec_t, enc_m, dec_m, samples)

    # Optimized RSA: use KeyCache (warm, cached keys)
    cache = KeyCache(key_size)
    priv, pub = cache.get()
    ct_sample = opt_encrypt(pub, msg_int)

    def _opt_encrypt_op():
        opt_encrypt(pub, msg_int)

    def _opt_decrypt_op():
        opt_decrypt(priv, ct_sample)

    print("    Measuring optimized encrypt (cached key)...")
    enc_t, enc_m = _measure(lambda: _opt_encrypt_op(), repeat=samples)
    print("    Measuring optimized decrypt (cached key + CRT)...")
    dec_t, dec_m = _measure(lambda: _opt_decrypt_op(), repeat=samples)
    optimised = BenchmarkResult("Optimized RSA (CRT + cached)", key_size, enc_t, dec_t, enc_m, dec_m, samples)

    return std, optimised


# ---------------------------------------------------------------------------
# Benchmark 2 — Individual optimization breakdown
# ---------------------------------------------------------------------------

def benchmark_optimization_breakdown(key_size: int = 2048, samples: int = 30) -> List[OptBreakdown]:
    """Measure each optimization technique individually to populate paper Table V."""
    import random
    results: List[OptBreakdown] = []

    base = random.getrandbits(key_size)
    exp = random.getrandbits(key_size)
    mod_n = random.getrandbits(key_size) | (1 << (key_size - 1)) | 1

    # Ensure mod is odd for Montgomery
    if mod_n % 2 == 0:
        mod_n |= 1

    # --- 1. Standard mod_exp (binary square-and-multiply) ---
    print("    [1/5] Binary square-and-multiply...")
    mean, sd = _bench_ms(lambda: std_mod_exp(base, exp, mod_n), samples)
    results.append(OptBreakdown("Binary sq-and-mult (standard)", mean, sd))

    # --- 2. Sliding-window WITHOUT Montgomery ---
    print("    [2/5] Sliding-window (no Montgomery)...")
    mean, sd = _bench_ms(lambda: sliding_window_no_mont(base, exp, mod_n), samples)
    results.append(OptBreakdown("Sliding-window only", mean, sd))

    # --- 3. Sliding-window WITH Montgomery ---
    print("    [3/5] Sliding-window + Montgomery...")
    mean, sd = _bench_ms(lambda: opt_mod_exp(base, exp, mod_n), samples)
    results.append(OptBreakdown("Sliding-window + Montgomery", mean, sd))

    # --- 4. CRT decryption vs standard decryption ---
    print("    [4/5] CRT decryption vs standard decryption...")
    priv_std, pub = std_gen(key_size)
    priv_opt, _ = opt_gen(key_size)
    msg = random.getrandbits(key_size // 2)
    ct_std = std_encrypt(pub, msg)
    ct_opt = opt_encrypt(pub, msg)

    mean_std_dec, sd = _bench_ms(lambda: std_decrypt(priv_std, ct_std), samples)
    results.append(OptBreakdown("Decrypt without CRT", mean_std_dec, sd))

    mean_opt_dec, sd = _bench_ms(lambda: opt_decrypt(priv_opt, ct_opt), samples)
    results.append(OptBreakdown("Decrypt with CRT", mean_opt_dec, sd))

    # --- 5. Key caching: cold start vs cached ---
    print("    [5/5] Key caching: cold start vs cached...")
    msg_bytes = os.urandom((key_size // 8) - 11)

    def cold_start():
        _, pub = std_gen(key_size)
        std_encrypt_bytes(pub, msg_bytes)

    cache = KeyCache(key_size)
    _, pub_cached = cache.get()

    def cached():
        opt_encrypt_bytes(pub_cached, msg_bytes)

    mean_cold, sd = _bench_ms(cold_start, min(samples, 10))
    results.append(OptBreakdown("Cold start (keygen+enc)", mean_cold, sd))

    mean_cached, sd = _bench_ms(cached, samples)
    results.append(OptBreakdown("Cached key (enc only)", mean_cached, sd))

    return results


# ---------------------------------------------------------------------------
# Benchmark 3 — Key-size sweep (optimized, cached)
# ---------------------------------------------------------------------------

def benchmark_key_sizes(key_sizes=(1024, 2048, 3072, 4096), samples: int = 30) -> List[BenchmarkResult]:
    import random
    results: List[BenchmarkResult] = []

    for ks in key_sizes:
        print(f"    RSA-{ks} (generating keys)...")
        cache = KeyCache(ks)
        priv, pub = cache.get()
        msg_int = random.getrandbits(ks // 2)
        ct_sample = opt_encrypt(pub, msg_int)

        enc_t, enc_m = _measure(lambda: opt_encrypt(pub, msg_int), repeat=samples)
        dec_t, dec_m = _measure(lambda: opt_decrypt(priv, ct_sample), repeat=samples)

        results.append(BenchmarkResult(f"RSA-{ks}", ks, enc_t, dec_t, enc_m, dec_m, samples))
        print(f"    RSA-{ks} done — enc={enc_t:.4f}ms, dec={dec_t:.4f}ms")

    return results


# ---------------------------------------------------------------------------
# Benchmark 4 — Hybrid RSA+AES vs Pure RSA (bulk data, from-scratch)
# ---------------------------------------------------------------------------

def benchmark_hybrid(data_sizes_kb=(1, 10, 50, 100, 500, 1000), samples: int = 15) -> Tuple[List[HybridResult], List[HybridResult]]:
    print("    Generating 2048-bit keys for hybrid test...")
    priv, pub = opt_gen(2048)
    cache = KeyCache(2048)
    _, pub_cached = cache.get()
    chunk_size = (2048 // 8) - 11  # max bytes per RSA block with PKCS#1 padding

    hybrid_results: List[HybridResult] = []
    pure_results: List[HybridResult] = []

    for sz in data_sizes_kb:
        data = secrets.token_bytes(sz * 1024)

        # Hybrid: RSA wraps AES key, AES encrypts bulk data
        def _hyb():
            opt_hybrid_enc(pub_cached, data)

        t, m = _measure(_hyb, repeat=max(samples // 2, 5))
        hybrid_results.append(HybridResult("Hybrid RSA+AES-GCM", sz, t, m, samples))

        # Pure RSA: encrypt in chunks
        def _pure():
            for i in range(0, len(data), chunk_size):
                opt_encrypt_bytes(pub_cached, data[i : i + chunk_size])

        n_chunks = max(1, len(data) // chunk_size)
        t, m = _measure(_pure, repeat=max(samples // 4, 3))
        pure_results.append(HybridResult("Pure RSA (chunked)", sz, t, m, max(samples // 4, 3)))

        print(f"    {sz}KB — Hybrid: {hybrid_results[-1].avg_time_ms:.3f}ms, Pure: {pure_results[-1].avg_time_ms:.3f}ms")

    return hybrid_results, pure_results


# ---------------------------------------------------------------------------
# Benchmark 5 — Dynamic load simulation (concurrent sessions)
# ---------------------------------------------------------------------------

def benchmark_load(concurrency_levels=(1, 5, 10, 25, 50), sessions_per_level: int = 50) -> List[LoadResult]:
    results: List[LoadResult] = []
    msg = os.urandom(100)

    for conc in concurrency_levels:
        print(f"    Concurrency={conc}...")
        cache = KeyCache(2048)
        priv, pub = cache.get()
        latencies: List[float] = []
        lock = threading.Lock()

        def _session(_):
            t0 = time.perf_counter()
            ct = opt_encrypt_bytes(pub, msg)
            opt_decrypt_bytes(priv, ct)
            elapsed = (time.perf_counter() - t0) * 1000
            with lock:
                latencies.append(elapsed)

        mem_before = tracemalloc.get_traced_memory()[0] if tracemalloc.is_tracing() else 0
        tracemalloc.start()
        t_start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=conc) as pool:
            list(pool.map(_session, range(sessions_per_level)))
        total_time = time.perf_counter() - t_start
        _, peak_mem = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        mem_after = peak_mem

        results.append(
            LoadResult(
                concurrency=conc,
                total_sessions=sessions_per_level,
                total_time_s=total_time,
                throughput_sps=sessions_per_level / total_time,
                avg_latency_ms=statistics.mean(latencies),
                peak_mem_mb=mem_after / (1024 * 1024),
            )
        )

    return results


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------

def _save_bar(filename, labels, values, ylabel, title, colors=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color=colors or "#4C72B0", edgecolor="white")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{val:.2f}", ha="center", va="bottom", fontsize=9)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"  Saved {filename}")


def _save_multi_line(filename, x, series: dict, xlabel, ylabel, title):
    fig, ax = plt.subplots(figsize=(8, 5))
    for label, y in series.items():
        ax.plot(x, y, marker="o", label=label)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"  Saved {filename}")


def _save_hbar(filename, labels, values, xlabel, title, colors=None):
    fig, ax = plt.subplots(figsize=(8, 5))
    y_pos = range(len(labels))
    bars = ax.barh(y_pos, values, color=colors or "#4C72B0", edgecolor="white")
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    for bar, val in zip(bars, values):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                f" {val:.4f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"  Saved {filename}")


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def main():
    out_dir = PROJECT_ROOT
    charts_dir = os.path.join(out_dir, "charts")
    os.makedirs(charts_dir, exist_ok=True)

    print("=" * 60)
    print("RSA Performance & Security Evaluation")
    print("(Using from-scratch standard_rsa and optimized_rsa)")
    print("=" * 60)

    # --- 1. Standard vs Optimized ---
    print("\n[1] Standard RSA vs Optimized RSA (2048-bit)")
    std, opt = benchmark_rsa_comparison(2048)
    for r in (std, opt):
        print(f"  {r.label}: enc={r.avg_encrypt_ms:.3f} ms  dec={r.avg_decrypt_ms:.3f} ms  "
              f"enc_mem={r.avg_encrypt_mem_kb:.1f} KB  dec_mem={r.avg_decrypt_mem_kb:.1f} KB")

    enc_speedup = std.avg_encrypt_ms / opt.avg_encrypt_ms if opt.avg_encrypt_ms > 0 else float("inf")
    dec_speedup = std.avg_decrypt_ms / opt.avg_decrypt_ms if opt.avg_decrypt_ms > 0 else float("inf")
    print(f"  >>> Encryption speedup: {enc_speedup:.1f}x   Decryption speedup: {dec_speedup:.1f}x")

    _save_bar(
        os.path.join(charts_dir, "std_vs_opt_encrypt.png"),
        ["Standard RSA\n(cold start)", "Optimized RSA\n(cached)"],
        [std.avg_encrypt_ms, opt.avg_encrypt_ms],
        "Time (ms)", "Encryption Time — Standard vs Optimized RSA (2048-bit)",
        colors=["#E74C3C", "#2ECC71"],
    )
    _save_bar(
        os.path.join(charts_dir, "std_vs_opt_decrypt.png"),
        ["Standard RSA\n(no CRT)", "Optimized RSA\n(CRT)"],
        [std.avg_decrypt_ms, opt.avg_decrypt_ms],
        "Time (ms)", "Decryption Time — Standard vs Optimized RSA (2048-bit)",
        colors=["#E74C3C", "#2ECC71"],
    )

    # --- 2. Individual optimization breakdown ---
    print("\n[2] Individual Optimization Breakdown (2048-bit)")
    breakdown = benchmark_optimization_breakdown(2048)

    print(f"\n  {'Technique':35s}  {'Mean (ms)':>12s}  {'Stdev':>10s}")
    print(f"  {'─' * 35}  {'─' * 12}  {'─' * 10}")
    for b in breakdown:
        print(f"  {b.technique:35s}  {b.mean_ms:12.4f}  {b.stdev_ms:10.4f}")

    # Compute speedups for paper Table V
    std_modexp_time = breakdown[0].mean_ms
    sw_time = breakdown[1].mean_ms
    sw_mont_time = breakdown[2].mean_ms
    dec_no_crt = breakdown[3].mean_ms
    dec_with_crt = breakdown[4].mean_ms
    cold_start = breakdown[5].mean_ms
    cached_enc = breakdown[6].mean_ms

    print(f"\n  Speedup Summary:")
    if sw_time > 0:
        print(f"    Sliding-window vs binary:     {std_modexp_time / sw_time:.2f}x")
    if sw_mont_time > 0:
        print(f"    + Montgomery vs sliding-window: {sw_time / sw_mont_time:.2f}x")
    if sw_mont_time > 0:
        print(f"    + Montgomery vs standard:      {std_modexp_time / sw_mont_time:.2f}x")
    if dec_with_crt > 0:
        print(f"    CRT decryption speedup:        {dec_no_crt / dec_with_crt:.2f}x")
    if cached_enc > 0:
        print(f"    Key caching speedup:           {cold_start / cached_enc:.1f}x")

    _save_hbar(
        os.path.join(charts_dir, "optimization_breakdown.png"),
        [b.technique for b in breakdown],
        [b.mean_ms for b in breakdown],
        "Time (ms)", "Individual Optimization Breakdown (2048-bit)",
    )

    # --- 3. Key-size sweep ---
    print("\n[3] Key-size comparison (optimized, cached keys)")
    ks_results = benchmark_key_sizes()
    df_ks = pd.DataFrame([vars(r) for r in ks_results])
    print(df_ks.to_string(index=False))

    _save_multi_line(
        os.path.join(charts_dir, "keysize_time.png"),
        [r.key_size for r in ks_results],
        {
            "Encrypt (ms)": [r.avg_encrypt_ms for r in ks_results],
            "Decrypt (ms)": [r.avg_decrypt_ms for r in ks_results],
        },
        "Key Size (bits)", "Time (ms)", "RSA Key Size vs Operation Time (Optimized)",
    )
    _save_multi_line(
        os.path.join(charts_dir, "keysize_memory.png"),
        [r.key_size for r in ks_results],
        {
            "Encrypt Mem (KB)": [r.avg_encrypt_mem_kb for r in ks_results],
            "Decrypt Mem (KB)": [r.avg_decrypt_mem_kb for r in ks_results],
        },
        "Key Size (bits)", "Memory (KB)", "RSA Key Size vs Memory Usage (Optimized)",
    )

    # --- 4. Hybrid vs Pure RSA ---
    print("\n[4] Hybrid RSA+AES vs Pure RSA (bulk data, from-scratch)")
    hyb_res, pure_res = benchmark_hybrid()
    print(f"\n  {'Size':>8s}  {'Hybrid (ms)':>12s}  {'Pure RSA (ms)':>14s}  {'Speedup':>8s}")
    print(f"  {'─'*8}  {'─'*12}  {'─'*14}  {'─'*8}")
    for h, p in zip(hyb_res, pure_res):
        speedup = p.avg_time_ms / h.avg_time_ms if h.avg_time_ms > 0 else float("inf")
        print(f"  {h.data_size_kb:>7d}KB  {h.avg_time_ms:12.3f}  {p.avg_time_ms:14.3f}  {speedup:7.1f}x")

    _save_multi_line(
        os.path.join(charts_dir, "hybrid_vs_pure.png"),
        [r.data_size_kb for r in hyb_res],
        {
            "Hybrid RSA+AES (ms)": [r.avg_time_ms for r in hyb_res],
            "Pure RSA (ms)": [r.avg_time_ms for r in pure_res],
        },
        "Data Size (KB)", "Time (ms)", "Hybrid RSA+AES vs Pure RSA Encryption (from scratch)",
    )

    # --- 5. Load simulation ---
    print("\n[5] Dynamic load simulation (optimized, cached keys)")
    load_results = benchmark_load()
    df_load = pd.DataFrame([vars(r) for r in load_results])
    print(df_load.to_string(index=False))

    _save_multi_line(
        os.path.join(charts_dir, "load_throughput.png"),
        [r.concurrency for r in load_results],
        {
            "Throughput (sessions/s)": [r.throughput_sps for r in load_results],
        },
        "Concurrency", "Sessions / sec", "RSA Throughput vs Concurrency (Optimized)",
    )
    _save_multi_line(
        os.path.join(charts_dir, "load_latency.png"),
        [r.concurrency for r in load_results],
        {
            "Avg Latency (ms)": [r.avg_latency_ms for r in load_results],
        },
        "Concurrency", "Latency (ms)", "RSA Latency vs Concurrency (Optimized)",
    )

    # --- Summary CSV ---
    csv_path = os.path.join(out_dir, "results_summary.csv")
    summary_rows = []

    # Std vs Opt
    for r in (std, opt):
        summary_rows.append({
            "benchmark": "std_vs_opt",
            "label": r.label,
            "key_size": r.key_size,
            "encrypt_ms": round(r.avg_encrypt_ms, 4),
            "decrypt_ms": round(r.avg_decrypt_ms, 4),
            "encrypt_mem_kb": round(r.avg_encrypt_mem_kb, 2),
            "decrypt_mem_kb": round(r.avg_decrypt_mem_kb, 2),
        })

    # Key-size sweep
    for r in ks_results:
        summary_rows.append({
            "benchmark": "keysize_sweep",
            "label": r.label,
            "key_size": r.key_size,
            "encrypt_ms": round(r.avg_encrypt_ms, 4),
            "decrypt_ms": round(r.avg_decrypt_ms, 4),
            "encrypt_mem_kb": round(r.avg_encrypt_mem_kb, 2),
            "decrypt_mem_kb": round(r.avg_decrypt_mem_kb, 2),
        })

    # Optimization breakdown
    for b in breakdown:
        summary_rows.append({
            "benchmark": "opt_breakdown",
            "label": b.technique,
            "key_size": 2048,
            "encrypt_ms": round(b.mean_ms, 4),
            "decrypt_ms": 0,
            "encrypt_mem_kb": 0,
            "decrypt_mem_kb": 0,
        })

    pd.DataFrame(summary_rows).to_csv(csv_path, index=False)
    print(f"\n  Summary CSV → {csv_path}")

    print("\n" + "=" * 60)
    print("All benchmarks complete. Charts saved to charts/")
    print("=" * 60)


if __name__ == "__main__":
    main()
