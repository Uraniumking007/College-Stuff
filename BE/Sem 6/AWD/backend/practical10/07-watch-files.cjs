// Practical 10: Basic File Operations using Node.js
// Example 7: Watching Files and Directories

const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');
const watchFile = path.join(dataDir, 'watch-me.txt');

console.log('=== File Watching Examples ===\n');

// Create a file to watch
fs.writeFileSync(watchFile, 'Initial content\n');

// 1. Watch a file for changes
console.log('1. Watching file for changes...');
console.log('   File:', watchFile);
console.log('   Try editing this file in another terminal or editor');
console.log('');

const fileWatcher = fs.watch(watchFile, (eventType, filename) => {
   console.log(`   📝 File changed! Event: ${eventType}`);
   console.log('   Current content:', fs.readFileSync(watchFile, 'utf8'));
});

// 2. Watch a directory for changes
console.log('2. Watching directory for changes...');
console.log('   Directory:', dataDir);
console.log('   Try adding/removing files in the data folder');
console.log('');

const dirWatcher = fs.watch(dataDir, (eventType, filename) => {
   if (filename) {
      console.log(`   📂 Directory changed! Event: ${eventType}, File: ${filename}`);
   } else {
      console.log('   📂 Directory changed! Event:', eventType);
   }
});

// 3. Demonstrate file changes programmatically
setTimeout(() => {
   console.log('\n3. Demonstrating programmatic changes...\n');

   // Append to file
   fs.appendFileSync(watchFile, 'Appended line 1\n');
   console.log('   → Appended line 1');

   setTimeout(() => {
      fs.appendFileSync(watchFile, 'Appended line 2\n');
      console.log('   → Appended line 2');

      setTimeout(() => {
         // Rename file
         const renamedFile = path.join(dataDir, 'watch-me-renamed.txt');
         fs.renameSync(watchFile, renamedFile);
         console.log('   → Renamed watch-me.txt to watch-me-renamed.txt');

         // Recreate for further watching
         setTimeout(() => {
            fs.writeFileSync(watchFile, 'Recreated file\n');
            console.log('   → Recreated watch-me.txt');

            // Create new file in directory
            setTimeout(() => {
               const newFile = path.join(dataDir, 'new-file.txt');
               fs.writeFileSync(newFile, 'New file created\n');
               console.log('   → Created new-file.txt');

               // Delete file from directory
               setTimeout(() => {
                  fs.unlinkSync(newFile);
                  console.log('   → Deleted new-file.txt');

                  setTimeout(() => {
                     // Stop watching and cleanup
                     console.log('\n4. Stopping watchers...');
                     fileWatcher.close();
                     dirWatcher.close();
                     console.log('   ✓ Watchers stopped');

                     // Cleanup test files
                     try {
                        fs.unlinkSync(path.join(dataDir, 'watch-me-renamed.txt'));
                        fs.unlinkSync(watchFile);
                        console.log('   ✓ Test files cleaned up');
                     } catch (err) {
                        // Ignore cleanup errors
                     }

                     console.log('\n✓ File watching demonstration completed!');
                     process.exit(0);
                  }, 1000);
               }, 1500);
            }, 1500);
         }, 1500);
      }, 1500);
   }, 1500);
}, 2000);

// Handle Ctrl+C gracefully
process.on('SIGINT', () => {
   console.log('\n\nReceived SIGINT, stopping watchers...');
   fileWatcher.close();
   dirWatcher.close();
   process.exit(0);
});

console.log('Watchers are active. Press Ctrl+C to stop early.\n');
