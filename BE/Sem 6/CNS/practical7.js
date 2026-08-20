"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.FileSizeModifier = void 0;
const fs = __importStar(require("fs"));
/**
 * FileSizeModifier - A simple class to modify file sizes by adding bytes
 */
class FileSizeModifier {
    /**
     * Increase file size by specified number of bytes
     * @param filePath Path to the file
     * @param bytes Number of bytes to add
     * @returns Promise that resolves when the operation is complete
     */
    async increase_by_bytes(filePath, bytes) {
        try {
            // Check if file exists
            if (!fs.existsSync(filePath)) {
                throw new Error(`File not found: ${filePath}`);
            }
            // Get current file stats
            const stats = fs.statSync(filePath);
            const currentSize = stats.size;
            // Calculate new size
            const newSize = currentSize + bytes;
            if (newSize < 0) {
                throw new Error('New file size cannot be negative');
            }
            // Create a temporary file with the new size
            const tempPath = filePath + '.tmp';
            // Write a file with the new size (filled with zeros)
            const buffer = Buffer.alloc(newSize);
            fs.writeFileSync(tempPath, buffer);
            // Replace original file with the new file
            fs.renameSync(tempPath, filePath);
            console.log(`File size increased from ${currentSize} to ${newSize} bytes`);
        }
        catch (error) {
            console.error('Error modifying file size:', error);
            throw error;
        }
    }
}
exports.FileSizeModifier = FileSizeModifier;
// Example usage
async function main() {
    const modifier = new FileSizeModifier();
    try {
        // Example: Increase file size by 1024 bytes
        await modifier.increase_by_bytes('example.txt', 1024);
        console.log('File size modification completed successfully');
    }
    catch (error) {
        console.error('Failed to modify file size:', error);
    }
}
// Uncomment to run the example
// main();
