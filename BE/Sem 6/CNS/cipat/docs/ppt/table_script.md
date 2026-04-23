# PPT Presentation Script — Table Explanations
## A Comparative Study of RSA Optimization Techniques for Secure Web Applications

**Note:** This script walks through each table from the paper (paper2.tex) as it appears in the presentation slides. Use this alongside the main conference_script.md for detailed table walkthroughs.

---

## Table 1 — Comparative Analysis of RSA Optimization Techniques (Slide 4–5)

> **Source:** `Table I — tab:algo_compare` in paper2.tex

This table compares six optimization techniques side-by-side across five dimensions: origin, mechanism, theoretical speedup, scope, and limitation.

Let me walk you through each row:

**CRT Decryption** — Originated from Quisquater and Couvreur in 1982. It splits the single full-size modular exponentiation `c^d mod n` into two half-size exponentiations — one mod p and one mod q — and recombines via Garner's formula. Theoretical speedup is 3 to 4 times. But note the limitation: it is vulnerable to the Bellcore fault attack, so any implementation must include fault verification.

**Montgomery Multiplication** — From Montgomery in 1985. It replaces the expensive division in modular reduction with bitwise shifts using the REDC algorithm. Theoretical speedup is 2 to 3 times per multiplication. Limitation: the conversion to and from Montgomery form adds overhead, and this technique is less effective in interpreted languages like Python.

**Sliding-Window Exponentiation** — From Knuth and documented in the Handbook of Applied Cryptography. It pre-computes a table of odd powers and scans the exponent in variable-length windows. This reduces the number of multiplications by 30 to 40 percent. Limitation: there is table storage overhead, and the gains are marginal for small exponents like `e = 65537`.

**Key Caching** — This is a practical deployment strategy rather than an algorithmic innovation. Generate keys once and reuse them across sessions. The speedup is enormous — 40 to 2000 times versus a cold start — because it eliminates the dominant key-generation bottleneck. Limitation: key rotation complexity and forward secrecy trade-offs.

**Batch Processing** — Based on Fiat's 1997 work on batch RSA. It amortizes the cost of a single modular exponentiation across k messages, achieving O(sqrt(k)) amortized cost per message. Limitation: it requires specific structural pre-conditions and has limited batch size.

**Hybrid RSA+AES** — The envelope encryption paradigm. RSA wraps an AES-256 key; AES encrypts the bulk data. Speedup ranges from 8 to 760 times for data larger than 256 bytes. Limitation: it introduces two-algorithm complexity and key management overhead.

The key takeaway from this table is that theoretical speedups do not always translate to practice — especially in interpreted language environments.

---

## Table 2 — Summary of Key Publications (Slide 3–4)

> **Source:** `Table II — tab:papers_compare` in paper2.tex

This table summarizes 15 landmark publications that form the backbone of our study, organized chronologically:

Starting from **1976** — Diffie and Hellman introduced the concept of asymmetric encryption and key exchange, laying the conceptual foundation for everything that follows.

**1978** — Rivest, Shamir, and Adleman published the first practical public-key encryption and signature scheme — the RSA cryptosystem itself.

**1982** — Quisquater and Couvreur showed that CRT yields approximately 4 times speedup for RSA decryption, making RSA practical for real-world use.

**1985** was a pivotal year — Montgomery introduced modular multiplication without trial division, and independently, Miller and Koblitz proposed elliptic curve cryptography, offering equivalent security with much smaller keys.

**1996** — Kocher demonstrated that execution time variations leak secret key information — the first timing attack on RSA.

**1997** — Shor published his polynomial-time quantum factoring algorithm, establishing the theoretical existential threat to RSA.

**1998** — Bleichenbacher demonstrated a practical chosen-ciphertext attack against RSA with PKCS#1 v1.5 padding, leading to the adoption of OAEP.

**1999** — Boneh published his comprehensive taxonomy of attacks on the RSA cryptosystem — an essential reference for understanding RSA vulnerabilities.

**2001** — Boneh, DeMillo, and Lipton showed that hardware faults during CRT computation can reveal private keys — the Bellcore attack.

**2001** — Lenstra and Verheul developed a systematic method for choosing cryptographic key lengths based on projected advances.

**2012** — Heninger et al. conducted a large-scale analysis finding that 0.2% of RSA public keys on the Internet shared a prime factor due to poor random number generation.

**2022–2023** — CRYSTALS-Kyber and CRYSTALS-Dilithium were selected by NIST as post-quantum standards for key encapsulation and digital signatures, both based on lattice problems.

This chronological progression shows how RSA has been continuously challenged, optimized, and is now heading toward eventual replacement by post-quantum alternatives.

---

