// Practical 10: Basic File Operations using Node.js
// Example 4: Getting File Information

const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');

console.log('=== File Information Examples ===\n');

// 1. Get file stats (async)
fs.stat(
   path.join(dataDir, 'example.txt'),
   (err, stats) => {
      if (err) {
         console.error('Error getting stats:', err);
         return;
      }

      console.log('1. File Stats (example.txt):');
      console.log('   Is file:', stats.isFile());
      console.log('   Is directory:', stats.isDirectory());
      console.log('   Size:', stats.size, 'bytes');
      console.log('   Created:', stats.birthtime);
      console.log('   Modified:', stats.mtime);
      console.log('   Accessed:', stats.atime);
      console.log('');
   }
);

// 2. Get file stats (sync)
try {
   const stats = fs.statSync(path.join(dataDir, 'sync-example.txt'));
   console.log('2. File Stats (sync-example.txt) - Sync:');
   console.log('   Size:', stats.size, 'bytes');
   console.log('   Permissions:', stats.mode.toString(8));
   console.log('');
} catch (err) {
   console.error('Error getting stats:', err);
}

// 3. Check file type
const checkFileType = (filePath) => {
   try {
      const stats = fs.statSync(filePath);
      if (stats.isFile()) {
         return 'File';
      } else if (stats.isDirectory()) {
         return 'Directory';
      } else if (stats.isSymbolicLink()) {
         return 'Symbolic Link';
      } else {
         return 'Other';
      }
   } catch (err) {
      return 'Does not exist';
   }
};

console.log('3. File Type Checks:');
console.log('   example.txt:', checkFileType(path.join(dataDir, 'example.txt')));
console.log('   sync-example.txt:', checkFileType(path.join(dataDir, 'sync-example.txt')));
console.log('   data folder:', checkFileType(dataDir));
console.log('   nonexistent.txt:', checkFileType(path.join(dataDir, 'nonexistent.txt')));
console.log('');

// 4. Check if file exists (async)
fs.access(
   path.join(dataDir, 'example.txt'),
   fs.constants.F_OK,
   (err) => {
      if (err) {
         console.log('4. File Access Check:');
         console.log('   ✗ example.txt is not accessible');
      } else {
         console.log('4. File Access Check:');
         console.log('   ✓ example.txt is accessible');
         console.log('');
      }
   }
);

// 5. Check file permissions
fs.access(
   path.join(dataDir, 'example.txt'),
   fs.constants.R_OK | fs.constants.W_OK,
   (err) => {
      if (err) {
         console.log('5. File Permissions:');
         console.log('   ✗ Cannot read and write');
      } else {
         console.log('5. File Permissions:');
         console.log('   ✓ Can read and write');
         console.log('');
      }
   }
);

// 6. List all files in directory with their sizes
fs.readdir(dataDir, (err, files) => {
   if (err) {
      console.error('Error reading directory:', err);
      return;
   }

   console.log('6. All Files in Data Directory:');
   files.forEach((file) => {
      const filePath = path.join(dataDir, file);
      const stats = fs.statSync(filePath);
      const type = stats.isDirectory() ? '[DIR]' : '[FILE]';
      console.log(`   ${type} ${file} - ${stats.size} bytes`);
   });
   console.log('');
});

// 7. Compare file modification times
setTimeout(() => {
   const file1 = path.join(dataDir, 'example.txt');
   const file2 = path.join(dataDir, 'sync-example.txt');

   const stats1 = fs.statSync(file1);
   const stats2 = fs.statSync(file2);

   console.log('7. File Modification Comparison:');
   console.log('   example.txt modified:', stats1.mtime);
   console.log('   sync-example.txt modified:', stats2.mtime);

   if (stats1.mtime > stats2.mtime) {
      console.log('   → example.txt is more recent');
   } else if (stats2.mtime > stats1.mtime) {
      console.log('   → sync-example.txt is more recent');
   } else {
      console.log('   → Both files modified at same time');
   }

   process.exit(0);
}, 1000);
