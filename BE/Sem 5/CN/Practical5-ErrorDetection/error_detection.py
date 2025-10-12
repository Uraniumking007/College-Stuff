import numpy as np
from typing import List, Tuple, Union


class SimpleParityCheck:
    """
    This method adds a single parity bit to detect odd number of bit errors.
    """
    
    @staticmethod
    def add_parity_bit(data: str, parity_type: str = 'even') -> str:
        """
        Add parity bit to the data.
        
        Args:
            data (str): Binary string data
            parity_type (str): 'even' or 'odd' parity
            
        Returns:
            str: Data with parity bit appended
        """
        if not all(bit in '01' for bit in data):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        # Count number of 1s in the data
        ones_count = data.count('1')
        
        if parity_type == 'even':
            # Even parity: parity bit makes total number of 1s even
            parity_bit = '0' if ones_count % 2 == 0 else '1'
        elif parity_type == 'odd':
            # Odd parity: parity bit makes total number of 1s odd
            parity_bit = '1' if ones_count % 2 == 0 else '0'
        else:
            raise ValueError("Parity type must be 'even' or 'odd'")
        
        return data + parity_bit
    
    @staticmethod
    def check_parity(data_with_parity: str, parity_type: str = 'even') -> Tuple[bool, str]:
        """
        Check if the data has correct parity.
        
        Args:
            data_with_parity (str): Binary string with parity bit
            parity_type (str): 'even' or 'odd' parity
            
        Returns:
            Tuple[bool, str]: (is_valid, original_data)
        """
        if not all(bit in '01' for bit in data_with_parity):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        if len(data_with_parity) < 2:
            raise ValueError("Data must contain at least one data bit and one parity bit")
        
        # Separate data and parity bit
        data = data_with_parity[:-1]
        received_parity = data_with_parity[-1]
        
        # Calculate expected parity
        ones_count = data.count('1')
        
        if parity_type == 'even':
            expected_parity = '0' if ones_count % 2 == 0 else '1'
        elif parity_type == 'odd':
            expected_parity = '1' if ones_count % 2 == 0 else '0'
        else:
            raise ValueError("Parity type must be 'even' or 'odd'")
        
        is_valid = received_parity == expected_parity
        return is_valid, data


class TwoDimensionalParityCheck:
    """
    2D Parity Check implementation for error detection and correction.
    
    This method arranges data in a matrix and adds parity bits for each row and column.
    """
    
    @staticmethod
    def create_2d_parity_matrix(data: str, rows: int, cols: int) -> np.ndarray:
        """
        Create a 2D parity matrix from binary data.
        
        Args:
            data (str): Binary string data
            rows (int): Number of rows in the matrix
            cols (int): Number of columns in the matrix
            
        Returns:
            np.ndarray: 2D matrix with parity bits
        """
        if not all(bit in '01' for bit in data):
            raise ValueError("Data must contain only binary digits (0 and 1)")
        
        if len(data) != rows * cols:
            raise ValueError(f"Data length ({len(data)}) must equal rows * cols ({rows * cols})")
        
        # Create matrix from data
        matrix = np.array([int(bit) for bit in data]).reshape(rows, cols)
        
        # Add row parity bits
        row_parities = []
        for row in matrix:
            row_parities.append(1 if row.sum() % 2 == 1 else 0)
        
        # Add column parity bits
        col_parities = []
        for col in matrix.T:
            col_parities.append(1 if col.sum() % 2 == 1 else 0)
        
        # Create extended matrix with parity bits
        extended_matrix = np.zeros((rows + 1, cols + 1), dtype=int)
        extended_matrix[:rows, :cols] = matrix
        extended_matrix[:rows, cols] = row_parities
        extended_matrix[rows, :cols] = col_parities
        
        # Calculate corner parity bit
        extended_matrix[rows, cols] = 1 if sum(row_parities) % 2 == 1 else 0
        
        return extended_matrix
    
    @staticmethod
    def check_2d_parity(matrix: np.ndarray) -> Tuple[bool, List[Tuple[int, int]]]:
        """
        Check 2D parity and detect error locations.
        
        Args:
            matrix (np.ndarray): 2D parity matrix
            
        Returns:
            Tuple[bool, List[Tuple[int, int]]]: (is_valid, error_locations)
        """
        rows, cols = matrix.shape
        error_locations = []
        
        # Check row parities
        row_errors = []
        for i in range(rows - 1):
            row_sum = matrix[i, :-1].sum()
            expected_parity = 1 if row_sum % 2 == 1 else 0
            actual_parity = matrix[i, -1]
            if expected_parity != actual_parity:
                row_errors.append(i)
        
        # Check column parities
        col_errors = []
        for j in range(cols - 1):
            col_sum = matrix[:-1, j].sum()
            expected_parity = 1 if col_sum % 2 == 1 else 0
            actual_parity = matrix[-1, j]
            if expected_parity != actual_parity:
                col_errors.append(j)
        
        # Find error locations (intersection of row and column errors)
        for row in row_errors:
            for col in col_errors:
                error_locations.append((row, col))
        
        is_valid = len(error_locations) == 0
        return is_valid, error_locations
    
    @staticmethod
    def correct_errors(matrix: np.ndarray, error_locations: List[Tuple[int, int]]) -> np.ndarray:
        """
        Correct detected errors by flipping bits at error locations.
        
        Args:
            matrix (np.ndarray): 2D parity matrix with errors
            error_locations (List[Tuple[int, int]]): List of (row, col) error positions
            
        Returns:
            np.ndarray: Corrected matrix
        """
        corrected_matrix = matrix.copy()
        
        for row, col in error_locations:
            # Flip the bit at error location
            corrected_matrix[row, col] = 1 - corrected_matrix[row, col]
        
        return corrected_matrix


