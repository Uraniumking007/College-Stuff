# Practical 5: Error Detection Methods Implementation

**Computer Networks - Semester 5**

This practical implements two common error detection methods used in computer networks and data communication:

1. **Simple Parity Check**
2. **2D Parity Check**

## Features

### Simple Parity Check
- Supports both even and odd parity
- Detects odd number of bit errors
- Simple and efficient for basic error detection
- Cannot correct errors, only detects them

### 2D Parity Check
- Arranges data in a matrix format
- Adds parity bits for each row and column
- Can detect and locate single-bit errors
- Can correct single-bit errors
- More robust than simple parity check

## Installation

### Option 1: Using the setup script (Recommended)
```bash
cd Practical5-ErrorDetection
./setup.sh
```

### Option 2: Manual setup
1. Navigate to the practical directory:
```bash
cd Practical5-ErrorDetection
```

2. Activate the global virtual environment:
```bash
source ../venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Activating the Virtual Environment
After setup, always activate the global virtual environment before running the code:
```bash
source ../venv/bin/activate
```

To deactivate when done:
```bash
deactivate
```

## Usage

**Note**: Always activate the global virtual environment first:
```bash
source ../venv/bin/activate
```

### Running the Main Program
```bash
python error_detection.py
```

This will run the demonstration and provide an interactive menu for testing both methods.

### Running Tests
```bash
python test_error_detection.py
```

This will run unit tests and show a quick demonstration.

### Using the Classes Directly

#### Simple Parity Check
```python
from error_detection import SimpleParityCheck

# Add even parity bit
data = "1011010"
data_with_parity = SimpleParityCheck.add_parity_bit(data, 'even')
print(f"Data with parity: {data_with_parity}")

# Check parity
is_valid, original = SimpleParityCheck.check_parity(data_with_parity, 'even')
print(f"Valid: {is_valid}, Original: {original}")
```

#### 2D Parity Check
```python
from error_detection import TwoDimensionalParityCheck

# Create 2D parity matrix
data = "101101010"
matrix = TwoDimensionalParityCheck.create_2d_parity_matrix(data, 3, 3)
print(f"2D Parity Matrix:\n{matrix}")

# Check for errors
is_valid, errors = TwoDimensionalParityCheck.check_2d_parity(matrix)
print(f"Valid: {is_valid}, Errors: {errors}")

# Correct errors if found
if errors:
    corrected_matrix = TwoDimensionalParityCheck.correct_errors(matrix, errors)
    print(f"Corrected Matrix:\n{corrected_matrix}")
```

## How It Works

### Simple Parity Check
1. Counts the number of 1s in the data
2. Adds a parity bit to make the total number of 1s even (even parity) or odd (odd parity)
3. During transmission, if the parity check fails, an error is detected

### 2D Parity Check
1. Arranges data in a matrix (e.g., 3x3)
2. Adds a parity bit for each row (making row sum even)
3. Adds a parity bit for each column (making column sum even)
4. Adds a corner parity bit for the parity bits themselves
5. Can detect and locate single-bit errors by finding the intersection of row and column parity failures
6. Can correct single-bit errors by flipping the bit at the error location

## Example Output

```
SIMPLE PARITY CHECK DEMONSTRATION
==================================================
Original data: 1011010
Data with even parity: 10110100
Parity check result: Valid
Original data recovered: 1011010

--- Simulating Error ---
Data with error: 10110101
Parity check result: Invalid (Error Detected!)

2D PARITY CHECK DEMONSTRATION
==================================================
Original data: 101101010
Matrix dimensions: 3x3

2D Parity Matrix:
[[1 0 1 0]
 [1 0 1 0]
 [0 1 0 1]
 [0 1 0 1]]

Parity check result: Valid

--- Simulating Error ---
Matrix with error:
[[1 0 1 0]
 [1 1 1 0]
 [0 1 0 1]
 [0 1 0 1]]
Parity check result: Invalid (Error Detected!)
Error locations: [(1, 1)]

Corrected matrix:
[[1 0 1 0]
 [1 0 1 0]
 [0 1 0 1]
 [0 1 0 1]]
After correction: Valid
```

## Files

- `error_detection.py` - Main implementation with both error detection methods
- `test_error_detection.py` - Unit tests and quick demonstration
- `requirements.txt` - Python dependencies
- `README.md` - This documentation file

## Error Detection Capabilities

| Method | Detects Single Errors | Detects Multiple Errors | Corrects Errors |
|--------|----------------------|------------------------|-----------------|
| Simple Parity | ✅ | ❌ (odd number only) | ❌ |
| 2D Parity | ✅ | ❌ (single bit only) | ✅ (single bit) |

## Applications

- **Simple Parity Check**: Used in simple communication protocols, memory systems
- **2D Parity Check**: Used in RAID systems, network protocols, storage systems

## Limitations

- Simple parity check cannot detect even number of errors
- 2D parity check can only correct single-bit errors
- Both methods add overhead (parity bits) to the original data
