"""
CRC (Cyclic Redundancy Check) Error Detection Implementation
==========================================================

This module implements CRC error detection methods with support for various
CRC polynomials commonly used in computer networks and data communication.

Author: CN Assignment - Practical 6
"""

from typing import List, Tuple, Union
import struct


class CRCDetection:
    """
    CRC (Cyclic Redundancy Check) implementation for error detection.
    
    Supports various CRC polynomials and provides both bit-level and byte-level
    CRC calculation methods.
    """
    
    # Common CRC polynomials
    CRC_POLYNOMIALS = {
        'CRC-8': 0x07,           # x^8 + x^2 + x + 1
        'CRC-16': 0x8005,        # x^16 + x^15 + x^2 + 1
        'CRC-32': 0x04C11DB7,    # x^32 + x^26 + x^23 + x^22 + x^16 + x^12 + x^11 + x^10 + x^8 + x^7 + x^5 + x^4 + x^2 + x + 1
        'CRC-CCITT': 0x1021,     # x^16 + x^12 + x^5 + 1
        'CRC-ANSI': 0x8005,      # x^16 + x^15 + x^2 + 1
        'CRC-DNP': 0x3D65,       # x^16 + x^13 + x^12 + x^11 + x^10 + x^8 + x^6 + x^5 + x^2 + 1
    }
    
    def __init__(self, polynomial: Union[str, int], width: int = None):
        """
        Initialize CRC detector with specified polynomial.
        
        Args:
            polynomial (Union[str, int]): CRC polynomial name or value
            width (int): CRC width in bits (auto-detected if None)
        """
        if isinstance(polynomial, str):
            if polynomial not in self.CRC_POLYNOMIALS:
                raise ValueError(f"Unknown CRC polynomial: {polynomial}")
            self.polynomial = self.CRC_POLYNOMIALS[polynomial]
            self.polynomial_name = polynomial
        else:
            self.polynomial = polynomial
            self.polynomial_name = f"Custom-0x{polynomial:04X}"
        
        # Auto-detect width if not provided
        if width is None:
            self.width = self._detect_width(self.polynomial)
        else:
            self.width = width
        
        # Create lookup table for faster computation
        self.lookup_table = self._create_lookup_table()
    
    def _detect_width(self, polynomial: int) -> int:
        """Detect CRC width from polynomial value."""
        width = 0
        temp = polynomial
        while temp > 0:
            width += 1
            temp >>= 1
        return width
    
    def _create_lookup_table(self) -> List[int]:
        """Create lookup table for faster CRC computation."""
        table = []
        for i in range(256):
            crc = i << (self.width - 8)
            for _ in range(8):
                if crc & (1 << (self.width - 1)):
                    crc = (crc << 1) ^ self.polynomial
                else:
                    crc <<= 1
                crc &= (1 << self.width) - 1
            table.append(crc)
        return table
    
    def calculate_crc_bitwise(self, data: str) -> str:
        """
        Calculate CRC using bitwise operations.
        
        Args:
            data (str): Binary string data
            
        Returns:
            str: CRC value as binary string
        """
        if not all(bit in '01' for bit in data):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        # Initialize CRC register
        crc = 0
        
        # Process each bit
        for bit in data:
            crc <<= 1
            if bit == '1':
                crc ^= 1
            
            # Check if MSB is set
            if crc & (1 << self.width):
                crc ^= self.polynomial
        
        # Return CRC as binary string
        return format(crc, f'0{self.width}b')
    
    def calculate_crc_table(self, data: str) -> str:
        """
        Calculate CRC using lookup table for faster computation.
        
        Args:
            data (str): Binary string data
            
        Returns:
            str: CRC value as binary string
        """
        if not all(bit in '01' for bit in data):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        # Pad data to byte boundary
        padded_data = data
        while len(padded_data) % 8 != 0:
            padded_data = '0' + padded_data
        
        # Initialize CRC register
        crc = 0
        
        # Process data byte by byte
        for i in range(0, len(padded_data), 8):
            byte = int(padded_data[i:i+8], 2)
            crc = ((crc << 8) ^ self.lookup_table[((crc >> (self.width - 8)) ^ byte) & 0xFF]) & ((1 << self.width) - 1)
        
        return format(crc, f'0{self.width}b')
    
    def calculate_crc_bytes(self, data: bytes) -> bytes:
        """
        Calculate CRC for byte data.
        
        Args:
            data (bytes): Byte data
            
        Returns:
            bytes: CRC value as bytes
        """
        crc = 0
        
        for byte in data:
            crc = ((crc << 8) ^ self.lookup_table[((crc >> (self.width - 8)) ^ byte) & 0xFF]) & ((1 << self.width) - 1)
        
        # Convert to bytes based on width
        if self.width <= 8:
            return bytes([crc])
        elif self.width <= 16:
            return struct.pack('>H', crc)
        elif self.width <= 32:
            return struct.pack('>I', crc)
        else:
            # For wider CRCs, return as many bytes as needed
            num_bytes = (self.width + 7) // 8
            return crc.to_bytes(num_bytes, 'big')
    
    def add_crc(self, data: str) -> str:
        """
        Add CRC to data.
        
        Args:
            data (str): Binary string data
            
        Returns:
            str: Data with CRC appended
        """
        crc = self.calculate_crc_table(data)
        return data + crc
    
    def verify_crc(self, data_with_crc: str) -> Tuple[bool, str]:
        """
        Verify CRC of data.
        
        Args:
            data_with_crc (str): Binary string with CRC appended
            
        Returns:
            Tuple[bool, str]: (is_valid, original_data)
        """
        if len(data_with_crc) < self.width:
            raise ValueError(f"Data must be at least {self.width} bits long")
        
        # Separate data and CRC
        data = data_with_crc[:-self.width]
        received_crc = data_with_crc[-self.width:]
        
        # Calculate expected CRC
        expected_crc = self.calculate_crc_table(data)
        
        is_valid = received_crc == expected_crc
        return is_valid, data
    
    def detect_errors(self, data_with_crc: str) -> Tuple[bool, str, str]:
        """
        Detect errors in data with CRC.
        
        Args:
            data_with_crc (str): Binary string with CRC appended
            
        Returns:
            Tuple[bool, str, str]: (has_errors, original_data, expected_crc)
        """
        is_valid, data = self.verify_crc(data_with_crc)
        expected_crc = self.calculate_crc_table(data)
        
        has_errors = not is_valid
        return has_errors, data, expected_crc


