from typing import List, Tuple, Sequence
import numpy as np


class SimpleParityCheck:
    @staticmethod
    def check_parity(data_with_parity: str, parity_type: str = 'even') -> Tuple[bool, str]:
        if not isinstance(data_with_parity, str) or not data_with_parity:
            raise ValueError("Data must be a non-empty binary string")

        if any(c not in '01' for c in data_with_parity):
            raise ValueError("Data must contain only binary digits (0 and 1)")

        if len(data_with_parity) < 2:
            raise ValueError("Data must contain at least one data bit and one parity bit")

        data, received_parity = data_with_parity[:-1], data_with_parity[-1]
        ones = data.count('1')

        if parity_type == 'even':
            expected = '0' if ones % 2 == 0 else '1'
        elif parity_type == 'odd':
            expected = '1' if ones % 2 == 0 else '0'
        else:
            raise ValueError("Parity type must be 'even' or 'odd'")

        return (received_parity == expected), data


class TwoDimensionalParityCheck:
    @staticmethod
    def check_2d_parity(matrix: Sequence[Sequence[int]]) -> Tuple[bool, List[Tuple[int, int]]]:
        arr = np.asarray(matrix, dtype=int)

        if arr.ndim != 2 or arr.shape[0] < 2 or arr.shape[1] < 2:
            raise ValueError("Matrix must be at least 2x2 (data + parity row/col)")

        data_block = arr[:-1, :-1]

        # Expected parity bits
        expected_row = (data_block.sum(axis=1) % 2).astype(int)
        expected_col = (data_block.sum(axis=0) % 2).astype(int)

        actual_row = arr[:-1, -1].astype(int)
        actual_col = arr[-1, :-1].astype(int)

        row_err_idx = np.where(expected_row != actual_row)[0]
        col_err_idx = np.where(expected_col != actual_col)[0]

        # Cartesian product of differing rows and columns are error bit positions
        error_locations: List[Tuple[int, int]] = [(int(r), int(c)) for r in row_err_idx for c in col_err_idx]

        return (len(error_locations) == 0), error_locations




def demo_false():
    # Very small demo showing examples that produce invalid/False results.
    s = "1010"
    bad = s + '1'  # wrong parity bit
    valid, orig = SimpleParityCheck.check_parity(bad, 'even')
    print(f"Simple false demo: {bad} -> valid={valid}, original={orig}")

    # 2D parity: build 2x2 and flip a data bit
    data2 = "1010"
    arr = np.fromiter((int(b) for b in data2), dtype=int).reshape(2, 2)
    # flip one data bit
    arr[0, 0] = 1 - arr[0, 0]
    ext = np.zeros((3, 3), dtype=int)
    ext[:2, :2] = arr
    ext[:2, 2] = (arr.sum(axis=1) % 2)
    ext[2, :2] = (arr.sum(axis=0) % 2)
    ext[2, 2] = int(ext[:2, 2].sum() % 2)
    valid2, errs2 = TwoDimensionalParityCheck.check_2d_parity(ext)
    print(f"2D false demo: flipped bit -> valid={valid2}, errors={errs2}")

def demo():
    """Very small demo showing function usage (call manually)."""
    s = "1010"
    valid, orig = SimpleParityCheck.check_parity(s + '0', 'even')
    print(f"Simple demo: {s}+parity -> valid={valid}, original={orig}")

    # 2x2 data -> extended 3x3 matrix
    data2 = "1010"
    arr = np.fromiter((int(b) for b in data2), dtype=int).reshape(2, 2)
    ext = np.zeros((3, 3), dtype=int)
    ext[:2, :2] = arr
    ext[:2, 2] = (arr.sum(axis=1) % 2)
    ext[2, :2] = (arr.sum(axis=0) % 2)
    ext[2, 2] = int(ext[:2, 2].sum() % 2)
    valid2, errs2 = TwoDimensionalParityCheck.check_2d_parity(ext)
    print(f"2D demo: 2x2 data -> valid={valid2}, errors={errs2}")
    demo_false()


demo()