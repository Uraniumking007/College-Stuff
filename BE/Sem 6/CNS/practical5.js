/**
 * File Size Modifier
 * 
 * A utility to modify file size by adding specified bytes to a file
 * This demonstrates file manipulation and size calculation
 */
function modifyFileSize(options) {
  const { filePath, bytesToAdd } = options;
  
  if (bytesToAdd < 0) {
    throw new Error("Bytes to add must be non-negative");
  }

  console.log(`Modifying file: ${filePath}`);
  console.log(`Adding ${bytesToAdd} bytes to file size`);
  
  // Create a dummy file with initial content
  const initialContent = "Initial file content with some text data";
  const initialSize = initialContent.length;
  
  console.log(`Initial file size: ${initialSize} bytes`);
  console.log(`Initial content: "${initialContent}"`);
  
  // Generate random data to add
  const randomData = generateRandomData(bytesToAdd);
  const finalContent = initialContent + randomData;
  const finalSize = finalContent.length;
  
  console.log(`Generated ${bytesToAdd} bytes of random data`);
  console.log(`Final file size: ${finalSize} bytes`);
  console.log(`Size increase: ${finalSize - initialSize} bytes`);
  console.log(`Final content preview: "${finalContent.substring(0, 50)}..."`);
}

/**
 * Generate random data of specified size
 */
function generateRandomData(size) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < size; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
}

// ============ TEST CASE ============
console.log("=".repeat(60));
console.log("FILE SIZE MODIFIER - TEST CASE");
console.log("=".repeat(60));

const TEST_FILE = "testfile.txt";
const BYTES_TO_ADD = 1024; // 1KB

console.log(`\nFile to modify: ${TEST_FILE}`);
console.log(`Bytes to add: ${BYTES_TO_ADD}`);

try {
  modifyFileSize({
    filePath: TEST_FILE,
    bytesToAdd: BYTES_TO_ADD
  });
  
  console.log("\n✓ File size modification completed successfully");
  console.log("Note: In a real implementation, this would modify an actual file");
  console.log("For this demo, we're simulating file size modification");
  
} catch (error) {
  console.log(`\n✗ Error: ${error.message}`);
}