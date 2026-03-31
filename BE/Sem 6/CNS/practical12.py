"""
File Size Increase Program
==========================

A program to increase file size by 10 (interpreted as 10 bytes).

Different interpretations:
1. Add 10 bytes to the file
2. Increase by 10%
3. Multiply size by 10

This implementation provides all three methods for flexibility.
"""

import os
import sys
from pathlib import Path


class FileSizeModifier:
    """Class to modify file sizes in different ways."""
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Get file size in bytes.
        
        Args:
            file_path: Path to the file
        
        Returns:
            File size in bytes
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        return os.path.getsize(file_path)
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """
        Format size in bytes to human-readable format.
        
        Args:
            size_bytes: Size in bytes
        
        Returns:
            Formatted string (e.g., "1.5 KB", "2.3 MB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def increase_by_bytes(file_path: str, bytes_to_add: int = 10) -> dict:
        """
        Increase file size by adding specified number of bytes.
        
        Args:
            file_path: Path to the file
            bytes_to_add: Number of bytes to add (default: 10)
        
        Returns:
            Dictionary with operation details
        """
        original_size = FileSizeModifier.get_file_size(file_path)
        
        # Open file in append mode and add bytes
        with open(file_path, 'ab') as f:
            # Write null bytes (padding)
            f.write(b'\x00' * bytes_to_add)
        
        new_size = FileSizeModifier.get_file_size(file_path)
        
        return {
            'method': 'add_bytes',
            'bytes_added': bytes_to_add,
            'original_size': original_size,
            'new_size': new_size,
            'size_increase': new_size - original_size,
            'original_size_formatted': FileSizeModifier.format_size(original_size),
            'new_size_formatted': FileSizeModifier.format_size(new_size)
        }
    
    @staticmethod
    def increase_by_percentage(file_path: str, percentage: float = 10.0) -> dict:
        """
        Increase file size by specified percentage.
        
        Args:
            file_path: Path to the file
            percentage: Percentage to increase (default: 10%)
        
        Returns:
            Dictionary with operation details
        """
        original_size = FileSizeModifier.get_file_size(file_path)
        bytes_to_add = int(original_size * (percentage / 100.0))
        
        # Ensure at least 1 byte is added
        bytes_to_add = max(1, bytes_to_add)
        
        with open(file_path, 'ab') as f:
            f.write(b'\x00' * bytes_to_add)
        
        new_size = FileSizeModifier.get_file_size(file_path)
        
        return {
            'method': 'percentage',
            'percentage': percentage,
            'bytes_added': bytes_to_add,
            'original_size': original_size,
            'new_size': new_size,
            'size_increase': new_size - original_size,
            'original_size_formatted': FileSizeModifier.format_size(original_size),
            'new_size_formatted': FileSizeModifier.format_size(new_size)
        }
    
    @staticmethod
    def increase_by_multiplier(file_path: str, multiplier: float = 10.0) -> dict:
        """
        Increase file size by multiplying it by specified factor.
        
        Args:
            file_path: Path to the file
            multiplier: Multiplier factor (default: 10x)
        
        Returns:
            Dictionary with operation details
        """
        original_size = FileSizeModifier.get_file_size(file_path)
        target_size = int(original_size * multiplier)
        bytes_to_add = target_size - original_size
        
        # Ensure at least 1 byte is added
        bytes_to_add = max(1, bytes_to_add)
        
        with open(file_path, 'ab') as f:
            f.write(b'\x00' * bytes_to_add)
        
        new_size = FileSizeModifier.get_file_size(file_path)
        
        return {
            'method': 'multiplier',
            'multiplier': multiplier,
            'bytes_added': bytes_to_add,
            'original_size': original_size,
            'new_size': new_size,
            'size_increase': new_size - original_size,
            'original_size_formatted': FileSizeModifier.format_size(original_size),
            'new_size_formatted': FileSizeModifier.format_size(new_size)
        }
    
    @staticmethod
    def create_test_file(file_path: str, content: str = "Hello, World!\n") -> None:
        """
        Create a test file with specified content.
        
        Args:
            file_path: Path where to create the file
            content: Content to write to the file
        """
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Created test file: {file_path}")
        print(f"Content: {content!r}")
        print(f"Initial size: {FileSizeModifier.format_size(FileSizeModifier.get_file_size(file_path))}")


def display_result(result: dict) -> None:
    """Display the result of file size modification."""
    print(f"\n{'='*70}")
    print(f"FILE SIZE MODIFICATION RESULT")
    print(f"{'='*70}")
    
    print(f"\nMethod: {result['method'].upper().replace('_', ' ')}")
    
    if result['method'] == 'add_bytes':
        print(f"Bytes added: {result['bytes_added']}")
    elif result['method'] == 'percentage':
        print(f"Percentage: {result['percentage']}%")
    elif result['method'] == 'multiplier':
        print(f"Multiplier: {result['multiplier']}x")
    
    print(f"\nOriginal size: {result['original_size']} bytes "
          f"({result['original_size_formatted']})")
    print(f"New size:      {result['new_size']} bytes "
          f"({result['new_size_formatted']})")
    print(f"Size increase: {result['size_increase']} bytes "
          f"({FileSizeModifier.format_size(result['size_increase'])})")
    
    print(f"\n✓ File size increased successfully!")


def method1_add_10_bytes():
    """Method 1: Increase file size by 10 bytes (literal interpretation)."""
    print("\n" + "="*70)
    print("METHOD 1: Increase File Size by 10 Bytes")
    print("="*70)
    print("\nInterpretation: Add exactly 10 bytes to the file")
    print("This is the most literal interpretation of 'increase by 10'")
    
    # Create a test file
    test_file = "test_method1.txt"
    FileSizeModifier.create_test_file(test_file, "Hello, World!\n")
    
    # Increase by 10 bytes
    result = FileSizeModifier.increase_by_bytes(test_file, bytes_to_add=10)
    display_result(result)
    
    # Clean up
    os.remove(test_file)
    print(f"\nCleaned up test file: {test_file}")


def method2_increase_by_10_percent():
    """Method 2: Increase file size by 10%."""
    print("\n" + "="*70)
    print("METHOD 2: Increase File Size by 10%")
    print("="*70)
    print("\nInterpretation: Increase file size by 10 percent")
    print("Example: 100 bytes → 110 bytes (10 bytes added)")
    
    # Create a test file
    test_file = "test_method2.txt"
    FileSizeModifier.create_test_file(test_file, "Hello, World!\n")
    
    # Increase by 10%
    result = FileSizeModifier.increase_by_percentage(test_file, percentage=10.0)
    display_result(result)
    
    # Clean up
    os.remove(test_file)
    print(f"\nCleaned up test file: {test_file}")


def method3_multiply_by_10():
    """Method 3: Multiply file size by 10."""
    print("\n" + "="*70)
    print("METHOD 3: Multiply File Size by 10")
    print("="*70)
    print("\nInterpretation: Make the file 10 times larger")
    print("Example: 100 bytes → 1000 bytes (900 bytes added)")
    
    # Create a test file
    test_file = "test_method3.txt"
    FileSizeModifier.create_test_file(test_file, "Hello, World!\n")
    
    # Multiply by 10
    result = FileSizeModifier.increase_by_multiplier(test_file, multiplier=10.0)
    display_result(result)
    
    # Clean up
    os.remove(test_file)
    print(f"\nCleaned up test file: {test_file}")


def interactive_mode():
    """Interactive mode for user to modify any file."""
    print("\n" + "="*70)
    print("INTERACTIVE MODE")
    print("="*70)
    
    file_path = input("\nEnter file path: ").strip()
    
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return
    
    original_size = FileSizeModifier.get_file_size(file_path)
    print(f"\nCurrent file size: {original_size} bytes "
          f"({FileSizeModifier.format_size(original_size)})")
    
    print("\nChoose modification method:")
    print("1. Add 10 bytes (default)")
    print("2. Increase by 10%")
    print("3. Multiply by 10")
    print("4. Custom amount")
    
    choice = input("\nEnter choice (1-4): ").strip() or "1"
    
    if choice == "1":
        result = FileSizeModifier.increase_by_bytes(file_path, bytes_to_add=10)
        display_result(result)
    elif choice == "2":
        result = FileSizeModifier.increase_by_percentage(file_path, percentage=10.0)
        display_result(result)
    elif choice == "3":
        result = FileSizeModifier.increase_by_multiplier(file_path, multiplier=10.0)
        display_result(result)
    elif choice == "4":
        try:
            amount = float(input("Enter amount: "))
            sub_choice = input("Add bytes (b), percentage (p), or multiplier (m)? ").strip().lower()
            
            if sub_choice == 'p':
                result = FileSizeModifier.increase_by_percentage(file_path, percentage=amount)
            elif sub_choice == 'm':
                result = FileSizeModifier.increase_by_multiplier(file_path, multiplier=amount)
            else:  # default to bytes
                result = FileSizeModifier.increase_by_bytes(file_path, bytes_to_add=int(amount))
            
            display_result(result)
        except ValueError as e:
            print(f"Error: Invalid input - {e}")
    else:
        print("Error: Invalid choice")


def technical_explanation():
    """Provide technical explanation of how file size increase works."""
    print("\n" + "="*70)
    print("TECHNICAL EXPLANATION")
    print("="*70)
    
    print("""
