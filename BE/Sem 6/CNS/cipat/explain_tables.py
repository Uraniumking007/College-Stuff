#!/usr/bin/env python3
"""
explain_tables.py — Explains every table from the presentation
cns-ppt.pdf using the source data in paper2.tex.

Run:  python3 explain_tables.py
"""

import csv
import os
import textwrap
from pathlib import Path

BASE = Path(__file__).resolve().parent

# ── helpers ──────────────────────────────────────────────────────────
def heading(title: str, width: int = 72) -> None:
    print(f"\n{'=' * width}")
    print(f"  {title}")
    print(f"{'=' * width}\n")


def sub(text: str) -> None:
    print(f"  {text}")


def wrap(text: str, indent: int = 4) -> None:
    for line in textwrap.wrap(text, width=80, initial_indent=" " * indent,
                              subsequent_indent=" " * indent):
        print(line)


def table_row(cols: list[str], widths: list[int]) -> str:
    parts = []
    for c, w in zip(cols, widths):
        parts.append(str(c).ljust(w))
    return " | ".join(parts)


def divider(widths: list[int]) -> str:
    return "-+-".join("-" * w for w in widths)


# ── data ─────────────────────────────────────────────────────────────
def load_csv() -> list[dict]:
    with open(BASE / "results_summary.csv") as f:
        return list(csv.DictReader(f))


# ── Table 1: Literature Review (PPT Slides 5-6) ─────────────────────
def explain_literature_review():
    heading("TABLE 1 — Literature Review (PPT Slides 5-6, paper2.tex Table II)")

    sub("Source: Section II of paper2.tex — Literature Survey\n")

    data = [
        ("Diffie & Hellman",       "1976", "Public-Key Cryptography",
         "Introduced concept of asymmetric encryption"),
        ("Rivest, Shamir, Adleman", "1978", "RSA Algorithm",
         "Developed first practical public-key cryptosystem"),
        ("Quisquater & Couvreur",  "1982", "CRT Optimization",
         "Improved RSA decryption speed (~4x faster)"),
        ("Montgomery",             "1985", "Montgomery Multiplication",
         "Faster modular multiplication without division"),
        ("Miller & Koblitz",       "1985-87", "ECC",
         "Alternative to RSA with smaller key sizes"),
        ("Kocher",                 "1996", "Timing Attacks",
         "Showed side-channel attack vulnerability in RSA"),
        ("Shor",                   "1997", "Quantum Computing",
         "RSA can be broken using quantum algorithms"),
        ("Bleichenbacher",         "1998", "RSA Attack",
         "Discovered padding-based attack on RSA"),
        ("Boneh",                  "1999", "RSA Security",
         "Surveyed multiple RSA attacks"),
        ("Fiat",                   "1990", "Batch RSA",
         "Introduced batch processing for efficiency"),
        ("Lenstra & Verheul",      "2001", "Key Size",
         "Provided key-size recommendations"),
        ("Heninger et al.",        "2012", "Weak Keys",
         "Found weak RSA keys due to poor randomness"),
        ("NIST",                   "2020", "Standards",
         "Recommended minimum 2048-bit RSA keys"),
        ("Avanzi et al.",          "2023", "Post-Quantum (Kyber)",
         "Introduced quantum-resistant encryption"),
        ("Bai et al.",             "2022", "Post-Quantum (Dilithium)",
         "Quantum-safe digital signature scheme"),
    ]

    widths = [24, 8, 26, 40]
    print(table_row(["Author(s)", "Year", "Technique / Area", "Key Contribution / Finding"], widths))
    print(divider(widths))
    for row in data:
        print(table_row(row, widths))

    print()
    wrap("This table maps 15 key publications (1976-2023) to their contributions "
         "in RSA optimization, security analysis, and post-quantum cryptography. "
         "It spans three eras: foundational (1976-1985), cryptanalysis (1996-2001), "
         "and post-quantum standardization (2012-2023).")
    print()
    wrap("Key takeaway: RSA has evolved through decades of optimization and attack "
         "research, but quantum computing (Shor 1997) ultimately necessitates a "
         "migration to lattice-based schemes like Kyber/Dilithium.")


