# Practical 7: Hamming Code Error Correction Implementation

**Computer Networks - Semester 5**

This practical implements Hamming Code error correction methods with support for various Hamming Code variants commonly used in computer networks and data storage systems.

## Features

### Hamming Code Implementation
- **Multiple Variants**: Support for Hamming(7,4), Hamming(15,11), Hamming(31,26), and custom variants
- **Encoding**: Convert data bits to Hamming Code with parity bits
- **Decoding**: Extract original data from Hamming Code
- **Error Detection**: Detect single-bit and multiple-bit errors
- **Error Correction**: Automatically correct single-bit errors
- **Efficiency Analysis**: Calculate and compare efficiency of different variants

### Error Simulation
- **Single Bit Errors**: Simulate single bit flips at specific positions
- **Multiple Bit Errors**: Simulate multiple random bit errors
- **Position Control**: Precise control over error locations
- **Error Analysis**: Analyze error detection and correction capabilities

## Installation

### Option 1: Using the setup script (Recommended)
```bash
cd Practical7-HammingCode
./setup.sh
```

### Option 2: Manual setup
1. Navigate to the practical directory:
```bash
cd Practical7-HammingCode
```

2. Activate the global virtual environment:
```bash
source ../venv/bin/activate
```

3. Install the required dependencies:
```bash
pip install -r ../requirements.txt
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
python hamming_code.py
```

This will run the demonstration and provide an interactive menu for testing Hamming Code methods.

### Running Tests
```bash
python test_hamming_code.py
```

This will run unit tests and show a quick demonstration.

### Using the Classes Directly

#### Basic Hamming Code Encoding/Decoding
```python
from hamming_code import HammingCode

# Create Hamming Code for 4 data bits (Hamming(7,4))
hamming = HammingCode(4)

# Encode data
data = "1011"
encoded = hamming.encode(data)
print(f"Encoded: {encoded}")

# Decode data
decoded, has_error, error_pos = hamming.decode(encoded)
print(f"Decoded: {decoded}")
print(f"Error detected: {has_error}")
```

#### Error Correction
```python
from hamming_code import HammingCode, HammingCodeErrorSimulator

# Create Hamming Code
hamming = HammingCode(4)
data = "1011"
encoded = hamming.encode(data)

# Introduce error
error_data = HammingCodeErrorSimulator.introduce_single_bit_error(encoded, 3)

# Correct error
corrected, has_error, error_pos = hamming.decode(error_data)
print(f"Error at position: {error_pos}")
print(f"Corrected data: {corrected}")
```

#### Different Hamming Code Variants
```python
from hamming_code import HammingCode, HammingCodeVariants

# Test different variants
variants = [4, 8, 11, 16, 26]
HammingCodeVariants.compare_variants(variants)

# Calculate efficiency
efficiency = HammingCodeVariants.calculate_efficiency(4)
print(f"Hamming(7,4) efficiency: {efficiency:.3f}")
```

## Hamming Code Variants

| Variant | Data Bits | Parity Bits | Total Bits | Efficiency | Description |
|---------|-----------|-------------|------------|------------|-------------|
| Hamming(7,4) | 4 | 3 | 7 | 0.571 | Most common variant |
| Hamming(15,11) | 11 | 4 | 15 | 0.733 | Extended variant |
| Hamming(31,26) | 26 | 5 | 31 | 0.839 | Large variant |
| Hamming(63,57) | 57 | 6 | 63 | 0.905 | Very large variant |

## How Hamming Code Works

### 1. Parity Bit Placement
Parity bits are placed at positions that are powers of 2 (1, 2, 4, 8, 16, ...).

### 2. Parity Bit Calculation
Each parity bit covers specific data bits:
- Parity bit 1 (position 1): Covers positions with bit 1 set (3, 5, 7, 9, ...)
- Parity bit 2 (position 2): Covers positions with bit 2 set (3, 6, 7, 10, ...)
- Parity bit 4 (position 4): Covers positions with bit 4 set (5, 6, 7, 12, ...)

### 3. Error Detection and Correction
1. **Syndrome Calculation**: Calculate syndrome by checking parity bits
2. **Error Position**: Syndrome value indicates the position of the error
3. **Error Correction**: Flip the bit at the error position

### 4. Mathematical Foundation
- For m data bits, we need r parity bits where: 2^r ≥ m + r + 1
- Hamming distance = 3 (can detect 2 errors, correct 1 error)

## Example Output

