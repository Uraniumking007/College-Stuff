"use strict";
// Basic Hill Cipher implementation in TypeScript
// Simplified version with minimal dependencies
class HillCipher {
    constructor(key, alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') {
        this.keyMatrix = key;
        this.matrixSize = key.length;
        this.alphabet = alphabet;
        // Validate key matrix
        if (this.matrixSize === 0) {
            throw new Error('Key matrix cannot be empty');
        }
        // Check if matrix is square
        for (const row of this.keyMatrix) {
            if (row.length !== this.matrixSize) {
                throw new Error('Key matrix must be square');
            }
        }
    }
    // Helper function to convert letter to number (A=0, B=1, etc.)
    letterToNumber(letter) {
        const index = this.alphabet.indexOf(letter.toUpperCase());
        if (index === -1) {
            throw new Error(`Invalid character: ${letter}`);
        }
        return index;
    }
    // Helper function to convert number to letter
    numberToLetter(number) {
        return this.alphabet[number % this.alphabet.length];
    }
    // Matrix multiplication for Hill cipher
    multiplyMatrices(a, b) {
        const result = [];
        for (let i = 0; i < a.length; i++) {
            result[i] = [];
            for (let j = 0; j < b[0].length; j++) {
                let sum = 0;
                for (let k = 0; k < a[0].length; k++) {
                    sum += a[i][k] * b[k][j];
                }
                result[i][j] = sum % this.alphabet.length;
            }
        }
        return result;
    }
    // Vector multiplication with matrix
    multiplyMatrixVector(matrix, vector) {
        const result = [];
        for (let i = 0; i < matrix.length; i++) {
            let sum = 0;
            for (let j = 0; j < vector.length; j++) {
                sum += matrix[i][j] * vector[j];
            }
            result[i] = sum % this.alphabet.length;
        }
        return result;
    }
    // Prepare text for encryption (pad with X if needed)
    prepareText(text) {
        text = text.toUpperCase().replace(/[^A-Z]/g, '');
        // Pad text to be multiple of matrix size
        while (text.length % this.matrixSize !== 0) {
            text += 'X';
        }
        return text;
    }
    // Encrypt text
    encrypt(plainText) {
        const preparedText = this.prepareText(plainText);
        let cipherText = '';
        // Process text in blocks of matrix size
        for (let i = 0; i < preparedText.length; i += this.matrixSize) {
            const block = preparedText.substring(i, i + this.matrixSize);
            // Convert block to numbers
            const vector = [];
            for (const char of block) {
                vector.push(this.letterToNumber(char));
            }
            // Multiply with key matrix
            const result = this.multiplyMatrixVector(this.keyMatrix, vector);
            // Convert back to letters
            for (const num of result) {
                cipherText += this.numberToLetter(num);
            }
        }
        return cipherText;
    }
    // Decrypt text
    decrypt(cipherText) {
        // Calculate inverse of key matrix modulo alphabet length
        const det = this.determinant(this.keyMatrix);
        const detInv = this.modularInverse(det, this.alphabet.length);
        if (detInv === -1) {
            throw new Error('Key matrix is not invertible');
        }
        const adjugate = this.adjugate(this.keyMatrix);
        const inverseKey = this.multiplyByScalar(adjugate, detInv);
        const preparedText = this.prepareText(cipherText);
        let plainText = '';
        // Process text in blocks of matrix size
        for (let i = 0; i < preparedText.length; i += this.matrixSize) {
            const block = preparedText.substring(i, i + this.matrixSize);
            // Convert block to numbers
            const vector = [];
            for (const char of block) {
                vector.push(this.letterToNumber(char));
            }
            // Multiply with inverse key matrix
            const result = this.multiplyMatrixVector(inverseKey, vector);
            // Convert back to letters
            for (const num of result) {
                plainText += this.numberToLetter(num);
            }
        }
        return plainText;
    }
    // Matrix determinant
    determinant(matrix) {
        const n = matrix.length;
        if (n === 1) {
            return matrix[0][0];
        }
        if (n === 2) {
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
        }
        let det = 0;
        for (let j = 0; j < n; j++) {
            det += matrix[0][j] * this.cofactor(matrix, 0, j);
        }
        return det % this.alphabet.length;
    }
    // Cofactor of matrix element
    cofactor(matrix, row, col) {
        const sign = (row + col) % 2 === 0 ? 1 : -1;
        const minor = this.minor(matrix, row, col);
        return sign * this.determinant(minor);
    }
    // Minor of matrix element
    minor(matrix, row, col) {
        const n = matrix.length;
        const minor = [];
        for (let i = 0; i < n; i++) {
            if (i === row)
                continue;
            minor[i] = [];
            for (let j = 0; j < n; j++) {
                if (j === col)
                    continue;
                minor[i].push(matrix[i][j]);
            }
        }
        return minor;
    }
    // Adjugate matrix (transpose of cofactor matrix)
    adjugate(matrix) {
        const n = matrix.length;
        const adjugate = [];
        for (let i = 0; i < n; i++) {
            adjugate[i] = [];
            for (let j = 0; j < n; j++) {
                adjugate[i][j] = this.cofactor(matrix, j, i);
            }
        }
        return adjugate;
    }
    // Modular inverse
    modularInverse(a, m) {
        a = ((a % m) + m) % m;
        for (let x = 1; x < m; x++) {
            if ((a * x) % m === 1) {
                return x;
            }
        }
        return -1;
    }
    // Multiply matrix by scalar modulo m
    multiplyByScalar(matrix, scalar) {
        const result = [];
        for (let i = 0; i < matrix.length; i++) {
            result[i] = [];
            for (let j = 0; j < matrix[0].length; j++) {
                result[i][j] = (matrix[i][j] * scalar) % this.alphabet.length;
            }
        }
        return result;
    }
}
// Example usage
function main() {
    // 2x2 key matrix example
    const key = [
        [3, 3],
        [2, 5]
    ];
    const cipher = new HillCipher(key);
    const plainText = "HELLO";
    console.log(`Plain text: ${plainText}`);
    const encrypted = cipher.encrypt(plainText);
    console.log(`Encrypted: ${encrypted}`);
    const decrypted = cipher.decrypt(encrypted);
    console.log(`Decrypted: ${decrypted}`);
    // 3x3 key matrix example
    const key3x3 = [
        [6, 24, 1],
        [13, 16, 10],
        [20, 17, 15]
    ];
    const cipher3x3 = new HillCipher(key3x3);
    const plainText3x3 = "ACT";
    console.log(`\n3x3 Example:`);
    console.log(`Plain text: ${plainText3x3}`);
    const encrypted3x3 = cipher3x3.encrypt(plainText3x3);
    console.log(`Encrypted: ${encrypted3x3}`);
    const decrypted3x3 = cipher3x3.decrypt(encrypted3x3);
    console.log(`Decrypted: ${decrypted3x3}`);
}
// Run examples
main();