class CRCErrorSimulator:
    """
    Utility class for simulating errors in CRC-protected data.
    """
    
    @staticmethod
    def introduce_single_bit_error(data: str, position: int = None) -> str:
        """
        Introduce a single bit error in the data.
        
        Args:
            data (str): Binary string data
            position (int): Position to flip bit (random if None)
            
        Returns:
            str: Data with single bit error
        """
        if position is None:
            import random
            position = random.randint(0, len(data) - 1)
        
        if position >= len(data):
            raise ValueError("Position out of range")
        
        data_list = list(data)
        data_list[position] = '1' if data_list[position] == '0' else '0'
        return ''.join(data_list)
    
    @staticmethod
    def introduce_burst_error(data: str, start_pos: int, length: int) -> str:
        """
        Introduce a burst error (multiple consecutive bit errors).
        
        Args:
            data (str): Binary string data
            start_pos (int): Starting position of burst error
            length (int): Length of burst error
            
        Returns:
            str: Data with burst error
        """
        if start_pos + length > len(data):
            raise ValueError("Burst error extends beyond data length")
        
        data_list = list(data)
        for i in range(start_pos, start_pos + length):
            data_list[i] = '1' if data_list[i] == '0' else '0'
        
        return ''.join(data_list)
    
    @staticmethod
    def introduce_random_errors(data: str, num_errors: int) -> str:
        """
        Introduce random bit errors in the data.
        
        Args:
            data (str): Binary string data
            num_errors (int): Number of random errors to introduce
            
        Returns:
            str: Data with random errors
        """
        import random
        
        if num_errors > len(data):
            raise ValueError("Number of errors cannot exceed data length")
        
        data_list = list(data)
        positions = random.sample(range(len(data)), num_errors)
        
        for pos in positions:
            data_list[pos] = '1' if data_list[pos] == '0' else '0'
        
        return ''.join(data_list)


