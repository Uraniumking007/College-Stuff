"""
Test script for error detection methods
======================================

This script provides unit tests for the error detection implementations.
"""

import unittest
from error_detection import SimpleParityCheck, TwoDimensionalParityCheck


class TestSimpleParityCheck(unittest.TestCase):
    """Test cases for Simple Parity Check."""
    
    def test_even_parity_addition(self):
        """Test adding even parity bit."""
        # Test case 1: Even number of 1s
        data = "1010"
        result = SimpleParityCheck.add_parity_bit(data, 'even')
        self.assertEqual(result, "10100")  # Should add 0
        
        # Test case 2: Odd number of 1s
        data = "1011"
        result = SimpleParityCheck.add_parity_bit(data, 'even')
        self.assertEqual(result, "10111")  # Should add 1
    
    def test_odd_parity_addition(self):
        """Test adding odd parity bit."""
        # Test case 1: Even number of 1s
        data = "1010"
        result = SimpleParityCheck.add_parity_bit(data, 'odd')
        self.assertEqual(result, "10101")  # Should add 1
        
        # Test case 2: Odd number of 1s
        data = "1011"
        result = SimpleParityCheck.add_parity_bit(data, 'odd')
        self.assertEqual(result, "10110")  # Should add 0
    
    def test_parity_check_valid(self):
        """Test parity check with valid data."""
        data_with_parity = "10100"  # Even parity
        is_valid, original = SimpleParityCheck.check_parity(data_with_parity, 'even')
        self.assertTrue(is_valid)
        self.assertEqual(original, "1010")
    
    def test_parity_check_invalid(self):
        """Test parity check with invalid data."""
        data_with_parity = "10101"  # Wrong parity for even
        is_valid, original = SimpleParityCheck.check_parity(data_with_parity, 'even')
        self.assertFalse(is_valid)
        self.assertEqual(original, "1010")
    
    def test_invalid_input(self):
        """Test with invalid input data."""
        with self.assertRaises(ValueError):
            SimpleParityCheck.add_parity_bit("1012", 'even')
        
        with self.assertRaises(ValueError):
            SimpleParityCheck.check_parity("1012", 'even')


class TestTwoDimensionalParityCheck(unittest.TestCase):
    """Test cases for 2D Parity Check."""
    
    def test_create_2d_parity_matrix(self):
        """Test creating 2D parity matrix."""
        data = "101101010"
        matrix = TwoDimensionalParityCheck.create_2d_parity_matrix(data, 3, 3)
        
        # Check dimensions
        self.assertEqual(matrix.shape, (4, 4))  # 3x3 data + 1 row + 1 col parity
        
        # Check that original data is preserved
        expected_data = [[1, 0, 1], [1, 0, 1], [0, 1, 0]]
        for i in range(3):
            for j in range(3):
                self.assertEqual(matrix[i, j], expected_data[i][j])
    
    def test_2d_parity_check_valid(self):
        """Test 2D parity check with valid data."""
        data = "101101010"
        matrix = TwoDimensionalParityCheck.create_2d_parity_matrix(data, 3, 3)
        is_valid, errors = TwoDimensionalParityCheck.check_2d_parity(matrix)
        
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_2d_parity_check_invalid(self):
        """Test 2D parity check with invalid data."""
        data = "101101010"
        matrix = TwoDimensionalParityCheck.create_2d_parity_matrix(data, 3, 3)
        
        # Introduce error
        matrix[1, 1] = 1 - matrix[1, 1]
        
        is_valid, errors = TwoDimensionalParityCheck.check_2d_parity(matrix)
        
        self.assertFalse(is_valid)
        self.assertIn((1, 1), errors)
    
    def test_error_correction(self):
        """Test error correction functionality."""
        data = "101101010"
        matrix = TwoDimensionalParityCheck.create_2d_parity_matrix(data, 3, 3)
        
        # Introduce error
        matrix[1, 1] = 1 - matrix[1, 1]
        
        # Detect errors
        is_valid, errors = TwoDimensionalParityCheck.check_2d_parity(matrix)
        self.assertFalse(is_valid)
        
        # Correct errors
        corrected_matrix = TwoDimensionalParityCheck.correct_errors(matrix, errors)
        
        # Verify correction
        is_corrected, _ = TwoDimensionalParityCheck.check_2d_parity(corrected_matrix)
        self.assertTrue(is_corrected)


def run_quick_demo():
    """Run a quick demonstration of the error detection methods."""
    print("QUICK DEMONSTRATION")
    print("==================")
    
    # Simple Parity Check Demo
    print("\n1. Simple Parity Check:")
    data = "1101010"
    print(f"   Original data: {data}")
    
    # Add even parity
    with_parity = SimpleParityCheck.add_parity_bit(data, 'even')
    print(f"   With even parity: {with_parity}")
    
    # Check parity
    is_valid, original = SimpleParityCheck.check_parity(with_parity, 'even')
    print(f"   Parity check: {'Valid' if is_valid else 'Invalid'}")
    
    # 2D Parity Check Demo
    print("\n2. 2D Parity Check:")
    data_2d = "101101010"
    print(f"   Original data: {data_2d}")
    
    # Create matrix
    matrix = TwoDimensionalParityCheck.create_2d_parity_matrix(data_2d, 3, 3)
    print(f"   2D Parity Matrix:")
    for row in matrix:
        print(f"   {row}")
    
    # Check parity
    is_valid_2d, errors = TwoDimensionalParityCheck.check_2d_parity(matrix)
    print(f"   Parity check: {'Valid' if is_valid_2d else 'Invalid'}")
    if errors:
        print(f"   Error locations: {errors}")


if __name__ == "__main__":
    # Run quick demo
    run_quick_demo()
    
    # Run unit tests
    print("\n" + "="*50)
    print("RUNNING UNIT TESTS")
    print("="*50)
    unittest.main(argv=[''], exit=False, verbosity=2)
