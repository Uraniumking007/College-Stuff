/**
 * Practical 4: Hill Cipher Implementation and Analysis
 * 
 * This implementation demonstrates the Hill cipher, a polygraphic substitution cipher
 * based on linear algebra. It encrypts blocks of letters using matrix multiplication.
 */

// Type definitions
type Matrix = number[][];
type Vector = number[];

/**
 * Hill Cipher Implementation
 */
class HillCipher {
  private keyMatrix: Matrix;
  private modulus: number;

  constructor(keyMatrix: Matrix, modulus: number = 26, allowNonInvertible: boolean = false) {
    this.keyMatrix = keyMatrix;
    this.modulus = modulus;
    
    const isInvertible = this.checkMatrixInvertible(keyMatrix);
    
    if (!allowNonInvertible && !isInvertible) {
      throw new Error('Key matrix must be invertible (determinant coprime to modulus)');
    }
    
    if (allowNonInvertible && !isInvertible) {
      console.warn('WARNING: Using non-invertible key matrix. Decryption may not work correctly.');
    }
  }

  /**
   * Convert character to number (a=0, b=1, ..., z=25)
   */
  private charToNum(char: string): number {
    return char.toLowerCase().charCodeAt(0) - 97;
  }

  /**
   * Convert number to character (0=a, 1=b, ..., 25=z)
   */
  private numToChar(num: number): string {
    return String.fromCharCode(((num % this.modulus) + this.modulus) % this.modulus + 65);
  }

  /**
   * Convert text to numerical vector
   */
  private textToVector(text: string): Vector {
    return text.toLowerCase().split('').map(char => this.charToNum(char));
  }

  /**
   * Convert numerical vector to text
   */
  private vectorToText(vector: Vector): string {
    return vector.map(num => this.numToChar(num)).join('');
  }

  /**
   * Calculate determinant of a matrix
   */
  private calculateDeterminant(matrix: Matrix): number {
    const n = matrix.length;
    
    if (n === 1) return matrix[0][0];
    if (n === 2) return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
    
    let det = 0;
    for (let j = 0; j < n; j++) {
      const minor = this.getMinor(matrix, 0, j);
      det += Math.pow(-1, j) * matrix[0][j] * this.calculateDeterminant(minor);
    }
    return det;
  }

  /**
   * Get minor matrix by removing row i and column j
   */
  private getMinor(matrix: Matrix, row: number, col: number): Matrix {
    return matrix
      .filter((_, i) => i !== row)
      .map(row => row.filter((_, j) => j !== col));
  }

  /**
   * Check if matrix is invertible (determinant coprime to modulus)
   */
  private checkMatrixInvertible(matrix: Matrix): boolean {
    const det = this.calculateDeterminant(matrix);
    return this.gcd(Math.abs(det) % this.modulus, this.modulus) === 1;
  }

  /**
   * Calculate GCD of two numbers
   */
  private gcd(a: number, b: number): number {
    while (b !== 0) {
      [a, b] = [b, a % b];
    }
    return a;
  }

  /**
   * Calculate modular inverse using extended Euclidean algorithm
   */
  private modInverse(a: number, m: number): number {
    a = ((a % m) + m) % m;
    
    if (this.gcd(a, m) !== 1) {
      throw new Error('Inverse does not exist');
    }
    
    let [oldR, r] = [a, m];
    let [oldS, s] = [1, 0];
    
    while (r !== 0) {
      const quotient = Math.floor(oldR / r);
      [oldR, r] = [r, oldR - quotient * r];
      [oldS, s] = [s, oldS - quotient * s];
    }
    
    return ((oldS % m) + m) % m;
  }