HOW FILE SIZE INCREASE WORKS:
------------------------------

Method: Append Mode Writing

Python's open() function with 'ab' mode (append binary):
- Opens file in append mode
- Positions file pointer at end of file
- Writing adds data without overwriting existing content

Code Structure:
    with open(file_path, 'ab') as f:
        f.write(b'\\x00' * 10)  # Write 10 null bytes

What Happens Internally:
1. Filesystem locates the file
2. File pointer moves to end of file (EOF)
3. Null bytes (\\x00) are written
4. File metadata updated (size in inode/directory entry)
5. File system allocates new disk blocks if needed

Why Null Bytes?
- Null bytes (\\x00) are safe padding
- Don't affect text files (invisible)
- Don't affect binary files (neutral)
- Can be stripped if needed

Alternative Methods:
1. Copy + Modify: Read entire file, modify, write back
   - Disadvantage: Uses 2x memory
   - Disadvantage: Risk of data corruption if interrupted

2. Truncate + Expand: Use truncate() system call
   - Advantage: Atomic operation
   - Advantage: Efficient for large files

3. Append (Used Here): Simple and safe
   - Advantage: Preserves original data
   - Advantage: Can be undone (truncate back)

File System Considerations:
- Block size: Files grow in filesystem blocks (usually 4KB)
- Sparse files: Some filesystems support holes (zero-filled regions)
- Fragmentation: Repeated modifications can fragment files
- Metadata: File size stored in inode/extents

