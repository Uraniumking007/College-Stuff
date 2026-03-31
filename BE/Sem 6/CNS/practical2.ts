interface MonoalphabeticEncryptParameters {
  plainText: string;
  key: string;
}

interface MonoalphabeticDecryptParameters {
  cipherText: string;
  key: string;
}

const ALPHABET_MONO = "abcdefghijklmnopqrstuvwxyz";
const ALPHABET_UPPER_MONO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

function buildEncryptMap(key: string): Map<string, string> {
  const keyLower = key.toLowerCase();
  const map = new Map<string, string>();
  for (let i = 0; i < ALPHABET_MONO.length; i++) {
    map.set(ALPHABET_MONO[i], keyLower[i]);
    map.set(ALPHABET_UPPER_MONO[i], keyLower[i].toUpperCase());
  }
  return map;
}

function buildDecryptMap(key: string): Map<string, string> {
  const keyLower = key.toLowerCase();
  const map = new Map<string, string>();
  for (let i = 0; i < ALPHABET_MONO.length; i++) {
    map.set(keyLower[i], ALPHABET_MONO[i]);
    map.set(keyLower[i].toUpperCase(), ALPHABET_UPPER_MONO[i]);
  }
  return map;
}

function isValidMonoKey(key: string): boolean {
  const k = key.replace(/\s/g, "").toLowerCase();
  if (k.length !== 26) return false;

  const seen = new Set<string>();
  for (const c of k) {
    if (c < "a" || c > "z") return false;
    if (seen.has(c)) return false;
    seen.add(c);
  }
  return true;
}

function monoalphabeticEncrypt({
  plainText,
  key,
}: MonoalphabeticEncryptParameters): string {
  if (!isValidMonoKey(key)) {
    throw new Error("Invalid key. Use exactly 26 unique letters (a–z).");
  }

  const map = buildEncryptMap(key);
  return plainText
    .split("")
    .map((char) => map.get(char) ?? char)
    .join("");
}

function monoalphabeticDecrypt({
  cipherText,
  key,
}: MonoalphabeticDecryptParameters): string {
  if (!isValidMonoKey(key)) {
    throw new Error("Invalid key. Use exactly 26 unique letters (a–z).");
  }

  const map = buildDecryptMap(key);
  return cipherText
    .split("")
    .map((char) => map.get(char) ?? char)
    .join("");
}

const plainText2 = "Tasty";
const key2 = "qwertyuiopasdfghjklzxcvbnm";

const encrypted2 = monoalphabeticEncrypt({ plainText: plainText2, key: key2 });
console.log("Plaintext:", plainText2);
console.log("Key:", key2);
console.log("Ciphertext:", encrypted2);

const decrypted2 = monoalphabeticDecrypt({ cipherText: encrypted2, key: key2 });
console.log("Decrypted:", decrypted2);
