"""
Test script for CRC error detection methods
==========================================

This script provides unit tests for the CRC detection implementations.
"""

import unittest
from crc_detection import CRCDetection, CRCErrorSimulator


class TestCRCDetection(unittest.TestCase):
    """Test cases for CRC Detection."""
    
    def test_crc_8_calculation(self):
        """Test CRC-8 calculation."""
        crc_detector = CRCDetection('CRC-8')
        
        # Test data
        data = "11010110"
        crc_bitwise = crc_detector.calculate_crc_bitwise(data)
        crc_table = crc_detector.calculate_crc_table(data)
        
        # Both methods should give same result
        self.assertEqual(crc_bitwise, crc_table)
        self.assertEqual(len(crc_bitwise), 8)
    
    def test_crc_16_calculation(self):
        """Test CRC-16 calculation."""
        crc_detector = CRCDetection('CRC-16')
        
        # Test data
        data = "1101011011001101"
        crc_bitwise = crc_detector.calculate_crc_bitwise(data)
        crc_table = crc_detector.calculate_crc_table(data)
        
        # Both methods should give same result
        self.assertEqual(crc_bitwise, crc_table)
        self.assertEqual(len(crc_bitwise), 16)
    
    def test_crc_32_calculation(self):
        """Test CRC-32 calculation."""
        crc_detector = CRCDetection('CRC-32')
        
        # Test data
        data = "110101101100110101011001"
        crc_bitwise = crc_detector.calculate_crc_bitwise(data)
        crc_table = crc_detector.calculate_crc_table(data)
        
        # Both methods should give same result
        self.assertEqual(crc_bitwise, crc_table)
        self.assertEqual(len(crc_bitwise), 32)
    
    def test_crc_ccitt_calculation(self):
        """Test CRC-CCITT calculation."""
        crc_detector = CRCDetection('CRC-CCITT')
        
        # Test data
        data = "1101011011001101"
        crc_bitwise = crc_detector.calculate_crc_bitwise(data)
        crc_table = crc_detector.calculate_crc_table(data)
        
        # Both methods should give same result
        self.assertEqual(crc_bitwise, crc_table)
        self.assertEqual(len(crc_bitwise), 16)
    
    def test_add_and_verify_crc(self):
        """Test adding and verifying CRC."""
        crc_detector = CRCDetection('CRC-16')
        
        # Test data
        data = "1011010110101101"
        
        # Add CRC
        data_with_crc = crc_detector.add_crc(data)
        
        # Verify CRC
        is_valid, original = crc_detector.verify_crc(data_with_crc)
        
        self.assertTrue(is_valid)
        self.assertEqual(original, data)
        self.assertEqual(len(data_with_crc), len(data) + 16)
    
    def test_error_detection(self):
        """Test error detection."""
        crc_detector = CRCDetection('CRC-16')
        
        # Test data
        data = "1011010110101101"
        data_with_crc = crc_detector.add_crc(data)
        
        # Introduce error
        error_data = CRCErrorSimulator.introduce_single_bit_error(data_with_crc, 5)
        
        # Detect error
        has_errors, original, expected_crc = crc_detector.detect_errors(error_data)
        
        self.assertTrue(has_errors)
        self.assertEqual(original, data)
    
    def test_byte_level_crc(self):
        """Test byte-level CRC calculation."""
        crc_detector = CRCDetection('CRC-16')
        
        # Test with ASCII string
        test_string = "Hello"
        test_bytes = test_string.encode('ascii')
        crc_bytes = crc_detector.calculate_crc_bytes(test_bytes)
        
        # CRC should be 2 bytes for CRC-16
        self.assertEqual(len(crc_bytes), 2)
    
    def test_custom_polynomial(self):
        """Test custom polynomial."""
        # Custom polynomial: x^8 + x^2 + x + 1 (same as CRC-8)
        custom_poly = 0x07
        crc_detector = CRCDetection(custom_poly, width=8)
        
        data = "11010110"
        crc = crc_detector.calculate_crc_table(data)
        
        self.assertEqual(len(crc), 8)
    
    def test_invalid_input(self):
        """Test with invalid input."""
        crc_detector = CRCDetection('CRC-8')
        
        # Test with non-binary data
        with self.assertRaises(ValueError):
            crc_detector.calculate_crc_bitwise("1102")
        
        with self.assertRaises(ValueError):
            crc_detector.calculate_crc_table("1102")
    
    def test_short_data_with_crc(self):
        """Test with data shorter than CRC width."""
        crc_detector = CRCDetection('CRC-16')
        
        # Data shorter than CRC width
        short_data = "11010110"  # 8 bits, but CRC is 16 bits
        
        with self.assertRaises(ValueError):
            crc_detector.verify_crc(short_data)


