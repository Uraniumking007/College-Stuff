// Practical 10: Basic File Operations using Node.js
// Example 6: Working with Directories

const fs = require('fs');
const path = require('path');

console.log('=== Directory Operations Examples ===\n');

const basePath = __dirname;

// 1. Create directory asynchronously
const newDir = path.join(basePath, 'new-folder');
fs.mkdir(newDir, (err) => {
   if (err) {
      if (err.code === 'EEXIST') {
         console.log('1. Create Directory (async):');
         console.log('   ✗ Directory already exists');
      } else {
         console.error('Error creating directory:', err);
      }
   } else {
      console.log('1. Create Directory (async):');
      console.log('   ✓ new-folder created');
   }
   console.log('');
});

// 2. Create directory synchronously
const syncDir = path.join(basePath, 'sync-folder');
try {
   fs.mkdirSync(syncDir);
   console.log('2. Create Directory (sync):');
   console.log('   ✓ sync-folder created');
   console.log('');
} catch (err) {
   if (err.code === 'EEXIST') {
      console.log('2. Create Directory (sync):');
      console.log('   ✗ Directory already exists');
      console.log('');
   }
}

// 3. Create nested directories (recursive)
const nestedDir = path.join(basePath, 'parent', 'child', 'grandchild');
fs.mkdir(nestedDir, { recursive: true }, (err) => {
   if (err) {
      console.error('Error creating nested directories:', err);
   } else {
      console.log('3. Create Nested Directories:');
      console.log('   ✓ parent/child/grandchild created');
      console.log('');
   }
});

// 4. Read directory contents asynchronously
fs.readdir(basePath, (err, files) => {
   if (err) {
      console.error('Error reading directory:', err);
      return;
   }

   console.log('4. Read Directory Contents (async):');
   console.log(`   Found ${files.length} items in: ${basePath}`);
   files.slice(0, 10).forEach((file) => {
      console.log('   -', file);
   });
   if (files.length > 10) {
      console.log('   ... and', files.length - 10, 'more items');
   }
   console.log('');
});

// 5. Read directory contents with details
setTimeout(() => {
   console.log('5. Read Directory with Details:');
   const files = fs.readdirSync(basePath);

   files.forEach((file) => {
      const filePath = path.join(basePath, file);
      const stats = fs.statSync(filePath);

      const type = stats.isDirectory() ? '[DIR]' : '[FILE]';
      const size = stats.isFile() ? `(${stats.size} bytes)` : '';
      const modified = stats.mtime.toLocaleDateString();

      console.log(`   ${type} ${file} ${size} - Modified: ${modified}`);
   });
   console.log('');
}, 500);

// 6. Check if path is directory
const checkPath = (targetPath) => {
   try {
      const stats = fs.statSync(targetPath);
      return stats.isDirectory();
   } catch (err) {
      return false;
   }
};

console.log('6. Directory Checks:');
console.log('   data folder exists:', checkPath(path.join(basePath, 'data')));
console.log('   new-folder exists:', checkPath(newDir));
console.log('   nonexistent exists:', checkPath(path.join(basePath, 'nonexistent')));
console.log('');

// 7. Delete directory (must be empty)
const emptyDir = path.join(basePath, 'temp-folder');
fs.mkdirSync(emptyDir);
fs.writeFileSync(path.join(emptyDir, 'temp.txt'), 'temp');

// First delete files in directory
fs.unlinkSync(path.join(emptyDir, 'temp.txt'));

// Then delete empty directory
fs.rmdir(emptyDir, (err) => {
   if (err) {
      console.error('Error deleting directory:', err);
   } else {
      console.log('7. Delete Empty Directory:');
      console.log('   ✓ temp-folder deleted');
      console.log('');
   }
});

// 8. Delete directory recursively (Node 14.14.0+)
const dirToDelete = path.join(basePath, 'delete-me');
fs.mkdirSync(dirToDelete, { recursive: true });
fs.writeFileSync(path.join(dirToDelete, 'file.txt'), 'content');

setTimeout(() => {
   fs.rm(dirToDelete, { recursive: true, force: true }, (err) => {
      if (err) {
         console.error('Error deleting directory:', err);
      } else {
         console.log('8. Delete Directory Recursive:');
         console.log('   ✓ delete-me folder deleted (with contents)');
         console.log('');
      }
   });
}, 1000);

// 9. Rename/move directory
const oldDirName = path.join(basePath, 'old-name');
const newDirName = path.join(basePath, 'new-name');

if (!fs.existsSync(oldDirName)) {
   fs.mkdirSync(oldDirName);
}

setTimeout(() => {
   fs.rename(oldDirName, newDirName, (err) => {
      if (err) {
         console.log('9. Rename Directory:');
         console.log('   ✗ Error:', err.message);
      } else {
         console.log('9. Rename Directory:');
         console.log('   ✓ old-name → new-name');
         console.log('');
      }

      console.log('✓ All directory operations completed!');
      process.exit(0);
   });
}, 1500);