## Table 3 — Standard vs. Optimized RSA Performance (Slide 7)

> **Source:** `Table III — tab:std_vs_opt` in paper2.tex

This is the headline results table. Let me explain each row carefully:

**Encryption row:**
- Standard RSA takes **55.556 milliseconds** — over 55 milliseconds to encrypt a single message.
- Optimized RSA takes just **0.026 milliseconds** — 26 microseconds.
- That is a **2136 times speedup**.

Where does this massive improvement come from? It is not from a faster encryption algorithm. It is from **key caching**. The standard implementation generates fresh 2048-bit keys for every single operation — that key generation alone takes over 55 milliseconds. The optimized variant reuses cached keys, reducing the actual encrypt call to just 26 microseconds.

**Decryption row:**
- Standard: **57.636 milliseconds**
- Optimized: **0.771 milliseconds**
- Speedup: **75 times**

Here the improvement comes from both key caching AND CRT-based decryption. CRT splits the decryption into two half-size exponentiations, and combined with cached keys, we get a 75-fold improvement.

**Memory rows:**
- Encryption memory: 0.9 KB standard vs 0.6 KB optimized — a 1.5 times reduction.
- Decryption memory: 0.9 KB vs 0.8 KB — a 1.1 times reduction.

Memory improvements are modest because the dominant memory cost is the key material itself, which cannot be compressed.

The critical insight: **the biggest performance bottleneck in standard RSA is not the encryption math — it is the key generation.** Eliminating repeated key generation through caching yields the single largest improvement.

---

## Table 4 — Key-Size Scaling Performance (Slide 8)

> **Source:** `Table IV — tab:keysize` in paper2.tex

This table shows how the optimized RSA implementation performs as we increase key size from 1024 to 4096 bits:

**Encryption column** — Look at how gently encryption time grows:
- 1024-bit: 0.014 ms
- 2048-bit: 0.025 ms
- 3072-bit: 0.043 ms
- 4096-bit: 0.069 ms

That is only a **4.9 times increase** for a **4 times key-size increase**. Why? Because encryption uses the public exponent `e = 65537`, which is always 17 bits regardless of the key size. The cost of `m^65537 mod n` grows slowly because the exponent does not change — only the modulus size increases.

**Decryption column** — The story is very different:
- 1024-bit: 0.131 ms
- 2048-bit: 0.740 ms
- 3072-bit: 1.820 ms
- 4096-bit: 3.585 ms

That is a **27.4 times increase** from 1024 to 4096 bits. The private exponent d is approximately the same size as the modulus, so decryption cost scales with the full O(n^2 log n) complexity of modular exponentiation.

**Growth factors per doubling:**
- 1024 to 2048: encrypt 1.8x, decrypt 5.6x
- 2048 to 3072: encrypt 1.7x, decrypt 2.5x
- 3072 to 4096: encrypt 1.6x, decrypt 2.0x

The decrypt growth factor decreases at larger sizes because CRT operates on half-size operands, but the absolute time increase is still significant.

**Memory columns** — Memory grows linearly from about 0.5 KB to 0.8 KB across the full range — well within practical limits for any server deployment.

**Practical implication:** Moving from 2048-bit to 4096-bit keys — which NIST recommends for long-term security — makes decryption nearly 5 times slower. This makes optimization techniques like CRT and key caching even more important at larger key sizes.

---

## Table 5 — Hybrid RSA+AES-GCM vs. Pure RSA (Slide 9)

> **Source:** `Table V — tab:hybrid` in paper2.tex

This table is perhaps the most important for practitioners. It compares pure RSA chunked encryption against hybrid RSA+AES-GCM across six data sizes:

**The setup:**
- Pure RSA encrypts data in 190-byte chunks (limited by RSA key size minus padding), requiring multiple RSA operations proportional to data size.
- Hybrid RSA performs exactly one RSA operation to wrap a 32-byte AES key, then AES-GCM handles the bulk data.

**Walking through the rows:**

- **1 KB**: Pure RSA takes 0.14 ms, hybrid takes 0.11 ms — hybrid is **1.3 times faster**. At small sizes, the overhead of AES key generation and the single RSA key-wrap partially offset the hybrid advantage.

- **10 KB**: Pure RSA jumps to 1.30 ms, hybrid stays at 0.04 ms — hybrid is **33 times faster**. AES-GCM processes 10 KB in near-constant time while RSA requires 53 chunk operations.

- **50 KB**: Pure RSA reaches 6.50 ms, hybrid remains at 0.04 ms — **163 times faster**.

- **100 KB**: 12.97 ms vs 0.05 ms — **260 times faster**.

- **500 KB**: 64.88 ms vs 0.10 ms — **649 times faster**.

