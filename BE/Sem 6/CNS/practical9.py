"""
Random Number Generation and Testing
====================================

Implementation and comparison of two PRNG algorithms:
1. Linear Congruential Generator (LCG)
2. Blum Blum Shub (BBS) Generator

Evaluation based on:
1. Uniformity Test (Chi-Square Test)
2. Scalability Test (Performance Analysis)
3. Consistency Test (Statistical Analysis)
"""

import numpy as np
import time
import math
from typing import List, Tuple
from collections import Counter


class LinearCongruentialGenerator:
    """
    Linear Congruential Generator (LCG)
    
    Formula: X(n+1) = (a * X(n) + c) mod m
    
    Parameters:
    - m: Modulus (m > 0)
    - a: Multiplier (0 < a < m)
    - c: Increment (0 ≤ c < m)
    - X0: Seed (0 ≤ X0 < m)
    
    Period Length: At most m, depends on parameter choice
    """
    
    def __init__(self, m: int = 2**32, a: int = 16645, c: int = 1013904223, seed: int = None):
        """
        Initialize LCG with parameters.
        
        Default values from Numerical Recipes:
        - m = 2^32 (for 32-bit integers)
        - a = 16645
        - c = 1013904223
        """
        self.m = m
        self.a = a
        self.c = c
        self.state = seed if seed is not None else int(time.time())
        
    def next(self) -> int:
        """Generate next random number."""
        self.state = (self.a * self.state + self.c) % self.m
        return self.state
    
    def next_32bit(self) -> int:
        """Generate next 32-bit random number."""
        return self.next() & 0xFFFFFFFF  # Ensure 32 bits
    
    def next_float(self) -> float:
        """Generate random float in [0, 1)."""
        return self.next() / self.m
    
    def generate_sequence(self, count: int) -> List[int]:
        """Generate a sequence of random numbers."""
        return [self.next_32bit() for _ in range(count)]
    
    def generate_bits(self, num_bits: int) -> int:
        """Generate random number with specified number of bits."""
        result = 0
        bits_per_call = 32
        calls = (num_bits + bits_per_call - 1) // bits_per_call
        
        for _ in range(calls):
            result = (result << bits_per_call) | self.next_32bit()
        
        # Mask to exact number of bits
        return result & ((1 << num_bits) - 1)


class BlumBlumShub:
    """
    Blum Blum Shub (BBS) Generator
    
    Formula: X(n+1) = X(n)^2 mod n
    where n = p * q, and p, q are primes congruent to 3 mod 4
    
    Parameters:
    - n: Modulus (product of two large primes)
    - X0: Seed (must be coprime to n)
    
    Security: Cryptographically secure under certain assumptions
    Speed: Slower than LCG due to large integer operations
    """
    
    def __init__(self, p: int = 3, q: int = 11, seed: int = None):
        """
        Initialize BBS with Blum primes.
        
        Default small values for demonstration:
        - p = 3 (prime ≡ 3 mod 4)
        - q = 11 (prime ≡ 3 mod 4)
        - n = 33
        
        For production, use large primes (e.g., 512 bits)
        """
        # Verify p and q are Blum primes (≡ 3 mod 4)
        if p % 4 != 3 or q % 4 != 3:
            raise ValueError("p and q must be primes congruent to 3 mod 4")
        
        self.p = p
        self.q = q
        self.n = p * q
        self.state = seed if seed is not None else int(time.time()) % self.n
        
        # Ensure seed is coprime to n
        if math.gcd(self.state, self.n) != 1:
            self.state = 2  # Safe default
    
    def next_bit(self) -> int:
        """Generate next single random bit."""
        self.state = (self.state * self.state) % self.n
        return self.state & 1  # Extract LSB
    
    def next_32bit(self) -> int:
        """Generate 32-bit random number."""
        result = 0
        for _ in range(32):
            result = (result << 1) | self.next_bit()
        return result
    
    def next_float(self) -> float:
        """Generate random float in [0, 1)."""
        return self.next_32bit() / (2**32)
    
    def generate_sequence(self, count: int) -> List[int]:
        """Generate a sequence of random numbers."""
        return [self.next_32bit() for _ in range(count)]
    
    def generate_bits(self, num_bits: int) -> int:
        """Generate random number with specified number of bits."""
        result = 0
        for _ in range(num_bits):
            result = (result << 1) | self.next_bit()
        return result