```
HAMMING CODE ERROR CORRECTION DEMONSTRATION
============================================================
Using Hamming(7,4) Code:
------------------------------
Data bits: 4
Parity bits: 3
Total bits: 7
Parity positions: [1, 2, 4]
Efficiency: 0.571

Original data: 1011
Encoded data: 0110011

Parity bit analysis:
  Parity bit 1 at position 1: 0
  Parity bit 2 at position 2: 1
  Parity bit 4 at position 4: 1

Verification (no errors): Valid
Decoded data: 1011
Error detected: No
Original data matches: Yes

HAMMING CODE ERROR CORRECTION DEMONSTRATION
============================================================
Original data: 1011
Encoded data: 0110011

Single Bit Error Correction:
----------------------------------------
Error at position 1: 1110011
  Detected at position: 1
  Corrected data: 1011
  Correction successful: Yes

Error at position 2: 0010011
  Detected at position: 2
  Corrected data: 1011
  Correction successful: Yes

Error at position 3: 0100011
  Detected at position: 3
  Corrected data: 1011
  Correction successful: Yes
```

## Error Correction Capabilities

| Error Type | Detection | Correction | Notes |
|------------|-----------|------------|-------|
| Single bit errors | 100% | 100% | Always detected and corrected |
| Double bit errors | 100% | 0% | Detected but not corrected |
| Multiple bit errors | Variable | 0% | May or may not be detected |

## Applications

- **Memory Systems**: ECC (Error-Correcting Code) memory
- **Storage Devices**: Hard drives, SSDs, RAID systems
- **Communication**: Satellite communication, wireless networks
- **Computer Architecture**: CPU caches, register files
- **Data Transmission**: Reliable data transfer protocols

## Advantages of Hamming Code

1. **Single Error Correction**: Can correct any single-bit error
2. **Double Error Detection**: Can detect any double-bit error
3. **Efficient**: Minimal overhead compared to other error correction codes
4. **Systematic**: Easy to implement in hardware and software
5. **Standardized**: Well-established mathematical foundation

## Limitations

1. **Single Error Only**: Cannot correct multiple errors
2. **Overhead**: Requires additional parity bits
3. **Complexity**: More complex than simple parity checks
4. **Burst Errors**: Limited effectiveness against burst errors

## Mathematical Properties

### Hamming Distance
- **Definition**: Minimum number of bit positions in which two codewords differ
- **Hamming Code Distance**: 3
- **Error Detection**: Can detect up to d-1 errors (2 errors)
- **Error Correction**: Can correct up to ⌊(d-1)/2⌋ errors (1 error)

### Efficiency Formula
```
Efficiency = Data Bits / Total Bits = m / (m + r)
```
Where:
- m = number of data bits
- r = number of parity bits

## Files

- `hamming_code.py` - Main Hamming Code implementation with all methods
- `test_hamming_code.py` - Unit tests and demonstrations
- Global `requirements.txt` - Python dependencies for all practicals
- `setup.sh` - Automated setup script
- `README.md` - This documentation file

## Testing

The implementation includes comprehensive unit tests covering:
- Hamming Code encoding and decoding
- Error detection and correction
- Different Hamming Code variants
- Error simulation methods
- Edge cases and error handling
- Integration tests

Run tests with:
```bash
python test_hamming_code.py
```

## Interactive Features

The main program provides an interactive menu for:
1. Testing Hamming Code encoding/decoding with custom data
2. Testing error correction with simulated errors
3. Testing multiple error scenarios
4. Comparing different Hamming Code variants
5. Comprehensive demonstrations

## Comparison with Other Error Correction Methods

| Method | Error Detection | Error Correction | Overhead | Complexity |
|--------|----------------|------------------|----------|------------|
| Simple Parity | Single bit | None | 1 bit | Low |
| 2D Parity | Single bit | Single bit | 2n+1 bits | Medium |
| CRC | Multiple bits | None | 8-32 bits | Medium |
| Hamming Code | 2 bits | 1 bit | 3-6 bits | High |

## Performance Analysis

### Efficiency Comparison
- **Hamming(7,4)**: 57.1% efficiency
- **Hamming(15,11)**: 73.3% efficiency
- **Hamming(31,26)**: 83.9% efficiency
- **Hamming(63,57)**: 90.5% efficiency

### Trade-offs
- **Higher efficiency**: More data bits per codeword
- **Lower efficiency**: Better error correction capability
- **Optimal choice**: Depends on application requirements
