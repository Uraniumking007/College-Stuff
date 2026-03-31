"""
Euclid's Algorithm for Finding GCD
===================================

Implementation of Euclidean algorithm to compute the Greatest Common Divisor (GCD)
of two integers.

Theorem: GCD(a, b) = GCD(b, a mod b)
Base case: GCD(a, 0) = a

Example: GCD(16, 12)
    GCD(16, 12) = GCD(12, 16 mod 12) = GCD(12, 4)
    GCD(12, 4)  = GCD(4, 12 mod 4)  = GCD(4, 0)
    GCD(4, 0)   = 4
    
    Therefore: GCD(16, 12) = 4
"""

def gcd_iterative(a: int, b: int) -> int:
    """
    Find GCD using Euclid's algorithm (iterative approach).
    
    Args:
        a: First integer (non-negative)
        b: Second integer (non-negative)
    
    Returns:
        GCD of a and b
    
    Time Complexity: O(log(min(a, b)))
    Space Complexity: O(1)
    
    Example:
        >>> gcd_iterative(16, 12)
        4
    """
    # Ensure non-negative inputs
    a, b = abs(a), abs(b)
    
    while b != 0:
        print(f"  GCD({a}, {b}) = GCD({b}, {a} mod {b} = {a % b})")
        a, b = b, a % b
    
    print(f"  GCD({a}, 0) = {a}")
    return a


def gcd_recursive(a: int, b: int, depth: int = 0) -> int:
    """
    Find GCD using Euclid's algorithm (recursive approach).
    
    Args:
        a: First integer (non-negative)
        b: Second integer (non-negative)
        depth: Recursion depth for indentation
    
    Returns:
        GCD of a and b
    
    Time Complexity: O(log(min(a, b)))
    Space Complexity: O(log(min(a, b))) due to recursion stack
    
    Example:
        >>> gcd_recursive(16, 12)
        4
    """
    # Ensure non-negative inputs
    a, b = abs(a), abs(b)
    
    indent = "  " * depth
    
    if b == 0:
        print(f"{indent}GCD({a}, 0) = {a}")
        return a
    
    print(f"{indent}GCD({a}, {b}) = GCD({b}, {a} mod {b} = {a % b})")
    return gcd_recursive(b, a % b, depth + 1)


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm.
    
    Finds GCD(a, b) AND integers x, y such that: ax + by = GCD(a, b)
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        Tuple (g, x, y) where g = GCD(a, b) and ax + by = g
    
    Time Complexity: O(log(min(a, b)))
    Space Complexity: O(log(min(a, b))) due to recursion
    
    Applications:
        - Finding modular multiplicative inverse
        - Solving linear Diophantine equations
        - RSA key generation
    
    Example:
        >>> extended_gcd(16, 12)
        (4, 1, -1)  # 16(1) + 12(-1) = 4
    """
    # Ensure non-negative inputs
    a, b = abs(a), abs(b)
    
    if b == 0:
        return a, 1, 0
    
    # Recursive call
    g, x1, y1 = extended_gcd(b, a % b)
    
    # Update x and y using results of recursive call
    x = y1
    y = x1 - (a // b) * y1
    
    return g, x, y


def extended_gcd_iterative(a: int, b: int) -> tuple[int, int, int]:
    """
    Extended Euclidean Algorithm (iterative approach).
    
    Finds GCD(a, b) AND integers x, y such that: ax + by = GCD(a, b)
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        Tuple (g, x, y) where g = GCD(a, b) and ax + by = g
    
    Example:
        >>> extended_gcd_iterative(16, 12)
        (4, 1, -1)  # 16(1) + 12(-1) = 4
    """
    # Ensure non-negative inputs
    a, b = abs(a), abs(b)
    
    # Initialize
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    
    # old_r = GCD, old_s and old_t are coefficients
    return old_r, old_s, old_t


def gcd_multiple(*numbers: int) -> int:
    """
    Find GCD of multiple numbers using Euclid's algorithm.
    
    Uses the property: GCD(a, b, c) = GCD(GCD(a, b), c)
    
    Args:
        *numbers: Variable number of integers
    
    Returns:
        GCD of all input numbers
    
    Example:
        >>> gcd_multiple(48, 36, 24)
        12
    """
    if not numbers:
        raise ValueError("At least one number is required")
    
    result = abs(numbers[0])
    for num in numbers[1:]:
        result = gcd_iterative_quiet(result, abs(num))
    
    return result


def gcd_iterative_quiet(a: int, b: int) -> int:
    """Helper function: GCD without printing steps."""
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """
    Find Least Common Multiple (LCM) using GCD.
    
    Formula: LCM(a, b) = |a × b| / GCD(a, b)
    
    Args:
        a: First integer
        b: Second integer
    
    Returns:
        LCM of a and b
    
    Example:
        >>> lcm(12, 18)
        36
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd_iterative_quiet(a, b)


