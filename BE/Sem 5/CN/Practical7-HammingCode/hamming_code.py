"""
Hamming Code Error Correction Implementation
==========================================

This module implements Hamming Code error correction methods with support for
various Hamming Code variants commonly used in computer networks and data storage.

Author: CN Assignment - Practical 7
"""

from typing import List, Tuple, Union
import math


class HammingCode:
    """
    Hamming Code implementation for error detection and correction.
    
    Supports various Hamming Code variants and provides both encoding and
    decoding with single-bit error correction capabilities.
    """
    
    def __init__(self, data_bits: int = 4):
        """
        Initialize Hamming Code with specified number of data bits.
        
        Args:
            data_bits (int): Number of data bits (default: 4)
        """
        self.data_bits = data_bits
        self.parity_bits = self._calculate_parity_bits(data_bits)
        self.total_bits = data_bits + self.parity_bits
        
        # Calculate parity bit positions (powers of 2)
        self.parity_positions = [2**i for i in range(self.parity_bits)]
        
        # Create mapping for which data bits each parity bit covers
        self.parity_coverage = self._create_parity_coverage()
    
    def _calculate_parity_bits(self, data_bits: int) -> int:
        """
        Calculate the number of parity bits needed for given data bits.
        
        Args:
            data_bits (int): Number of data bits
            
        Returns:
            int: Number of parity bits required
        """
        # For Hamming Code: 2^r >= m + r + 1
        # where r = parity bits, m = data bits
        for r in range(1, 20):  # Reasonable upper limit
            if 2**r >= data_bits + r + 1:
                return r
        raise ValueError(f"Cannot find suitable number of parity bits for {data_bits} data bits")
    
    def _create_parity_coverage(self) -> List[List[int]]:
        """
        Create mapping of which data bits each parity bit covers.
        
        Returns:
            List[List[int]]: List where each element contains data bit positions covered by that parity bit
        """
        coverage = []
        
        for parity_pos in self.parity_positions:
            covered_bits = []
            for bit_pos in range(1, self.total_bits + 1):
                if bit_pos != parity_pos and bit_pos & parity_pos:  # Check if bit position has this parity bit set
                    covered_bits.append(bit_pos)
            coverage.append(covered_bits)
        
        return coverage
    
    def encode(self, data: str) -> str:
        """
        Encode data using Hamming Code.
        
        Args:
            data (str): Binary string data
            
        Returns:
            str: Encoded data with parity bits
        """
        if not all(bit in '01' for bit in data):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        if len(data) != self.data_bits:
            raise ValueError(f"Data must be exactly {self.data_bits} bits long")
        
        # Create array for encoded data
        encoded = ['0'] * (self.total_bits + 1)  # +1 because we use 1-based indexing
        
        # Place data bits in non-parity positions
        data_index = 0
        for pos in range(1, self.total_bits + 1):
            if pos not in self.parity_positions:
                encoded[pos] = data[data_index]
                data_index += 1
        
        # Calculate and place parity bits
        for i, parity_pos in enumerate(self.parity_positions):
            parity_value = 0
            for bit_pos in self.parity_coverage[i]:
                parity_value ^= int(encoded[bit_pos])
            encoded[parity_pos] = str(parity_value)
        
        # Return encoded data (skip position 0)
        return ''.join(encoded[1:])
    
    def decode(self, encoded_data: str) -> Tuple[str, bool, int]:
        """
        Decode Hamming Code and detect/correct single-bit errors.
        
        Args:
            encoded_data (str): Encoded binary string with parity bits
            
        Returns:
            Tuple[str, bool, int]: (decoded_data, has_error, error_position)
        """
        if not all(bit in '01' for bit in encoded_data):
            raise ValueError("Encoded data must contain only binary digits (0 and 1)")
        
        if len(encoded_data) != self.total_bits:
            raise ValueError(f"Encoded data must be exactly {self.total_bits} bits long")
        
        # Create array for easier manipulation (1-based indexing)
        data_array = ['0'] + list(encoded_data)
        
        # Calculate syndrome (error position)
        syndrome = 0
        for i, parity_pos in enumerate(self.parity_positions):
            parity_value = 0
            for bit_pos in self.parity_coverage[i]:
                parity_value ^= int(data_array[bit_pos])
            
            # If calculated parity doesn't match stored parity, set corresponding bit in syndrome
            if parity_value != int(data_array[parity_pos]):
                syndrome |= parity_pos
        
        # Extract original data
        decoded_data = ''
        for pos in range(1, self.total_bits + 1):
            if pos not in self.parity_positions:
                decoded_data += data_array[pos]
        
        # Determine if there's an error and correct if possible
        has_error = syndrome != 0
        error_position = syndrome if has_error else 0
        
        # If there's an error, correct it
        if has_error and syndrome <= self.total_bits:
            data_array[syndrome] = '1' if data_array[syndrome] == '0' else '0'
            
            # Re-extract corrected data
            decoded_data = ''
            for pos in range(1, self.total_bits + 1):
                if pos not in self.parity_positions:
                    decoded_data += data_array[pos]
        
        return decoded_data, has_error, error_position
    
    def verify(self, encoded_data: str) -> Tuple[bool, int]:
        """
        Verify Hamming Code without correcting errors.
        
        Args:
            encoded_data (str): Encoded binary string with parity bits
            
        Returns:
            Tuple[bool, int]: (is_valid, error_position)
        """
        if not all(bit in '01' for bit in encoded_data):
            raise ValueError("Encoded data must contain only binary digits (0 and 1)")
        
        if len(encoded_data) != self.total_bits:
            raise ValueError(f"Encoded data must be exactly {self.total_bits} bits long")
        
        # Create array for easier manipulation (1-based indexing)
        data_array = ['0'] + list(encoded_data)
        
        # Calculate syndrome
        syndrome = 0
        for i, parity_pos in enumerate(self.parity_positions):
            parity_value = 0
            for bit_pos in self.parity_coverage[i]:
                parity_value ^= int(data_array[bit_pos])
            
            if parity_value != int(data_array[parity_pos]):
                syndrome |= parity_pos
        
        is_valid = syndrome == 0
        return is_valid, syndrome
    
    def get_info(self) -> dict:
        """
        Get information about the Hamming Code configuration.
        
        Returns:
            dict: Configuration information
        """
        return {
            'data_bits': self.data_bits,
            'parity_bits': self.parity_bits,
            'total_bits': self.total_bits,
            'parity_positions': self.parity_positions,
            'parity_coverage': self.parity_coverage,
            'efficiency': self.data_bits / self.total_bits
        }


