function gcd10(a: number, b: number): number {
    while (b !== 0) {
        ;[a, b] = [b, a % b]
    }
    return Math.abs(a)
}

function totientNaive10(n: number): number {
    if (n <= 0) return 0

    let count = 0
    for (let k = 1; k < n; k++) {
        if (gcd10(n, k) === 1) count++
    }
    return count
}

function totientEfficient10(n: number): number {
    if (n <= 0) return 0

    let result = n
    let original = n

    if (n % 2 === 0) {
        result -= Math.floor(result / 2)
        while (n % 2 === 0) {
            n = Math.floor(n / 2)
        }
    }

    for (let p = 3; p * p <= n; p += 2) {
        if (n % p === 0) {
            result -= Math.floor(result / p)
            while (n % p === 0) {
                n = Math.floor(n / p)
            }
        }
    }

    if (n > 1) {
        result -= Math.floor(result / n)
    }

    return result
}

const testNumbers = [35, 37]

console.log("EULER'S TOTIENT FUNCTION φ(n)")
console.log("φ(n) = count of integers k where 1 ≤ k < n and gcd(n, k) = 1\n")

for (const n of testNumbers) {
    console.log(`n = ${n}`)
    const phiNaive = totientNaive10(n)
    const phiEfficient = totientEfficient10(n)
    console.log(`φ(${n}) = ${phiEfficient}`)

    if (phiNaive === phiEfficient) {
        console.log(`✓ Verified: Both methods give same result`)
    } else {
        console.log(`✗ Mismatch: Naive=${phiNaive}, Efficient=${phiEfficient}`)
    }
    console.log()
}
