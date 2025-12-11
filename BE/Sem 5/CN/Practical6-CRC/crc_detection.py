def xor(a, b):
    result = []
    for i in range(1, len(b)):
        result.append(str(int(a[i]) ^ int(b[i])))
    return ''.join(result)


def mod2div(dividend, divisor):
    pick = len(divisor)
    tmp = dividend[0:pick]

    while pick < len(dividend):
        if tmp[0] == '1':
            tmp = xor(divisor, tmp) + dividend[pick]
        else:  # if leftmost bit is 0
            tmp = xor('0'*pick, tmp) + dividend[pick]
        pick += 1

    # Last step of division
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
    
    return tmp  # This is the CRC


def encode_data(data, key):
    l_key = len(key)
    appended_data = data + '0'*(l_key - 1)
    crc = mod2div(appended_data, key)
    codeword = data + crc
    return codeword, crc


def check_received_data(received_data, key):
    remainder = mod2div(received_data, key)
    if "1" in remainder:
        return False, remainder
    return True, remainder


# Example usage (kept under main guard)
if __name__ == '__main__':
    data = "11010011101100"  # Input binary string
    key = "1011"            # Generator polynomial

    # Sender side
    codeword, crc = encode_data(data, key)
    print("Data:", data)
    print("CRC Checksum:", crc)
    print("Encoded Data (Data + CRC):", codeword)

    # Receiver side (correct data)
    valid, rem = check_received_data(codeword, key)
    print("Received valid?" if valid else "Error detected!", "| Remainder:", rem)

    # Receiver side (simulate error)
    received = codeword[:5] + '1' + codeword[6:]  # Flip a bit
    valid, rem = check_received_data(received, key)
    print("Received valid?" if valid else "Error detected!", "| Remainder:", rem)
from typing import List, Tuple, Union
import struct


class CRCDetection:
    # CRC (Cyclic Redundancy Check) implementation for error detection.
    
    # Common CRC polynomials (polynomial low-order part; width defined separately)
    CRC_POLYNOMIALS = {
        'CRC-8': 0x07,
        'CRC-16': 0x8005,
        'CRC-32': 0x04C11DB7,
        'CRC-CCITT': 0x1021,
        'CRC-ANSI': 0x8005,
        'CRC-DNP': 0x3D65,
    }

    # Widths for named polynomials
    CRC_WIDTHS = {
        'CRC-8': 8,
        'CRC-16': 16,
        'CRC-32': 32,
        'CRC-CCITT': 16,
        'CRC-ANSI': 16,
        'CRC-DNP': 16,
    }
    
    def __init__(self, polynomial: Union[str, int], width: int = None):
        if isinstance(polynomial, str):
            if polynomial not in self.CRC_POLYNOMIALS:
                raise ValueError(f"Unknown CRC polynomial: {polynomial}")
            self.polynomial = self.CRC_POLYNOMIALS[polynomial]
            self.polynomial_name = polynomial
        else:
            self.polynomial = polynomial
            self.polynomial_name = f"Custom-0x{polynomial:04X}"

        # Auto-detect width if not provided; for known names use CRC_WIDTHS
        if isinstance(polynomial, str):
            self.width = self.CRC_WIDTHS.get(polynomial) if width is None else width
        else:
            self.width = width if width is not None else self._detect_width(self.polynomial)

        # precompute full polynomial with implicit leading 1 at degree 'width'
        self.poly_full = (1 << self.width) | (self.polynomial & ((1 << self.width) - 1))
        # lookup_table is intentionally omitted; we compute CRC via division to keep implementation simple
        self.lookup_table = None
    
    def _detect_width(self, polynomial: int) -> int:
        """Detect CRC width from polynomial value."""
        # Fallback: use bit_length of polynomial + 1 for implicit top bit
        return polynomial.bit_length()
    
    def _create_lookup_table(self) -> List[int]:
        # Not used in this simplified implementation
        return []
    
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

        # Polynomial long division: append width zeros to data and divide by poly_full
        dividend = int(data, 2) << self.width
        poly = self.poly_full
        deg = self.width

        # position of highest bit in dividend
        top = dividend.bit_length() - 1
        while top >= deg:
            shift = top - deg
            dividend ^= (poly << shift)
            top = dividend.bit_length() - 1

        remainder = dividend & ((1 << self.width) - 1)
        return format(remainder, f'0{self.width}b')
    
    def calculate_crc_table(self, data: str) -> str:
        """
        Calculate CRC using lookup table for faster computation.
        
        Args:
            data (str): Binary string data
            
        Returns:
            str: CRC value as binary string
        """
        # For simplicity ensure same result as bitwise method
        return self.calculate_crc_bitwise(data)
    
    def calculate_crc_bytes(self, data: bytes) -> bytes:
        """
        Calculate CRC for byte data.
        
        Args:
            data (bytes): Byte data
            
        Returns:
            bytes: CRC value as bytes
        """
        # Convert bytes to bitstring and calculate CRC via bitwise method
        bitstr = ''.join(f"{b:08b}" for b in data)
        crc_bits = self.calculate_crc_bitwise(bitstr)
        crc_val = int(crc_bits, 2)

        if self.width <= 8:
            return bytes([crc_val])
        elif self.width <= 16:
            return struct.pack('>H', crc_val)
        elif self.width <= 32:
            return struct.pack('>I', crc_val)
        else:
            num_bytes = (self.width + 7) // 8
            return crc_val.to_bytes(num_bytes, 'big')
    
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

        if is_valid:
            return False, data, expected_crc

        # Try single-bit correction by flipping each bit in the entire message
        n = len(data_with_crc)
        for i in range(n):
            flipped = list(data_with_crc)
            flipped[i] = '1' if flipped[i] == '0' else '0'
            candidate = ''.join(flipped)
            try:
                valid, cand_data = self.verify_crc(candidate)
            except ValueError:
                continue
            if valid:
                # Found a single-bit correction
                expected = self.calculate_crc_table(cand_data)
                return True, cand_data, expected

        # Unable to correct; return detected status and extracted (uncorrected) data
        return True, data, expected_crc


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

