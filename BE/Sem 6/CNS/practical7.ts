function gcdS(a: number, b: number): number {
  let dividend = a;
  let divisor = b;

  console.log(`Finding GCD(${a}, ${b})`);

  while (divisor !== 0) {
    const remainder = dividend % divisor;
    console.log(`  ${dividend} % ${divisor} = ${remainder}`);
    dividend = divisor;
    divisor = remainder;
  }

  return dividend;
}

console.log("GCD(16, 12):");
const result1 = gcdS(16, 12);
console.log(`  GCD = ${result1}\n`);

console.log("GCD(48, 18):");
const result2 = gcdS(48, 18);
console.log(`  GCD = ${result2}\n`);

console.log("GCD(1071, 462):");
const result3 = gcdS(1071, 462);
console.log(`  GCD = ${result3}\n`);