# ── Table 2: Standard vs Optimized RSA (PPT Slide 10) ──────────────
def explain_std_vs_opt(rows: list[dict]):
    heading("TABLE 2 — Standard vs. Optimized RSA (PPT Slide 10, paper2.tex Table III)")

    sub("Source: paper2.tex Section V-B, benchmark 'std_vs_opt'\n")

    std = rows[0]
    opt = rows[1]

    widths = [22, 16, 18, 12]
    print(table_row(["Operation", "Standard (ms)", "Optimized (ms)", "Speedup"], widths))
    print(divider(widths))

    enc_speedup = f"{float(std['encrypt_ms']) / float(opt['encrypt_ms']):.0f}x"
    dec_speedup = f"{float(std['decrypt_ms']) / float(opt['decrypt_ms']):.0f}x"
    enc_mem = f"{float(std['encrypt_mem_kb']) / float(opt['encrypt_mem_kb']):.1f}x"
    dec_mem = f"{float(std['decrypt_mem_kb']) / float(opt['decrypt_mem_kb']):.1f}x"

    print(table_row(["Encrypt",          std["encrypt_ms"],  opt["encrypt_ms"],  enc_speedup], widths))
    print(table_row(["Decrypt",          std["decrypt_ms"],  opt["decrypt_ms"],  dec_speedup], widths))
    print(table_row(["Enc Memory (KB)",  std["encrypt_mem_kb"], opt["encrypt_mem_kb"], enc_mem], widths))
    print(table_row(["Dec Memory (KB)",  std["decrypt_mem_kb"], opt["decrypt_mem_kb"], dec_mem], widths))

    print()
    wrap("WHY the huge difference?")
    wrap("- Standard RSA generates a FRESH 2048-bit key pair every single call. "
         "Key generation dominates the 55.5 ms encrypt time.")
    wrap("- Optimized RSA uses a KeyCache — keys are generated once and reused, "
         "bringing encrypt down to 0.026 ms (a 2136x speedup).")
    wrap("- Decryption benefits from BOTH key caching AND CRT-based computation "
         "(two half-size exponentiations), giving 75x improvement.")
    print()
    wrap("The memory improvement is modest (1.1-1.5x) because the actual modular "
         "arithmetic operands are similar; caching saves time, not space.")


# ── Table 3: Key-Size Scaling (PPT Slide 10, paper2.tex Table IV) ──
def explain_keysize(rows: list[dict]):
    heading("TABLE 3 — Key-Size Scaling (PPT Slide 10, paper2.tex Table IV)")

    sub("Source: paper2.tex Section V-C, benchmark 'keysize_sweep'\n")

    widths = [12, 12, 12, 14, 14]
    print(table_row(["Key Size", "Enc (ms)", "Dec (ms)", "Enc Mem (KB)", "Dec Mem (KB)"], widths))
    print(divider(widths))

    for r in rows[2:]:  # rows 2-5 are keysize sweep
        print(table_row(
            [r["key_size"], r["encrypt_ms"], r["decrypt_ms"],
             r["encrypt_mem_kb"], r["decrypt_mem_kb"]], widths))

    print()
    wrap("Encryption grows modestly: 0.014 ms (1024-bit) -> 0.069 ms (4096-bit) = 4.9x")
    wrap("  Reason: public exponent e = 65537 is always 17 bits, so encrypt cost barely scales.")
    print()
    wrap("Decryption grows steeply: 0.131 ms (1024-bit) -> 3.585 ms (4096-bit) = 27.4x")
    wrap("  Reason: private exponent d is as wide as the key, giving O(n^2 log n) complexity.")
    print()
    wrap("Growth per doubling:")
    wrap("  1024 -> 2048:  encrypt 1.8x,  decrypt 5.6x")
    wrap("  2048 -> 3072:  encrypt 1.7x,  decrypt 2.5x")
    wrap("  3072 -> 4096:  encrypt 1.6x,  decrypt 2.0x")
    print()
    wrap("Practical implication: moving from 2048 to 4096-bit keys (NIST long-term "
         "recommendation) multiplies decryption time by ~4.8x — a significant cost "
         "that must be offset by optimizations like CRT and key caching.")


# ── Table 4: Hybrid RSA+AES vs Pure RSA (PPT Slide 11, paper2.tex Table V)
def explain_hybrid():
    heading("TABLE 4 — Hybrid RSA+AES-GCM vs. Pure RSA (PPT Slide 11, paper2.tex Table V)")

    sub("Source: paper2.tex Section V-D, 'Hybrid Encryption' benchmark\n")

    widths = [12, 16, 14, 10]
    print(table_row(["Data Size", "Pure RSA (ms)", "Hybrid (ms)", "Speedup"], widths))
    print(divider(widths))

    hybrid_data = [
        ("1 KB",    "0.14",   "0.11",  "1.3x"),
        ("10 KB",   "1.30",   "0.04",  "33x"),
        ("50 KB",   "6.50",   "0.04",  "163x"),
        ("100 KB",  "12.97",  "0.05",  "260x"),
        ("500 KB",  "64.88",  "0.10",  "649x"),
        ("1000 KB", "129.18", "0.17",  "760x"),
    ]
    for row in hybrid_data:
        print(table_row(row, widths))

    print()
    wrap("Pure RSA must encrypt data in 190-byte chunks (key_size/8 - padding), so "
         "time scales linearly with data size: 0.14 ms at 1 KB -> 129 ms at 1 MB.")
    wrap("Hybrid RSA+AES performs exactly ONE RSA operation (to wrap the 32-byte AES "
         "key), then AES-GCM handles bulk encryption at near-constant cost.")
    print()
    wrap("At 1 KB the speedup is modest (1.3x) because RSA overhead is similar to "
         "AES cost. By 1 MB, hybrid is 760x faster.")
    wrap("Key insight: RSA should NEVER be used alone for data > 256 bytes. Always "
         "use the hybrid envelope approach (RSA wraps AES key, AES encrypts data).")


