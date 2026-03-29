# Practical 10: Basic File Operations using Node.js

This directory contains practical examples demonstrating fundamental file system operations using Node.js's built-in `fs` module for backend development.

## Overview

Each example file demonstrates a different aspect of Node.js file system operations:

1. **01-create-files.cjs** - Creating and writing files (async/sync)
2. **02-read-files.cjs** - Reading files (async/sync, text, JSON, binary)
3. **03-append-files.cjs** - Appending data to existing files
4. **04-file-info.cjs** - Getting file statistics and metadata
5. **05-delete-files.cjs** - Deleting and renaming files
6. **06-directories.cjs** - Working with directories (create, read, delete)
7. **07-watch-files.cjs** - Watching files and directories for changes

## Prerequisites

- Node.js installed (v14 or higher recommended)
- Basic understanding of JavaScript
- Terminal/command prompt access

## Running the Examples

Each example is independent and can be run individually:

### 1. Create Files

```bash
cd backend/practical10
node 01-create-files.cjs
```

**Features:**
- Write files asynchronously and synchronously
- Create text files, JSON files, and binary files
- Create a data directory automatically

**Output:**
- Creates a `data/` folder with multiple example files
- Demonstrates different write methods

### 2. Read Files

```bash
cd backend/practical10
node 02-read-files.cjs
```

**Features:**
- Read files asynchronously and synchronously
- Read text, JSON, and binary files
- Read files line by line using streams
- Check file existence

**Note:** Run `01-create-files.cjs` first to generate the data files.

### 3. Append to Files

```bash
cd backend/practical10
node 03-append-files.cjs
```

**Features:**
- Append data to existing files
- Create and append to log files
- Append formatted data and JSON
- Demonstrates both async and sync methods

**Output:**
- Creates `data/app.log` with various log entries

### 4. Get File Information

```bash
cd backend/practical10
node 04-file-info.cjs
```

**Features:**
- Get file statistics (size, dates, permissions)
- Check file types (file, directory, symbolic link)
- Check file existence and permissions
- List directory contents with details
- Compare file modification times

**Note:** Requires files from `01-create-files.cjs`.

### 5. Delete and Rename Files

```bash
cd backend/practical10
node 05-delete-files.cjs
```

**Features:**
- Delete files asynchronously and synchronously
- Rename and move files
- Copy files with backup
- Safe delete with backup before deletion
- Delete multiple files matching a pattern

**Warning:** This will delete and rename files. Run `01-create-files.cjs` first to generate test files.

### 6. Directory Operations

```bash
cd backend/practical10
node 06-directories.cjs
```

**Features:**
- Create directories (async/sync)
- Create nested directories recursively
- Read directory contents
- Check if path is a directory
- Delete empty directories
- Delete directories recursively
- Rename/move directories

**Output:**
- Creates and manages various test directories

### 7. Watch Files and Directories

```bash
cd backend/practical10
node 07-watch-files.cjs
```

**Features:**
- Watch files for changes
- Watch directories for changes
- Detect file creation, modification, and deletion
- Programmatic file change demonstrations
- Graceful watcher cleanup

**Note:** This example runs for ~15 seconds demonstrating various file changes automatically.

## Key Concepts Covered

### File System Module (fs)

- **Async vs Sync operations:** When to use each approach
- **Callbacks:** Handling asynchronous operations
- **Error handling:** Proper error management
- **File paths:** Using `path` module for cross-platform compatibility

### File Operations

- **Create:** `writeFile`, `writeFileSync`
- **Read:** `readFile`, `readFileSync`
- **Append:** `appendFile`, `appendFileSync`
- **Delete:** `unlink`, `unlinkSync`
- **Rename:** `rename`, `renameSync`
- **Copy:** `copyFile`, `copyFileSync`

### File Information

- **Stats:** `stat`, `statSync` - Get file metadata
- **Exists:** `exists`, `existsSync` - Check file existence
- **Access:** `access`, `accessSync` - Check file permissions

### Directory Operations

- **Create:** `mkdir`, `mkdirSync` - With/without recursive option
- **Read:** `readdir`, `readdirSync` - List directory contents
- **Delete:** `rmdir`, `rm` - Remove empty/non-empty directories
- **Check:** `stat.isDirectory()` - Verify if path is directory

### File Watching

- **Watch:** `fs.watch()` - Monitor files/directories for changes
- **Events:** Detect change events and filenames
- **Cleanup:** Properly close watchers to prevent memory leaks

