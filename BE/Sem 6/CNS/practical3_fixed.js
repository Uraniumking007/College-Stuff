"use strict";
// Playfair cipher: plaintext in pairs (digraphs). I and J share one cell.
// Polyalphabetic > monoalphabetic: same letter → different cipher letters by context, so frequency analysis is harder.
const ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ";
function buildMatrix(key) {
    const k = key.toUpperCase().replace(/J/g, "I").replace(/[^A-Z]/g, "");
    const used = new Set();
    const letters = [];
    for (const c of k + ALPHABET) {
        if (!used.has(c)) {
            used.add(c);
            letters.push(c);
        }
    }
    const matrix = [];
    for (let r = 0; r < 5; r++)
        matrix.push(letters.slice(r * 5, r * 5 + 5));
    return matrix;
}
function find(matrix, ch) {
    const c = ch === "J" ? "I" : ch;
    for (let r = 0; r < 5; r++)
        for (let col = 0; col < 5; col++)
            if (matrix[r][col] === c)
                return [r, col];
    return [0, 0];
}
function digraphs(text) {
    const s = text.toUpperCase().replace(/J/g, "I").replace(/[^A-Z]/g, "");
    const out = [];
    for (let i = 0; i < s.length; i += 2) {
        const a = s[i];
        const b = i + 1 < s.length ? s[i + 1] : "X";
        out.push(a === b ? a + "X" : a + b);
        if (a === b)
            i--;
    }
    return out;
}
function transform(matrix, a, b, step) {
    const [r1, c1] = find(matrix, a);
    const [r2, c2] = find(matrix, b);
    if (r1 === r2)
        return matrix[r1][(c1 + step + 5) % 5] + matrix[r2][(c2 + step + 5) % 5];
    if (c1 === c2)
        return matrix[(r1 + step + 5) % 5][c1] + matrix[(r2 + step + 5) % 5][c2];
    return matrix[r1][c2] + matrix[r2][c1];
}
function playfairEncrypt(plainText, key) {
    const m = buildMatrix(key);
    return digraphs(plainText).map((dg) => transform(m, dg[0], dg[1], 1)).join(" ");
}
function playfairDecrypt(cipherText, key) {
    const m = buildMatrix(key);
    const s = cipherText.toUpperCase().replace(/\s/g, "");
    const out = [];
    for (let i = 0; i < s.length; i += 2)
        out.push(s.slice(i, i + 2));
    return out.map((dg) => transform(m, dg[0], dg[1], -1)).join("");
}
const KEY = "MONARCHY";
const PLAINTEXT = "ar mu hs ea";
console.log("Key:", KEY);
console.log("Plaintext:", PLAINTEXT);
console.log("Ciphertext:", playfairEncrypt(PLAINTEXT, KEY));
console.log("Decrypted:", playfairDecrypt(playfairEncrypt(PLAINTEXT, KEY), KEY));