# ── Table 5: Concurrent Throughput (PPT Slide 11, paper2.tex Table VI)
def explain_concurrency():
    heading("TABLE 5 — Concurrent Session Throughput (PPT Slide 11, paper2.tex Table VI)")

    sub("Source: paper2.tex Section V-E, 'Concurrency' benchmark\n")

    widths = [10, 20, 20, 16]
    print(table_row(["Threads", "Throughput (sess/s)", "Avg Latency (ms)", "Peak Mem (MB)"], widths))
    print(divider(widths))

    conc_data = [
        ("1",  "1294", "0.77", "0.11"),
        ("5",  "1249", "1.61", "0.03"),
        ("10", "1249", "0.78", "0.02"),
        ("25", "1249", "0.78", "0.00"),
        ("50", "1236", "0.79", "0.00"),
    ]
    for row in conc_data:
        print(table_row(row, widths))

    print()
    wrap("The optimized implementation maintains ~1236-1294 sessions/second across "
         "ALL concurrency levels (1 to 50 threads) with no degradation.")
    wrap("Average latency stays under 2 ms even at 50 threads, and memory usage "
         "actually decreases slightly with more threads (shared cached keys).")
    print()
    wrap("This stability is thanks to key caching — all threads share the same "
         "pre-generated key pair, so there is no key-generation bottleneck under load.")
    wrap("In a real web server, this means the optimized RSA can handle hundreds of "
         "TLS handshakes per second without queuing delays.")


# ── Table 6: Theoretical vs Experimental Summary (paper2.tex Table VII)
def explain_summary():
    heading("TABLE 6 — Theoretical vs. Experimental Speedup (paper2.tex Table VII)")

    sub("Source: paper2.tex Section V-F, 'Summary of Comparative Findings'\n")

    widths = [22, 18, 22]
    print(table_row(["Optimization", "Theory", "Observed"], widths))
    print(divider(widths))

    summary = [
        ("CRT Decryption",       "3-4x",      "1.2x (2048-bit)"),
        ("Montgomery Mult.",     "2-3x",      "0.3x (Python)"),
        ("Sliding-Window",       "30-40% fewer mult.", "Marginal in Python"),
        ("Key Caching",          "N/A (deployment)",   "75-2136x"),
        ("Hybrid RSA+AES",       "8-400x",    "1.3-760x"),
    ]
    for row in summary:
        print(table_row(row, widths))

    print()
    wrap("CRT and Montgomery/Sliding-Window underperform their theoretical predictions "
         "because Python's interpreter overhead (object creation, GC, function dispatch) "
         "dominates per-operation cost for moderate key sizes.")
    wrap("Key caching and hybrid encryption — which reduce the NUMBER of expensive "
         "operations rather than per-operation cost — deliver the largest real gains.")
    print()
    wrap("Bottom line: In Python/interpreted environments, focus on eliminating "
         "operations (caching, hybrid) rather than optimizing individual operations "
         "(Montgomery, sliding-window). Save low-level math optimizations for C/Rust.")


# ── main ─────────────────────────────────────────────────────────────
def main():
    print()
    print("=" * 72)
    print("  TABLE EXPLANATIONS FOR cns-ppt.pdf")
    print("  Source LaTeX: cipat/latex/paper2.tex")
    print("  Data: cipat/results_summary.csv")
    print("=" * 72)

    rows = load_csv()

    explain_literature_review()
    explain_std_vs_opt(rows)
    explain_keysize(rows)
    explain_hybrid()
    explain_concurrency()
    explain_summary()

    print()
    print("=" * 72)
    print("  END OF TABLE EXPLANATIONS")
    print("  Total tables explained: 6")
    print("  PPT slides covered: 5, 6, 10, 11")
    print("  LaTeX sections: II, V-B, V-C, V-D, V-E, V-F")
    print("=" * 72)
    print()


if __name__ == "__main__":
    main()