- **1 MB**: 129.18 ms vs 0.17 ms — **760 times faster**.

Notice the pattern: pure RSA time grows linearly with data size (each additional 190-byte chunk adds roughly the same time), while hybrid time grows almost imperceptibly — from 0.04 ms at 10 KB to just 0.17 ms at 1 MB. AES-GCM has hardware acceleration and near-constant throughput regardless of data size.

**The message for web developers:** RSA should never encrypt data directly beyond a few hundred bytes. Always use hybrid encryption where RSA wraps an AES key and AES handles the payload. This is not optional — it is a fundamental architectural requirement.

---

## Table 6 — Concurrent Session Throughput (Slide 10)

> **Source:** `Table VI — tab:concurrency` in paper2.tex

This table simulates a realistic web server scenario with 1 to 50 concurrent threads performing optimized RSA operations:

**Throughput column:**
- 1 thread: 1294 sessions/second
- 5 threads: 1249 sessions/second
- 10 threads: 1249 sessions/second
- 25 threads: 1249 sessions/second
- 50 threads: 1236 sessions/second

The throughput is remarkably stable — ranging from 1236 to 1294 sessions per second across all concurrency levels. There is no degradation, no errors, no timeouts.

**Average Latency column:**
- 1 thread: 0.77 ms
- 5 threads: 1.61 ms (slightly higher due to thread coordination)
- 10 threads: 0.78 ms
- 25 threads: 0.78 ms
- 50 threads: 0.79 ms

Even at 50 concurrent threads, average latency remains under 2 milliseconds. The slight spike at 5 threads is likely due to thread pool initialization overhead, after which the system stabilizes.

**Peak Memory column:**
Memory usage is negligible across all levels — peaking at 0.11 MB for a single thread and dropping to essentially zero at higher concurrency. This is because the cached keys are shared across threads.

**Why is performance so stable?** Because key caching eliminates the dominant bottleneck. Without caching, each thread would need to generate its own 2048-bit key pair, which would cause severe contention and memory pressure. With caching, all threads simply retrieve pre-computed keys and perform the lightweight encrypt/decrypt operations.

**Practical takeaway:** The optimized implementation can comfortably handle over 1200 concurrent TLS handshake simulations per second on a single machine, confirming its suitability for real-world multi-user web applications.

---

## Table 7 — Theoretical vs. Experimental Speedup (Slide 11)

> **Source:** `Table VII — tab:summary` in paper2.tex

This is our synthesis table. It compares what the theoretical literature predicts against what we actually observed in our experiments:

**CRT Decryption:**
- Theory: 3 to 4 times speedup
- Observed: 1.2 times at 2048-bit
- **Why the gap?** The theoretical 4x assumes the only cost is the modular exponentiation itself. In Python, the overhead of function calls, object creation, and Garner recombination (converting results back from mod-p/mod-q to mod-n) eats into the theoretical gain. In a compiled language like C, the observed speedup would be much closer to theory.

**Montgomery Multiplication:**
- Theory: 2 to 3 times speedup
- Observed: **0.3 times** — actually slower!
- **Why?** Montgomery multiplication replaces division with shifts. In Python, the built-in `pow(a, b, n)` is already optimized in C. Our Montgomery implementation in pure Python adds conversion overhead and interpreter dispatch costs that outweigh the arithmetic savings. This is a textbook example of an optimization that works in hardware but backfires in interpreted languages.

**Sliding-Window Exponentiation:**
- Theory: 30 to 40 percent fewer multiplications
- Observed: Marginal improvement in Python
- **Why?** Same reason — Python's per-operation overhead dominates the reduced multiplication count. The savings of a few hundred multiplications at the C level are negligible compared to the thousands of Python function calls involved.

**Key Caching:**
- Theory: N/A — this is a deployment strategy, not an algorithm
- Observed: 75 to 2136 times speedup
- **Why so large?** Because key generation is the single most expensive operation in RSA. Generating two large primes and computing `d = e^(-1) mod phi(n)` takes 55+ milliseconds. Reusing cached keys reduces this to a dictionary lookup — essentially free.

**Hybrid RSA+AES:**
- Theory: 8 to 400 times for bulk data
- Observed: 1.3 to 760 times
- **Assessment:** The experimental results actually exceed the theoretical prediction at large data sizes, because AES-GCM benefits from hardware acceleration (AES-NI instructions) that pure RSA cannot match.

**The overarching conclusion:** In interpreted language environments, optimizations that reduce the **number** of expensive operations (key caching, hybrid encryption) dramatically outperform optimizations that reduce the **per-operation cost** (Montgomery, sliding-window). Web application architects should prioritize the former.

---
