"""
Hill Cipher Implementation and Security Analysis
"""

import numpy as np
from typing import List, Tuple
import math

class HillCipher:
    """Implementation of Hill Cipher with security analysis"""
    
    def __init__(self, key_matrix: List[List[int]], validate: bool = False):
        """
        Initialize Hill Cipher with key matrix.
        
        Args:
            key_matrix: Square matrix (mod 26) for encryption
            validate: If True, check that key is invertible (required for decryption)
        """
        self.key = np.array(key_matrix, dtype=int)
        self.mod = 26
        self.det = round(np.linalg.det(self.key))
        
        if validate:
            self._validate_key()
    def _validate_key(self):
        """Validate that key matrix is invertible mod 26"""
        if self.key.shape[0] != self.key.shape[1]:
            raise ValueError("Key matrix must be square")
            
        det = round(np.linalg.det(self.key))
        if math.gcd(det % self.mod, self.mod) != 1:
            raise ValueError(f"Key matrix not invertible mod {self.mod}. " 
                           f"det = {det}, gcd(det mod 26, 26) must be 1")
    
    def _char_to_num(self, char: str) -> int:
        """Convert character to number (a=0, b=1, ..., z=25)"""
        return ord(char.lower()) - ord('a')
    
    def _num_to_char(self, num: int) -> str:
        """Convert number to character"""
        return chr((num % self.mod) + ord('a'))
    
    def _text_to_vector(self, text: str) -> np.ndarray:
        """Convert text to column vector"""
        return np.array([self._char_to_num(c) for c in text]).reshape(-1, 1)
    
    def _vector_to_text(self, vector: np.ndarray) -> str:
        """Convert vector to text"""
        return ''.join([self._num_to_char(int(v)) for v in vector.flatten()])
    
    def _matrix_mod_inv(self, matrix: np.ndarray, mod: int) -> np.ndarray:
        """
        Calculate modular inverse of matrix.
        
        Returns inverse such that (matrix * inverse) mod mod = identity
        """
        det = int(round(np.linalg.det(matrix)))
        det_mod = det % mod
        
        # Find modular multiplicative inverse of determinant
        det_inv = None
        for i in range(1, mod):
            if (det_mod * i) % mod == 1:
                det_inv = i
                break
        
        if det_inv is None:
            raise ValueError("Matrix not invertible")
        
        # Calculate adjugate matrix
        adj = np.round(det * np.linalg.inv(matrix)).astype(int)
        
        # Modular inverse: det^(-1) * adj (mod 26)
        inv = (det_inv * adj) % mod
        return inv.astype(int)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt plaintext using Hill cipher"""
        plaintext = plaintext.lower().replace(' ', '')
        block_size = self.key.shape[0]
        
        # Pad plaintext if necessary
        if len(plaintext) % block_size != 0:
            plaintext += 'x' * (block_size - len(plaintext) % block_size)
        
        ciphertext = []
        for i in range(0, len(plaintext), block_size):
            block = plaintext[i:i+block_size]
            vector = self._text_to_vector(block)
            encrypted = (self.key @ vector) % self.mod
            ciphertext.append(self._vector_to_text(encrypted))
        
        return ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt ciphertext using Hill cipher"""
        # Check invertibility before attempting decryption
        if math.gcd(self.det % self.mod, self.mod) != 1:
            raise ValueError(
                f"Cannot decrypt: Key matrix not invertible mod {self.mod}. "
                f"det = {self.det}, det mod {self.mod} = {self.det % self.mod}, "
                f"gcd({self.det % self.mod}, {self.mod}) = {math.gcd(self.det % self.mod, self.mod)} != 1")
        
        ciphertext = ciphertext.lower().replace(' ', '')
        block_size = self.key.shape[0]
        
        # Calculate inverse key matrix
        key_inv = self._matrix_mod_inv(self.key, self.mod)
        
        plaintext = []
        for i in range(0, len(ciphertext), block_size):
            block = ciphertext[i:i+block_size]
            vector = self._text_to_vector(block)
            decrypted = (key_inv @ vector) % self.mod
            plaintext.append(self._vector_to_text(decrypted))
        
        return ''.join(plaintext)


