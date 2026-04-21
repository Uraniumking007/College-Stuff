function gcd(a: number, b: number): number {
    while (b !== 0) {
        const temp = b
        b = a % b
        a = temp
    }
    return a
}

function isRelativelyPrime(a: number, b: number): boolean {
    return gcd(a, b) === 1
}

function eulerTotient(n: number): number {
    let count = 0
    for (let i = 1; i < n; i++) {
        if (isRelativelyPrime(i, n)) {
            count++
        }
    }
    return count
}

function displayTotientInfo(n: number): void {
    const phi = eulerTotient(n)
    const relativelyPrimes: number[] = []
    
    for (let i = 1; i < n; i++) {
        if (isRelativelyPrime(i, n)) {
            relativelyPrimes.push(i)
        }
    }
    
    console.log(`φ(${n}) = ${phi}`)
    console.log(`  Numbers relatively prime to ${n}: [${relativelyPrimes.join(", ")}]`)
}

console.log("=== Euler's Totient Function ===\n")

displayTotientInfo(35)
console.log()
displayTotientInfo(37)

console.log("\n=== Observations ===")
console.log("For n = 35 (composite: 5 × 7):")
console.log("  φ(35) = 24")
console.log("  Formula: φ(35) = 35 × (1 - 1/5) × (1 - 1/7) = 35 × 4/5 × 6/7 = 24 ✓")

console.log("\nFor n = 37 (prime):")
console.log("  φ(37) = 36")
console.log("  Formula: φ(p) = p - 1 for prime p = 37 - 1 = 36 ✓")

console.log("\n=== Key Behavior ===")
console.log("1. For prime p: φ(p) = p - 1")
console.log("2. For composite n: φ(n) < n - 1")
console.log("3. Multiplicative: φ(ab) = φ(a) × φ(b) when gcd(a,b) = 1")