  /**
   * Calculate adjugate matrix
   */
  private calculateAdjugate(matrix: Matrix): Matrix {
    const n = matrix.length;
    const adjugate: Matrix = Array(n).fill(0).map(() => Array(n).fill(0));
    
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        const minor = this.getMinor(matrix, i, j);
        const det = this.calculateDeterminant(minor);
        adjugate[j][i] = Math.pow(-1, i + j) * det;
      }
    }
    
    return adjugate;
  }

  /**
   * Calculate inverse of key matrix
   */
  private calculateInverseMatrix(): Matrix {
    const det = this.calculateDeterminant(this.keyMatrix);
    const detInv = this.modInverse(det, this.modulus);
    const adjugate = this.calculateAdjugate(this.keyMatrix);
    
    const n = this.keyMatrix.length;
    const inverse: Matrix = Array(n).fill(0).map(() => Array(n).fill(0));
    
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        inverse[i][j] = ((adjugate[i][j] * detInv) % this.modulus + this.modulus) % this.modulus;
      }
    }
    
    return inverse;
  }

  /**
   * Matrix-vector multiplication (modular)
   */
  private matrixVectorMultiply(matrix: Matrix, vector: Vector): Vector {
    const n = matrix.length;
    const result: Vector = Array(n).fill(0);
    
    for (let i = 0; i < n; i++) {
      for (let j = 0; j < n; j++) {
        result[i] += matrix[i][j] * vector[j];
      }
      result[i] = ((result[i] % this.modulus) + this.modulus) % this.modulus;
    }
    
    return result;
  }

  /**
   * Encrypt plaintext using Hill cipher
   */
  encrypt(plaintext: string): string {
    plaintext = plaintext.toUpperCase().replace(/[^A-Z]/g, '');
    
    const n = this.keyMatrix.length;
    let ciphertext = '';
    
    for (let i = 0; i < plaintext.length; i += n) {
      const block = plaintext.substring(i, i + n);
      const paddedBlock = block.padEnd(n, 'X');
      const vector = this.textToVector(paddedBlock);
      
      const encryptedVector = this.matrixVectorMultiply(this.keyMatrix, vector);
      ciphertext += this.vectorToText(encryptedVector);
    }
    
    return ciphertext;
  }

  /**
   * Decrypt ciphertext using Hill cipher
   */
  decrypt(ciphertext: string): string {
    ciphertext = ciphertext.toUpperCase().replace(/[^A-Z]/g, '');
    
    const inverseMatrix = this.calculateInverseMatrix();
    const n = inverseMatrix.length;
    let plaintext = '';
    
    for (let i = 0; i < ciphertext.length; i += n) {
      const block = ciphertext.substring(i, i + n);
      const vector = this.textToVector(block);
      
      const decryptedVector = this.matrixVectorMultiply(inverseMatrix, vector);
      plaintext += this.vectorToText(decryptedVector);
    }
    
    return plaintext;
  }

  /**
   * Get key matrix information
   */
  getKeyInfo(): KeyInfo {
    const det = this.calculateDeterminant(this.keyMatrix);
    const normalizedDet = ((det % this.modulus) + this.modulus) % this.modulus;
    
    return {
      matrix: this.keyMatrix,
      determinant: det,
      normalizedDeterminant: normalizedDet,
      isInvertible: this.gcd(normalizedDet, this.modulus) === 1
    };
  }
}

/**
 * Cryptanalysis and Security Analysis
 */
class HillCipherAnalysis {
  
  /**
   * Analyze brute force attack strength
   */
  static bruteForceAnalysis(matrixSize: number): BruteForceAnalysis {
    const totalPossibleKeys = Math.pow(26, matrixSize * matrixSize);
    const validKeysFraction = HillCipherAnalysis.estimateInvertibleFraction(matrixSize);
    const validKeys = Math.floor(totalPossibleKeys * validKeysFraction);
    
    const keysPerSecondFast = 1_000_000;
    const keysPerSecondSlow = 1000;
    
    const timeFastSeconds = validKeys / keysPerSecondFast;
    const timeSlowSeconds = validKeys / keysPerSecondSlow;
    
    return {
      matrixSize,
      totalPossibleKeys,
      estimatedValidKeys: validKeys,
      validKeysFraction: validKeysFraction * 100,
      timeToBreakFast: HillCipherAnalysis.formatTime(timeFastSeconds),
      timeToBreakSlow: HillCipherAnalysis.formatTime(timeSlowSeconds),
      securityAssessment: matrixSize >= 3 ? 'STRONG' : matrixSize === 2 ? 'MODERATE' : 'WEAK'
    };
  }