class HammingCodeErrorSimulator:
    """
    Utility class for simulating errors in Hamming Code protected data.
    """
    
    @staticmethod
    def introduce_single_bit_error(encoded_data: str, position: int = None) -> str:
        """
        Introduce a single bit error in the encoded data.
        
        Args:
            encoded_data (str): Encoded binary string
            position (int): Position to flip bit (1-based, random if None)
            
        Returns:
            str: Encoded data with single bit error
        """
        if position is None:
            import random
            position = random.randint(1, len(encoded_data))
        
        if position < 1 or position > len(encoded_data):
            raise ValueError(f"Position must be between 1 and {len(encoded_data)}")
        
        data_list = list(encoded_data)
        data_list[position - 1] = '1' if data_list[position - 1] == '0' else '0'
        return ''.join(data_list)
    
    @staticmethod
    def introduce_multiple_errors(encoded_data: str, num_errors: int) -> str:
        """
        Introduce multiple bit errors in the encoded data.
        
        Args:
            encoded_data (str): Encoded binary string
            num_errors (int): Number of errors to introduce
            
        Returns:
            str: Encoded data with multiple errors
        """
        import random
        
        if num_errors > len(encoded_data):
            raise ValueError("Number of errors cannot exceed data length")
        
        data_list = list(encoded_data)
        positions = random.sample(range(len(encoded_data)), num_errors)
        
        for pos in positions:
            data_list[pos] = '1' if data_list[pos] == '0' else '0'
        
        return ''.join(data_list)