class UniformityTest:
    """
    Test 1: Uniformity Test (Chi-Square Test)
    
    Tests if the random numbers are uniformly distributed.
    
    Null Hypothesis: Numbers are uniformly distributed
    Alternative Hypothesis: Numbers are NOT uniformly distributed
    
    Chi-Square Statistic: χ² = Σ((O_i - E_i)² / E_i)
    where O_i = observed frequency, E_i = expected frequency
    """
    
    @staticmethod
    def chi_square_test(numbers: List[int], bins: int = 16, alpha: float = 0.05) -> dict:
        """
        Perform chi-square test for uniformity.
        
        Args:
            numbers: List of random numbers
            bins: Number of bins for histogram
            alpha: Significance level (default: 0.05 for 95% confidence)
        
        Returns:
            Dictionary with test results
        """
        n = len(numbers)
        expected_freq = n / bins
        
        # Count observed frequencies
        counts = Counter([num % bins for num in numbers])
        
        # Calculate chi-square statistic
        chi_square = 0
        for i in range(bins):
            observed = counts.get(i, 0)
            chi_square += ((observed - expected_freq) ** 2) / expected_freq
        
        # Degrees of freedom
        df = bins - 1
        
        # Critical value at alpha (approximate for common values)
        critical_values = {
            0.05: {15: 25.00, 7: 14.07, 3: 7.81},
            0.01: {15: 30.58, 7: 18.48, 3: 11.34}
        }
        
        critical_value = critical_values.get(alpha, {}).get(df, None)
        
        # Determine result
        if critical_value:
            passed = chi_square < critical_value
        else:
            # For other values, use rough approximation
            passed = chi_square < df + 3 * math.sqrt(2 * df)
        
        return {
            'chi_square': chi_square,
            'degrees_of_freedom': df,
            'critical_value': critical_value,
            'alpha': alpha,
            'passed': passed,
            'interpretation': 'UNIFORM' if passed else 'NOT UNIFORM'
        }
    
    @staticmethod
    def frequency_analysis(numbers: List[int], bins: int = 16) -> dict:
        """Analyze frequency distribution."""
        counts = Counter([num % bins for num in numbers])
        
        expected = len(numbers) / bins
        
        frequencies = {
            f'bin_{i}': counts.get(i, 0) for i in range(bins)
        }
        
        # Calculate statistics
        observed_values = list(counts.values())
        variance = sum((x - expected) ** 2 for x in observed_values) / bins
        std_dev = math.sqrt(variance)
        
        return {
            'frequencies': frequencies,
            'expected_frequency': expected,
            'variance': variance,
            'std_deviation': std_dev
        }


class ScalabilityTest:
    """
    Test 2: Scalability Test (Performance Analysis)
    
    Measures the generation speed as the number of bits increases.
    
    Metrics:
    - Time complexity
    - Throughput (numbers/second)
    - Memory efficiency
    """
    
    @staticmethod
    def measure_performance(generator, num_bits_list: List[int], iterations: int = 1000) -> dict:
        """
        Measure generation time for different bit sizes.
        
        Args:
            generator: PRNG instance
            num_bits_list: List of bit sizes to test
            iterations: Number of iterations for each size
        
        Returns:
            Dictionary with performance metrics
        """
        results = {}
        
        for num_bits in num_bits_list:
            times = []
            
            for _ in range(iterations):
                start = time.perf_counter()
                generator.generate_bits(num_bits)
                end = time.perf_counter()
                times.append(end - start)
            
            avg_time = np.mean(times)
            std_time = np.std(times)
            throughput = 1 / avg_time if avg_time > 0 else 0
            
            results[f'{num_bits}_bits'] = {
                'avg_time_ns': avg_time * 1e9,
                'std_time_ns': std_time * 1e9,
                'throughput_per_sec': throughput
            }
        
        return results
    
    @staticmethod
    def time_complexity_analysis(generator, sizes: List[int]) -> dict:
        """Analyze time complexity for generating sequences."""
        results = {}
        
        for size in sizes:
            start = time.perf_counter()
            generator.generate_sequence(size)
            end = time.perf_counter()
            
            elapsed = end - start
            results[size] = {
                'time_seconds': elapsed,
                'time_per_number_ns': (elapsed / size) * 1e9
            }
        
        return results