def demonstrate_crc_methods():
    """Demonstrate different CRC methods and error detection."""
    print("=" * 60)
    print("CRC (CYCLIC REDUNDANCY CHECK) DEMONSTRATION")
    print("=" * 60)
    
    # Test data
    test_data = "1101011011001101"
    print(f"Original data: {test_data}")
    print(f"Data length: {len(test_data)} bits")
    
    # Test different CRC polynomials
    crc_types = ['CRC-8', 'CRC-16', 'CRC-32', 'CRC-CCITT']
    
    for crc_type in crc_types:
        print(f"\n--- {crc_type} ---")
        
        # Create CRC detector
        crc_detector = CRCDetection(crc_type)
        print(f"Polynomial: 0x{crc_detector.polynomial:04X}")
        print(f"Width: {crc_detector.width} bits")
        
        # Calculate CRC
        crc_bitwise = crc_detector.calculate_crc_bitwise(test_data)
        crc_table = crc_detector.calculate_crc_table(test_data)
        
        print(f"CRC (bitwise): {crc_bitwise}")
        print(f"CRC (table):   {crc_table}")
        print(f"Methods match: {crc_bitwise == crc_table}")
        
        # Add CRC to data
        data_with_crc = crc_detector.add_crc(test_data)
        print(f"Data with CRC: {data_with_crc}")
        
        # Verify CRC
        is_valid, original = crc_detector.verify_crc(data_with_crc)
        print(f"CRC verification: {'Valid' if is_valid else 'Invalid'}")
        print(f"Original data: {original}")


def demonstrate_error_detection():
    """Demonstrate CRC error detection capabilities."""
    print("\n" + "=" * 60)
    print("CRC ERROR DETECTION DEMONSTRATION")
    print("=" * 60)
    
    # Test data
    test_data = "1011010110101101"
    print(f"Original data: {test_data}")
    
    # Use CRC-16 for demonstration
    crc_detector = CRCDetection('CRC-16')
    data_with_crc = crc_detector.add_crc(test_data)
    print(f"Data with CRC-16: {data_with_crc}")
    
    # Test different types of errors
    error_simulator = CRCErrorSimulator()
    
    # Single bit error
    print("\n--- Single Bit Error ---")
    error_data = error_simulator.introduce_single_bit_error(data_with_crc, 5)
    print(f"Data with error: {error_data}")
    
    has_errors, original, expected_crc = crc_detector.detect_errors(error_data)
    print(f"Error detected: {'Yes' if has_errors else 'No'}")
    if has_errors:
        print(f"Expected CRC: {expected_crc}")
        print(f"Received CRC: {error_data[-crc_detector.width:]}")
    
    # Burst error
    print("\n--- Burst Error (3 bits) ---")
    burst_error_data = error_simulator.introduce_burst_error(data_with_crc, 8, 3)
    print(f"Data with burst error: {burst_error_data}")
    
    has_errors, original, expected_crc = crc_detector.detect_errors(burst_error_data)
    print(f"Error detected: {'Yes' if has_errors else 'No'}")
    
    # Multiple random errors
    print("\n--- Multiple Random Errors (2 bits) ---")
    random_error_data = error_simulator.introduce_random_errors(data_with_crc, 2)
    print(f"Data with random errors: {random_error_data}")
    
    has_errors, original, expected_crc = crc_detector.detect_errors(random_error_data)
    print(f"Error detected: {'Yes' if has_errors else 'No'}")


