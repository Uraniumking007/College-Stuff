function gcdIterative9(a: number, b: number): number {
    a = Math.abs(a)
    b = Math.abs(b)

    while (b !== 0) {
        ;[a, b] = [b, a % b]
    }

    return a
}

function gcdRecursive9(a: number, b: number): number {
    a = Math.abs(a)
    b = Math.abs(b)

    if (b === 0) {
        return a
    }

    return gcdRecursive9(b, a % b)
}

function extendedGCD9(a: number, b: number): [number, number, number] {
    a = Math.abs(a)
    b = Math.abs(b)

    if (b === 0) {
        return [a, 1, 0]
    }

    const [g, x1, y1] = extendedGCD9(b, a % b)
    const x = y1
    const y = x1 - Math.floor(a / b) * y1

    return [g, x, y]
}

function lcm9(a: number, b: number): number {
    if (a === 0 || b === 0) return 0
    return Math.abs(a * b) / gcdIterative9(a, b)
}

const a9 = 16
const b9 = 12

console.log("EUCLID'S ALGORITHM")
console.log(`\nFinding GCD(${a9}, ${b9})`)

const resultIterative = gcdIterative9(a9, b9)
console.log(`Iterative: GCD(${a9}, ${b9}) = ${resultIterative}`)

const resultRecursive = gcdRecursive9(a9, b9)
console.log(`Recursive: GCD(${a9}, ${b9}) = ${resultRecursive}`)

const [g9, x9, y9] = extendedGCD9(a9, b9)
console.log(`\nExtended GCD(${a9}, ${b9}):`)
console.log(`  GCD = ${g9}`)
console.log(`  Coefficients: x = ${x9}, y = ${y9}`)
console.log(`  Verification: ${a9}(${x9}) + ${b9}(${y9}) = ${a9 * x9 + b9 * y9}`)

const resultLCM = lcm9(a9, b9)
console.log(`\nLCM(${a9}, ${b9}) = ${resultLCM}`)
console.log(`Formula: |${a9} × ${b9}| / GCD(${a9}, ${b9}) = ${Math.abs(a9 * b9)} / ${g9} = ${resultLCM}`)