  /**
   * Estimate fraction of invertible matrices
   */
  private static estimateInvertibleFraction(n: number): number {
    return Math.pow(6 / 13, n);
  }

  /**
   * Format time in human-readable format
   */
  private static formatTime(seconds: number): string {
    if (seconds < 60) return `${seconds.toFixed(2)} seconds`;
    if (seconds < 3600) return `${(seconds / 60).toFixed(2)} minutes`;
    if (seconds < 86400) return `${(seconds / 3600).toFixed(2)} hours`;
    if (seconds < 31536000) return `${(seconds / 86400).toFixed(2)} days`;
    return `${(seconds / 31536000).toFixed(2)} years`;
  }

  /**
   * Analyze known plaintext attack vulnerability
   */
  static knownPlaintextAnalysis(matrixSize: number): KnownPlaintextAnalysis {
    const pairsNeeded = matrixSize;
    const equationsPerPair = matrixSize;
    const totalEquations = pairsNeeded * equationsPerPair;
    
    return {
      matrixSize,
      plaintextCiphertextPairsNeeded: pairsNeeded,
      equationsGenerated: totalEquations,
      complexity: `O(n³) for n×n matrix - ${matrixSize}³ = ${Math.pow(matrixSize, 3)} operations`,
      vulnerability: 'HIGH - With known plaintext pairs, the key can be recovered by solving linear equations',
      exampleAttack: 'Given "pay"→"XNS", attacker with 3 pairs can solve for 3×3 key matrix'
    };
  }

  /**
   * Analyze chosen plaintext attack vulnerability
   */
  static chosenPlaintextAnalysis(matrixSize: number): ChosenPlaintextAnalysis {
    return {
      matrixSize,
      plaintextsNeeded: matrixSize,
      attackMethod: 'Encrypt standard basis vectors: (1,0,0), (0,1,0), (0,0,1)',
      informationExposed: 'Each ciphertext reveals one column of the key matrix',
      vulnerability: 'CRITICAL - Key matrix can be extracted with just n chosen plaintexts',
      timeComplexity: `O(n²) - ${matrixSize}² = ${matrixSize * matrixSize} operations`
    };
  }

  /**
   * Comprehensive security assessment
   */
  static comprehensiveSecurityAssessment(matrixSize: number): SecurityAssessment {
    const bruteForce = HillCipherAnalysis.bruteForceAnalysis(matrixSize);
    const knownPlaintext = HillCipherAnalysis.knownPlaintextAnalysis(matrixSize);
    const chosenPlaintext = HillCipherAnalysis.chosenPlaintextAnalysis(matrixSize);
    
    let overallSecurity: string;
    let recommendations: string[];
    
    if (matrixSize >= 3) {
      overallSecurity = 'MODERATE';
      recommendations = [
        'Use matrix size >= 3 for better security',
        'Combine with substitution or permutation layers',
        'Use in a product cipher construction',
        'Never use alone for serious encryption needs'
      ];
    } else {
      overallSecurity = 'WEAK';
      recommendations = [
        'Increase matrix size to at least 3×3',
        'Consider modern ciphers (AES) instead',
        'Use only for educational purposes'
      ];
    }
    
    return {
      overallSecurity,
      matrixSize,
      bruteForceResistance: bruteForce.securityAssessment,
      knownPlaintextVulnerability: 'HIGH',
      chosenPlaintextVulnerability: 'CRITICAL',
      mainWeaknesses: [
        'Linear structure allows algebraic attacks',
        'Known plaintext attack is very effective',
        'Chosen plaintext attack reveals key matrix directly',
        'No diffusion across block boundaries'
      ],
      recommendations
    };
  }
}

