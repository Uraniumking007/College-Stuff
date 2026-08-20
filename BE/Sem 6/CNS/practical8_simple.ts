/**
 * RSA Algorithm Implementation - Test Case Only
 */

function modExp(base: bigint, exp: bigint, mod: bigint): bigint {
  let result = 1n
  base = base % mod
  while (exp > 0n) {
    if (exp % 2n === 1n) result = (result * base) % mod
    exp = exp / 2n
    base = (base * base) % mod
  }
  return result
}

function gcd(a: bigint, b: bigint): bigint {
  while (b !== 0n) { [a, b] = [b, a % b] }
  return a
}

function extendedGcd(a: bigint, b: bigint): [bigint, bigint, bigint] {
  if (a === 0n) return [b, 0n, 1n]
  const [g, x1, y1] = extendedGcd(b % a, a)
  return [g, y1 - (b / a) * x1, x1]
}

function modInverse(a: bigint, m: bigint): bigint | null {
  const [g, x] = extendedGcd(a, m)
  return g !== 1n ? null : ((x % m) + m) % m
}

// Test Case
const p = 17n, q = 11n, e = 7n, M = 88n
const n = p * q
const phi = (p - 1n) * (q - 1n)
const d = modInverse(e, phi)!
const C = modExp(M, e, n)
const decryptedM = modExp(C, d, n)

console.log("RSA Algorithm Test Case")
console.log("======================")
console.log(\`p = \${p}, q = \${q}\`)
console.log(\`n = p × q = \${n}\`)
console.log(\`φ(n) = (p-1) × (q-1) = \${phi}\`)
console.log(\`e = \${e}\`)
console.log(\`d = \${d}\`)
console.log(\`Verification: d × e mod φ(n) = \${(d * e) % phi}\`)
console.log(\`M = \${M}\`)
console.log(\`C = M^e mod n = \${C}\`)
console.log(\`M (decrypted) = C^d mod n = \${decryptedM}\`)

if (C === 11n && decryptedM === M) {
  console.log("\n✓ Test case PASSED")
} else {
  console.log("\n✗ Test case FAILED")
}