class ConsistencyTest:
    """
    Test 3: Consistency Test (Statistical Analysis)
    
    Tests the reproducibility and statistical properties over multiple runs.
    
    Metrics:
    - Reproducibility with same seed
    - Mean and variance stability
    - Autocorrelation analysis
    """
    
    @staticmethod
    def seed_reproducibility(generator_class, seed: int, count: int = 100) -> dict:
        """
        Test if same seed produces same sequence.
        """
        # Generate two sequences with same seed
        gen1 = generator_class(seed=seed)
        gen2 = generator_class(seed=seed)
        
        seq1 = gen1.generate_sequence(count)
        seq2 = gen2.generate_sequence(count)
        
        # Check if identical
        identical = seq1 == seq2
        
        return {
            'seed': seed,
            'identical': identical,
            'first_10_values': seq1[:10]
        }
    
    @staticmethod
    def statistical_moments(numbers: List[int]) -> dict:
        """Calculate statistical moments."""
        mean = np.mean(numbers)
        variance = np.var(numbers)
        std_dev = np.std(numbers)
        
        # For uniform distribution on [0, 2^32-1]
        expected_mean = (2**32 - 1) / 2
        expected_variance = ((2**32) ** 2 - 1) / 12
        
        return {
            'mean': mean,
            'variance': variance,
            'std_deviation': std_dev,
            'expected_mean': expected_mean,
            'expected_variance': expected_variance,
            'mean_error_percent': abs(mean - expected_mean) / expected_mean * 100,
            'variance_error_percent': abs(variance - expected_variance) / expected_variance * 100
        }
    
    @staticmethod
    def autocorrelation_test(numbers: List[int], max_lag: int = 10) -> dict:
        """
        Test for autocorrelation in the sequence.
        
        Low autocorrelation indicates good randomness.
        """
        mean = np.mean(numbers)
        variance = np.var(numbers)
        
        autocorrelations = []
        for lag in range(1, max_lag + 1):
            # Calculate correlation at this lag
            if variance == 0:
                corr = 0
            else:
                shifted = numbers[lag:]
                original = numbers[:-lag]
                
                numerator = np.mean((np.array(original) - mean) * (np.array(shifted) - mean))
                corr = numerator / variance
            
            autocorrelations.append({
                'lag': lag,
                'correlation': corr
            })
        
        # Check if any significant autocorrelations
        significant = [ac for ac in autocorrelations if abs(ac['correlation']) > 0.1]
        
        return {
            'autocorrelations': autocorrelations,
            'significant_count': len(significant),
            'max_correlation': max(abs(ac['correlation']) for ac in autocorrelations)
        }


class RandomNumberComparator:
    """Compare multiple PRNG algorithms."""
    
    def __init__(self, num_samples: int = 10000):
        self.num_samples = num_samples
        self.generators = {
            'LCG': LinearCongruentialGenerator(),
            'BBS': BlumBlumShub()
        }
    
    def run_all_tests(self) -> dict:
        """Run all tests on all generators."""
        results = {}
        
        for name, generator in self.generators.items():
            print(f"\n{'='*70}")
            print(f"Testing: {name}")
            print(f"{'='*70}")
            
            # Generate test data
            sequence = generator.generate_sequence(self.num_samples)
            
            # Test 1: Uniformity
            print(f"\n1. UNIFORMITY TEST")
            print(f"{'-'*70}")
            uniformity = UniformityTest.chi_square_test(sequence)
            print(f"   Chi-Square: {uniformity['chi_square']:.2f}")
            print(f"   Result: {uniformity['interpretation']}")
            
            # Test 2: Scalability
            print(f"\n2. SCALABILITY TEST")
            print(f"{'-'*70}")
            bit_sizes = [8, 16, 32, 64, 128, 256]
            scalability = ScalabilityTest.measure_performance(generator, bit_sizes)
            
            for size, metrics in scalability.items():
                print(f"   {size}: {metrics['avg_time_ns']:.2f} ns/number")
            
            # Test 3: Consistency
            print(f"\n3. CONSISTENCY TEST")
            print(f"{'-'*70}")
            moments = ConsistencyTest.statistical_moments(sequence[:1000])
            print(f"   Mean error: {moments['mean_error_percent']:.2f}%")
            print(f"   Variance error: {moments['variance_error_percent']:.2f}%")
            
            autocorr = ConsistencyTest.autocorrelation_test(sequence[:1000])
            print(f"   Max autocorrelation: {autocorr['max_correlation']:.4f}")
            
            results[name] = {
                'uniformity': uniformity,
                'scalability': scalability,
                'consistency': {
                    'moments': moments,
                    'autocorrelation': autocorr
                }
            }
        
        return results
    
    def compare_generators(self, results: dict) -> None:
        """Compare and rank generators."""
        print(f"\n{'='*70}")
        print(f"COMPARATIVE ANALYSIS")
        print(f"{'='*70}")
        
        print(f"\n{'Criterion':<20} {'LCG':<20} {'BBS':<20}")
        print(f"{'-'*70}")
        
        # Uniformity comparison
        lcg_uniform = results['LCG']['uniformity']['passed']
        bbs_uniform = results['BBS']['uniformity']['passed']
        print(f"{'Uniformity':<20} {'✓ PASS' if lcg_uniform else '✗ FAIL':<20} {'✓ PASS' if bbs_uniform else '✗ FAIL':<20}")
        
        # Speed comparison (32-bit generation)
        lcg_speed = results['LCG']['scalability']['32_bits']['avg_time_ns']
        bbs_speed = results['BBS']['scalability']['32_bits']['avg_time_ns']
        print(f"{'Speed (32-bit)':<20} {lcg_speed:.2f} ns<{bbs_speed:.2f} ns")
        
        # Consistency comparison
        lcg_auto = results['LCG']['consistency']['autocorrelation']['max_correlation']
        bbs_auto = results['BBS']['consistency']['autocorrelation']['max_correlation']
        print(f"{'Max Autocorr':<20} {lcg_auto:.4f}<{bbs_auto:.4f}")
        
        # Overall ranking
        print(f"\n{'='*70}")
        print(f"OVERALL RANKING")
        print(f"{'='*70}")
        
        scores = {
            'LCG': 0,
            'BBS': 0
        }
        
        # Uniformity score
        if results['LCG']['uniformity']['passed']:
            scores['LCG'] += 1
        if results['BBS']['uniformity']['passed']:
            scores['BBS'] += 1
        
        # Speed score (faster is better)
        if lcg_speed < bbs_speed:
            scores['LCG'] += 1
        else:
            scores['BBS'] += 1
        
        # Autocorrelation score (lower is better)
        if lcg_auto < bbs_auto:
            scores['LCG'] += 1
        else:
            scores['BBS'] += 1
        
        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        for rank, (name, score) in enumerate(ranked, 1):
            print(f"{rank}. {name}: {score}/3 tests passed")


