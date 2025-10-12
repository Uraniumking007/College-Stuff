"""
Test script for Hamming Code error correction methods
===================================================

This script provides unit tests for the Hamming Code implementations.
"""

import unittest
from hamming_code import HammingCode, HammingCodeErrorSimulator, HammingCodeVariants


class TestHammingCode(unittest.TestCase):
    """Test cases for Hamming Code."""
    
    def test_hamming_7_4_initialization(self):
        """Test Hamming(7,4) initialization."""
        hamming = HammingCode(4)
        info = hamming.get_info()
        
        self.assertEqual(info['data_bits'], 4)
        self.assertEqual(info['parity_bits'], 3)
        self.assertEqual(info['total_bits'], 7)
        self.assertEqual(info['parity_positions'], [1, 2, 4])
    
    def test_hamming_15_11_initialization(self):
        """Test Hamming(15,11) initialization."""
        hamming = HammingCode(11)
        info = hamming.get_info()
        
        self.assertEqual(info['data_bits'], 11)
        self.assertEqual(info['parity_bits'], 4)
        self.assertEqual(info['total_bits'], 15)
        self.assertEqual(info['parity_positions'], [1, 2, 4, 8])
    
    def test_encoding_hamming_7_4(self):
        """Test Hamming(7,4) encoding."""
        hamming = HammingCode(4)
        
        # Test case 1
        data = "1011"
        encoded = hamming.encode(data)
        self.assertEqual(len(encoded), 7)
        
        # Test case 2
        data = "0000"
        encoded = hamming.encode(data)
        self.assertEqual(len(encoded), 7)
    
    def test_encoding_hamming_15_11(self):
        """Test Hamming(15,11) encoding."""
        hamming = HammingCode(11)
        
        data = "10110101101"
        encoded = hamming.encode(data)
        self.assertEqual(len(encoded), 15)
    
    def test_decoding_without_errors(self):
        """Test decoding without errors."""
        hamming = HammingCode(4)
        
        data = "1011"
        encoded = hamming.encode(data)
        decoded, has_error, error_pos = hamming.decode(encoded)
        
        self.assertEqual(decoded, data)
        self.assertFalse(has_error)
        self.assertEqual(error_pos, 0)
    
    def test_verification_without_errors(self):
        """Test verification without errors."""
        hamming = HammingCode(4)
        
        data = "1011"
        encoded = hamming.encode(data)
        is_valid, error_pos = hamming.verify(encoded)
        
        self.assertTrue(is_valid)
        self.assertEqual(error_pos, 0)
    
    def test_single_bit_error_correction(self):
        """Test single bit error correction."""
        hamming = HammingCode(4)
        
        data = "1011"
        encoded = hamming.encode(data)
        
        # Test error at each position
        for error_pos in range(1, 8):
            error_data = HammingCodeErrorSimulator.introduce_single_bit_error(encoded, error_pos)
            decoded, has_error, detected_pos = hamming.decode(error_data)
            
            self.assertTrue(has_error)
            self.assertEqual(detected_pos, error_pos)
            self.assertEqual(decoded, data)
    
    def test_verification_with_errors(self):
        """Test verification with errors."""
        hamming = HammingCode(4)
        
        data = "1011"
        encoded = hamming.encode(data)
        
        # Introduce error at position 3
        error_data = HammingCodeErrorSimulator.introduce_single_bit_error(encoded, 3)
        is_valid, error_pos = hamming.verify(error_data)
        
        self.assertFalse(is_valid)
        self.assertEqual(error_pos, 3)
    
    def test_multiple_bit_errors(self):
        """Test multiple bit errors (should not be correctable)."""
        hamming = HammingCode(4)
        
        data = "1011"
        encoded = hamming.encode(data)
        
        # Introduce 2-bit error
        error_data = HammingCodeErrorSimulator.introduce_multiple_errors(encoded, 2)
        decoded, has_error, error_pos = hamming.decode(error_data)
        
        # Should detect error but may not correct properly
        self.assertTrue(has_error)
        # Note: The decoded data may not match original due to multiple errors
    
    def test_invalid_input_encoding(self):
        """Test encoding with invalid input."""
        hamming = HammingCode(4)
        
        # Test with non-binary data
        with self.assertRaises(ValueError):
            hamming.encode("1012")
        
        # Test with wrong length
        with self.assertRaises(ValueError):
            hamming.encode("101")  # Too short
        
        with self.assertRaises(ValueError):
            hamming.encode("10111")  # Too long
    
    def test_invalid_input_decoding(self):
        """Test decoding with invalid input."""
        hamming = HammingCode(4)
        
        # Test with non-binary data
        with self.assertRaises(ValueError):
            hamming.decode("1012011")
        
        # Test with wrong length
        with self.assertRaises(ValueError):
            hamming.decode("101101")  # Too short
        
        with self.assertRaises(ValueError):
            hamming.decode("10110111")  # Too long
    
    def test_parity_coverage_calculation(self):
        """Test parity coverage calculation."""
        hamming = HammingCode(4)
        coverage = hamming.parity_coverage
        
        # For Hamming(7,4), parity positions are [1, 2, 4]
        # Parity bit 1 (position 1) should cover positions with bit 1 set: 3, 5, 7
        # Parity bit 2 (position 2) should cover positions with bit 2 set: 3, 6, 7
        # Parity bit 4 (position 4) should cover positions with bit 4 set: 5, 6, 7
        
        expected_coverage = [
            [3, 5, 7],  # Parity bit 1
            [3, 6, 7],  # Parity bit 2
            [5, 6, 7]   # Parity bit 4
        ]
        
        self.assertEqual(coverage, expected_coverage)
    
    def test_efficiency_calculation(self):
        """Test efficiency calculation."""
        hamming = HammingCode(4)
        info = hamming.get_info()
        
        # For Hamming(7,4): efficiency = 4/7 ≈ 0.571
        expected_efficiency = 4 / 7
        self.assertAlmostEqual(info['efficiency'], expected_efficiency, places=3)


