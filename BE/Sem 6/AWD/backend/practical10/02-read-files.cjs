// Practical 10: Basic File Operations using Node.js
// Example 2: Reading Files

const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');

console.log('=== File Reading Examples ===\n');

// 1. Read file asynchronously (recommended)
fs.readFile(
   path.join(dataDir, 'example.txt'),
   'utf8',
   (err, data) => {
      if (err) {
         console.error('Error reading file:', err);
         return;
      }
      console.log('1. Read file (async):');
      console.log('   Content:', data);
      console.log('');
   }
);

// 2. Read file synchronously
try {
   const data = fs.readFileSync(
      path.join(dataDir, 'sync-example.txt'),
      'utf8'
   );
   console.log('2. Read file (sync):');
   console.log('   Content:', data);
   console.log('');
} catch (err) {
   console.error('Error reading file:', err);
}

// 3. Read JSON file
fs.readFile(
   path.join(dataDir, 'user-data.json'),
   'utf8',
   (err, data) => {
      if (err) {
         console.error('Error reading JSON:', err);
         return;
      }
      const userData = JSON.parse(data);
      console.log('3. Read JSON file:');
      console.log('   Parsed data:', userData);
      console.log('');
   }
);

// 4. Read file as Buffer (binary data)
fs.readFile(
   path.join(dataDir, 'buffer-example.bin'),
   (err, data) => {
      if (err) {
         console.error('Error reading buffer:', err);
         return;
      }
      console.log('4. Read binary file:');
      console.log('   Buffer length:', data.length);
      console.log('   Decoded:', data.toString('utf8'));
      console.log('');
   }
);

// 5. Read file line by line (using streams)
const readline = require('readline');
const fileStream = fs.createReadStream(path.join(dataDir, 'lines.txt'));

const rl = readline.createInterface({
   input: fileStream,
   crlfDelay: Infinity
});

console.log('5. Read file line by line:');
rl.on('line', (line) => {
   console.log('   ', line);
});

rl.on('close', () => {
   console.log('');
   console.log('✓ All reading operations completed!');
   process.exit(0);
});

// 6. Check if file exists before reading
const filePath = path.join(dataDir, 'example.txt');
if (fs.existsSync(filePath)) {
   console.log('6. File exists check:');
   console.log('   ✓ example.txt exists');
   console.log('');
} else {
   console.log('6. File exists check:');
   console.log('   ✗ example.txt does not exist');
   console.log('');
}