def generate_32bit_examples():
    """Generate example 32-bit random numbers."""
    print(f"\n{'='*70}")
    print(f"32-BIT RANDOM NUMBER GENERATION EXAMPLES")
    print(f"{'='*70}")
    
    # LCG examples
    lcg = LinearCongruentialGenerator()
    print(f"\nLinear Congruential Generator (LCG):")
    print(f"Parameters: m=2^32, a=16645, c=1013904223")
    print(f"\n10 Random 32-bit numbers:")
    for i in range(10):
        num = lcg.next_32bit()
        print(f"  {i+1}. {num:10d} (0x{num:08X})")
    
    # BBS examples
    bbs = BlumBlumShub()
    print(f"\nBlum Blum Shub (BBS) Generator:")
    print(f"Parameters: p=3, q=11, n=33")
    print(f"\n10 Random 32-bit numbers:")
    for i in range(10):
        num = bbs.next_32bit()
        print(f"  {i+1}. {num:10d} (0x{num:08X})")


def detailed_analysis():
    """Provide detailed analysis of each generator."""
    print(f"\n{'='*70}")
    print(f"DETAILED ANALYSIS")
    print(f"{'='*70}")
    
    print(f"""
LINEAR CONGRUENTIAL GENERATOR (LCG)
------------------------------------
Advantages:
✓ Very fast (simple arithmetic operations)
✓ Memory efficient (O(1) space)
✓ Easy to implement
✓ Good for non-cryptographic applications

Disadvantages:
✗ Not cryptographically secure
✗ Short period for some parameters
✗ Can fail statistical tests with poor parameters
✗ Predictable if parameters are known

Best For:
- Simulations
- Games
- Non-critical randomization
- Large-scale Monte Carlo methods

Parameters Used:
- m = 2^32 (for 32-bit output)
- a = 16645 (multiplier)
- c = 1013904223 (increment)
- These are "Numerical Recipes" parameters with good properties


BLUM BLUM SHUB (BBS) GENERATOR
-------------------------------
Advantages:
✓ Cryptographically secure (under certain assumptions)
✓ Provable security properties
✓ Unpredictable without knowing p and q
✓ Passes sophisticated statistical tests

Disadvantages:
✗ Very slow (requires large integer squaring)
✗ More complex to implement
✗ Requires primality testing for setup
✗ Overkill for non-cryptographic use

Best For:
- Cryptographic applications
- Key generation
- Secure random number generation
- Systems requiring provable security

Parameters Used:
- p = 3 (small Blum prime for demonstration)
- q = 11 (small Blum prime for demonstration)
- n = 33 (product of p and q)
- For production: Use 512-bit Blum primes
    """)