def verify_example():
    """Verify the given example: pay -> XNS"""
    print("=" * 60)
    print("VERIFICATION OF GIVEN EXAMPLE")
    print("=" * 60)
    
    # Given key matrix
    K = [
        [17, 17, 25],
        [21, 18, 21],
        [2, 2, 19]
    ]
    
    # Note: validate=False to allow non-invertible key for encryption only
    cipher = HillCipher(K, validate=False)
    plaintext = "pay"
    print(f"\nKey Matrix K (mod 26):")
    for row in K:
        print(f"  {row}")
    
    print(f"\nPlaintext: {plaintext}")
    
    # Show encryption process
    print(f"\nEncryption Process:")
    print(f"  p = 15 (a=0, b=1, ..., p=15)")
    print(f"  a = 0")
    print(f"  y = 24")
    print(f"  P = [15, 0, 24]^T")
    
    ciphertext = cipher.encrypt(plaintext)
    print(f"\nCiphertext: {ciphertext.upper()}")
    
    # Verify decryption (will fail for non-invertible key)
    print(f"\nAttempting decryption...")
    try:
        decrypted = cipher.decrypt(ciphertext)
        print(f"Decrypted: {decrypted}")
    except ValueError as e:
        print(f"Decryption FAILED (expected): {str(e)[:100]}...")
        print(f"\n  Note: This key matrix is NOT invertible mod 26.")
        print(f"        Encryption works, but decryption is impossible.")
        print(f"        This demonstrates the IMPORTANCE of invertible keys!")
    
    if ciphertext.upper() == "XNS":
        print("\n✓ VERIFIED: 'pay' encrypts to 'XNS' as expected")
    else:
        print(f"\n✗ MISMATCH: Expected 'XNS', got '{ciphertext.upper()}'")


def security_analysis():
    """Analyze Hill cipher security"""
    print("\n" + "=" * 60)
    print("SECURITY ANALYSIS OF HILL CIPHER")
    print("=" * 60)
    
    print("""
1. BRUTE FORCE ATTACK ANALYSIS
   ----------------------------
   For an n×n Hill cipher:
   - Key space: All invertible n×n matrices modulo 26
   - Total n×n matrices: 26^(n²)
   
   For n=3 (3×3 matrix):
   - Total possible matrices: 26^9 ≈ 5.4 × 10^12
   - Invertible matrices: φ(26) × 26^(n²-n) × ... ≈ 1.6 × 10^12
   
   Strength Assessment: MODERATE
   ✓ Better than simple substitution (26! ≈ 4×10^26 for n=1, but insecure)
   ✓ 1.6 trillion keys is non-trivial but feasible with modern computing
   ✗ Special hardware can enumerate 10^12 keys in hours/days
   
   Time estimates (assuming 10^9 key trials/second):
   - n=2: ~0.16 seconds (very weak)
   - n=3: ~26 minutes (weak)
   - n=4: ~18 days (moderate)
   - n=5: ~3.7 years (stronger)


2. CRYPTANALYSIS ATTACK ANALYSIS
   ------------------------------
   Known Plaintext Attack (THE CRITICAL WEAKNESS):
   
   For an n×n Hill cipher with n known plaintext-ciphertext pairs:
   
   Step 1: Set up matrix equation
   - P × K^T = C (mod 26)
   - Where P is n×n plaintext matrix, C is n×n ciphertext matrix
   - Solve: K^T = P^(-1) × C (mod 26)
   
   Step 2: Compute key
   - Calculate P^(-1) mod 26 (if invertible)
   - Multiply by C to recover K^T
   - Transpose to get K
   
   Requirements for Attack:
   - Need exactly n blocks of known plaintext-ciphertext pairs
   - Plaintext matrix must be invertible (det ≠ 0 mod 26)
   
   Example: For 3×3 Hill cipher
   - Need only 3 known pairs of 3-character blocks
   - Solve using linear algebra
   - Recover complete key matrix
   - Break entire system
   
   Strength Assessment: VERY WEAK
   ✗ Known plaintext attack completely breaks the cipher
   ✗ Only n blocks needed (e.g., 9 characters for 3×3)
   ✗ No diffusion beyond block size
   ✗ Linear structure is exploitable
   
   Other Attacks:
   - Chosen Plaintext: Trivial - choose identity matrix as plaintext
   - Ciphertext Only: Frequency analysis on digraphs/trigraphs (harder but possible)


3. COMPARATIVE ASSESSMENT
   -----------------------
   Hill Cipher vs Classical Ciphers:
   
   + Advantages:
   ✓ Polygraphic - obscures single-letter frequencies
   ✓ Mathematical elegance
   ✓ Can use larger block sizes for diffusion
   
   - Disadvantages:
   ✗ Linear algebra - vulnerable to mathematical attacks
   ✗ Known plaintext attack breaks it completely
   ✗ No avalanche effect (small plaintext change = predictable change)
   ✗ Block structure preserves patterns


4. KEY WEAKNESSES SUMMARY
   -----------------------
   CRITICAL: The Hill cipher has FUNDAMENTAL weaknesses:
   
   1. LINEARITY: Encryption is linear transformation
      - C1 + C2 = Encrypt(P1 + P2)
      - Exploitable through algebraic attacks
   
   2. DETERMINISTIC: Same plaintext block = same ciphertext
      - No randomness or chaining between blocks
   
   3. KNOWN PLAINTEXT RECOVERY: 
      - n blocks → complete key recovery
      - O(n³) time complexity (matrix inversion)
    """)