class HammingCodeVariants:
    """
    Collection of different Hamming Code variants and utilities.
    """
    
    @staticmethod
    def get_standard_variants() -> dict:
        """
        Get information about standard Hamming Code variants.
        
        Returns:
            dict: Standard variants information
        """
        return {
            'Hamming(7,4)': {'data_bits': 4, 'total_bits': 7, 'description': 'Most common variant'},
            'Hamming(15,11)': {'data_bits': 11, 'total_bits': 15, 'description': 'Extended variant'},
            'Hamming(31,26)': {'data_bits': 26, 'total_bits': 31, 'description': 'Large variant'},
            'Hamming(63,57)': {'data_bits': 57, 'total_bits': 63, 'description': 'Very large variant'},
        }
    
    @staticmethod
    def calculate_efficiency(data_bits: int) -> float:
        """
        Calculate the efficiency of Hamming Code for given data bits.
        
        Args:
            data_bits (int): Number of data bits
            
        Returns:
            float: Efficiency ratio (data_bits / total_bits)
        """
        hamming = HammingCode(data_bits)
        return hamming.get_info()['efficiency']
    
    @staticmethod
    def compare_variants(data_bits_list: List[int]) -> None:
        """
        Compare different Hamming Code variants.
        
        Args:
            data_bits_list (List[int]): List of data bit counts to compare
        """
        print("Hamming Code Variants Comparison")
        print("=" * 50)
        print(f"{'Data Bits':<10} {'Parity Bits':<12} {'Total Bits':<12} {'Efficiency':<12}")
        print("-" * 50)
        
        for data_bits in data_bits_list:
            hamming = HammingCode(data_bits)
            info = hamming.get_info()
            efficiency = info['efficiency']
            print(f"{data_bits:<10} {info['parity_bits']:<12} {info['total_bits']:<12} {efficiency:<12.3f}")


def demonstrate_hamming_code():
    """Demonstrate Hamming Code encoding and decoding."""
    print("=" * 60)
    print("HAMMING CODE ERROR CORRECTION DEMONSTRATION")
    print("=" * 60)
    
    # Test with Hamming(7,4) - most common variant
    print("Using Hamming(7,4) Code:")
    print("-" * 30)
    
    hamming = HammingCode(4)
    info = hamming.get_info()
    
    print(f"Data bits: {info['data_bits']}")
    print(f"Parity bits: {info['parity_bits']}")
    print(f"Total bits: {info['total_bits']}")
    print(f"Parity positions: {info['parity_positions']}")
    print(f"Efficiency: {info['efficiency']:.3f}")
    
    # Test data
    test_data = "1011"
    print(f"\nOriginal data: {test_data}")
    
    # Encode data
    encoded_data = hamming.encode(test_data)
    print(f"Encoded data: {encoded_data}")
    
    # Show parity bit positions
    print("\nParity bit analysis:")
    for i, pos in enumerate(info['parity_positions']):
        print(f"  Parity bit {i+1} at position {pos}: {encoded_data[pos-1]}")
    
    # Verify without errors
    is_valid, error_pos = hamming.verify(encoded_data)
    print(f"\nVerification (no errors): {'Valid' if is_valid else 'Invalid'}")
    
    # Decode without errors
    decoded_data, has_error, error_position = hamming.decode(encoded_data)
    print(f"Decoded data: {decoded_data}")
    print(f"Error detected: {'Yes' if has_error else 'No'}")
    print(f"Original data matches: {'Yes' if decoded_data == test_data else 'No'}")


def demonstrate_error_correction():
    """Demonstrate Hamming Code error correction capabilities."""
    print("\n" + "=" * 60)
    print("HAMMING CODE ERROR CORRECTION DEMONSTRATION")
    print("=" * 60)
    
    hamming = HammingCode(4)
    test_data = "1011"
    encoded_data = hamming.encode(test_data)
    
    print(f"Original data: {test_data}")
    print(f"Encoded data: {encoded_data}")
    
    # Test single bit errors at different positions
    error_simulator = HammingCodeErrorSimulator()
    
    print("\nSingle Bit Error Correction:")
    print("-" * 40)
    
    for error_pos in range(1, len(encoded_data) + 1):
        # Introduce error
        error_data = error_simulator.introduce_single_bit_error(encoded_data, error_pos)
        
        # Decode and correct
        decoded_data, has_error, detected_pos = hamming.decode(error_data)
        
        print(f"Error at position {error_pos}: {error_data}")
        print(f"  Detected at position: {detected_pos}")
        print(f"  Corrected data: {decoded_data}")
        print(f"  Correction successful: {'Yes' if decoded_data == test_data else 'No'}")
        print()


def demonstrate_multiple_errors():
    """Demonstrate Hamming Code limitations with multiple errors."""
    print("\n" + "=" * 60)
    print("HAMMING CODE MULTIPLE ERROR LIMITATIONS")
    print("=" * 60)
    
    hamming = HammingCode(4)
    test_data = "1011"
    encoded_data = hamming.encode(test_data)
    
    print(f"Original data: {test_data}")
    print(f"Encoded data: {encoded_data}")
    
    error_simulator = HammingCodeErrorSimulator()
    
    print("\nMultiple Error Scenarios:")
    print("-" * 30)
    
    # Test 2-bit errors
    error_data_2 = error_simulator.introduce_multiple_errors(encoded_data, 2)
    decoded_data, has_error, error_pos = hamming.decode(error_data_2)
    
    print(f"2-bit error data: {error_data_2}")
    print(f"Error detected: {'Yes' if has_error else 'No'}")
    print(f"Decoded data: {decoded_data}")
    print(f"Correction successful: {'Yes' if decoded_data == test_data else 'No'}")
    print("Note: Hamming Code can only correct single-bit errors!")


