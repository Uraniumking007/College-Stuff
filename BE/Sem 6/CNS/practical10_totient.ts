// Euler's Totient Function - Practical 10
// φ(n) = number of positive integers less than n that are relatively prime to n

function gcd(a: number, b: number): number {
    while (b) {
        [a, b] = [b, a % b];
    }
    return a;
}

function totient_efficient(n: number): number {
    if (n <= 0) return 0;
    
    let result = n;
    let original = n;
    
    // Check for factor 2
    if (n % 2 === 0) {
        result -= result / 2;
        while (n % 2 === 0) {
            n /= 2;
        }
    }
    
    // Check for odd factors
    let p = 3;
    while (p * p <= n) {
        if (n % p === 0) {
            result -= result / p;
            while (n % p === 0) {
                n /= p;
            }
        }
        p += 2;
    }
    
    // If n is a prime > 2
    if (n > 1) {
        result -= result / n;
    }
    
    return result;
}

function find_coprime_numbers(n: number): number[] {
    const coprimes: number[] = [];
    for (let k = 1; k < n; k++) {
        if (gcd(n, k) === 1) {
            coprimes.push(k);
        }
    }
    return coprimes;
}

// Example usage
console.log("Euler's Totient Function φ(n)");
console.log("φ(n) = count of integers k where 1 ≤ k < n and gcd(n, k) = 1");

// Test with 35 and 37
for (const n of [35, 37]) {
    console.log(`\nAnalysis for n = ${n}`);
    console.log(`φ(${n}) = ${totient_efficient(n)}`);
    console.log(`Numbers coprime to ${n}:`, find_coprime_numbers(n));
}