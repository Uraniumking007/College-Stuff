interface ColumnarTranspositionEncryptParameters {
   plainText: string
   key: string
}

interface ColumnarTranspositionDecryptParameters {
   cipherText: string
   key: string
}

function validateKey(key: string): void {
   if (!key || key.length === 0) {
      throw new Error("Key cannot be empty")
   }

   if (!/^\d+$/.test(key)) {
      throw new Error("Key must contain only digits")
   }

   const keyDigits = key.split('').map(Number)
   const expected = Array.from({ length: key.length }, (_, i) => i + 1)
   const sorted = [...keyDigits].sort((a, b) => a - b)

   for (let i = 0; i < sorted.length; i++) {
      if (sorted[i] !== expected[i]) {
         throw new Error(`Key must be a permutation of 1 to ${key.length}`)
      }
   }
}

function getReadingOrder(key: string): number[] {
   const keyDigits = key.split('').map(Number)
   const order: number[] = []

   const pairs = keyDigits.map((value, index) => ({ value, index }))
   pairs.sort((a, b) => a.value - b.value)

   for (const pair of pairs) {
      order.push(pair.index)
   }

   return order
}

function columnarTranspositionEncrypt({
   plainText,
   key
}: ColumnarTranspositionEncryptParameters): string {
   validateKey(key)

   const normalizedText = plainText.toUpperCase().replace(/\s+/g, '')
   const numCols = key.length
   const numRows = Math.ceil(normalizedText.length / numCols)

   const grid: string[][] = Array.from({ length: numRows }, () =>
      Array(numCols).fill('')
   )

   let index = 0
   for (let row = 0; row < numRows; row++) {
      for (let col = 0; col < numCols; col++) {
         if (index < normalizedText.length) {
            grid[row][col] = normalizedText[index++]
         }
      }
   }

   const readingOrder = getReadingOrder(key)

   let result = ''
   for (const col of readingOrder) {
      for (let row = 0; row < numRows; row++) {
         result += grid[row][col]
      }
   }

   return result
}

function columnarTranspositionDecrypt({
   cipherText,
   key
}: ColumnarTranspositionDecryptParameters): string {
   validateKey(key)

   const normalizedText = cipherText.toUpperCase().replace(/\s+/g, '')
   const numCols = key.length
   const numRows = Math.ceil(normalizedText.length / numCols)

   const totalChars = normalizedText.length
   const fullRows = Math.floor(totalChars / numCols)
   const remainder = totalChars % numCols

   const colLengths: number[] = []
   for (let i = 0; i < numCols; i++) {
      colLengths.push(fullRows + (i < remainder ? 1 : 0))
   }

   const readingOrder = getReadingOrder(key)

   const grid: string[][] = Array.from({ length: numRows }, () =>
      Array(numCols).fill('')
   )

   let textIndex = 0
   for (const col of readingOrder) {
      const colLength = colLengths[col]
      for (let row = 0; row < colLength; row++) {
         grid[row][col] = normalizedText[textIndex++]
      }
   }

   let result = ''
   for (let row = 0; row < numRows; row++) {
      for (let col = 0; col < numCols; col++) {
         result += grid[row][col]
      }
   }

   return result
}

function demonstrateColumnarTranspositionCipher(): void {
   const key = "4312567"
   const plainText = "attackpostponeduntiltwoam"

   const encrypted = columnarTranspositionEncrypt({ plainText, key })
   const decrypted = columnarTranspositionDecrypt({ cipherText: encrypted, key })
   console.log("Key:", key)
   console.log("Plaintext:", plainText)
   console.log("Ciphertext:", encrypted)
   console.log("Decrypted:", decrypted)
   console.log("Match:", decrypted.toLowerCase() === plainText.toLowerCase())

   const plainText2 = "Enemyattackstonight"
   const key2 = "3142"

   const encrypted2 = columnarTranspositionEncrypt({ plainText: plainText2, key: key2 })
   const decrypted2 = columnarTranspositionDecrypt({ cipherText: encrypted2, key: key2 })
   console.log("Key:", key2)
   console.log("Plaintext:", plainText2)
   console.log("Ciphertext:", encrypted2)
   console.log("Decrypted:", decrypted2)
   console.log("Match:", decrypted2.toLowerCase() === plainText2.toLowerCase())
}

demonstrateColumnarTranspositionCipher()