class TestCRCErrorSimulator(unittest.TestCase):
    """Test cases for CRC Error Simulator."""
    
    def test_single_bit_error(self):
        """Test single bit error introduction."""
        data = "11010110"
        
        # Introduce error at position 2
        error_data = CRCErrorSimulator.introduce_single_bit_error(data, 2)
        
        # Check that only one bit is different
        differences = sum(1 for a, b in zip(data, error_data) if a != b)
        self.assertEqual(differences, 1)
        
        # Check that the specific bit was flipped
        self.assertNotEqual(data[2], error_data[2])
    
    def test_burst_error(self):
        """Test burst error introduction."""
        data = "1101011011001101"
        
        # Introduce burst error of length 3 starting at position 4
        error_data = CRCErrorSimulator.introduce_burst_error(data, 4, 3)
        
        # Check that exactly 3 bits are different
        differences = sum(1 for a, b in zip(data, error_data) if a != b)
        self.assertEqual(differences, 3)
        
        # Check that the burst is in the correct position
        for i in range(4, 7):
            self.assertNotEqual(data[i], error_data[i])
    
    def test_random_errors(self):
        """Test random error introduction."""
        data = "1101011011001101"
        
        # Introduce 2 random errors
        error_data = CRCErrorSimulator.introduce_random_errors(data, 2)
        
        # Check that exactly 2 bits are different
        differences = sum(1 for a, b in zip(data, error_data) if a != b)
        self.assertEqual(differences, 2)
    
    def test_error_position_bounds(self):
        """Test error position bounds checking."""
        data = "11010110"
        
        # Test position out of bounds
        with self.assertRaises(ValueError):
            CRCErrorSimulator.introduce_single_bit_error(data, 10)
        
        with self.assertRaises(ValueError):
            CRCErrorSimulator.introduce_burst_error(data, 5, 5)
    
    def test_too_many_random_errors(self):
        """Test too many random errors."""
        data = "11010110"
        
        # Try to introduce more errors than data length
        with self.assertRaises(ValueError):
            CRCErrorSimulator.introduce_random_errors(data, 10)


class TestCRCComparison(unittest.TestCase):
    """Test cases for comparing different CRC methods."""
    
    def test_different_polynomials_same_data(self):
        """Test that different polynomials give different results."""
        data = "1101011011001101"
        
        crc_8 = CRCDetection('CRC-8')
        crc_16 = CRCDetection('CRC-16')
        crc_32 = CRCDetection('CRC-32')
        
        crc_8_result = crc_8.calculate_crc_table(data)
        crc_16_result = crc_16.calculate_crc_table(data)
        crc_32_result = crc_32.calculate_crc_table(data)
        
        # All should be different
        self.assertNotEqual(crc_8_result, crc_16_result)
        self.assertNotEqual(crc_16_result, crc_32_result)
        self.assertNotEqual(crc_8_result, crc_32_result)
    
    def test_same_polynomial_different_data(self):
        """Test that same polynomial gives different results for different data."""
        crc_detector = CRCDetection('CRC-16')
        
        data1 = "1101011011001101"
        data2 = "1101011011001100"  # One bit different
        
        crc1 = crc_detector.calculate_crc_table(data1)
        crc2 = crc_detector.calculate_crc_table(data2)
        
        # Should be different
        self.assertNotEqual(crc1, crc2)


def run_quick_demo():
    """Run a quick demonstration of the CRC methods."""
    print("QUICK CRC DEMONSTRATION")
    print("======================")
    
    # Test data
    data = "1101011011001101"
    print(f"Test data: {data}")
    
    # Test CRC-16
    print("\n1. CRC-16:")
    crc_16 = CRCDetection('CRC-16')
    crc = crc_16.calculate_crc_table(data)
    data_with_crc = crc_16.add_crc(data)
    print(f"   CRC: {crc}")
    print(f"   Data with CRC: {data_with_crc}")
    
    # Test error detection
    print("\n2. Error Detection:")
    error_data = CRCErrorSimulator.introduce_single_bit_error(data_with_crc, 5)
    has_errors, original, expected_crc = crc_16.detect_errors(error_data)
    print(f"   Data with error: {error_data}")
    print(f"   Error detected: {'Yes' if has_errors else 'No'}")
    
    # Test byte-level CRC
    print("\n3. Byte-level CRC:")
    text = "Hello"
    text_bytes = text.encode('ascii')
    crc_bytes = crc_16.calculate_crc_bytes(text_bytes)
    print(f"   Text: {text}")
    print(f"   ASCII bytes: {text_bytes.hex()}")
    print(f"   CRC-16 checksum: {crc_bytes.hex()}")


if __name__ == "__main__":
    # Run quick demo
    run_quick_demo()
    
    # Run unit tests
    print("\n" + "="*60)
    print("RUNNING UNIT TESTS")
    print("="*60)
    unittest.main(argv=[''], exit=False, verbosity=2)