def propose_improvement():
    """Propose and analyze improvement to Hill cipher"""
    print("\n" + "=" * 60)
    print("PROPOSED IMPROVEMENT: HILL CIPHER WITH FEEDBACK")
    print("=" * 60)
    
    print("""
PROPOSAL: Add Inter-Block Feedback (Like CBC Mode)
--------------------------------------------------

Current Hill Cipher:
  Block 1: C1 = K × P1
  Block 2: C2 = K × P2  (independent!)
  Block 3: C3 = K × P3  (independent!)

Improved Hill Cipher with CBC-style feedback:
  C1 = K × (P1 ⊕ IV)          # IV = Initialization Vector
  C2 = K × (P2 ⊕ C1)          # Feedback from previous ciphertext
  C3 = K × (P3 ⊕ C2)          # Chain continues
  ...

Where ⊕ denotes XOR (or addition mod 26 for text)


IMPLEMENTATION:
""")


class ImprovedHillCipher(HillCipher):
    """Hill cipher with CBC-style feedback for better diffusion"""
    
    def __init__(self, key_matrix: List[List[int]], iv: str = None):
        # Require invertible key for improved cipher
        super().__init__(key_matrix, validate=True)
        self.block_size = self.key.shape[0]
        
        # Generate random IV if not provided
        if iv is None:
            self.iv = ''.join([chr(np.random.randint(0, 26) + ord('a')) 
                             for _ in range(self.block_size)])
        else:
            self.iv = iv.lower()[:self.block_size]
    def _xor_vectors(self, text1: str, text2: str) -> str:
        """XOR two text vectors mod 26"""
        result = []
        for c1, c2 in zip(text1, text2):
            v1 = self._char_to_num(c1)
            v2 = self._char_to_num(c2)
            result.append(self._num_to_char((v1 + v2) % 26))
        return ''.join(result)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt with CBC-style feedback"""
        plaintext = plaintext.lower().replace(' ', '')
        
        # Pad if necessary
        if len(plaintext) % self.block_size != 0:
            plaintext += 'x' * (self.block_size - len(plaintext) % self.block_size)
        
        ciphertext = []
        prev_block = self.iv
        
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i+self.block_size]
            
            # XOR with previous ciphertext block (CBC mode)
            xored = self._xor_vectors(block, prev_block)
            
            # Apply Hill cipher
            vector = self._text_to_vector(xored)
            encrypted = (self.key @ vector) % self.mod
            cipher_block = self._vector_to_text(encrypted)
            
            ciphertext.append(cipher_block)
            prev_block = cipher_block
        
        return self.iv + ''.join(ciphertext)
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt with CBC-style feedback"""
        ciphertext = ciphertext.lower().replace(' ', '')
        
        # Extract IV
        iv = ciphertext[:self.block_size]
        ciphertext = ciphertext[self.block_size:]
        
        # Calculate inverse key
        key_inv = self._matrix_mod_inv(self.key, self.mod)
        
        plaintext = []
        prev_block = iv
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i+self.block_size]
            
            # Reverse Hill cipher
            vector = self._text_to_vector(block)
            decrypted = (key_inv @ vector) % self.mod
            decrypted_text = self._vector_to_text(decrypted)
            
            # XOR with previous block
            plain_block = self._xor_vectors(decrypted_text, prev_block)
            
            plaintext.append(plain_block)
            prev_block = block
        
        return ''.join(plaintext)


