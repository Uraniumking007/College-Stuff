function modExp8(base: bigint, exp: bigint, mod: bigint): bigint {
    let result = 1n
    base = base % mod
    while (exp > 0n) {
        if (exp % 2n === 1n) result = (result * base) % mod
        exp = exp / 2n
        base = (base * base) % mod
    }
    return result
}

function gcd8(a: bigint, b: bigint): bigint {
    while (b !== 0n) {
        const temp = b
        b = a % b
        a = temp
    }
    return a
}

function extendedGcd8(
    a: bigint,
    b: bigint
): [bigint, bigint, bigint] {
    if (a === 0n) return [b, 0n, 1n]
    const [g, x1, y1] = extendedGcd8(b % a, a)
    const x = y1 - (b / a) * x1
    const y = x1
    return [g, x, y]
}

function modInverse8(a: bigint, m: bigint): bigint | null {
    const [g, x] = extendedGcd8(a, m)
    if (g !== 1n) return null
    return ((x % m) + m) % m
}

function generateRSAKeyPair8(p: bigint, q: bigint, e: bigint) {
    const n = p * q
    const phi = (p - 1n) * (q - 1n)
    const d = modInverse8(e, phi)

    return {
        publicKey: { n, e },
        privateKey: { n, d },
        phi
    }
}

function rsaEncrypt8(M: bigint, publicKey: { n: bigint; e: bigint }): bigint {
    return modExp8(M, publicKey.e, publicKey.n)
}

function rsaDecrypt8(C: bigint, privateKey: { n: bigint; d: bigint }): bigint {
    return modExp8(C, privateKey.d, privateKey.n)
}

console.log('RSA ALGORITHM - PRACTICAL 8')

const p8 = 17n
const q8 = 11n
const e8 = 7n
const M8 = 88n
const expectedD8 = 23n
const expectedC8 = 11n

console.log('\n--- Test Case Parameters ---')
console.log('Prime p = ' + p8)
console.log('Prime q = ' + q8)
console.log('Encryption key e = ' + e8)
console.log('Plaintext M = ' + M8)

console.log('\n--- Key Generation ---')
const keyPair8 = generateRSAKeyPair8(p8, q8, e8)
console.log('n = p × q = ' + keyPair8.publicKey.n)
console.log('φ(n) = (p-1) × (q-1) = ' + keyPair8.phi)
console.log('e = ' + keyPair8.publicKey.e)

if (keyPair8.privateKey.d !== null) {
    console.log('d = ' + keyPair8.privateKey.d)
    console.log('Verification: d × e mod φ(n) = ' + ((keyPair8.privateKey.d * keyPair8.publicKey.e) % keyPair8.phi))

    console.log('\n--- Verification ---')
    if (keyPair8.privateKey.d === expectedD8) {
        console.log('✓ Decryption key verified: d = ' + keyPair8.privateKey.d)
    } else {
        console.log('✗ Decryption key mismatch: expected ' + expectedD8 + ', got ' + keyPair8.privateKey.d)
    }

    console.log('\n--- Encryption ---')
    const C8 = rsaEncrypt8(M8, keyPair8.publicKey)
    console.log('C = M^e mod n')
    console.log('C = ' + M8 + '^' + keyPair8.publicKey.e + ' mod ' + keyPair8.publicKey.n)
    console.log('C = ' + C8)

    if (C8 === expectedC8) {
        console.log('✓ Ciphertext verified: C = ' + C8)
    } else {
        console.log('✗ Ciphertext mismatch: expected ' + expectedC8 + ', got ' + C8)
    }

    console.log('\n--- Decryption ---')
    const privateKeyNonNull = { n: keyPair8.privateKey.n, d: keyPair8.privateKey.d }
    const decryptedM8 = rsaDecrypt8(C8, privateKeyNonNull)
    console.log('M = C^d mod n')
    console.log('M = ' + C8 + '^' + privateKeyNonNull.d + ' mod ' + privateKeyNonNull.n)
    console.log('M = ' + decryptedM8)

    if (decryptedM8 === M8) {
        console.log('✓ Decryption verified: M = ' + decryptedM8)
    } else {
        console.log('✗ Decryption failed: expected ' + M8 + ', got ' + decryptedM8)
    }

    console.log('\nSUMMARY')
    console.log('Test case: ' + (C8 === expectedC8 && decryptedM8 === M8 ? 'PASSED ✓' : 'FAILED ✗'))
    console.log('All verifications: ' + (keyPair8.privateKey.d === expectedD8 && C8 === expectedC8 && decryptedM8 === M8 ? 'PASSED ✓' : 'FAILED ✗'))
} else {
    console.log('✗ Failed to generate valid decryption key')
}