class TestHammingCodeErrorSimulator(unittest.TestCase):
    """Test cases for Hamming Code Error Simulator."""
    
    def test_single_bit_error_introduction(self):
        """Test single bit error introduction."""
        data = "1011011"
        
        # Test error at position 3
        error_data = HammingCodeErrorSimulator.introduce_single_bit_error(data, 3)
        
        # Check that only one bit is different
        differences = sum(1 for a, b in zip(data, error_data) if a != b)
        self.assertEqual(differences, 1)
        
        # Check that the specific bit was flipped
        self.assertNotEqual(data[2], error_data[2])  # Position 3 is index 2
    
    def test_multiple_errors_introduction(self):
        """Test multiple errors introduction."""
        data = "101101101101101"
        
        # Introduce 3 errors
        error_data = HammingCodeErrorSimulator.introduce_multiple_errors(data, 3)
        
        # Check that exactly 3 bits are different
        differences = sum(1 for a, b in zip(data, error_data) if a != b)
        self.assertEqual(differences, 3)
    
    def test_error_position_bounds(self):
        """Test error position bounds checking."""
        data = "1011011"
        
        # Test position out of bounds
        with self.assertRaises(ValueError):
            HammingCodeErrorSimulator.introduce_single_bit_error(data, 0)
        
        with self.assertRaises(ValueError):
            HammingCodeErrorSimulator.introduce_single_bit_error(data, 8)
    
    def test_too_many_errors(self):
        """Test too many errors."""
        data = "1011011"
        
        # Try to introduce more errors than data length
        with self.assertRaises(ValueError):
            HammingCodeErrorSimulator.introduce_multiple_errors(data, 8)


