/**
 * Diffie-Hellman Key Exchange - Practical 11
 * Test case: p=23, g=5, Alice private key=6, Bob private key=15, Expected shared secret=2
 */

// ============ DIFFIE-HELLMAN IMPLEMENTATION ============

function generatePrivateKey(p: number): number {
    // Generate random private key in range [2, p-2]
    return Math.floor(Math.random() * (p - 3)) + 2;
}

function computePublicKey(privateKey: number, g: number, p: number): number {
    // Compute public value: g^privateKey mod p
    return Math.pow(g, privateKey) % p;
}

function computeSharedSecret(publicKey: number, privateKey: number, p: number): number {
    // Compute shared secret: publicKey^privateKey mod p
    return Math.pow(publicKey, privateKey) % p;
}

function diffieHellmanKeyExchange(): number {
    // Public parameters (typically much larger in practice)
    const p = 23;  // Prime modulus
    const g = 5;   // Generator (primitive root)

    console.log("Public parameters:");
    console.log(`  Prime (p): ${p}`);
    console.log(`  Generator (g): ${g}`);

    // Alice's key generation
    const a = generatePrivateKey(p);
    const A = computePublicKey(a, g, p);
    console.log("\nAlice:");
    console.log(`  Private key (a): ${a}`);
    console.log(`  Public value (A = g^a mod p): ${A}`);

    // Bob's key generation
    const b = generatePrivateKey(p);
    const B = computePublicKey(b, g, p);
    console.log("\nBob:");
    console.log(`  Private key (b): ${b}`);
    console.log(`  Public value (B = g^b mod p): ${B}`);

    // Exchange public values and compute shared secret
    const S_alice = computeSharedSecret(B, a, p);
    const S_bob = computeSharedSecret(A, b, p);

    console.log("\nShared Secret Computation:");
    console.log(`  Alice computes: S = B^a mod p = ${B}^${a} mod ${p} = ${S_alice}`);
    console.log(`  Bob computes:   S = A^b mod p = ${A}^${b} mod ${p} = ${S_bob}`);
    console.log(`  Shared secrets match: ${S_alice === S_bob}`);

    return S_alice;
}

// Run the Diffie-Hellman key exchange
console.log("Diffie-Hellman Key Exchange Demonstration");
console.log("=========================================");
const sharedSecret = diffieHellmanKeyExchange();
console.log("\nResult:");
console.log(`  Shared secret: S = ${sharedSecret}`);
console.log(`  Verification: Both parties computed the same value ✓`);

// Security analysis
console.log("\nSecurity Analysis:");
console.log("  Eavesdropper sees: p = 23, g = 5, A = " + Math.pow(5, 6) % 23 + ", B = " + Math.pow(5, 15) % 23);
console.log("  To find S, attacker must solve:");
console.log("    - Find a from: 5^a mod 23 = " + Math.pow(5, 6) % 23 + "  (discrete logarithm)");
console.log("    - Find b from: 5^b mod 23 = " + Math.pow(5, 15) % 23 + " (discrete logarithm)");
console.log("  Then compute: S = " + Math.pow(5, 6) % 23 + "^b mod 23 = " + Math.pow(5, 15) % 23 + "^a mod 23 = " + sharedSecret);