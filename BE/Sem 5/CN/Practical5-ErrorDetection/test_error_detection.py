"""
Lightweight tests adjusted for the simplified API in error_detection.py.

These tests exercise only:
 - SimpleParityCheck.check_parity
 - TwoDimensionalParityCheck.check_2d_parity

They construct parity-bearing inputs directly instead of relying on helper functions.
"""

import unittest
import numpy as np

from error_detection import SimpleParityCheck, TwoDimensionalParityCheck


class TestSimpleParityCheck(unittest.TestCase):
    """Test cases for Simple Parity Check (check_parity only)."""

    def test_parity_check_valid(self):
        data_with_parity = "10100"  # Even parity for "1010"
        is_valid, original = SimpleParityCheck.check_parity(data_with_parity, 'even')
        self.assertTrue(is_valid)
        self.assertEqual(original, "1010")

    def test_parity_check_invalid(self):
        data_with_parity = "10101"  # Wrong parity for even
        is_valid, original = SimpleParityCheck.check_parity(data_with_parity, 'even')
        self.assertFalse(is_valid)
        self.assertEqual(original, "1010")

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            SimpleParityCheck.check_parity("1012", 'even')

        with self.assertRaises(ValueError):
            SimpleParityCheck.check_parity("1", 'even')  # too short


def _build_2d_parity_matrix(data: str, rows: int, cols: int) -> np.ndarray:
    """Helper to build an extended parity matrix (rows+1 x cols+1) from raw data."""
    if len(data) != rows * cols:
        raise ValueError("Invalid data length for specified dimensions")

    mat = np.array([int(b) for b in data]).reshape(rows, cols)

    # row parities
    row_parities = [(1 if row.sum() % 2 == 1 else 0) for row in mat]
    # column parities
    col_parities = [(1 if col.sum() % 2 == 1 else 0) for col in mat.T]

    extended = np.zeros((rows + 1, cols + 1), dtype=int)
    extended[:rows, :cols] = mat
    extended[:rows, cols] = row_parities
    extended[rows, :cols] = col_parities
    extended[rows, cols] = 1 if sum(row_parities) % 2 == 1 else 0
    return extended


class TestTwoDimensionalParityCheck(unittest.TestCase):
    """Test cases for 2D parity check using constructed matrices."""

    def test_2d_parity_check_valid(self):
        data = "101101010"
        matrix = _build_2d_parity_matrix(data, 3, 3)
        is_valid, errors = TwoDimensionalParityCheck.check_2d_parity(matrix)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_2d_parity_check_invalid(self):
        data = "101101010"
        matrix = _build_2d_parity_matrix(data, 3, 3)
        # flip a data bit
        matrix[1, 1] = 1 - matrix[1, 1]
        is_valid, errors = TwoDimensionalParityCheck.check_2d_parity(matrix)
        self.assertFalse(is_valid)
        self.assertIn((1, 1), errors)


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False, verbosity=2)