Applications:
- Padding files to specific sizes (e.g., for encryption)
- Reserving space for future writes
- Alignment requirements (e.g., disk sectors)
- Testing filesystem behavior
- Benchmarking I/O performance
    """)


def safety_warning():
    """Display safety warnings and best practices."""
    print("\n" + "="*70)
    print("SAFETY WARNING & BEST PRACTICES")
    print("="*70)
    
    print("""
⚠️  IMPORTANT SAFETY CONSIDERATIONS:

1. DATA INTEGRITY:
   ✓ Always backup important files before modification
   ✓ Use copy mode for testing first
   ✗ Don't modify system files or active databases
   ✗ Don't modify files while they're in use by other programs

2. DISK SPACE:
   ✓ Check available disk space before large increases
   ✓ Be aware that 10x multiplication can be huge (1MB → 10MB)
   ✗ Don't fill up disk (causes system instability)

3. FILE CORRUPTION:
   ✓ Use atomic operations when possible
   ✓ Validate file path before modification
   ✗ Don't modify compressed archives directly
   ✗ Don't modify executable files (breaks checksums)

4. REVERSIBILITY:
   ✓ Store original size if you need to revert
   ✓ Can truncate back: open(path, 'ab').truncate(original_size)
   ✗ Null bytes may affect some file formats

5. PERMISSIONS:
   ✓ Ensure write permission on file
   ✓ Ensure write permission on directory
   ✗ Don't modify files in /sys, /proc, /dev

EXAMPLE OF REVERTING:
    original_size = 1024  # Store this first!
    # ... modify file ...
    # To revert:
    with open(file_path, 'ab') as f:
        f.truncate(original_size)

BEST PRACTICES:
1. Test on non-critical files first
2. Use absolute paths to avoid confusion
3. Check return values and exceptions
4. Log modifications for audit trail
5. Consider using tempfile module for temporary files
    """)


def command_line_usage():
    """Show command-line usage examples."""
    print("\n" + "="*70)
    print("COMMAND-LINE USAGE")
    print("="*70)
    
    print("""