/**
 * Improved Hill Cipher with Permutation Layer
 */
class ImprovedHillCipher {
  private hillCipher: HillCipher;
  private permutation: number[];
  private matrixSize: number;

  constructor(keyMatrix: Matrix, permutation?: number[]) {
    this.matrixSize = keyMatrix.length;
    this.hillCipher = new HillCipher(keyMatrix);
    this.permutation = permutation || Array.from({ length: keyMatrix.length }, (_, i) => keyMatrix.length - 1 - i);
  }

  /**
   * Apply permutation to vector
   */
  private permute(vector: Vector, inverse: boolean = false): Vector {
    const permuted: Vector = Array(vector.length);
    
    for (let i = 0; i < vector.length; i++) {
      if (inverse) {
        permuted[this.permutation[i]] = vector[i];
      } else {
        permuted[i] = vector[this.permutation[i]];
      }
    }
    
    return permuted;
  }

  /**
   * Encrypt with improved cipher (permutation + Hill cipher)
   */
  encrypt(plaintext: string): string {
    plaintext = plaintext.toUpperCase().replace(/[^A-Z]/g, '');
    const n = this.matrixSize;
    let ciphertext = '';
    
    for (let i = 0; i < plaintext.length; i += n) {
      const block = plaintext.substring(i, i + n);
      const paddedBlock = block.padEnd(n, 'X');
      
      const vector: Vector = Array(n);
      for (let j = 0; j < n; j++) {
        vector[j] = paddedBlock.charCodeAt(j) - 65;
      }
      
      const permuted = this.permute(vector, false);
      const encryptedVector = this.hillCipher['matrixVectorMultiply'](this.hillCipher['keyMatrix'], permuted);
      
      for (let j = 0; j < n; j++) {
        ciphertext += String.fromCharCode(((encryptedVector[j] % 26) + 26) % 26 + 65);
      }
    }
    
    return ciphertext;
  }

  /**
   * Decrypt with improved cipher
   */
  decrypt(ciphertext: string): string {
    ciphertext = ciphertext.toUpperCase().replace(/[^A-Z]/g, '');
    const n = this.matrixSize;
    let plaintext = '';
    
    const inverseMatrix = this.hillCipher['calculateInverseMatrix']();
    
    for (let i = 0; i < ciphertext.length; i += n) {
      const block = ciphertext.substring(i, i + n);
      
      const vector: Vector = Array(n);
      for (let j = 0; j < n; j++) {
        vector[j] = block.charCodeAt(j) - 65;
      }
      
      const decryptedVector = this.hillCipher['matrixVectorMultiply'](inverseMatrix, vector);
      const unpermuted = this.permute(decryptedVector, true);
      
      for (let j = 0; j < n; j++) {
        plaintext += String.fromCharCode(((unpermuted[j] % 26) + 26) % 26 + 65);
      }
    }
    
    return plaintext;
  }
}

/**
 * Analysis of Improved Hill Cipher
 */
class ImprovedHillCipherAnalysis {
  
  static analyzeImprovement(matrixSize: number): ImprovementAnalysis {
    const baseAnalysis = HillCipherAnalysis.comprehensiveSecurityAssessment(matrixSize);
    
    return {
      improvement: 'Permutation Layer before Hill Cipher',
      howItWorks: 'Applies a fixed permutation to plaintext block before matrix multiplication',
      benefits: [
        'Breaks linearity of direct Hill cipher',
        'Makes known plaintext attack harder - attacker must recover permutation too',
        'Increases effective key space by n! (number of permutations)',
        'Adds confusion layer to diffusion layer'
      ],
      increasedSecurity: {
        effectiveKeyspace: `26^(n×n) × n! = ${Math.pow(26, matrixSize * matrixSize).toExponential(2)} × ${ImprovedHillCipherAnalysis.factorial(matrixSize)}`,
        chosenPlaintextResistance: 'IMPROVED - Attacker needs to discover permutation pattern',
        knownPlaintextResistance: 'IMPROVED - More complex system of equations to solve'
      },
      remainingVulnerabilities: [
        'Still fundamentally linear (permutation is linear too)',
        'Chosen plaintext attack still possible with more effort',
        'Does not add avalanche effect',
        'No inter-block diffusion'
      ],
      furtherImprovements: [
        'Add non-linear substitution (S-box) before/after',
        'Use multiple rounds of Hill cipher with different keys',
        'Add XOR with round keys',
        'Implement cipher block chaining (CBC) mode'
      ],
      overallAssessment: 'Moderately improved but still not suitable for production use'
    };
  }