def demonstrate_simple_parity():
    """Demonstrate simple parity check functionality."""
    print("=" * 50)
    print("SIMPLE PARITY CHECK DEMONSTRATION")
    print("=" * 50)
    
    # Test data
    test_data = "1011010"
    print(f"Original data: {test_data}")
    
    # Add even parity
    data_with_parity = SimpleParityCheck.add_parity_bit(test_data, 'even')
    print(f"Data with even parity: {data_with_parity}")
    
    # Check parity
    is_valid, original = SimpleParityCheck.check_parity(data_with_parity, 'even')
    print(f"Parity check result: {'Valid' if is_valid else 'Invalid'}")
    print(f"Original data recovered: {original}")
    
    # Simulate error
    print("\n--- Simulating Error ---")
    error_data = data_with_parity[:-1] + ('1' if data_with_parity[-1] == '0' else '0')
    print(f"Data with error: {error_data}")
    
    is_valid_error, _ = SimpleParityCheck.check_parity(error_data, 'even')
    print(f"Parity check result: {'Valid' if is_valid_error else 'Invalid (Error Detected!)'}")


def demonstrate_2d_parity():
    """Demonstrate 2D parity check functionality."""
    print("\n" + "=" * 50)
    print("2D PARITY CHECK DEMONSTRATION")
    print("=" * 50)
    
    # Test data
    test_data = "101101010"
    rows, cols = 3, 3
    print(f"Original data: {test_data}")
    print(f"Matrix dimensions: {rows}x{cols}")
    
    # Create 2D parity matrix
    parity_matrix = TwoDimensionalParityCheck.create_2d_parity_matrix(test_data, rows, cols)
    print(f"\n2D Parity Matrix:")
    print(parity_matrix)
    
    # Check parity
    is_valid, errors = TwoDimensionalParityCheck.check_2d_parity(parity_matrix)
    print(f"\nParity check result: {'Valid' if is_valid else 'Invalid'}")
    if errors:
        print(f"Error locations: {errors}")
    
    # Simulate error
    print("\n--- Simulating Error ---")
    error_matrix = parity_matrix.copy()
    error_matrix[1, 1] = 1 - error_matrix[1, 1]  # Flip bit at position (1,1)
    print(f"Matrix with error:")
    print(error_matrix)
    
    is_valid_error, error_locations = TwoDimensionalParityCheck.check_2d_parity(error_matrix)
    print(f"Parity check result: {'Valid' if is_valid_error else 'Invalid (Error Detected!)'}")
    if error_locations:
        print(f"Error locations: {error_locations}")
        
        # Correct the error
        corrected_matrix = TwoDimensionalParityCheck.correct_errors(error_matrix, error_locations)
        print(f"\nCorrected matrix:")
        print(corrected_matrix)
        
        # Verify correction
        is_corrected, _ = TwoDimensionalParityCheck.check_2d_parity(corrected_matrix)
        print(f"After correction: {'Valid' if is_corrected else 'Still has errors'}")


def main():
    """Main function to demonstrate both error detection methods."""
    print("ERROR DETECTION METHODS IMPLEMENTATION")
    print("=====================================")
    
    # Demonstrate simple parity check
    demonstrate_simple_parity()
    
    # Demonstrate 2D parity check
    demonstrate_2d_parity()
    
    print("\n" + "=" * 50)
    print("INTERACTIVE TESTING")
    print("=" * 50)
    
    # Interactive testing
    while True:
        print("\nChoose an option:")
        print("1. Test Simple Parity Check")
        print("2. Test 2D Parity Check")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == '1':
            data = input("Enter binary data: ").strip()
            parity_type = input("Enter parity type (even/odd): ").strip().lower()
            
            try:
                with_parity = SimpleParityCheck.add_parity_bit(data, parity_type)
                print(f"Data with {parity_type} parity: {with_parity}")
                
                is_valid, original = SimpleParityCheck.check_parity(with_parity, parity_type)
                print(f"Parity check: {'Valid' if is_valid else 'Invalid'}")
                print(f"Original data: {original}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '2':
            data = input("Enter binary data: ").strip()
            rows = int(input("Enter number of rows: "))
            cols = int(input("Enter number of columns: "))
            
            try:
                matrix = TwoDimensionalParityCheck.create_2d_parity_matrix(data, rows, cols)
                print(f"2D Parity Matrix:\n{matrix}")
                
                is_valid, errors = TwoDimensionalParityCheck.check_2d_parity(matrix)
                print(f"Parity check: {'Valid' if is_valid else 'Invalid'}")
                if errors:
                    print(f"Error locations: {errors}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
