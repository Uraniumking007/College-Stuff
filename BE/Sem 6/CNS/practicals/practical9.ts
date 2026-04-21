// ===========================================
// PRACTICAL 9: Random Number Generators
// ===========================================

// ----------------------
// TYPE DEFINITIONS
// ----------------------

interface LCGParameters {
   seed: number
   a?: number
   c?: number
   m?: number
}

interface BBSParameters {
   seed: number
   p?: number
   q?: number
}

interface TestResult {
   method: string
   uniformity: { pass: boolean; score: string }
   scalability: { pass: boolean; score: string }
   consistency: { pass: boolean; score: string }
   overall: string
}

// ----------------------
// LINEAR CONGRUENTIAL GENERATOR
// Formula: X(n+1) = (a * X(n) + c) mod m
// ----------------------

function linearCongruentialGenerator(params: LCGParameters): number[] {
   const { seed, a = 1103515245, c = 12345, m = Math.pow(2, 32) } = params
   const numbers: number[] = []
   let current = seed

   for (let i = 0; i < 1000; i++) {
      current = (a * current + c) % m
      numbers.push(current)
   }

   return numbers
}

// ----------------------
// BLUM BLUM SHUB GENERATOR
// Formula: X(n+1) = X(n)^2 mod n, where n = p * q
// Output bit: X(n+1) mod 2
// ----------------------

function blumBlumShubGenerator(params: BBSParameters): number[] {
   const { seed, p = 499, q = 523 } = params
   const n = p * q
   const numbers: number[] = []
   let current = seed % n

   // Generate 32-bit numbers (1000 numbers for testing)
   let bitBuffer = 0
   let bitsCollected = 0
   let numberCount = 0

   while (numberCount < 1000) {
      current = (current * current) % n
      const bit = current % 2

      bitBuffer = (bitBuffer << 1) | bit
      bitsCollected++

      if (bitsCollected === 32) {
         // Convert to unsigned 32-bit integer
         numbers.push(bitBuffer >>> 0)
         bitBuffer = 0
         bitsCollected = 0
         numberCount++
      }
   }

   return numbers
}

// ----------------------
// TEST 1: UNIFORMITY TEST
// Checks if numbers are evenly distributed
// ----------------------

function testUniformity(numbers: number[], methodName: string): { pass: boolean; score: string } {
   const binCount = 10
   const bins = new Array(binCount).fill(0)
   const max = Math.pow(2, 32)

   // Count numbers in each bin
   for (const num of numbers) {
      const binIndex = Math.floor((num / max) * binCount)
      bins[Math.min(binIndex, binCount - 1)]++
   }

   // Expected count per bin
   const expected = numbers.length / binCount
   const chiSquared = bins.reduce((sum, count) => {
      return sum + Math.pow(count - expected, 2) / expected
   }, 0)

   // Chi-squared critical value for 9 degrees of freedom at 0.05 significance: ~16.9
   const pass = chiSquared < 16.9
   const score = `χ² = ${chiSquared.toFixed(2)} (critical: 16.9)`

   console.log(`\n  ${methodName} Uniformity Test:`)
   console.log(`    Bins: [${bins.join(", ")}]`)
   console.log(`    ${score}`)

   return { pass, score }
}

// ----------------------
// TEST 2: SCALABILITY TEST
// Checks if generator works for different output sizes
// ----------------------

function testScalability(methodName: string): { pass: boolean; score: string } {
   // Use larger sizes to get measurable times
   const sizes = [10000, 100000, 1000000]
   const results: number[] = []

   for (const size of sizes) {
      const start = performance.now()

      if (methodName === "LCG") {
         let current = 12345
         const a = 1103515245, c = 12345, m = Math.pow(2, 32)
         for (let i = 0; i < size; i++) {
            current = (a * current + c) % m
         }
      } else {
         const p = 499, q = 523, n = p * q
         let current = 12345 % n
         for (let i = 0; i < size; i++) {
            current = (current * current) % n
         }
      }

      const elapsed = performance.now() - start
      results.push(elapsed)
   }

   // Check if time scales roughly linearly (expect ~10x for 10x size increase)
   const ratio1 = results[1] / results[0]
   const ratio2 = results[2] / results[1]
   const pass = Math.abs(ratio1 - 10) < 3 && Math.abs(ratio2 - 10) < 3

   const score = `Times: ${results.map(r => r.toFixed(2) + "ms").join(", ")} (ratios: ${ratio1.toFixed(2)}, ${ratio2.toFixed(2)})`

   console.log(`\n  ${methodName} Scalability Test:`)
   console.log(`    ${score}`)

   return { pass, score }
}

// ----------------------
// TEST 3: CONSISTENCY TEST
// Checks if same seed produces same output
// ----------------------

function testConsistency(methodName: string): { pass: boolean; score: string } {
   const seed = 42
   let run1: number[], run2: number[]

   if (methodName === "LCG") {
      run1 = linearCongruentialGenerator({ seed }).slice(0, 10)
      run2 = linearCongruentialGenerator({ seed }).slice(0, 10)
   } else {
      run1 = blumBlumShubGenerator({ seed }).slice(0, 10)
      run2 = blumBlumShubGenerator({ seed }).slice(0, 10)
   }

   let pass = true
   for (let i = 0; i < run1.length; i++) {
      if (run1[i] !== run2[i]) {
         pass = false
         break
      }
   }

   const score = pass ? "Same output for same seed ✓" : "Different output for same seed ✗"

   console.log(`\n  ${methodName} Consistency Test:`)
   console.log(`    Run 1: [${run1.slice(0, 5).join(", ")}...]`)
   console.log(`    Run 2: [${run2.slice(0, 5).join(", ")}...]`)
   console.log(`    ${score}`)

   return { pass, score }
}