def demonstrate_byte_level_crc():
    """Demonstrate CRC calculation for byte data."""
    print("\n" + "=" * 60)
    print("BYTE-LEVEL CRC DEMONSTRATION")
    print("=" * 60)
    
    # Test with ASCII string
    test_string = "Hello, World!"
    test_bytes = test_string.encode('ascii')
    print(f"Test string: {test_string}")
    print(f"ASCII bytes: {test_bytes.hex()}")
    
    # Calculate CRC for different polynomials
    for crc_type in ['CRC-8', 'CRC-16', 'CRC-32']:
        crc_detector = CRCDetection(crc_type)
        crc_bytes = crc_detector.calculate_crc_bytes(test_bytes)
        print(f"{crc_type} checksum: {crc_bytes.hex()}")


def main():
    """Main function to demonstrate CRC error detection methods."""
    print("CRC ERROR DETECTION METHODS IMPLEMENTATION")
    print("==========================================")
    
    # Demonstrate CRC methods
    demonstrate_crc_methods()
    
    # Demonstrate error detection
    demonstrate_error_detection()
    
    # Demonstrate byte-level CRC
    demonstrate_byte_level_crc()
    
    print("\n" + "=" * 60)
    print("INTERACTIVE TESTING")
    print("=" * 60)
    
    # Interactive testing
    while True:
        print("\nChoose an option:")
        print("1. Test CRC calculation")
        print("2. Test error detection")
        print("3. Test byte-level CRC")
        print("4. Compare CRC polynomials")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            data = input("Enter binary data: ").strip()
            crc_type = input("Enter CRC type (CRC-8, CRC-16, CRC-32, CRC-CCITT): ").strip()
            
            try:
                crc_detector = CRCDetection(crc_type)
                crc = crc_detector.calculate_crc_table(data)
                data_with_crc = crc_detector.add_crc(data)
                
                print(f"CRC ({crc_type}): {crc}")
                print(f"Data with CRC: {data_with_crc}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            data = input("Enter binary data: ").strip()
            crc_type = input("Enter CRC type: ").strip()
            
            try:
                crc_detector = CRCDetection(crc_type)
                data_with_crc = crc_detector.add_crc(data)
                
                # Introduce error
                error_pos = int(input("Enter position to introduce error (0-based): "))
                error_data = CRCErrorSimulator.introduce_single_bit_error(data_with_crc, error_pos)
                
                print(f"Original data with CRC: {data_with_crc}")
                print(f"Data with error: {error_data}")
                
                has_errors, original, expected_crc = crc_detector.detect_errors(error_data)
                print(f"Error detected: {'Yes' if has_errors else 'No'}")
                if has_errors:
                    print(f"Expected CRC: {expected_crc}")
                    print(f"Received CRC: {error_data[-crc_detector.width:]}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            text = input("Enter text string: ").strip()
            crc_type = input("Enter CRC type: ").strip()
            
            try:
                crc_detector = CRCDetection(crc_type)
                text_bytes = text.encode('ascii')
                crc_bytes = crc_detector.calculate_crc_bytes(text_bytes)
                
                print(f"Text: {text}")
                print(f"ASCII bytes: {text_bytes.hex()}")
                print(f"{crc_type} checksum: {crc_bytes.hex()}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '4':
            data = input("Enter binary data: ").strip()
            
            print(f"\nCRC comparison for data: {data}")
            print("-" * 50)
            
            for crc_type in ['CRC-8', 'CRC-16', 'CRC-32', 'CRC-CCITT']:
                try:
                    crc_detector = CRCDetection(crc_type)
                    crc = crc_detector.calculate_crc_table(data)
                    print(f"{crc_type:10}: {crc}")
                except ValueError as e:
                    print(f"{crc_type:10}: Error - {e}")
        
        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