def verify_example():
    """Verify the given example: GCD(16, 12) = 4"""
    print("=" * 70)
    print("VERIFICATION OF GIVEN EXAMPLE")
    print("=" * 70)
    print("\nExample: Find GCD(16, 12)")
    print("-" * 70)
    
    a, b = 16, 12
    
    print("\nMethod 1: Iterative Approach")
    print("  Steps:")
    result = gcd_iterative(a, b)
    
    print(f"\n  Result: GCD({16}, {12}) = {result}")
    
    print("\n" + "-" * 70)
    print("\nMethod 2: Recursive Approach")
    print("  Steps:")
    result_rec = gcd_recursive(a, b)
    
    print(f"\n  Result: GCD({16}, {12}) = {result_rec}")
    
    print("\n" + "-" * 70)
    print(f"\n✓ VERIFIED: GCD(16, 12) = {result}")
    
    return result


def demonstration():
    """Demonstrate various GCD calculations"""
    print("\n" + "=" * 70)
    print("ADDITIONAL EXAMPLES")
    print("=" * 70)
    
    examples = [
        (12, 4),
        (48, 18),
        (1071, 462),
        (0, 5),
        (17, 0),
        (0, 0)
    ]
    
    for a, b in examples:
        print(f"\nExample: GCD({a}, {b})")
        print("-" * 40)
        result = gcd_iterative_quiet(a, b)
        print(f"Result: GCD({a}, {b}) = {result}")
    
    # Demonstrate GCD of multiple numbers
    print("\n" + "=" * 70)
    print("GCD OF MULTIPLE NUMBERS")
    print("=" * 70)
    
    print("\nExample: GCD(48, 36, 24, 12)")
    result = gcd_multiple(48, 36, 24, 12)
    print(f"Result: {result}")
    
    # Demonstrate LCM
    print("\n" + "=" * 70)
    print("LEAST COMMON MULTIPLE (LCM)")
    print("=" * 70)
    
    print("\nExample: LCM(12, 18)")
    result_lcm = lcm(12, 18)
    print(f"Formula: LCM(12, 18) = |12 × 18| / GCD(12, 18)")
    print(f"        LCM(12, 18) = 216 / {gcd_iterative_quiet(12, 18)}")
    print(f"Result: LCM(12, 18) = {result_lcm}")


def extended_gcd_demo():
    """Demonstrate Extended Euclidean Algorithm"""
    print("\n" + "=" * 70)
    print("EXTENDED EUCLIDEAN ALGORITHM")
    print("=" * 70)
    
    print("""
The Extended Euclidean Algorithm finds:
1. GCD(a, b)
2. Coefficients x, y such that: ax + by = GCD(a, b)

Applications:
- Finding modular multiplicative inverse
- Solving linear Diophantine equations
- RSA encryption/decryption
    """)
    
    examples = [
        (16, 12),
        (48, 18),
        (240, 46),
        (35, 15)
    ]
    
    for a, b in examples:
        print(f"\nExample: extended_gcd({a}, {b})")
        print("-" * 40)
        g, x, y = extended_gcd(a, b)
        print(f"GCD: {g}")
        print(f"Coefficients: x = {x}, y = {y}")
        print(f"Verification: {a}({x}) + {b}({y}) = {a*x} + {b*y} = {a*x + b*y}")
        
        if g != 0:
            # Modular inverse demonstration (when coprime)
            if g == 1:
                print(f"  → Modular inverse of {b} mod {a}: {y % a}")
                print(f"  Verification: {b} × {y % a} mod {a} = {(b * (y % a)) % a}")


