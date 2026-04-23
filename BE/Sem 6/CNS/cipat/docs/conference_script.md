# Conference Presentation Script
## A Comparative Study of RSA Optimization Techniques for Secure Web Applications

**Presenters:** Bhavesh Patil, Devendra Patil, Sakti Vala
**Affiliation:** Department of Information Technology, C. K. Pithawala College of Engineering, Surat

---

## Slide 1 — Title Slide

Good morning/afternoon everyone. We are Bhavesh Patil, Devendra Patil, and Sakti Vala from the Department of Information Technology at C. K. Pithawala College of Engineering, Surat.

Today we are presenting our research titled **"A Comparative Study of RSA Optimization Techniques for Secure Web Applications."**

This paper evaluates and compares the major optimization techniques available for the RSA cryptosystem, specifically in the context of modern web applications that demand both strong security and low-latency communication.

---

## Slide 2 — Introduction and Motivation

RSA — the Rivest-Shamir-Adleman cryptosystem — has been a cornerstone of public-key cryptography since 1978. It underpins TLS handshakes, digital signatures, certificate authorities, and authentication systems across the internet.

However, RSA carries a significant computational cost. Modular exponentiation with operands spanning thousands of bits makes RSA operations orders of magnitude slower than symmetric alternatives like AES. This performance gap is a real problem for web applications that must handle hundreds or thousands of concurrent secure connections.

At the same time, the threat landscape is evolving. Classical cryptanalytic attacks, timing attacks, fault injection attacks, and the looming threat of quantum computing via Shor's algorithm all constrain how we can safely deploy RSA.

So the central question we address in this paper is: **which RSA optimization techniques, drawn from the existing literature, provide the most significant practical performance improvements for web applications?**

---

## Slide 3 — Literature Survey Overview

We conducted a systematic review of 30 key publications spanning from 1959 to 2024, covering four main areas:

**First**, the foundations of public-key cryptography — starting with Diffie and Hellman's 1976 proposal of asymmetric encryption, through to Rivest, Shamir, and Adleman's original 1978 RSA paper, and alternative systems like Elliptic Curve Cryptography.

**Second**, RSA performance optimization techniques — including the Chinese Remainder Theorem for accelerated decryption, Montgomery multiplication for efficient modular arithmetic, sliding-window exponentiation, and key caching strategies.

**Third**, cryptanalysis and security — covering Boneh's comprehensive survey of RSA attacks, timing attacks by Kocher, fault attacks, and protocol-level attacks like Bleichenbacher's chosen-ciphertext attack.

**And fourth**, hybrid encryption architectures and post-quantum cryptography — including the NIST standardization of CRYSTALS-Kyber and CRYSTALS-Dilithium as RSA's eventual successors.

---

## Slide 4 — Optimization Techniques Compared

Let us walk through the six optimization techniques we evaluated:

**1. CRT-based Decryption.** Proposed by Quisquater and Couvreur in 1982. Instead of computing `c^d mod n` directly, it splits the computation into two half-size modular exponentiations — one mod p and one mod q — then recombines the results using Garner's formula. Theoretically, this yields a 3 to 4 times speedup.

**2. Montgomery Multiplication.** Introduced by Montgomery in 1985. It replaces expensive modular reduction — which requires division — with bitwise shifts and additions. Theoretically provides a 2 to 3 times speedup per multiplication.

**3. Sliding-Window Exponentiation.** Instead of processing the exponent one bit at a time, this method pre-computes a table of odd powers and processes the exponent in windows of w bits, reducing the number of multiplications by 30 to 40 percent.

**4. Key Caching.** In real web server deployments, RSA key pairs are generated once and reused. Caching pre-generated keys eliminates the dominant key-generation bottleneck.

**5. Batch Processing.** Based on Fiat's 1997 work, this amortizes the cost of a single modular exponentiation across multiple messages.

**6. Hybrid RSA+AES Encryption.** RSA wraps a random AES-256-GCM key, and AES handles the actual bulk data encryption. This combines RSA's key management with AES's hardware-accelerated throughput.

---

## Slide 5 — System Architecture

Our experimental framework consists of four modules:

