import * as fs from 'fs';
import * as path from 'path';

/**
 * FileSizeModifier - A simple class to modify file sizes by adding bytes
 */
export class FileSizeModifier {
    /**
     * Increase file size by specified number of bytes
     * @param filePath Path to the file
     * @param bytes Number of bytes to add
     * @returns Promise that resolves when the operation is complete
     */
    async increase_by_bytes(filePath: string, bytes: number): Promise<void> {
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
        } catch (error) {
            console.error('Error modifying file size:', error);
            throw error;
        }
    }
}

// Example usage
async function main() {
    const modifier = new FileSizeModifier();
    
    try {
        // Example: Increase file size by 1024 bytes
        await modifier.increase_by_bytes('example.txt', 1024);
        console.log('File size modification completed successfully');
    } catch (error) {
        console.error('Failed to modify file size:', error);
    }
}

// Uncomment to run the example
// main();