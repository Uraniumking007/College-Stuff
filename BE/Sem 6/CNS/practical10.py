"""
Euler's Totient Function - Practical 10
φ(n) = number of positive integers less than n that are relatively prime to n
"""

import math


def gcd(a, b):
    """Compute GCD using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a


def totient_naive(n):
    """
    Naive implementation: count numbers coprime to n.
    Time complexity: O(n log n)
    """
    if n <= 0:
        return 0
    count = 0
    for k in range(1, n):
        if gcd(n, k) == 1:
            count += 1
    return count


def totient_efficient(n):
    """
    Efficient implementation using prime factorization.
    Formula: φ(n) = n × Π(1 - 1/p) for all distinct prime factors p of n
    Time complexity: O(√n)
    """
    if n <= 0:
        return 0
    
    result = n
    original = n
    
    # Check for factor 2
    if n % 2 == 0:
        result -= result // 2
        while n % 2 == 0:
            n //= 2
    
    # Check for odd factors
    p = 3
    while p * p <= n:
        if n % p == 0:
            result -= result // p
            while n % p == 0:
                n //= p
        p += 2
    
    # If n is a prime > 2
    if n > 1:
        result -= result // n
    
    return result


def find_coprime_numbers(n):
    """List all numbers less than n that are coprime to n."""
    return [k for k in range(1, n) if gcd(n, k) == 1]


def analyze_totient(n):
    """Analyze and display totient function behavior for a number."""
    print(f"\n{'='*60}")
    print(f"Analysis for n = {n}")
    print(f"{'='*60}")
    
    # Check if prime
    is_prime = n > 1 and all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))
    print(f"Is {n} prime? {is_prime}")
    
    # Prime factorization
    factors = []
    temp = n
    for i in range(2, int(math.sqrt(n)) + 1):
        while temp % i == 0:
            factors.append(i)
            temp //= i
    if temp > 1:
        factors.append(temp)
    
    if factors:
        print(f"Prime factorization: {' × '.join(map(str, factors))}")
    else:
        print(f"Prime factorization: {n} is prime")
    
    # Calculate using formula
    coprimes = find_coprime_numbers(n)
    phi_naive = totient_naive(n)
    phi_efficient = totient_efficient(n)
    
    print(f"\nφ({n}) using naive method: {phi_naive}")
    print(f"φ({n}) using efficient method: {phi_efficient}")
    print(f"Numbers coprime to {n}: {coprimes}")
    print(f"Count: {len(coprimes)}")


def main():
    print("Euler's Totient Function φ(n)")
    print("φ(n) = count of integers k where 1 ≤ k < n and gcd(n, k) = 1")
    
    # Compute for 35 and 37
    for n in [35, 37]:
        analyze_totient(n)
    
    # Additional observations
    print(f"\n{'='*60}")
    print("BEHAVIOR ANALYSIS")
    print(f"{'='*60}")
    
    print("\nKey Properties Observed:")
    print("1. For a prime p: φ(p) = p - 1")
    print("   → Example: φ(37) = 36 (all numbers 1 to 36 are coprime)")
    
    print("\n2. For distinct primes p, q: φ(p × q) = (p-1)(q-1)")
    print("   → Example: φ(35) = φ(5×7) = 4 × 6 = 24")
    
    print("\n3. General formula: φ(n) = n × Π(1 - 1/p) for distinct primes p|n")
    print("   → φ(35) = 35 × (1-1/5) × (1-1/7) = 35 × 4/5 × 6/7 = 24")
    print("   → φ(37) = 37 × (1-1/37) = 36")
    
    print("\n4. φ(n) < n for all n > 1")
    print(f"   → φ(35) = 24 < 35")
    print(f"   → φ(37) = 36 < 37")
    
    print("\n5. φ(n) is maximized when n is prime")
    print("   → For prime p: φ(p) = p - 1 (maximum possible)")
    
    # Show range of totient values
    print(f"\n{'='*60}")
    print("Totient Values for n = 1 to 20")
    print(f"{'='*60}")
    print("n  | φ(n) | Type")
    print("-" * 30)
    for i in range(1, 21):
        phi = totient_efficient(i)
        is_prime = i > 1 and all(i % j != 0 for j in range(2, int(math.sqrt(i)) + 1))
        p_type = "PRIME" if is_prime else ("1" if i == 1 else "Composite")
        print(f"{i:2d} | {phi:4d} | {p_type}")


if __name__ == "__main__":
    main()