**standard_rsa/** — A baseline, textbook RSA implementation with no algorithmic optimizations. It generates fresh keys per call, uses naive square-and-multiply exponentiation, and includes no caching.

**optimized_rsa/** — An enhanced implementation incorporating all eight optimizations from our survey: CRT decryption, sliding-window exponentiation, Montgomery multiplication, key caching via a KeyCache class, batch functions, pre-computed CRT parameters, hybrid RSA+AES-256-GCM envelope encryption, and fault-attack verification.

**tests/** — Six benchmark test suites covering correctness, speed, memory, hybrid encryption comparison, key-size scaling, and concurrency.

**perf_eval.py** — The primary benchmark runner using Python's cryptography library for AES operations and tracemalloc for memory profiling.

---

## Slide 6 — Experimental Setup

All experiments were conducted on an Apple Silicon platform with 10 performance cores and 16 GB of unified memory, running macOS.

We used Python 3.14 with the cryptography library version 46.0.7.

Our evaluation covered six benchmark dimensions:
1. Correctness verification with 40 assertions
2. Speed benchmarks with 50 samples per measurement
3. Memory allocation profiling using tracemalloc
4. Hybrid versus pure RSA encryption across data sizes from 1 KB to 1 MB
5. Key-size scaling across 1024, 2048, 3072, and 4096-bit keys
6. Concurrent throughput simulation with 1 to 50 threads

---

## Slide 7 — Results: Standard vs. Optimized RSA

Now let us look at the results.

For 2048-bit keys, the comparison between standard and optimized RSA is striking:

- **Encryption**: Standard RSA takes 55.6 milliseconds, while optimized takes just 0.026 milliseconds — a **2136 times speedup**.
- **Decryption**: Standard takes 57.6 milliseconds versus 0.77 milliseconds optimized — a **75 times speedup**.
- **Memory**: The optimized version uses slightly less memory for both encryption and decryption.

The dramatic encryption speedup of 2136 times is primarily due to key caching. The standard implementation generates fresh 2048-bit keys for every operation — a cold start that dominates execution time. The optimized variant simply reuses cached keys, eliminating this bottleneck entirely.

---

## Slide 8 — Results: Key-Size Scaling

We evaluated how the optimized implementation scales across four key sizes:

For **encryption**, time grows modestly — from 0.014 milliseconds at 1024-bit to 0.069 milliseconds at 4096-bit. That is only a 4.9 times increase for a 4 times key-size increase. This is because the public exponent `e = 65537` remains fixed at 17 bits regardless of key size.

For **decryption**, the growth is steeper — from 0.131 milliseconds at 1024-bit to 3.585 milliseconds at 4096-bit, a 27.4 times increase. This is consistent with the O(n² log n) complexity of modular exponentiation.

Memory consumption grows linearly from about 0.5 KB to 0.8 KB across the range — well within practical limits.

---

## Slide 9 — Results: Hybrid vs. Pure RSA

This is perhaps our most important practical finding.

We compared pure RSA chunked encryption against hybrid RSA+AES-GCM across six data sizes:

- At **1 KB**, hybrid is already 1.3 times faster.
- At **10 KB**, hybrid is 33 times faster.
- At **100 KB**, hybrid is 260 times faster.
- At **1 MB**, hybrid is **760 times faster**.

Pure RSA must encrypt data in small 190-byte chunks, requiring many separate RSA operations. The hybrid approach performs exactly one RSA operation to wrap the AES key, regardless of data size, with AES-GCM handling bulk encryption at near-constant time.

The message is clear: **RSA should never be used alone for data exceeding a few hundred bytes.** Hybrid encryption is not just an optimization — it is a necessity.

---

## Slide 10 — Results: Concurrent Throughput

We simulated concurrent web sessions using 1 to 50 threads.

The optimized implementation maintains stable throughput of approximately **1236 to 1294 sessions per second** across all concurrency levels, with no degradation or errors.

Average latency remains under 2 milliseconds even at 50 concurrent threads.

This confirms that key caching effectively eliminates the primary bottleneck under concurrent load, making the optimized implementation suitable for multi-user web application scenarios.

---

## Slide 11 — Theoretical vs. Experimental Comparison

An important nuance in our findings is the gap between theoretical predictions and observed performance:

- **CRT Decryption**: Theory predicts 3 to 4 times speedup. We observed 1.2 times at 2048-bit. The gap is because the theoretical analysis assumes compiled-language execution.
- **Montgomery Multiplication**: Theory predicts 2 to 3 times. We observed 0.3 times — actually slower in Python. The conversion overhead and Python's interpreter costs dominate the arithmetic savings.
- **Sliding-Window**: Theory predicts 30 to 40 percent fewer multiplications. The gain was marginal in Python for similar reasons.
- **Key Caching**: Theory does not formally predict a speedup — it is a deployment strategy. We observed 75 to 2136 times improvement.
- **Hybrid RSA+AES**: Theory predicts 8 to 400 times. We observed 1.3 to 760 times, confirming the prediction.

The key insight is that optimizations which reduce the **number** of expensive operations — like key caching and hybrid encryption — deliver the largest practical improvements in interpreted language environments.

---

## Slide 12 — Conclusions

To summarize our principal findings:

**1. Key caching is the highest-impact optimization**, providing 75 to 2136 times speedup by eliminating repeated key generation. This validates the importance of key management infrastructure.

**2. Hybrid RSA+AES-GCM is essential for bulk data**, outperforming pure RSA by up to 760 times.

**3. CRT provides measurable but modest decryption improvement** in interpreted environments — 1.2 times rather than the theoretical 4 times.

**4. Montgomery multiplication and sliding-window exponentiation underperform in Python** due to interpreter overhead. These are better suited to compiled languages or hardware.

**5. RSA scales approximately quadratically with key size**, making the transition to 3072-bit or 4096-bit keys a significant performance concern.

**6. Concurrent throughput is stable** at over 1200 sessions per second, confirming suitability for multi-user web scenarios.

---

## Slide 13 — Recommendations and Future Work

Based on our findings, we offer three actionable recommendations for web application architects:

**1. Adopt hybrid encryption as the default** for all data payloads. RSA should wrap AES keys, not encrypt data directly.

**2. Implement key caching with periodic rotation** to eliminate the key-generation bottleneck while maintaining reasonable forward secrecy.

**3. Begin planning for post-quantum migration.** With NIST standardizing CRYSTALS-Kyber and CRYSTALS-Dilithium, RSA's security margin will continue to narrow. The optimization techniques we studied buy time, but the transition to lattice-based schemes is inevitable.

For future work, we recommend replicating these benchmarks in compiled languages like C or Rust, evaluating energy consumption for edge and IoT deployments, and comparing RSA directly against CRYSTALS-Kyber in hybrid configurations.

---

## Closing

Thank you for your attention. We would be happy to take any questions.

Our complete experimental code and benchmark data are available for review. The 30 references surveyed in this study are documented in the paper's bibliography for anyone wishing to explore specific techniques in greater depth.

Thank you.
