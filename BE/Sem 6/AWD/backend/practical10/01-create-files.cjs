// Practical 10: Basic File Operations using Node.js
// Example 1: Creating and Writing Files

const fs = require('fs');
const path = require('path');

// Create a data directory if it doesn't exist
const dataDir = path.join(__dirname, 'data');
if (!fs.existsSync(dataDir)) {
   fs.mkdirSync(dataDir);
}

console.log('=== File Creation Examples ===\n');

// 1. Write to a file (async - recommended)
fs.writeFile(
   path.join(dataDir, 'example.txt'),
   'Hello, this is my first file created with Node.js!',
   'utf8',
   (err) => {
      if (err) {
         console.error('Error writing file:', err);
         return;
      }
      console.log('✓ File created: example.txt');
   }
);

// 2. Write to a file (synchronous)
try {
   fs.writeFileSync(
      path.join(dataDir, 'sync-example.txt'),
      'This file was created synchronously!'
   );
   console.log('✓ File created (sync): sync-example.txt');
} catch (err) {
   console.error('Error writing file:', err);
}

// 3. Write JSON data to a file
const userData = {
   id: 1,
   name: 'John Doe',
   email: 'john@example.com',
   createdAt: new Date().toISOString()
};

fs.writeFile(
   path.join(dataDir, 'user-data.json'),
   JSON.stringify(userData, null, 2),
   'utf8',
   (err) => {
      if (err) {
         console.error('Error writing JSON:', err);
         return;
      }
      console.log('✓ JSON file created: user-data.json');
   }
);

// 4. Write multiple lines to a file
const lines = [
   'Line 1: Node.js file system is powerful',
   'Line 2: You can read, write, and update files',
   'Line 3: File operations can be sync or async',
   'Line 4: Always handle errors properly'
];

fs.writeFile(
   path.join(dataDir, 'lines.txt'),
   lines.join('\n'),
   'utf8',
   (err) => {
      if (err) {
         console.error('Error writing lines:', err);
         return;
      }
      console.log('✓ File with lines created: lines.txt');
   }
);

// 5. Create a file with a buffer (binary data)
const bufferData = Buffer.from('Hello from Buffer!');
fs.writeFile(
   path.join(dataDir, 'buffer-example.bin'),
   bufferData,
   (err) => {
      if (err) {
         console.error('Error writing buffer:', err);
         return;
      }
      console.log('✓ Binary file created: buffer-example.bin');
   }
);

setTimeout(() => {
   console.log('\nAll files created successfully!');
   console.log('Check the "data" folder to see the created files.');
   process.exit(0);
}, 1000);
