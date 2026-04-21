interface RSAKeyPair {
   p: number
   q: number
   n: number
   phi: number
   e: number
   d: number
}

interface RSAEncryptParameters {
   message: number
   e: number
   n: number
}

interface RSADecryptParameters {
   ciphertext: number
   d: number
   n: number
}

function rsaGcd(a: number, b: number): number {
   a = Math.abs(a)
   b = Math.abs(b)
   while (b !== 0) {
      const temp = b
      b = a % b
      a = temp
   }
   return a
}

function modPow(base: number, exp: number, mod: number): number {
   if (mod === 1) return 0

   let result = 1
   base = base % mod

   while (exp > 0) {
      if (exp % 2 === 1) {
         result = (result * base) % mod
      }
      base = (base * base) % mod
      exp = Math.floor(exp / 2)
   }

   return result
}

function rsaModInverse(e: number, phi: number): number {
   let m0 = phi
   let y = 0
   let x = 1

   if (phi === 1) return 0

   let a = e
   let b = phi

   while (a > 1) {
      const q = Math.floor(a / b)

      let t = b
      b = a % b
      a = t

      t = y
      y = x - q * y
      x = t
   }

   if (x < 0) x += m0

   return x
}

function isPrime(num: number): boolean {
   if (num <= 1) return false
   if (num <= 3) return true
   if (num % 2 === 0 || num % 3 === 0) return false

   for (let i = 5; i * i <= num; i += 6) {
      if (num % i === 0 || num % (i + 2) === 0) {
         return false
      }
   }
   return true
}

function generateRSAKeyPair(p: number, q: number, e: number): RSAKeyPair {
   if (!isPrime(p)) {
      throw new Error(`p must be prime: ${p} is not prime`)
   }
   if (!isPrime(q)) {
      throw new Error(`q must be prime: ${q} is not prime`)
   }
   if (p === q) {
      throw new Error("p and q must be different primes")
   }

   const n = p * q
   const phi = (p - 1) * (q - 1)

   if (e <= 1 || e >= phi) {
      throw new Error(`e must satisfy 1 < e < φ(n): 1 < ${e} < ${phi}`)
   }

   if (rsaGcd(e, phi) !== 1) {
      throw new Error(`e must be coprime with φ(n): gcd(${e}, ${phi}) = ${rsaGcd(e, phi)}`)
   }

   const d = rsaModInverse(e, phi)

   return { p, q, n, phi, e, d }
}

function rsaEncrypt({ message, e, n }: RSAEncryptParameters): number {
   if (message >= n) {
      throw new Error(`Message must be less than n: ${message} >= ${n}`)
   }
   if (message < 0) {
      throw new Error(`Message must be non-negative: ${message}`)
   }

   return modPow(message, e, n)
}

function rsaDecrypt({ ciphertext, d, n }: RSADecryptParameters): number {
   if (ciphertext >= n) {
      throw new Error(`Ciphertext must be less than n: ${ciphertext} >= ${n}`)
   }
   if (ciphertext < 0) {
      throw new Error(`Ciphertext must be non-negative: ${ciphertext}`)
   }

   return modPow(ciphertext, d, n)
}

function demonstrateRSAAlgorithm(): void {
   const keyPair = generateRSAKeyPair(17, 11, 7)
   const message = 88
   const ciphertext = rsaEncrypt({ message, e: keyPair.e, n: keyPair.n })
   const decrypted = rsaDecrypt({ ciphertext, d: keyPair.d, n: keyPair.n })

   console.log("Test 1: p=17, q=11, e=7, M=88")
   console.log("n:", keyPair.n, "phi:", keyPair.phi, "d:", keyPair.d)
   console.log("d expected 23, match:", keyPair.d === 23)
   console.log("Ciphertext:", ciphertext, "expected 11, match:", ciphertext === 11)
   console.log("Decrypted:", decrypted, "match:", decrypted === message)

   const keyPair2 = generateRSAKeyPair(61, 53, 17)
   const message2 = 123
   const ciphertext2 = rsaEncrypt({ message: message2, e: keyPair2.e, n: keyPair2.n })
   const decrypted2 = rsaDecrypt({ ciphertext: ciphertext2, d: keyPair2.d, n: keyPair2.n })

   console.log("Test 2: p=61, q=53, e=17, M=123")
   console.log("n:", keyPair2.n, "phi:", keyPair2.phi, "d:", keyPair2.d)
   console.log("Ciphertext:", ciphertext2)
   console.log("Decrypted:", decrypted2, "match:", decrypted2 === message2)
}

demonstrateRSAAlgorithm()