Usage Examples:

1. Interactive Mode (Default):
   $ python practical12.py
   
2. Method 1: Add 10 Bytes:
   $ python practical12.py --method1
   
3. Method 2: Increase by 10%:
   $ python practical12.py --method2
   
4. Method 3: Multiply by 10:
   $ python practical12.py --method3
   
5. Custom File:
   $ python practical12.py --file myfile.txt --bytes 100
   
6. All Methods (Demo):
   $ python practical12.py --all

Python API Usage:
    from practical12 import FileSizeModifier
    
    # Add 10 bytes
    result = FileSizeModifier.increase_by_bytes("myfile.txt", 10)
    
    # Increase by 10%
    result = FileSizeModifier.increase_by_percentage("myfile.txt", 10.0)
    
    # Multiply by 10
    result = FileSizeModifier.increase_by_multiplier("myfile.txt", 10.0)
    
    # Check result
    print(f"Original: {result['original_size']}")
    print(f"New: {result['new_size']}")
    """)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Increase file size by 10 (interpreted in different ways)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python practical12.py --all           # Run all demonstration methods
  python practical12.py --method1        # Add 10 bytes
  python practical12.py --interactive    # Interactive mode
  python practical12.py --file data.txt --bytes 100  # Custom
        """
    )
    
    parser.add_argument('--method1', action='store_true',
                       help='Increase by 10 bytes (literal)')
    parser.add_argument('--method2', action='store_true',
                       help='Increase by 10 percent')
    parser.add_argument('--method3', action='store_true',
                       help='Multiply size by 10')
    parser.add_argument('--all', action='store_true',
                       help='Run all demonstration methods')
    parser.add_argument('--interactive', action='store_true',
                       help='Interactive mode')
    parser.add_argument('--file', type=str,
                       help='File to modify (for interactive/custom mode)')
    parser.add_argument('--bytes', type=int,
                       help='Custom bytes to add')
    parser.add_argument('--explain', action='store_true',
                       help='Show technical explanation')
    parser.add_argument('--warning', action='store_true',
                       help='Show safety warnings')
    
    args = parser.parse_args()
    
    print("="*70)
    print("FILE SIZE INCREASE PROGRAM")
    print("Practical 12: Increase File Size by 10")
    print("="*70)
    
    # Show technical explanation if requested
    if args.explain:
        technical_explanation()
        print()
    
    # Show safety warning if requested
    if args.warning:
        safety_warning()
        print()
    
    # Run based on arguments
    if args.method1:
        method1_add_10_bytes()
    elif args.method2:
        method2_increase_by_10_percent()
    elif args.method3:
        method3_multiply_by_10()
    elif args.all:
        method1_add_10_bytes()
        method2_increase_by_10_percent()
        method3_multiply_by_10()
        
        print("\n" + "="*70)
        print("SUMMARY: All Three Methods Demonstrated")
        print("="*70)
        print("\nMethod 1 (Add 10 bytes): Most literal interpretation")
        print("Method 2 (10% increase): Proportional interpretation")
        print("Method 3 (10x multiplier): Multiplicative interpretation")
        print("\nRecommended: Method 1 (Add 10 bytes) - Simplest and clearest")
    elif args.interactive or args.file:
        if args.file:
            interactive_mode()
        else:
            interactive_mode()
    else:
        # Default: Show all methods
        print("\nNo arguments provided. Running all demonstration methods...")
        print("Use --help for usage information.\n")
        
        method1_add_10_bytes()
        method2_increase_by_10_percent()
        method3_multiply_by_10()
        
        print("\n" + "="*70)
        print("SUMMARY: All Three Methods Demonstrated")
        print("="*70)
        print("\nMethod 1 (Add 10 bytes): Most literal interpretation")
        print("Method 2 (10% increase): Proportional interpretation")
        print("Method 3 (10x multiplier): Multiplicative interpretation")
        print("\nRecommended: Method 1 (Add 10 bytes) - Simplest and clearest")
        
        print("\n" + "="*70)
        print("For more options, run: python practical12.py --help")
        print("="*70)
    
    print("\n" + "="*70)
    print("PROGRAM COMPLETE")
    print("="*70)