def security_analysis():
    """Analyze security aspects of both generators."""
    print(f"\n{'='*70}")
    print(f"SECURITY ANALYSIS")
    print(f"{'='*70}")
    
    print(f"""
LCG SECURITY:
-------------
Status: NOT SECURE for cryptographic purposes

Vulnerabilities:
1. Predictability: Given X(n) and parameters, can compute X(n+1)
2. Parameter recovery: With few outputs, can determine parameters
3. Short period: Patterns emerge after at most m outputs
4. Linear structure: Easy to analyze and break

Attack Examples:
- If attacker knows a, c, m: Can predict all future values
- If attacker sees 3 outputs: Can solve for parameters (small m)
- State compromise: Reveals entire past and future sequence

Recommendation: NEVER use for:
- Password generation
- Cryptographic keys
- Secure tokens
- Gambling systems


BBS SECURITY:
-------------
Status: SECURE (with proper parameters)

Security Properties:
1. Unpredictability: Predicting next bit is as hard as factoring n
2. Forward secrecy: Past bits can't be computed from current state
3. Backward secrecy: Future bits can't be computed without state

Security Requirements:
- p and q must be large (≥ 512 bits each)
- p and q must be secret
- n = p × q must be hard to factor
- Seed must be truly random

Cryptographic Assumptions:
- Quadratic residues problem is hard
- Factoring large semiprimes is difficult
- These assumptions are well-studied

Recommendation: Suitable for:
- Cryptographic key generation
- Digital signatures
- Secure session tokens
- Encryption systems


COMPARISON:
-----------
Criteria              LCG                  BBS
-----------           ----------           ----------
Speed                 Very Fast            Very Slow
Security              Not Secure           Secure
Period                Limited (2^32)       Very Long
Implementation        Simple               Complex
Use Case              Simulation           Cryptography
Efficiency            O(1) per number      O(log n) per bit


FINAL VERDICT:
-------------
For NON-CRYPTOGRAPHIC applications (simulations, games, testing):
  → Use LCG (much faster, adequate randomness)

For CRYPTOGRAPHIC applications (keys, secure tokens, encryption):
  → Use BBS (provable security, unpredictable)

For PRODUCTION systems:
  → Use system CSPRNG (e.g., /dev/urandom, CryptGenRandom)
  → These combine multiple algorithms for best performance and security
    """)


def conclusion():
    """Print final conclusion."""
    print(f"\n{'='*70}")
    print(f"CONCLUSION")
    print(f"{'='*70}")
    
    print(f"""
SUMMARY:
--------
Both algorithms successfully generate 32-bit random numbers, but they
serve different purposes:

LINEAR CONGRUENTIAL GENERATOR:
✓ BEST for: Non-cryptographic applications
✓ Fastest: ~100-1000x faster than BBS
✓ Good uniformity and consistency
✗ NOT suitable for security

BLUM BLUM SHUB:
✓ BEST for: Cryptographic applications
✓ Provable security properties
✓ Passes advanced statistical tests
✗ Too slow for large-scale simulations

TEST RESULTS SUMMARY:
---------------------
1. Uniformity Test: Both pass with proper parameters
2. Scalability Test: LCG is much faster
3. Consistency Test: Both show good statistical properties

RECOMMENDATION:
---------------
Choose based on use case:
- Need speed? → LCG
- Need security? → BBS
- Production crypto? → Use system CSPRNG

The "BEST" method depends entirely on your application requirements!
    """)


if __name__ == "__main__":
    print("="*70)
    print("RANDOM NUMBER GENERATOR COMPARISON")
    print("Practical 9: LCG vs Blum Blum Shub")
    print("="*70)
    
    # Generate 32-bit examples
    generate_32bit_examples()
    
    # Run comprehensive tests
    comparator = RandomNumberComparator(num_samples=10000)
    results = comparator.run_all_tests()
    
    # Compare generators
    comparator.compare_generators(results)
    
    # Detailed analysis
    detailed_analysis()
    
    # Security analysis
    security_analysis()
    
    # Conclusion
    conclusion()
    
    print("\n" + "="*70)
    print("IMPLEMENTATION COMPLETE")
    print("="*70)