## Best Practices Demonstrated

1. **Always handle errors:** All file operations should have error handling
2. **Use async for I/O:** Prefer async operations for better performance
3. **Use path module:** Cross-platform file path handling
4. **Check file existence:** Before operations that require existing files
5. **Clean up resources:** Close watchers and delete temporary files
6. **Use meaningful file names:** Clear, descriptive file naming

## Common File System Methods Reference

| Method | Description | Async | Sync |
|--------|-------------|-------|------|
| `writeFile` | Write data to file | ✓ | ✓ |
| `readFile` | Read file contents | ✓ | ✓ |
| `appendFile` | Append data to file | ✓ | ✓ |
| `unlink` | Delete file | ✓ | ✓ |
| `rename` | Rename/move file | ✓ | ✓ |
| `copyFile` | Copy file | ✓ | ✓ |
| `mkdir` | Create directory | ✓ | ✓ |
| `readdir` | Read directory | ✓ | ✓ |
| `rmdir` | Remove empty directory | ✓ | ✓ |
| `rm` | Remove (recursive) | ✓ | ✓ |
| `stat` | Get file stats | ✓ | ✓ |
| `exists` | Check if exists | ✓ | ✓ |
| `access` | Check permissions | ✓ | ✓ |
| `watch` | Watch for changes | ✓ | ✗ |

## Tips

1. **Run in order:** Start with `01-create-files.cjs` to generate test data
2. **Clean slate:** Each run creates/overwrites files - no manual cleanup needed
3. **Error messages:** Watch for error messages - they indicate missing prerequisites
4. **Data folder:** All file operations use the `data/` subdirectory
5. **Stop execution:** Press `Ctrl+C` to stop any running example
6. **File watchers:** Example 7 runs automatically - no manual interaction needed

## Next Steps

After mastering file operations:
- Learn streams for large file handling
- Explore file upload handling in web applications
- Understand file permissions and security
- Study file system events and real-time applications
- Learn about working with different file encodings
- Explore cloud storage integration (AWS S3, etc.)

## Common Issues

**Issue:** `ENOENT: no such file or directory`
**Solution:** Run `01-create-files.cjs` first to generate required test files

**Issue:** `EACCES: permission denied`
**Solution:** Check file/folder permissions. Avoid running as root.

**Issue:** `EEXIST: file already exists`
**Solution:** Some examples check for existence. Delete the `data/` folder to start fresh.

**Issue:** Watchers not detecting changes
**Solution:** Some editors have "safe save" that renames files. Use direct save or check your editor settings.

**Issue:** Port/Address errors
**Solution:** These examples don't use ports. If you see port errors, you're running the wrong file.

## Real-World Applications

File operations are essential for:
- **Log files:** Application logging and error tracking
- **Configuration files:** Reading and writing app settings
- **Data persistence:** Saving user data without a database
- **File uploads:** Handling user-uploaded files
- **Batch processing:** Processing multiple files
- **Data export:** Generating reports and exports
- **Backup systems:** Creating and managing backups
- **File monitoring:** Watching for file changes in real-time

## Resources

- [Node.js File System Documentation](https://nodejs.org/api/fs.html)
- [Node.js Path Module](https://nodejs.org/api/path.html)
- [Node.js Streams](https://nodejs.org/api/stream.html)
- [File System Best Practices](https://nodejs.org/en/docs/guides/simple-profiling/)

## Exercises

Try these modifications to deepen your understanding:

1. **Logging System:** Create a logging utility that writes to different log levels (info, warn, error)
2. **File Manager:** Build a simple CLI file manager with create, read, delete operations
3. **Configuration Loader:** Create a system that loads and parses JSON configuration files
4. **Backup Utility:** Write a script that backs up specific directories to a timestamped folder
5. **Log Rotator:** Implement log rotation based on file size or date
6. **File Search:** Create a utility to search for files by name or content
7. **Directory Tree:** Build a program that displays a directory tree structure

## Troubleshooting

**Files not being created:**
- Check write permissions in the directory
- Ensure the script runs without errors
- Verify the `data/` directory exists or can be created

**Watchers not working:**
- Some file systems have limitations on file watching
- Virtual machines and network drives may have issues
- Try using a local directory

**Permission errors:**
- Don't run as root/sudo unless necessary
- Check file and directory ownership
- Verify read/write permissions on the folder