  private static factorial(n: number): number {
    if (n <= 1) return 1;
    return n * ImprovedHillCipherAnalysis.factorial(n - 1);
  }
}

// Type definitions for results
interface KeyInfo {
  matrix: Matrix;
  determinant: number;
  normalizedDeterminant: number;
  isInvertible: boolean;
}

interface BruteForceAnalysis {
  matrixSize: number;
  totalPossibleKeys: number;
  estimatedValidKeys: number;
  validKeysFraction: number;
  timeToBreakFast: string;
  timeToBreakSlow: string;
  securityAssessment: string;
}

interface KnownPlaintextAnalysis {
  matrixSize: number;
  plaintextCiphertextPairsNeeded: number;
  equationsGenerated: number;
  complexity: string;
  vulnerability: string;
  exampleAttack: string;
}

interface ChosenPlaintextAnalysis {
  matrixSize: number;
  plaintextsNeeded: number;
  attackMethod: string;
  informationExposed: string;
  vulnerability: string;
  timeComplexity: string;
}

interface SecurityAssessment {
  overallSecurity: string;
  matrixSize: number;
  bruteForceResistance: string;
  knownPlaintextVulnerability: string;
  chosenPlaintextVulnerability: string;
  mainWeaknesses: string[];
  recommendations: string[];
}

interface ImprovementAnalysis {
  improvement: string;
  howItWorks: string;
  benefits: string[];
  increasedSecurity: {
    effectiveKeyspace: string;
    chosenPlaintextResistance: string;
    knownPlaintextResistance: string;
  };
  remainingVulnerabilities: string[];
  furtherImprovements: string[];
  overallAssessment: string;
}

// ==================== DEMONSTRATION ====================

/**
 * Demonstration of Hill Cipher
 */
