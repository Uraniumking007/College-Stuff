# Practical 10: Quick Run Guide

## Quick Start

### Step 1: Navigate to the practical directory
```bash
cd backend/practical10
```

### Step 2: Run the examples in order

**Example 1: Create Files (REQUIRED FIRST)**
```bash
node 01-create-files.cjs
```
This creates test data files in the `data/` folder.

**Example 2: Read Files**
```bash
node 02-read-files.cjs
```
Reads the files created in Example 1.

**Example 3: Append to Files**
```bash
node 03-append-files.cjs
```
Creates and appends to a log file.

**Example 4: Get File Information**
```bash
node 04-file-info.cjs
```
Displays file statistics and metadata.

**Example 5: Delete and Rename Files**
```bash
node 05-delete-files.cjs
```
Demonstrates file deletion and renaming operations.

**Example 6: Directory Operations**
```bash
node 06-directories.cjs
```
Shows how to create, read, and delete directories.

**Example 7: Watch Files**
```bash
node 07-watch-files.cjs
```
Watches files and directories for changes (runs for ~15 seconds).

## Clean Up

To remove all generated files and folders:
```bash
# Remove data folder
rm -rf data/

# Remove generated folders
rm -rf new-folder sync-folder parent backup temp-folder delete-me old-name new-name
```

## Requirements

- Node.js installed (v14+)
- No dependencies needed (uses only Node.js built-in modules)

## What You'll Learn

1. ✅ Creating and writing files
2. ✅ Reading files (text, JSON, binary)
3. ✅ Appending data to files
4. ✅ Getting file information and stats
5. ✅ Deleting and renaming files
6. ✅ Working with directories
7. ✅ Watching files for changes

## Common Commands Reference

| Task | Async | Sync |
|------|-------|------|
| Write | `fs.writeFile()` | `fs.writeFileSync()` |
| Read | `fs.readFile()` | `fs.readFileSync()` |
| Append | `fs.appendFile()` | `fs.appendFileSync()` |
| Delete | `fs.unlink()` | `fs.unlinkSync()` |
| Rename | `fs.rename()` | `fs.renameSync()` |
| Create Dir | `fs.mkdir()` | `fs.mkdirSync()` |
| Read Dir | `fs.readdir()` | `fs.readdirSync()` |
| Delete Dir | `fs.rmdir()` / `fs.rm()` | `fs.rmdirSync()` / `fs.rmSync()` |

## Need Help?

See the full README.md for detailed explanations of each example.