def demonstrate_variants():
    """Demonstrate different Hamming Code variants."""
    print("\n" + "=" * 60)
    print("HAMMING CODE VARIANTS DEMONSTRATION")
    print("=" * 60)
    
    # Show standard variants
    variants = HammingCodeVariants.get_standard_variants()
    print("Standard Hamming Code Variants:")
    print("-" * 40)
    
    for name, info in variants.items():
        print(f"{name}: {info['description']}")
        print(f"  Data bits: {info['data_bits']}, Total bits: {info['total_bits']}")
    
    # Compare efficiency
    print("\nEfficiency Comparison:")
    print("-" * 25)
    HammingCodeVariants.compare_variants([4, 8, 11, 16, 26, 32])


def main():
    """Main function to demonstrate Hamming Code error correction methods."""
    print("HAMMING CODE ERROR CORRECTION METHODS IMPLEMENTATION")
    print("====================================================")
    
    # Demonstrate basic Hamming Code
    demonstrate_hamming_code()
    
    # Demonstrate error correction
    demonstrate_error_correction()
    
    # Demonstrate multiple error limitations
    demonstrate_multiple_errors()
    
    # Demonstrate variants
    demonstrate_variants()
    
    print("\n" + "=" * 60)
    print("INTERACTIVE TESTING")
    print("=" * 60)
    
    # Interactive testing
    while True:
        print("\nChoose an option:")
        print("1. Test Hamming Code encoding/decoding")
        print("2. Test error correction")
        print("3. Test multiple errors")
        print("4. Compare Hamming Code variants")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            data_bits = int(input("Enter number of data bits (4, 8, 11, etc.): "))
            data = input(f"Enter {data_bits}-bit binary data: ").strip()
            
            try:
                hamming = HammingCode(data_bits)
                encoded = hamming.encode(data)
                decoded, has_error, error_pos = hamming.decode(encoded)
                
                print(f"Original data: {data}")
                print(f"Encoded data: {encoded}")
                print(f"Decoded data: {decoded}")
                print(f"Error detected: {'Yes' if has_error else 'No'}")
                print(f"Data matches: {'Yes' if decoded == data else 'No'}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            data_bits = int(input("Enter number of data bits: "))
            data = input(f"Enter {data_bits}-bit binary data: ").strip()
            error_pos = int(input("Enter position to introduce error (1-based): "))
            
            try:
                hamming = HammingCode(data_bits)
                encoded = hamming.encode(data)
                error_data = HammingCodeErrorSimulator.introduce_single_bit_error(encoded, error_pos)
                decoded, has_error, detected_pos = hamming.decode(error_data)
                
                print(f"Original data: {data}")
                print(f"Encoded data: {encoded}")
                print(f"Data with error: {error_data}")
                print(f"Error detected at position: {detected_pos}")
                print(f"Corrected data: {decoded}")
                print(f"Correction successful: {'Yes' if decoded == data else 'No'}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            data_bits = int(input("Enter number of data bits: "))
            data = input(f"Enter {data_bits}-bit binary data: ").strip()
            num_errors = int(input("Enter number of errors to introduce: "))
            
            try:
                hamming = HammingCode(data_bits)
                encoded = hamming.encode(data)
                error_data = HammingCodeErrorSimulator.introduce_multiple_errors(encoded, num_errors)
                decoded, has_error, error_pos = hamming.decode(error_data)
                
                print(f"Original data: {data}")
                print(f"Encoded data: {encoded}")
                print(f"Data with {num_errors} errors: {error_data}")
                print(f"Error detected: {'Yes' if has_error else 'No'}")
                print(f"Decoded data: {decoded}")
                print(f"Correction successful: {'Yes' if decoded == data else 'No'}")
                print("Note: Hamming Code can only correct single-bit errors!")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '4':
            data_bits_list = input("Enter data bit counts (comma-separated, e.g., 4,8,11,16): ").strip()
            try:
                data_bits = [int(x.strip()) for x in data_bits_list.split(',')]
                HammingCodeVariants.compare_variants(data_bits)
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
