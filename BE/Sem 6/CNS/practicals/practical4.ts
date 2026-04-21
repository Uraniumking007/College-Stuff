/**
 * Practical 4: Hill Cipher Implementation and Analysis
 * 
 * This implementation demonstrates the Hill cipher using functional programming.
 * All functions are pure and stateless, with dependencies passed as parameters.
 */

type Matrix = number[][];
type Vector = number[];

// ============================================================================
// Character and Text Conversion Utilities
// ============================================================================

const charToNum = (char: string): number =>
  char.toLowerCase().charCodeAt(0) - 97;

const numToChar = (num: number, modulus: number): string =>
  String.fromCharCode((((num % modulus) + modulus) % modulus) + 65);

const textToVector = (text: string): Vector =>
  text.toLowerCase().split("").map(charToNum);

const vectorToText = (vector: Vector, modulus: number): string =>
  vector.map(num => numToChar(num, modulus)).join("");

// ============================================================================
// Matrix Operations
// ============================================================================

const getMinor = (matrix: Matrix, row: number, col: number): Matrix =>
  matrix
    .filter((_, i) => i !== row)
    .map(r => r.filter((_, j) => j !== col));

const calculateDeterminant = (matrix: Matrix): number => {
  const n = matrix.length;

  if (n === 1) return matrix[0][0];
  if (n === 2)
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];

  let det = 0;
  for (let j = 0; j < n; j++) {
    const minor = getMinor(matrix, 0, j);
    det += Math.pow(-1, j) * matrix[0][j] * calculateDeterminant(minor);
  }
  return det;
};

const gcd = (a: number, b: number): number => {
  while (b !== 0) {
    [a, b] = [b, a % b];
  }
  return a;
};

const modInverse = (a: number, m: number): number => {
  const normalizedA = ((a % m) + m) % m;

  if (gcd(normalizedA, m) !== 1) {
    throw new Error("Inverse does not exist");
  }

  let [oldR, r] = [normalizedA, m];
  let [oldS, s] = [1, 0];

  while (r !== 0) {
    const quotient = Math.floor(oldR / r);
    [oldR, r] = [r, oldR - quotient * r];
    [oldS, s] = [s, oldS - quotient * s];
  }

  return ((oldS % m) + m) % m;
};

const calculateAdjugate = (matrix: Matrix): Matrix => {
  const n = matrix.length;
  const adjugate: Matrix = Array(n)
    .fill(0)
    .map(() => Array(n).fill(0));

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      const minor = getMinor(matrix, i, j);
      const det = calculateDeterminant(minor);
      adjugate[j][i] = Math.pow(-1, i + j) * det;
    }
  }

  return adjugate;
};

const calculateInverseMatrix = (keyMatrix: Matrix, modulus: number): Matrix => {
  const det = calculateDeterminant(keyMatrix);
  const detInv = modInverse(det, modulus);
  const adjugate = calculateAdjugate(keyMatrix);

  const n = keyMatrix.length;
  const inverse: Matrix = Array(n)
    .fill(0)
    .map(() => Array(n).fill(0));

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      inverse[i][j] =
        (((adjugate[i][j] * detInv) % modulus) + modulus) % modulus;
    }
  }

  return inverse;
};

const matrixVectorMultiply = (
  matrix: Matrix,
  vector: Vector,
  modulus: number
): Vector => {
  const n = matrix.length;
  const result: Vector = Array(n).fill(0);

  for (let i = 0; i < n; i++) {
    for (let j = 0; j < n; j++) {
      result[i] += matrix[i][j] * vector[j];
    }
    result[i] = ((result[i] % modulus) + modulus) % modulus;
  }

  return result;
};

// ============================================================================
// Encryption and Decryption
// ============================================================================

const encrypt = (plaintext: string, keyMatrix: Matrix, modulus: number): string => {
  const sanitizedText = plaintext.toUpperCase().replace(/[^A-Z]/g, "");
  const n = keyMatrix.length;

  const encryptBlock = (start: number): string => {
    const block = sanitizedText.substring(start, start + n);
    const paddedBlock = block.padEnd(n, "X");
    const vector = textToVector(paddedBlock);
    const encryptedVector = matrixVectorMultiply(keyMatrix, vector, modulus);
    return vectorToText(encryptedVector, modulus);
  };

  return Array.from(
    { length: Math.ceil(sanitizedText.length / n) },
    (_, i) => encryptBlock(i * n)
  ).join("");
};

const decrypt = (ciphertext: string, keyMatrix: Matrix, modulus: number): string => {
  const sanitizedText = ciphertext.toUpperCase().replace(/[^A-Z]/g, "");
  const inverseMatrix = calculateInverseMatrix(keyMatrix, modulus);
  const n = inverseMatrix.length;

  const decryptBlock = (start: number): string => {
    const block = sanitizedText.substring(start, start + n);
    const vector = textToVector(block);
    const decryptedVector = matrixVectorMultiply(inverseMatrix, vector, modulus);
    return vectorToText(decryptedVector, modulus);
  };

  return Array.from(
    { length: Math.ceil(sanitizedText.length / n) },
    (_, i) => decryptBlock(i * n)
  ).join("");
};

// ============================================================================
// Key Information and Validation
// ============================================================================

const getKeyInfo = (keyMatrix: Matrix, modulus: number) => {
  const det = calculateDeterminant(keyMatrix);
  const normalizedDet = ((det % modulus) + modulus) % modulus;

  return {
    determinant: det,
    normalizedDeterminant: normalizedDet,
    isInvertible: gcd(normalizedDet, modulus) === 1,
  };
};

// ============================================================================
// Demonstration
// ============================================================================

const demonstrateHillCipher = (): void => {
  const keyMatrix: Matrix = [
    [3, 3, 2],
    [2, 5, 3],
    [2, 2, 3],
  ];
  const modulus = 26;

  const formattedKeyMatrix = keyMatrix
    .map((row) => `| ${row.join(" ")} |`)
    .join("\n");
  console.log(`Key matrix:\n${formattedKeyMatrix}`);

  const keyInfo = getKeyInfo(keyMatrix, modulus);
  console.log("\nKey matrix info:");
  console.log(`  Determinant: ${keyInfo.determinant}`);
  console.log(`  Normalized determinant (mod 26): ${keyInfo.normalizedDeterminant}`);
  console.log(`  Is invertible: ${keyInfo.isInvertible}`);

  const plaintext = "pay";
  const ciphertext = encrypt(plaintext, keyMatrix, modulus);
  const decrypted = decrypt(ciphertext, keyMatrix, modulus);

  console.log("\nEncryption/Decryption:");
  console.log(`  Plaintext:  ${plaintext}`);
  console.log(`  Ciphertext: ${ciphertext}`);
  console.log(`  Decrypted:  ${decrypted}`);
};

demonstrateHillCipher();