class TestHammingCodeVariants(unittest.TestCase):
    """Test cases for Hamming Code Variants."""
    
    def test_standard_variants(self):
        """Test standard variants information."""
        variants = HammingCodeVariants.get_standard_variants()
        
        self.assertIn('Hamming(7,4)', variants)
        self.assertIn('Hamming(15,11)', variants)
        self.assertIn('Hamming(31,26)', variants)
        self.assertIn('Hamming(63,57)', variants)
        
        # Check Hamming(7,4) details
        hamming_7_4 = variants['Hamming(7,4)']
        self.assertEqual(hamming_7_4['data_bits'], 4)
        self.assertEqual(hamming_7_4['total_bits'], 7)
    
    def test_efficiency_calculation(self):
        """Test efficiency calculation for different variants."""
        # Test Hamming(7,4)
        efficiency_7_4 = HammingCodeVariants.calculate_efficiency(4)
        expected_7_4 = 4 / 7
        self.assertAlmostEqual(efficiency_7_4, expected_7_4, places=3)
        
        # Test Hamming(15,11)
        efficiency_15_11 = HammingCodeVariants.calculate_efficiency(11)
        expected_15_11 = 11 / 15
        self.assertAlmostEqual(efficiency_15_11, expected_15_11, places=3)
    
    def test_large_data_bits(self):
        """Test with larger number of data bits."""
        # Test with 26 data bits (should create Hamming(31,26))
        hamming = HammingCode(26)
        info = hamming.get_info()
        
        self.assertEqual(info['data_bits'], 26)
        self.assertEqual(info['total_bits'], 31)
        self.assertEqual(info['parity_bits'], 5)


class TestHammingCodeIntegration(unittest.TestCase):
    """Integration tests for Hamming Code."""
    
    def test_complete_workflow(self):
        """Test complete encoding -> error -> decoding workflow."""
        hamming = HammingCode(4)
        
        # Test with multiple data patterns
        test_cases = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111",
                     "1000", "1001", "1010", "1011", "1100", "1101", "1110", "1111"]
        
        for data in test_cases:
            # Encode
            encoded = hamming.encode(data)
            
            # Verify no errors initially
            is_valid, _ = hamming.verify(encoded)
            self.assertTrue(is_valid)
            
            # Decode without errors
            decoded, has_error, _ = hamming.decode(encoded)
            self.assertFalse(has_error)
            self.assertEqual(decoded, data)
            
            # Test single bit error correction
            for error_pos in range(1, len(encoded) + 1):
                error_data = HammingCodeErrorSimulator.introduce_single_bit_error(encoded, error_pos)
                corrected, has_error, detected_pos = hamming.decode(error_data)
                
                self.assertTrue(has_error)
                self.assertEqual(detected_pos, error_pos)
                self.assertEqual(corrected, data)
    
    def test_different_hamming_variants(self):
        """Test different Hamming Code variants."""
        variants = [4, 8, 11, 16]
        
        for data_bits in variants:
            hamming = HammingCode(data_bits)
            
            # Create test data
            data = "1" * data_bits
            
            # Encode
            encoded = hamming.encode(data)
            
            # Verify
            is_valid, _ = hamming.verify(encoded)
            self.assertTrue(is_valid)
            
            # Decode
            decoded, has_error, _ = hamming.decode(encoded)
            self.assertFalse(has_error)
            self.assertEqual(decoded, data)


def run_quick_demo():
    """Run a quick demonstration of the Hamming Code methods."""
    print("QUICK HAMMING CODE DEMONSTRATION")
    print("===============================")
    
    # Test Hamming(7,4)
    print("\n1. Hamming(7,4) Code:")
    hamming = HammingCode(4)
    data = "1011"
    encoded = hamming.encode(data)
    decoded, has_error, error_pos = hamming.decode(encoded)
    
    print(f"   Original data: {data}")
    print(f"   Encoded data: {encoded}")
    print(f"   Decoded data: {decoded}")
    print(f"   Error detected: {'Yes' if has_error else 'No'}")
    
    # Test error correction
    print("\n2. Error Correction:")
    error_data = HammingCodeErrorSimulator.introduce_single_bit_error(encoded, 3)
    corrected, has_error, detected_pos = hamming.decode(error_data)
    
    print(f"   Data with error: {error_data}")
    print(f"   Error detected at position: {detected_pos}")
    print(f"   Corrected data: {corrected}")
    print(f"   Correction successful: {'Yes' if corrected == data else 'No'}")
    
    # Test efficiency
    print("\n3. Efficiency:")
    info = hamming.get_info()
    print(f"   Data bits: {info['data_bits']}")
    print(f"   Total bits: {info['total_bits']}")
    print(f"   Efficiency: {info['efficiency']:.3f}")


if __name__ == "__main__":
    # Run quick demo
    run_quick_demo()
    
    # Run unit tests
    print("\n" + "="*60)
    print("RUNNING UNIT TESTS")
    print("="*60)
    unittest.main(argv=[''], exit=False, verbosity=2)