// ----------------------
// MAIN EXECUTION
// ----------------------

function runAllTests(): TestResult[] {
   console.log("╔════════════════════════════════════════════════════════════╗")
   console.log("║     PRACTICAL 9: Random Number Generator Comparison       ║")
   console.log("╚════════════════════════════════════════════════════════════╝")

   const seed = 12345

   // Test LCG
   console.log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
   console.log("METHOD 1: LINEAR CONGRUENTIAL GENERATOR")
   console.log("Formula: X(n+1) = (a * X(n) + c) mod m")
   console.log("Parameters: a = 1103515245, c = 12345, m = 2^32")

   const lcgNumbers = linearCongruentialGenerator({ seed })
   console.log(`\nFirst 10 32-bit numbers (seed = ${seed}):`)
   console.log(`[${lcgNumbers.slice(0, 10).join(", ")}]`)

   const lcgUniformity = testUniformity(lcgNumbers, "LCG")
   const lcgScalability = testScalability("LCG")
   const lcgConsistency = testConsistency("LCG")

   // Test BBS
   console.log("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
   console.log("METHOD 2: BLUM BLUM SHUB GENERATOR")
   console.log("Formula: X(n+1) = X(n)^2 mod n (n = p * q)")
   console.log("Parameters: p = 499, q = 523 (both ≡ 3 mod 4)")

   const bbsNumbers = blumBlumShubGenerator({ seed })
   console.log(`\nFirst 10 32-bit numbers (seed = ${seed}):`)
   console.log(`[${bbsNumbers.slice(0, 10).join(", ")}]`)

   const bbsUniformity = testUniformity(bbsNumbers, "BBS")
   const bbsScalability = testScalability("BBS")
   const bbsConsistency = testConsistency("BBS")

   // Final Comparison
   console.log("\n╔════════════════════════════════════════════════════════════╗")
   console.log("║                    FINAL RESULTS                           ║")
   console.log("╚════════════════════════════════════════════════════════════╝")

   const lcgResult: TestResult = {
      method: "Linear Congruential Generator",
      uniformity: lcgUniformity,
      scalability: lcgScalability,
      consistency: lcgConsistency,
      overall: ""
   }

   const bbsResult: TestResult = {
      method: "Blum Blum Shub",
      uniformity: bbsUniformity,
      scalability: bbsScalability,
      consistency: bbsConsistency,
      overall: ""
   }

   // Determine winner
   const lcgPasses = [lcgUniformity.pass, lcgScalability.pass, lcgConsistency.pass].filter(Boolean).length
   const bbsPasses = [bbsUniformity.pass, bbsScalability.pass, bbsConsistency.pass].filter(Boolean).length

   lcgResult.overall = lcgPasses === 3 ? "PASS ✓" : lcgPasses >= 2 ? "PARTIAL ~" : "FAIL ✗"
   bbsResult.overall = bbsPasses === 3 ? "PASS ✓" : bbsPasses >= 2 ? "PARTIAL ~" : "FAIL ✗"

   // Print summary table
   console.log("\n┌────────────────────────────────┬───────────┬───────────┬───────────┬──────────┐")
   console.log("│ Method                         │ Uniformity│ Scalability│ Consistency│ Overall  │")
   console.log("├────────────────────────────────┼───────────┼───────────┼───────────┼──────────┤")
   console.log(`│ LCG                            │ ${lcgUniformity.pass ? "PASS      " : "FAIL      "}│ ${lcgScalability.pass ? "PASS      " : "FAIL      "}│ ${lcgConsistency.pass ? "PASS      " : "FAIL      "}│ ${lcgResult.overall} │`)
   console.log(`│ Blum Blum Shub                 │ ${bbsUniformity.pass ? "PASS      " : "FAIL      "}│ ${bbsScalability.pass ? "PASS      " : "FAIL      "}│ ${bbsConsistency.pass ? "PASS      " : "FAIL      "}│ ${bbsResult.overall} │`)
   console.log("└────────────────────────────────┴───────────┴───────────┴───────────┴──────────┘")

   console.log("\n📊 CONCLUSION:")
   if (lcgPasses > bbsPasses) {
      console.log("   → Linear Congruential Generator performs better")
      console.log("   → Faster and more uniform distribution")
   } else if (bbsPasses > lcgPasses) {
      console.log("   → Blum Blum Shub performs better")
      console.log("   → Cryptographically stronger but slower")
   } else {
      console.log("   → Both methods perform equally well")
   }

   console.log("\n" + "─".repeat(66))
   console.log("  NOTES:")
   console.log("  • LCG: Fast, simple, good for simulations")
   console.log("  • BBS: Slower, cryptographically secure, good for security")
   console.log("  • Best choice depends on use case: speed vs security")
   console.log("─".repeat(66))

   return [lcgResult, bbsResult]
}

// Run the tests
runAllTests()
