// Practical 10 Controller - Basic File Operations using Node.js
angular.module("app").controller("Practical10Controller", [
   "$scope",
   function($scope) {
      // Initialize scope variables
      $scope.practicalTitle = "Practical 10 - Basic File Operations using Node.js";
      $scope.practicalDescription =
         "Demonstrating fundamental file system operations using Node.js built-in fs module";

      // File operation examples data
      $scope.fileExamples = [
         {
            id: 1,
            title: "Create Files",
            file: "01-create-files.cjs",
            description: "Creating and writing files (async/sync)",
            features: [
               "Write files asynchronously and synchronously",
               "Create text files, JSON files, and binary files",
               "Create a data directory automatically",
            ],
            runCommand: "node 01-create-files.cjs",
         },
         {
            id: 2,
            title: "Read Files",
            file: "02-read-files.cjs",
            description: "Reading files (async/sync, text, JSON, binary)",
            features: [
               "Read files asynchronously and synchronously",
               "Read text, JSON, and binary files",
               "Read files line by line using streams",
               "Check file existence",
            ],
            runCommand: "node 02-read-files.cjs",
         },
         {
            id: 3,
            title: "Append to Files",
            file: "03-append-files.cjs",
            description: "Appending data to existing files",
            features: [
               "Append data to existing files",
               "Create and append to log files",
               "Append formatted data and JSON",
               "Demonstrates both async and sync methods",
            ],
            runCommand: "node 03-append-files.cjs",
         },
         {
            id: 4,
            title: "Get File Information",
            file: "04-file-info.cjs",
            description: "Getting file statistics and metadata",
            features: [
               "Get file statistics (size, dates, permissions)",
               "Check file types (file, directory, symbolic link)",
               "Check file existence and permissions",
               "List directory contents with details",
            ],
            runCommand: "node 04-file-info.cjs",
         },
         {
            id: 5,
            title: "Delete and Rename Files",
            file: "05-delete-files.cjs",
            description: "Deleting and renaming files",
            features: [
               "Delete files asynchronously and synchronously",
               "Rename and move files",
               "Copy files with backup",
               "Safe delete with backup before deletion",
            ],
            runCommand: "node 05-delete-files.cjs",
         },
         {
            id: 6,
            title: "Directory Operations",
            file: "06-directories.cjs",
            description: "Working with directories",
            features: [
               "Create directories (async/sync)",
               "Create nested directories recursively",
               "Read directory contents",
               "Delete empty and non-empty directories",
            ],
            runCommand: "node 06-directories.cjs",
         },
         {
            id: 7,
            title: "Watch Files",
            file: "07-watch-files.cjs",
            description: "Watching files and directories for changes",
            features: [
               "Watch files for changes",
               "Watch directories for changes",
               "Detect file creation, modification, and deletion",
               "Automatic cleanup and demonstration",
            ],
            runCommand: "node 07-watch-files.cjs",
         },
      ];

      // Common issues and solutions
      $scope.commonIssues = [
         {
            error: "ENOENT: no such file or directory",
            solution: "Run 01-create-files.cjs first to generate required test files",
         },
         {
            error: "EACCES: permission denied",
            solution: "Check file/folder permissions. Avoid running as root.",
         },
         {
            error: "EEXIST: file already exists",
            solution:
               "Some examples check for existence. Delete the data/ folder to start fresh.",
         },
      ];

      // Tips
      $scope.tips = [
         "Run in order: Start with 01-create-files.cjs to generate test data",
         "Clean slate: Each run creates/overwrites files - no manual cleanup needed",
         "Error messages: Watch for error messages - they indicate missing prerequisites",
         "Data folder: All file operations use the data/ subdirectory",
         "Stop execution: Press Ctrl+C to stop any running example",
         "File watchers: Example 7 runs automatically - no manual interaction needed",
      ];

      // File system methods reference
      $scope.fsMethods = [
         { name: "writeFile", description: "Write data to file", async: "✓", sync: "✓" },
         { name: "readFile", description: "Read file contents", async: "✓", sync: "✓" },
         { name: "appendFile", description: "Append data to file", async: "✓", sync: "✓" },
         { name: "unlink", description: "Delete file", async: "✓", sync: "✓" },
         { name: "rename", description: "Rename/move file", async: "✓", sync: "✓" },
         { name: "copyFile", description: "Copy file", async: "✓", sync: "✓" },
         { name: "mkdir", description: "Create directory", async: "✓", sync: "✓" },
         { name: "readdir", description: "Read directory", async: "✓", sync: "✓" },
         { name: "rmdir", description: "Remove empty directory", async: "✓", sync: "✓" },
         { name: "rm", description: "Remove (recursive)", async: "✓", sync: "✓" },
         { name: "stat", description: "Get file stats", async: "✓", sync: "✓" },
         { name: "exists", description: "Check if exists", async: "✓", sync: "✓" },
         { name: "access", description: "Check permissions", async: "✓", sync: "✓" },
         { name: "watch", description: "Watch for changes", async: "✓", sync: "✗" },
      ];

      // Log controller initialization
      console.log("Practical10Controller loaded");
      console.log("Practical:", $scope.practicalTitle);
   },
]);
