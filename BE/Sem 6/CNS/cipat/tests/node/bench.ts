/**
 * RSA Performance & Security Evaluation — TypeScript / Node.js
 *
 * Benchmarks the from-scratch standard_rsa and optimized_rsa
 * TypeScript implementations. Mirrors the Python perf_eval.py methodology.
 *
 * Run: node --experimental-strip-types tests/node/bench.ts
 */

import { performance } from "node:perf_hooks";
import { randomBytes } from "node:crypto";
import { writeFileSync, mkdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

// ---------------------------------------------------------------------------
// Resolve paths
// ---------------------------------------------------------------------------
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = join(__dirname, "..", "..");
const chartsDir = join(projectRoot, "charts", "node");
if (!existsSync(chartsDir)) mkdirSync(chartsDir, { recursive: true });

// ---------------------------------------------------------------------------
// Import implementations — use dynamic import with absolute paths
// ---------------------------------------------------------------------------
const stdPath = join(projectRoot, "src", "ts", "standard_rsa", "rsa.ts");
const optPath = join(projectRoot, "src", "ts", "optimized_rsa", "rsa.ts");

const std = await import(stdPath);
const opt = await import(optPath);

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------
interface BenchmarkResult {
  label: string;
  keySize: number;
  avgEncryptMs: number;
  avgDecryptMs: number;
  avgEncryptMemKb: number;
  avgDecryptMemKb: number;
  samples: number;
}

interface HybridResult {
  label: string;
  dataSizeKb: number;
  avgTimeMs: number;
  avgMemKb: number;
  samples: number;
}

interface LoadResult {
  concurrency: number;
  totalSessions: number;
  totalTimeS: number;
  throughputSps: number;
  avgLatencyMs: number;
  peakMemBytes: number;
}

interface OptBreakdown {
  technique: string;
  meanMs: number;
  stdevMs: number;
}

// ---------------------------------------------------------------------------
// Utility helpers
// ---------------------------------------------------------------------------

function randomBigInt(bits: number): bigint {
  const bytes = Math.ceil(bits / 8);
  const buf = randomBytes(bytes);
  let result = 0n;
  for (const b of buf) {
    result = (result << 8n) | BigInt(b);
  }
  return result & ((1n << BigInt(bits)) - 1n);
}

function measureMs(fn: () => void, repeats: number): { mean: number; stdev: number } {
  const times: number[] = [];
  for (let i = 0; i < repeats; i++) {
    const t0 = performance.now();
    fn();
    const t1 = performance.now();
    times.push(t1 - t0);
  }
  const mean = times.reduce((a, b) => a + b, 0) / times.length;
  const variance = times.length > 1
    ? times.reduce((sum, t) => sum + (t - mean) ** 2, 0) / (times.length - 1)
    : 0;
  return { mean, stdev: Math.sqrt(variance) };
}

function measureWithMem(fn: () => void, repeats: number): { avgMs: number; avgMemKb: number } {
  const times: number[] = [];
  const memDeltas: number[] = [];

  for (let i = 0; i < repeats; i++) {
    globalThis.gc?.(); // hint if --expose-gc
    const memBefore = process.memoryUsage().heapUsed;
    const t0 = performance.now();
    fn();
    const t1 = performance.now();
    const memAfter = process.memoryUsage().heapUsed;
    times.push(t1 - t0);
    memDeltas.push(Math.max(0, memAfter - memBefore) / 1024);
  }

  return {
    avgMs: times.reduce((a, b) => a + b, 0) / times.length,
    avgMemKb: memDeltas.reduce((a, b) => a + b, 0) / memDeltas.length,
  };
}

// ---------------------------------------------------------------------------
// CSV output helper
// ---------------------------------------------------------------------------
function writeCsv(rows: Record<string, string | number>[], path: string) {
  if (rows.length === 0) return;
  const headers = Object.keys(rows[0]);
  const lines = [
    headers.join(","),
    ...rows.map((r) => headers.map((h) => r[h]).join(",")),
  ];
  writeFileSync(path, lines.join("\n"));
  console.log(`  CSV → ${path}`);
}

// ---------------------------------------------------------------------------
// Benchmark 1 — Standard RSA vs Optimized RSA
// ---------------------------------------------------------------------------
function benchmarkRsaComparison(keySize = 2048, samples = 30): [BenchmarkResult, BenchmarkResult] {
  const msgInt = randomBigInt(keySize >> 1);

  // Standard: cold start (keygen + encrypt/decrypt per sample)
  console.log("    Measuring standard encrypt (cold start, keygen+encrypt)...");
  const stdEnc = measureWithMem(() => {
    const { pub } = std.generateKeypair(keySize);
    std.encrypt(pub, msgInt);
  }, Math.min(samples, 10));

  console.log("    Measuring standard decrypt (cold start, keygen+enc+dec)...");
  const stdDec = measureWithMem(() => {
    const { priv, pub } = std.generateKeypair(keySize);
    const ct = std.encrypt(pub, msgInt);
    std.decrypt(priv, ct);
  }, Math.min(samples, 10));

  const stdResult: BenchmarkResult = {
    label: "Standard RSA (from scratch)",
    keySize,
    avgEncryptMs: stdEnc.avgMs,
    avgDecryptMs: stdDec.avgMs,
    avgEncryptMemKb: stdEnc.avgMemKb,
    avgDecryptMemKb: stdDec.avgMemKb,
    samples,
  };

  // Optimized: use KeyCache (warm, cached keys)
  const cache = new opt.KeyCache(keySize);
  const { priv, pub } = cache.get();
  const ctSample = opt.encrypt(pub, msgInt);

  console.log("    Measuring optimized encrypt (cached key)...");
  const optEnc = measureWithMem(() => opt.encrypt(pub, msgInt), samples);

  console.log("    Measuring optimized decrypt (cached key + CRT)...");
  const optDec = measureWithMem(() => opt.decrypt(priv, ctSample), samples);

  const optResult: BenchmarkResult = {
    label: "Optimized RSA (CRT + cached)",
    keySize,
    avgEncryptMs: optEnc.avgMs,
    avgDecryptMs: optDec.avgMs,
    avgEncryptMemKb: optEnc.avgMemKb,
    avgDecryptMemKb: optDec.avgMemKb,
    samples,
  };

  return [stdResult, optResult];
}

// ---------------------------------------------------------------------------
// Benchmark 2 — Individual optimization breakdown
// ---------------------------------------------------------------------------
function benchmarkOptimizationBreakdown(keySize = 2048, samples = 30): OptBreakdown[] {
  const results: OptBreakdown[] = [];

  const base = randomBigInt(keySize);
  const exp = randomBigInt(keySize);
  let modN = randomBigInt(keySize) | (1n << BigInt(keySize - 1)) | 1n;
  if (modN % 2n === 0n) modN |= 1n;

  // 1. Binary square-and-multiply
  console.log("    [1/5] Binary square-and-multiply...");
  let m = measureMs(() => std.modExp(base, exp, modN), samples);
  results.push({ technique: "Binary sq-and-mult (standard)", meanMs: m.mean, stdevMs: m.stdev });

  // 2. Sliding-window without Montgomery
  console.log("    [2/5] Sliding-window (no Montgomery)...");
  m = measureMs(() => opt.slidingWindowNoMont(base, exp, modN), samples);
  results.push({ technique: "Sliding-window only", meanMs: m.mean, stdevMs: m.stdev });

  // 3. Sliding-window with Montgomery
  console.log("    [3/5] Sliding-window + Montgomery...");
  m = measureMs(() => opt.modExpSlidingWindow(base, exp, modN), samples);
  results.push({ technique: "Sliding-window + Montgomery", meanMs: m.mean, stdevMs: m.stdev });

  // 4. CRT decryption vs standard decryption
  console.log("    [4/5] CRT decryption vs standard decryption...");
  const { priv: privStd, pub } = std.generateKeypair(keySize);
  const { priv: privOpt } = opt.generateKeypair(keySize);
  const msg = randomBigInt(keySize >> 1);
  const ctStd = std.encrypt(pub, msg);
  const ctOpt = opt.encrypt(pub, msg);

  m = measureMs(() => std.decrypt(privStd, ctStd), samples);
  results.push({ technique: "Decrypt without CRT", meanMs: m.mean, stdevMs: m.stdev });

  m = measureMs(() => opt.decrypt(privOpt, ctOpt), samples);
  results.push({ technique: "Decrypt with CRT", meanMs: m.mean, stdevMs: m.stdev });

  // 5. Key caching: cold start vs cached
  console.log("    [5/5] Key caching: cold start vs cached...");
  const msgBytes = randomBytes((keySize >> 3) - 11);

  m = measureMs(() => {
    const { pub: p } = std.generateKeypair(keySize);
    std.encryptBytes(p, Buffer.from(msgBytes));
  }, Math.min(samples, 10));
  results.push({ technique: "Cold start (keygen+enc)", meanMs: m.mean, stdevMs: m.stdev });

  const cache = new opt.KeyCache(keySize);
  const { pub: pubCached } = cache.get();
  m = measureMs(() => opt.encryptBytes(pubCached, Buffer.from(msgBytes)), samples);
  results.push({ technique: "Cached key (enc only)", meanMs: m.mean, stdevMs: m.stdev });

  return results;
}

// ---------------------------------------------------------------------------
// Benchmark 3 — Key-size sweep
// ---------------------------------------------------------------------------
function benchmarkKeySizes(
  keySizes = [1024, 2048, 3072, 4096],
  samples = 30,
): BenchmarkResult[] {
  const results: BenchmarkResult[] = [];

  for (const ks of keySizes) {
    console.log(`    RSA-${ks} (generating keys)...`);
    const cache = new opt.KeyCache(ks);
    const { priv, pub } = cache.get();
    const msgInt = randomBigInt(ks >> 1);
    const ctSample = opt.encrypt(pub, msgInt);

    const enc = measureWithMem(() => opt.encrypt(pub, msgInt), samples);
    const dec = measureWithMem(() => opt.decrypt(priv, ctSample), samples);

    results.push({
      label: `RSA-${ks}`,
      keySize: ks,
      avgEncryptMs: enc.avgMs,
      avgDecryptMs: dec.avgMs,
      avgEncryptMemKb: enc.avgMemKb,
      avgDecryptMemKb: dec.avgMemKb,
      samples,
    });
    console.log(`    RSA-${ks} done — enc=${enc.avgMs.toFixed(4)}ms, dec=${dec.avgMs.toFixed(4)}ms`);
  }

  return results;
}

// ---------------------------------------------------------------------------
// Benchmark 4 — Hybrid RSA+AES vs Pure RSA
// ---------------------------------------------------------------------------
function benchmarkHybrid(
  dataSizesKb = [1, 10, 50, 100, 500, 1000],
  samples = 15,
): [HybridResult[], HybridResult[]] {
  console.log("    Generating 2048-bit keys for hybrid test...");
  const { pub } = opt.generateKeypair(2048);
  const cache = new opt.KeyCache(2048);
  const { pub: pubCached } = cache.get();
  const chunkSize = (2048 >> 3) - 11; // max bytes per RSA block with PKCS#1

  const hybridResults: HybridResult[] = [];
  const pureResults: HybridResult[] = [];

  for (const sz of dataSizesKb) {
    const data = randomBytes(sz * 1024);

    // Hybrid: RSA wraps AES key, AES encrypts bulk data
    const hyb = measureWithMem(() => opt.hybridEncrypt(pubCached, data), Math.max(samples >> 1, 5));
    hybridResults.push({
      label: "Hybrid RSA+AES-GCM",
      dataSizeKb: sz,
      avgTimeMs: hyb.avgMs,
      avgMemKb: hyb.avgMemKb,
      samples,
    });

    // Pure RSA: encrypt in chunks
    const pure = measureWithMem(() => {
      for (let i = 0; i < data.length; i += chunkSize) {
        opt.encryptBytes(pubCached, data.subarray(i, i + chunkSize));
      }
    }, Math.max(samples >> 2, 3));
    pureResults.push({
      label: "Pure RSA (chunked)",
      dataSizeKb: sz,
      avgTimeMs: pure.avgMs,
      avgMemKb: pure.avgMemKb,
      samples: Math.max(samples >> 2, 3),
    });

    const speedup = pure.avgMs / hyb.avgMs;
    console.log(`    ${sz}KB — Hybrid: ${hyb.avgMs.toFixed(3)}ms, Pure: ${pure.avgMs.toFixed(3)}ms (${speedup.toFixed(1)}x)`);
  }

  return [hybridResults, pureResults];
}

// ---------------------------------------------------------------------------
// Benchmark 5 — Dynamic load simulation (using worker threads)
// ---------------------------------------------------------------------------
function benchmarkLoad(
  concurrencyLevels = [1, 5, 10, 25, 50],
  sessionsPerLevel = 50,
): LoadResult[] {
  const results: LoadResult[] = [];

  const cache = new opt.KeyCache(2048);
  const { priv, pub } = cache.get();
  const msg = randomBytes(100);

  for (const conc of concurrencyLevels) {
    console.log(`    Concurrency=${conc}...`);

    // Node.js is single-threaded for CPU-bound work (like Python with GIL).
    // We run sessions sequentially — the concurrency level simulates
    // how many sessions a server would handle in parallel (conceptually).
    const latencies: number[] = [];
    const start = performance.now();

    for (let i = 0; i < sessionsPerLevel; i++) {
      const t0 = performance.now();
      const ct = opt.encryptBytes(pub, Buffer.from(msg));
      opt.decryptBytes(priv, ct);
      latencies.push(performance.now() - t0);
    }

    const totalTime = (performance.now() - start) / 1000;
    const avgLat = latencies.reduce((a, b) => a + b, 0) / latencies.length;
    const mem = process.memoryUsage().heapUsed;

    results.push({
      concurrency: conc,
      totalSessions: sessionsPerLevel,
      totalTimeS: totalTime,
      throughputSps: sessionsPerLevel / totalTime,
      avgLatencyMs: avgLat,
      peakMemBytes: mem,
    });
  }

  return results;
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------
async function main() {
  console.log("=".repeat(60));
  console.log("RSA Performance & Security Evaluation — TypeScript / Node.js");
  console.log("(Using from-scratch standard_rsa and optimized_rsa)");
  console.log("=".repeat(60));

  const csvRows: Record<string, string | number>[] = [];

  // --- 1. Standard vs Optimized ---
  console.log("\n[1] Standard RSA vs Optimized RSA (2048-bit)");
  const [stdResult, optResult] = benchmarkRsaComparison(2048);

  for (const r of [stdResult, optResult]) {
    console.log(
      `  ${r.label}: enc=${r.avgEncryptMs.toFixed(3)}ms  dec=${r.avgDecryptMs.toFixed(3)}ms  ` +
      `enc_mem=${r.avgEncryptMemKb.toFixed(1)}KB  dec_mem=${r.avgDecryptMemKb.toFixed(1)}KB`,
    );
  }

  const encSpeedup = stdResult.avgEncryptMs / optResult.avgEncryptMs || Infinity;
  const decSpeedup = stdResult.avgDecryptMs / optResult.avgDecryptMs || Infinity;
  console.log(`  >>> Encryption speedup: ${encSpeedup.toFixed(1)}x   Decryption speedup: ${decSpeedup.toFixed(1)}x`);

  csvRows.push(
    {
      benchmark: "std_vs_opt", label: stdResult.label, key_size: stdResult.keySize,
      encrypt_ms: stdResult.avgEncryptMs.toFixed(4), decrypt_ms: stdResult.avgDecryptMs.toFixed(4),
      encrypt_mem_kb: stdResult.avgEncryptMemKb.toFixed(2), decrypt_mem_kb: stdResult.avgDecryptMemKb.toFixed(2),
    },
    {
      benchmark: "std_vs_opt", label: optResult.label, key_size: optResult.keySize,
      encrypt_ms: optResult.avgEncryptMs.toFixed(4), decrypt_ms: optResult.avgDecryptMs.toFixed(4),
      encrypt_mem_kb: optResult.avgEncryptMemKb.toFixed(2), decrypt_mem_kb: optResult.avgDecryptMemKb.toFixed(2),
    },
  );

  // --- 2. Individual optimization breakdown ---
  console.log("\n[2] Individual Optimization Breakdown (2048-bit)");
  const breakdown = benchmarkOptimizationBreakdown(2048);

  console.log(`\n  ${"Technique".padEnd(35)}  ${"Mean (ms)".padStart(12)}  ${"Stdev".padStart(10)}`);
  console.log(`  ${"─".repeat(35)}  ${"─".repeat(12)}  ${"─".repeat(10)}`);
  for (const b of breakdown) {
    console.log(`  ${b.technique.padEnd(35)}  ${b.meanMs.toFixed(4).padStart(12)}  ${b.stdevMs.toFixed(4).padStart(10)}`);
    csvRows.push({
      benchmark: "opt_breakdown", label: b.technique, key_size: 2048,
      encrypt_ms: b.meanMs.toFixed(4), decrypt_ms: "0",
      encrypt_mem_kb: "0", decrypt_mem_kb: "0",
    });
  }

  // Speedup summary
  const [stdModExp, swOnly, swMont, decNoCrt, decWithCrt, coldStart, cachedEnc] = breakdown;
  console.log("\n  Speedup Summary:");
  if (swOnly.meanMs > 0) console.log(`    Sliding-window vs binary:     ${(stdModExp.meanMs / swOnly.meanMs).toFixed(2)}x`);
  if (swMont.meanMs > 0) console.log(`    + Montgomery vs sliding-window: ${(swOnly.meanMs / swMont.meanMs).toFixed(2)}x`);
  if (swMont.meanMs > 0) console.log(`    + Montgomery vs standard:      ${(stdModExp.meanMs / swMont.meanMs).toFixed(2)}x`);
  if (decWithCrt.meanMs > 0) console.log(`    CRT decryption speedup:        ${(decNoCrt.meanMs / decWithCrt.meanMs).toFixed(2)}x`);
  if (cachedEnc.meanMs > 0) console.log(`    Key caching speedup:           ${(coldStart.meanMs / cachedEnc.meanMs).toFixed(1)}x`);

  // --- 3. Key-size sweep ---
  console.log("\n[3] Key-size comparison (optimized, cached keys)");
  const ksResults = benchmarkKeySizes();

  for (const r of ksResults) {
    console.log(
      `  ${r.label}: enc=${r.avgEncryptMs.toFixed(4)}ms  dec=${r.avgDecryptMs.toFixed(4)}ms`,
    );
    csvRows.push({
      benchmark: "keysize_sweep", label: r.label, key_size: r.keySize,
      encrypt_ms: r.avgEncryptMs.toFixed(4), decrypt_ms: r.avgDecryptMs.toFixed(4),
      encrypt_mem_kb: r.avgEncryptMemKb.toFixed(2), decrypt_mem_kb: r.avgDecryptMemKb.toFixed(2),
    });
  }

  // --- 4. Hybrid vs Pure RSA ---
  console.log("\n[4] Hybrid RSA+AES vs Pure RSA (bulk data, from-scratch)");
  const [hybRes, pureRes] = benchmarkHybrid();

  console.log(`\n  ${"Size".padStart(8)}  ${"Hybrid (ms)".padStart(12)}  ${"Pure RSA (ms)".padStart(14)}  ${"Speedup".padStart(8)}`);
  console.log(`  ${"─".repeat(8)}  ${"─".repeat(12)}  ${"─".repeat(14)}  ${"─".repeat(8)}`);
  for (let i = 0; i < hybRes.length; i++) {
    const speedup = pureRes[i].avgTimeMs / hybRes[i].avgTimeMs || Infinity;
    console.log(
      `  ${`${hybRes[i].dataSizeKb}KB`.padStart(7)}  ${hybRes[i].avgTimeMs.toFixed(3).padStart(12)}  ${pureRes[i].avgTimeMs.toFixed(3).padStart(14)}  ${speedup.toFixed(1).padStart(7)}x`,
    );
  }

  // --- 5. Load simulation ---
  console.log("\n[5] Dynamic load simulation (optimized, cached keys)");
  const loadResults = benchmarkLoad();

  for (const r of loadResults) {
    console.log(
      `  conc=${r.concurrency}  throughput=${r.throughputSps.toFixed(1)} sess/s  latency=${r.avgLatencyMs.toFixed(1)}ms`,
    );
  }

  // --- Summary CSV ---
  const csvPath = join(projectRoot, "benchmarks", "node_results_summary.csv");
  writeCsv(csvRows, csvPath);

  console.log("\n" + "=".repeat(60));
  console.log("All benchmarks complete.");
  console.log("=".repeat(60));
}

main().catch((err) => {
  console.error("Benchmark failed:", err);
  process.exit(1);
});