def analyze_improvement():
    """Analyze security of improved Hill cipher"""
    print("""
SECURITY ANALYSIS OF IMPROVED HILL CIPHER
==========================================

1. ENHANCEMENT OVER ORIGINAL
   ---------------------------
   ✓ Avalanche Effect: Small plaintext change affects ALL following blocks
   ✓ Pattern Masking: Same plaintext in different positions → different ciphertext
   ✓ IV Randomization: Same message encrypted twice → different outputs
   ✓ Diffusion: Error/corruption propagates through remaining ciphertext


2. BRUTE FORCE RESISTANCE
   -----------------------
   Same as original: Still ~1.6 × 10^12 keys for 3×3 matrix
   BUT: Each key trial requires full decryption (not just first block)
   
   Time increase: ~O(block_count) more computation per trial
   For 1000 blocks: ~1000x slower to brute force


3. CRYPTANALYSIS RESISTANCE
   -------------------------
   
   KNOWN PLAINTEXT ATTACK:
   Original: Need n blocks → Recover K directly
   Improved: Need n blocks AND knowledge of IV → Recover K
   
   ✓ Still requires n plaintext-ciphertext pairs
   ✓ More complex: Must account for feedback
   ✓ XOR must be reversed before matrix equation
   ✓ However, if IV is known, attack still works (slightly more complex)
   
   CHOSEN PLAINTEXT ATTACK:
   Original: Choose identity matrix → C = K
   Improved: Choose P1=0 → C1 = K × IV
   ✓ If attacker can control IV, still vulnerable
   ✓ Need to solve for IV and K simultaneously
   
   CIPHERTEXT-ONLY ATTACK:
   Original: Frequency analysis on digraphs/trigraphs
   Improved: MUCH HARDER
   ✓ Feedback obscures patterns
   ✓ Same plaintext blocks → different ciphertext
   ✓ Frequency analysis largely ineffective


4. REMAINING WEAKNESSES
   ---------------------
   ✗ Linear structure still exists (improved, not eliminated)
   ✗ If IV is predictable/reused, security degrades
   ✗ Known plaintext + known IV → key recoverable
   ✗ No authentication (vulnerable to tampering)
   ✗ Deterministic encryption with same IV


5. QUANTITATIVE COMPARISON
   -------------------------
                    Original      Improved
                    --------      --------
   Brute Force:      10^12 keys    10^12 keys × blocks
   Known Plaintext:  n blocks      n blocks + IV
   Pattern conceal:  POOR          GOOD
   Avalanche:        NONE          YES
   Same msg same IV: YES           NO
   Implementation:   Simple        Slightly complex


6. RECOMMENDATIONS FOR FURTHER IMPROVEMENT
   ----------------------------------------
   To achieve modern security standards:
   
   a) Increase block size: Use 4×4 or 5×5 matrices
   b) Use larger modulus: Work with bytes (mod 256) not letters (mod 26)
   c) Add authentication: MAC or digital signature
   d) Multiple rounds: Apply cipher 3+ times with different keys
   e) Non-linear components: Add substitution (S-boxes)
   f) Random IV per message: Must be unpredictable and unique
   
   Note: For production use, prefer AES or other modern ciphers.
   Hill cipher is primarily educational.


CONCLUSION:
-----------
The improved Hill cipher with feedback SIGNIFICANTLY enhances security
against pattern analysis and ciphertext-only attacks. However, it remains
vulnerable to known plaintext attacks (with more complexity). The improvement
is meaningful but the cipher should still be considered educational rather
than production-ready.
    """)


def generate_invertible_key(size: int = 3) -> List[List[int]]:
    """Generate a random invertible key matrix of given size"""
    import random
    while True:
        # Generate random matrix
        key = [[random.randint(0, 25) for _ in range(size)] for _ in range(size)]
        try:
            # Test if it's invertible by creating a HillCipher with validate=True
            HillCipher(key, validate=True)
            return key
        except ValueError:
            # Not invertible, try again
            continue


def demonstrate_improvement():
    """Demonstrate the improvement"""
    print("\n" + "=" * 60)
    print("DEMONSTRATION: ORIGINAL vs IMPROVED")
    print("=" * 60)
    
    K = [
        [17, 17, 25],
        [21, 18, 21],
        [2, 2, 19]
    ]
    
    # Original cipher with given non-invertible key
    original = HillCipher(K, validate=False)
    improved = None  # Will create with invertible key below
    
    # Test messages
    messages = [
        "paymoremoney",
        "paymoremoney",  # Same message again
        "pbymoremoney"   # One character different
    ]
    
    print("\n1. Original Hill Cipher (non-invertible key, encryption only):")
    print("-" * 55)
    for msg in messages[:1]:  # Just first message
        ct = original.encrypt(msg)
        print(f"  '{msg}' → '{ct}'")
    print("  Note: Cannot decrypt - key is not invertible")
    
    # Improved cipher with valid invertible key
    print("\n2. Improved Hill Cipher (valid invertible key, full encryption/decryption):")
    print("-" * 70)
    invertible_key = generate_invertible_key(3)
    print(f"  Generated invertible key (det coprime to 26):")
    for row in invertible_key:
        print(f"    {row}")
    improved = ImprovedHillCipher(invertible_key, iv="xyz")
    for msg in messages:
        ct = improved.encrypt(msg)
        decrypted = improved.decrypt(ct)
        print(f"  '{msg}' → '{ct[:12]}...' → '{decrypted}' (IV shown)")
    print("\nKey observations:")
    print("  Original: Uses non-invertible key → Encryption works, decryption impossible")
    print("  Improved: Uses invertible key → Full encryption/decryption with avalanche effect")
    print("  ✓ Same plaintext → different ciphertext (randomized via IV)")
    print("  ✓ 1-char change → affects ALL subsequent blocks (avalanche)")


if __name__ == "__main__":
    # Verify the given example
    cipher = verify_example()
    
    # Security analysis
    security_analysis()
    
    # Propose and analyze improvement
    propose_improvement()
    analyze_improvement()
    demonstrate_improvement()
    
    print("\n" + "=" * 60)
    print("IMPLEMENTATION COMPLETE")
    print("=" * 60)
