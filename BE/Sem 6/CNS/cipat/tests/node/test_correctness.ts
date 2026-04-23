/**
 * Correctness test — verify both standard and optimized RSA work.
 * Run: node --experimental-strip-types tests/node/test_correctness.ts
 */

import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { randomBytes } from "node:crypto";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = join(__dirname, "..", "..");

const std = await import(join(projectRoot, "src", "ts", "standard_rsa", "rsa.ts"));
const opt = await import(join(projectRoot, "src", "ts", "optimized_rsa", "rsa.ts"));

let passed = 0;
let failed = 0;

function assert(cond: boolean, label: string) {
  if (cond) {
    console.log(`  PASS: ${label}`);
    passed++;
  } else {
    console.error(`  FAIL: ${label}`);
    failed++;
  }
}

// --- Standard RSA ---
console.log("\n=== Standard RSA ===");

const stdKp = std.generateKeypair(2048);
const msg = 42n;
const ct = std.encrypt(stdKp.pub, msg);
const pt = std.decrypt(stdKp.priv, ct);
assert(pt === msg, "Standard encrypt/decrypt round-trip");

const msgBytes = Buffer.from("Hello RSA from TypeScript!");
const ctBytes = std.encryptBytes(stdKp.pub, msgBytes);
const ptBytes = std.decryptBytes(stdKp.priv, ctBytes);
assert(ptBytes.toString() === msgBytes.toString(), "Standard encryptBytes/decryptBytes round-trip");

// Hybrid
const bigData = randomBytes(1024);
const env = std.hybridEncrypt(stdKp.pub, bigData);
const decData = std.hybridDecrypt(stdKp.priv, env);
assert(decData.toString() === bigData.toString(), "Standard hybrid encrypt/decrypt round-trip");

// --- Optimized RSA ---
console.log("\n=== Optimized RSA ===");

const optKp = opt.generateKeypair(2048);
const ct2 = opt.encrypt(optKp.pub, msg);
const pt2 = opt.decrypt(optKp.priv, ct2);
assert(pt2 === msg, "Optimized encrypt/decrypt round-trip");

const ctBytes2 = opt.encryptBytes(optKp.pub, msgBytes);
const ptBytes2 = opt.decryptBytes(optKp.priv, ctBytes2);
assert(ptBytes2.toString() === msgBytes.toString(), "Optimized encryptBytes/decryptBytes round-trip");

// KeyCache
const cache = new opt.KeyCache(2048);
const { priv, pub } = cache.get();
const cachedCt = opt.encryptBytes(pub, msgBytes);
const cachedPt = opt.decryptBytes(priv, cachedCt);
assert(cachedPt.toString() === msgBytes.toString(), "KeyCache encrypt/decrypt round-trip");

// Hybrid
const env2 = opt.hybridEncrypt(pub, bigData);
const decData2 = opt.hybridDecrypt(priv, env2);
assert(decData2.toString() === bigData.toString(), "Optimized hybrid encrypt/decrypt round-trip");

// Batch
const msgs = [Buffer.from("msg1"), Buffer.from("msg2"), Buffer.from("msg3")];
const batchCt = opt.batchEncrypt(pub, msgs);
const batchPt = opt.batchDecrypt(priv, batchCt);
assert(
  batchPt.every((p, i) => p.toString() === msgs[i].toString()),
  "Batch encrypt/decrypt round-trip",
);

// Montgomery
const montCtx = new opt.MontgomeryContext(104729n);
const a = 12345n;
const b = 67890n;
const montResult = montCtx.fromMont(montCtx.mul(montCtx.toMont(a), montCtx.toMont(b)));
assert(montResult === (a * b) % 104729n, "Montgomery multiplication correctness");

// Sliding window no Mont
const swResult = opt.slidingWindowNoMont(7n, 13n, 100n);
assert(swResult === 7n ** 13n % 100n, "Sliding window (no Montgomery) correctness");

// --- Summary ---
console.log(`\n${"=".repeat(40)}`);
console.log(`Results: ${passed} passed, ${failed} failed`);
if (failed > 0) process.exit(1);
