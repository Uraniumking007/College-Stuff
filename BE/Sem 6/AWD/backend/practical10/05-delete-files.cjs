// Practical 10: Basic File Operations using Node.js
// Example 5: Deleting and Renaming Files

const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');

console.log('=== File Delete and Rename Examples ===\n');

// Create test files first
const testFile1 = path.join(dataDir, 'to-be-deleted.txt');
const testFile2 = path.join(dataDir, 'to-be-renamed.txt');

fs.writeFileSync(testFile1, 'This file will be deleted');
fs.writeFileSync(testFile2, 'This file will be renamed');

console.log('✓ Test files created');
console.log('');

// 1. Delete file asynchronously
fs.unlink(testFile1, (err) => {
   if (err) {
      console.error('Error deleting file:', err);
      return;
   }
   console.log('1. Delete File (async):');
   console.log('   ✓ to-be-deleted.txt deleted');
   console.log('');
});

// 2. Delete file synchronously
const syncDeleteFile = path.join(dataDir, 'sync-delete.txt');
fs.writeFileSync(syncDeleteFile, 'This will be deleted synchronously');

try {
   fs.unlinkSync(syncDeleteFile);
   console.log('2. Delete File (sync):');
   console.log('   ✓ sync-delete.txt deleted');
   console.log('');
} catch (err) {
   console.error('Error deleting file:', err);
}

// 3. Rename file asynchronously
const newFileName = path.join(dataDir, 'renamed-file.txt');
fs.rename(testFile2, newFileName, (err) => {
   if (err) {
      console.error('Error renaming file:', err);
      return;
   }
   console.log('3. Rename File (async):');
   console.log('   ✓ to-be-renamed.txt → renamed-file.txt');
   console.log('');
});

// 4. Rename file synchronously
const oldFile = path.join(dataDir, 'lines.txt');
const newFile = path.join(dataDir, 'my-lines.txt');

try {
   fs.renameSync(oldFile, newFile);
   console.log('4. Rename File (sync):');
   console.log('   ✓ lines.txt → my-lines.txt');
   console.log('');
} catch (err) {
   console.log('4. Rename File (sync):');
   console.log('   ✗ File not found or error:', err.message);
   console.log('');
}

// 5. Move file to different location
const originalFile = path.join(dataDir, 'example.txt');
const backupDir = path.join(__dirname, 'backup');

// Create backup directory
if (!fs.existsSync(backupDir)) {
   fs.mkdirSync(backupDir);
}

const backupFile = path.join(backupDir, 'example-backup.txt');
fs.copyFile(originalFile, backupFile, (err) => {
   if (err) {
      console.error('Error copying file:', err);
      return;
   }
   console.log('5. Copy File:');
   console.log('   ✓ example.txt copied to backup/example-backup.txt');
   console.log('');
});

// 6. Delete multiple files matching pattern
setTimeout(() => {
   console.log('6. Delete Multiple Files:');
   const files = fs.readdirSync(dataDir);
   let deletedCount = 0;

   files.forEach((file) => {
      if (file.endsWith('.bin')) {
         const filePath = path.join(dataDir, file);
         try {
            fs.unlinkSync(filePath);
            console.log(`   ✓ Deleted: ${file}`);
            deletedCount++;
         } catch (err) {
            console.error(`   ✗ Error deleting ${file}:`, err.message);
         }
      }
   });

   if (deletedCount === 0) {
      console.log('   No .bin files found to delete');
   }
   console.log('');
}, 500);

// 7. Safe delete (with backup)
setTimeout(() => {
   const fileToBackupAndDelete = path.join(dataDir, 'sync-example.txt');
   const backupLocation = path.join(backupDir, 'sync-example-backup.txt');

   console.log('7. Safe Delete (with backup):');

   if (fs.existsSync(fileToBackupAndDelete)) {
      // Copy to backup first
      fs.copyFileSync(fileToBackupAndDelete, backupLocation);

      // Then delete original
      fs.unlinkSync(fileToBackupAndDelete);

      console.log('   ✓ File backed up to backup folder');
      console.log('   ✓ Original file deleted');
   } else {
      console.log('   ✗ File not found');
   }

   console.log('');
   console.log('✓ All delete/rename operations completed!');

   setTimeout(() => {
      process.exit(0);
   }, 500);
}, 1500);