def analysis():
    """Provide analysis of Euclid's algorithm"""
    print("\n" + "=" * 70)
    print("ALGORITHM ANALYSIS")
    print("=" * 70)
    
    print("""
1. TIME COMPLEXITY ANALYSIS
   --------------------------
   Euclidean Algorithm: O(log(min(a, b)))
   
   Worst Case: Consecutive Fibonacci numbers
   - F(n+1), F(n) requires maximum number of steps
   - Number of steps ≈ 5 × log10(min(a, b))
   
   Example:
   - GCD(1597, 987) = 1  # 15 steps
   - GCD(832040, 514229) = 1  # 30 steps
   
   This is exponentially faster than naive factorization:
   - Naive: O(√n) for factoring each number
   - Euclid: O(log n) for finding GCD directly


2. SPACE COMPLEXITY ANALYSIS
   ---------------------------
   Iterative: O(1)
   - Only stores current remainder
   - Constant memory regardless of input size
   
   Recursive: O(log(min(a, b)))
   - Stack depth equals number of recursive calls
   - Each call stores new variables


3. CORRECTNESS PROOF
   ------------------
   Theorem: GCD(a, b) = GCD(b, a mod b)
   
   Proof:
   Let d = GCD(a, b). We need to show d = GCD(b, a mod b)
   
   Step 1: d divides both a and b
       → a = d × m, b = d × n  (for integers m, n)
   
   Step 2: a mod b = a - ⌊a/b⌋ × b
       → a mod b = d × m - ⌊a/b⌋ × d × n
       → a mod b = d × (m - ⌊a/b⌋ × n)
       → Therefore, d divides (a mod b)
   
   Step 3: Since d divides b and (a mod b)
       → d is a common divisor of (b, a mod b)
       → d ≤ GCD(b, a mod b)
   
   Step 4: Conversely, let c = GCD(b, a mod b)
       → c divides b and (a mod b)
       → c divides a = b × ⌊a/b⌋ + (a mod b)
       → c divides both a and b
       → c ≤ GCD(a, b) = d
   
   Conclusion: d = c  ∎


4. LAMÉ'S THEOREM
   ---------------
   The number of steps in Euclid's algorithm is at most
   5 times the number of digits in the smaller number.
   
   Specifically: For a > b ≥ 1, the number of divisions
   is at most 5 × log₁₀(b)


5. COMPARISON WITH OTHER METHODS
   -------------------------------
   
   Method 1: Prime Factorization
   - Find all prime factors of both numbers
   - Take common factors with minimum exponents
   - Complexity: O(√n) for factoring
   - Slower than Euclid for large numbers
   
   Method 2: Binary GCD Algorithm (Stein's Algorithm)
   - Uses only subtraction and bit operations
   - Avoids expensive division/modulo operations
   - Useful for computer implementations
   - Same asymptotic complexity: O(log n)
   
   Method 3: Euclidean Algorithm
   - Simple and efficient
   - Optimal for most practical purposes
   - Foundation for extended GCD applications


6. PRACTICAL APPLICATIONS
   ------------------------
   
   a) Cryptography:
      - RSA: Finding modular inverses
      - Public/Private key generation
      - Key exchange protocols
   
   b) Number Theory:
      - Solving Diophantine equations
      - Finding modular arithmetic solutions
      - Proving divisibility properties
   
   c) Computer Science:
      - Simplifying fractions
      - Hash function design
      - Random number generation
      - Computer graphics (pixel ratios)
   
   d) Real-World:
      - Gear ratio optimization
      - Time calculations
      - Scheduling problems
      - Pattern matching
    """)


if __name__ == "__main__":
    # Verify the given example
    verify_example()
    
    # Additional demonstrations
    demonstration()
    
    # Extended Euclidean Algorithm
    extended_gcd_demo()
    
    # Algorithm analysis
    analysis()
    
    print("\n" + "=" * 70)
    print("IMPLEMENTATION COMPLETE")
    print("=" * 70)
    print("\nSummary:")
    print("  ✓ Euclidean Algorithm (Iterative & Recursive)")
    print("  ✓ Extended Euclidean Algorithm")
    print("  ✓ GCD of multiple numbers")
    print("  ✓ Least Common Multiple (LCM)")
    print("  ✓ Comprehensive analysis and demonstrations")
    print("=" * 70)