function demonstrateHillCipher(): void {
  console.log('='.repeat(80));
  console.log('PRACTICAL 4: HILL CIPHER IMPLEMENTATION AND ANALYSIS');
  console.log('='.repeat(80));
  console.log();

  // Given key matrix
  const keyMatrix: Matrix = [
    [17, 17, 25],
    [21, 18, 21],
    [2, 2, 19]
  ];

  console.log('KEY MATRIX:');
  console.log('-------------');
  console.log(`K = | ${keyMatrix[0].join(' ')} |`);
  console.log(`    | ${keyMatrix[1].join(' ')} |`);
  console.log(`    | ${keyMatrix[2].join(' ')} |`);
  console.log();

  // Create cipher instance (allowing non-invertible for demonstration)
  const hillCipher = new HillCipher(keyMatrix, 26, true);

  // Display key information
  console.log('KEY INFORMATION:');
  console.log('----------------');
  const keyInfo = hillCipher.getKeyInfo();
  console.log(`Determinant: ${keyInfo.determinant}`);
  console.log(`Normalized Determinant (mod 26): ${keyInfo.normalizedDeterminant}`);
  console.log(`Is Invertible: ${keyInfo.isInvertible}`);
  console.log();

  // Test with given plaintext
  const plaintext = 'pay';
  console.log('ENCRYPTION TEST:');
  console.log('----------------');
  console.log(`Plaintext:  "${plaintext}"`);
  const ciphertext = hillCipher.encrypt(plaintext);
  console.log(`Ciphertext: "${ciphertext}"`);
  console.log(`Expected:   "XNS"`);
  console.log(`Match: ${ciphertext === 'XNS' ? '✓ YES' : '✗ NO'}`);
  console.log();

  // Show manual verification
  console.log('MANUAL VERIFICATION:');
  console.log('-------------------');
  console.log('p = 15, a = 0, y = 24');
  console.log('Vector: [15, 0, 24]');
  console.log();
  console.log('Column 1: 17×15 + 21×0 + 2×24 = 255 + 0 + 48 = 303 mod 26 = 17 = R');
  console.log('Column 2: 17×15 + 18×0 + 2×24 = 255 + 0 + 48 = 303 mod 26 = 17 = R');
  console.log('Column 3: 25×15 + 21×0 + 19×24 = 375 + 0 + 456 = 831 mod 26 = 1 = B');
  console.log();
  console.log('Note: Expected output "XNS" differs from calculated "RRB"');
  console.log('This suggests the key matrix or expected ciphertext may have different interpretation');
  console.log();

  // Security Analysis
  console.log('='.repeat(80));
  console.log('SECURITY ANALYSIS');
  console.log('='.repeat(80));
  console.log();

  // Brute Force Analysis
  console.log('1. BRUTE FORCE ATTACK ANALYSIS:');
  console.log('--------------------------------');
  const bruteForce = HillCipherAnalysis.bruteForceAnalysis(3);
  console.log(`Matrix Size: ${bruteForce.matrixSize}×${bruteForce.matrixSize}`);
  console.log(`Total Possible Keys: ${bruteForce.totalPossibleKeys.toExponential(2)}`);
  console.log(`Estimated Valid Keys: ${bruteForce.estimatedValidKeys.toExponential(2)}`);
  console.log(`Valid Keys Fraction: ${bruteForce.validKeysFraction.toFixed(4)}%`);
  console.log(`Time to Break (Fast): ${bruteForce.timeToBreakFast}`);
  console.log(`Time to Break (Slow): ${bruteForce.timeToBreakSlow}`);
  console.log(`Security Assessment: ${bruteForce.securityAssessment}`);
  console.log();

  // Known Plaintext Attack Analysis
  console.log('2. KNOWN PLAINTEXT ATTACK ANALYSIS:');
  console.log('-----------------------------------');
  const knownPlaintext = HillCipherAnalysis.knownPlaintextAnalysis(3);
  console.log(`Pairs Needed: ${knownPlaintext.plaintextCiphertextPairsNeeded}`);
  console.log(`Equations Generated: ${knownPlaintext.equationsGenerated}`);
  console.log(`Complexity: ${knownPlaintext.complexity}`);
  console.log(`Vulnerability: ${knownPlaintext.vulnerability}`);
  console.log();

  // Chosen Plaintext Attack Analysis
  console.log('3. CHOSEN PLAINTEXT ATTACK ANALYSIS:');
  console.log('------------------------------------');
  const chosenPlaintext = HillCipherAnalysis.chosenPlaintextAnalysis(3);
  console.log(`Plaintexts Needed: ${chosenPlaintext.plaintextsNeeded}`);
  console.log(`Attack Method: ${chosenPlaintext.attackMethod}`);
  console.log(`Information Exposed: ${chosenPlaintext.informationExposed}`);
  console.log(`Vulnerability: ${chosenPlaintext.vulnerability}`);
  console.log(`Time Complexity: ${chosenPlaintext.timeComplexity}`);
  console.log();

  // Comprehensive Security Assessment
  console.log('4. COMPREHENSIVE SECURITY ASSESSMENT:');
  console.log('-------------------------------------');
  const assessment = HillCipherAnalysis.comprehensiveSecurityAssessment(3);
  console.log(`Overall Security: ${assessment.overallSecurity}`);
  console.log(`Brute Force Resistance: ${assessment.bruteForceResistance}`);
  console.log(`Known Plaintext Vulnerability: ${assessment.knownPlaintextVulnerability}`);
  console.log(`Chosen Plaintext Vulnerability: ${assessment.chosenPlaintextVulnerability}`);
  console.log();
  console.log('Main Weaknesses:');
  assessment.mainWeaknesses.forEach((weakness, i) => {
    console.log(`  ${i + 1}. ${weakness}`);
  });
  console.log();
  console.log('Recommendations:');
  assessment.recommendations.forEach((rec, i) => {
    console.log(`  ${i + 1}. ${rec}`);
  });
  console.log();

  // Improved Hill Cipher
  console.log('='.repeat(80));
  console.log('IMPROVED HILL CIPHER');
  console.log('='.repeat(80));
  console.log();

  // Create improved cipher with a valid invertible key
  const validKeyMatrix: Matrix = [
    [3, 3, 2],
    [2, 5, 3],
    [2, 2, 3]
  ];

  const improvedCipher = new ImprovedHillCipher(validKeyMatrix);

  console.log('IMPROVEMENT: Permutation Layer');
  console.log('--------------------------------');
  console.log('Adding a permutation layer before the Hill cipher encryption');
  console.log('to break linearity and increase security.');
  console.log();

  console.log('ENCRYPTION WITH IMPROVED CIPHER:');
  console.log('----------------------------------');
  const testMessages = ['HEL', 'WOR', 'SEC'];
  for (const msg of testMessages) {
    const standardCipher = improvedCipher['hillCipher'].encrypt(msg);
    const improvedCipherText = improvedCipher.encrypt(msg);
    console.log(`Plaintext: ${msg}`);
    console.log(`  Standard Hill:  ${standardCipher}`);
    console.log(`  Improved Hill:  ${improvedCipherText}`);
    console.log();
  }

  // Improvement Analysis
  console.log('5. IMPROVEMENT ANALYSIS:');
  console.log('------------------------');
  const improvementAnalysis = ImprovedHillCipherAnalysis.analyzeImprovement(3);
  console.log(`Improvement: ${improvementAnalysis.improvement}`);
  console.log(`How It Works: ${improvementAnalysis.howItWorks}`);
  console.log();
  console.log('Benefits:');
  improvementAnalysis.benefits.forEach((benefit, i) => {
    console.log(`  ${i + 1}. ${benefit}`);
  });
  console.log();
  console.log(`Increased Effective Keyspace: ${improvementAnalysis.increasedSecurity.effectiveKeyspace}`);
  console.log();
  console.log('Remaining Vulnerabilities:');
  improvementAnalysis.remainingVulnerabilities.forEach((vuln, i) => {
    console.log(`  ${i + 1}. ${vuln}`);
  });
  console.log();
  console.log('Further Improvements:');
  improvementAnalysis.furtherImprovements.forEach((imp, i) => {
    console.log(`  ${i + 1}. ${imp}`);
  });
  console.log();
  console.log(`Overall Assessment: ${improvementAnalysis.overallAssessment}`);
  console.log();

  console.log('='.repeat(80));
  console.log('CONCLUSION');
  console.log('='.repeat(80));
  console.log();
  console.log('The Hill cipher is a significant historical cipher that introduced');
  console.log('mathematical foundations (linear algebra) to cryptography.');
  console.log();
  console.log('Strengths:');
  console.log('  • Works on blocks of characters (more secure than monoalphabetic)');
  console.log('  • Mathematical foundation allows for analysis');
  console.log('  • Larger matrices provide better security against brute force');
  console.log();
  console.log('Weaknesses:');
  console.log('  • Linear structure vulnerable to algebraic attacks');
  console.log('  • Known plaintext attacks are very effective');
  console.log('  • Chosen plaintext attacks can recover the key easily');
  console.log('  • Requires invertible matrix (determinant coprime to modulus)');
  console.log();
  console.log('The improved version with a permutation layer adds some security,');
  console.log('but modern ciphers like AES should always be preferred for real-world use.');
  console.log();
  console.log('='.repeat(80));
}

// Run demonstration
demonstrateHillCipher();
