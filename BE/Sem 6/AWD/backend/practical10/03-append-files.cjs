// Practical 10: Basic File Operations using Node.js
// Example 3: Appending to Files

const fs = require('fs');
const path = require('path');

const dataDir = path.join(__dirname, 'data');
const logFile = path.join(dataDir, 'app.log');

console.log('=== File Append Examples ===\n');

// 1. Create initial log file
fs.writeFileSync(logFile, 'Log file created at ' + new Date().toISOString() + '\n');
console.log('✓ Initial log file created');

// 2. Append to file asynchronously
fs.appendFile(
   logFile,
   'INFO: Application started\n',
   (err) => {
      if (err) {
         console.error('Error appending to file:', err);
         return;
      }
      console.log('✓ Appended (async): INFO message');

      // Append another line
      fs.appendFile(
         logFile,
         'INFO: User logged in\n',
         (err) => {
            if (err) {
               console.error('Error appending:', err);
               return;
            }
            console.log('✓ Appended (async): User login');
         }
      );
   }
);

// 3. Append to file synchronously
try {
   fs.appendFileSync(logFile, 'DEBUG: Debug information logged\n');
   console.log('✓ Appended (sync): DEBUG message');
} catch (err) {
   console.error('Error appending:', err);
}

// 4. Append multiple lines
const logEntries = [
   'WARN: High memory usage detected',
   'ERROR: Connection timeout',
   'INFO: Retrying connection...'
];

logEntries.forEach((entry, index) => {
   setTimeout(() => {
      fs.appendFile(
         logFile,
         entry + '\n',
         (err) => {
            if (err) {
               console.error('Error appending log:', err);
               return;
            }
            console.log(`✓ Appended: ${entry}`);
         }
      );
   }, (index + 1) * 500);
});

// 5. Append formatted data
const userData = {
   name: 'Jane Doe',
   action: 'file_upload',
   timestamp: new Date().toISOString()
};

setTimeout(() => {
   fs.appendFile(
      logFile,
      JSON.stringify(userData) + '\n',
      (err) => {
         if (err) {
            console.error('Error appending JSON:', err);
            return;
         }
         console.log('✓ Appended: JSON log entry');

         // Display final file content
         setTimeout(() => {
            console.log('\n=== Final Log File Content ===');
            const content = fs.readFileSync(logFile, 'utf8');
            console.log(content);
            process.exit(0);
         }, 500);
      }
   );
}, 3000);
