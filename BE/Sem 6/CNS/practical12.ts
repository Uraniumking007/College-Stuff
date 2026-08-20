/**
 * GCD (Greatest Common Divisor) calculation functions
 */

/**
 * Calculate GCD using iterative Euclidean algorithm
 * @param a First number
 * @param b Second number
 * @returns Greatest common divisor of a and b
 */
export function gcd_iterative(a: number, b: number): number {
    a = Math.abs(a);
    b = Math.abs(b);
    
    while (b !== 0) {
        const temp = b;
        b = a % b;
        a = temp;
    }
    
    return a;
}

/**
 * Calculate Extended GCD using Euclidean algorithm
 * Returns [gcd, x, y] where ax + by = gcd(a, b)
 * @param a First number
 * @param b Second number
 * @returns [gcd, x, y]
 */
export function extended_gcd(a: number, b: number): [number, number, number] {
    a = Math.abs(a);
    b = Math.abs(b);
    
    let x = 0, y = 1;
    let u = 1, v = 0;
    
    while (a !== 0) {
        const q = Math.floor(b / a);
        const r = b % a;
        
        const m = x - u * q;
        const n = y - v * q;
        
        b = a;
        a = r;
        
        x = u;
        y = v;
        u = m;
        v = n;
    }
    
    return [b, x, y];
}

/**
 * Calculate Least Common Multiple (LCM) of two numbers
 * @param a First number
 * @param b Second number
 * @returns LCM of a and b
 */
export function lcm(a: number, b: number): number {
    if (a === 0 || b === 0) {
        return 0;
    }
    
    return Math.abs(a * b) / gcd_iterative(a, b);
}

// Test cases
console.log('GCD(48, 18) =', gcd_iterative(48, 18)); // 6
console.log('GCD(101, 103) =', gcd_iterative(101, 103)); // 1

const [gcd, x, y] = extended_gcd(48, 18);
console.log('Extended GCD(48, 18) =', gcd, x, y); // 6, -1, 3

console.log('LCM(4, 6) =', lcm(4, 6)); // 12
console.log('LCM(21, 6) =', lcm(21, 6)); // 42