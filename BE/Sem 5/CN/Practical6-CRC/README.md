# Practical 6: CRC (Cyclic Redundancy Check) Error Detection Implementation

**Computer Networks - Semester 5**

This practical implements CRC (Cyclic Redundancy Check) error detection methods with support for various CRC polynomials commonly used in computer networks and data communication.

## Features

### CRC Implementation
- **Multiple CRC Polynomials**: Support for CRC-8, CRC-16, CRC-32, CRC-CCITT, CRC-ANSI, and CRC-DNP
- **Bitwise and Table-based Calculation**: Two different CRC calculation methods for comparison
- **Byte-level CRC**: Support for calculating CRC on byte data (ASCII strings)
- **Custom Polynomials**: Ability to use custom CRC polynomials
- **Error Detection**: Comprehensive error detection and verification

### Error Simulation
- **Single Bit Errors**: Simulate single bit flips
- **Burst Errors**: Simulate consecutive bit errors
- **Random Errors**: Simulate multiple random bit errors
- **Error Position Control**: Precise control over error locations

## Installation

### Option 1: Using the setup script (Recommended)
```bash
cd Practical6-CRC
./setup.sh
```

### Option 2: Manual setup
1. Navigate to the practical directory:
```bash
cd Practical6-CRC
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
python crc_detection.py
```

This will run the demonstration and provide an interactive menu for testing CRC methods.

### Running Tests
```bash
python test_crc_detection.py
```

This will run unit tests and show a quick demonstration.

### Using the Classes Directly

#### Basic CRC Calculation
```python
from crc_detection import CRCDetection

# Create CRC detector for CRC-16
crc_detector = CRCDetection('CRC-16')

# Calculate CRC for binary data
data = "1101011011001101"
crc = crc_detector.calculate_crc_table(data)
print(f"CRC: {crc}")

# Add CRC to data
data_with_crc = crc_detector.add_crc(data)
print(f"Data with CRC: {data_with_crc}")

# Verify CRC
is_valid, original = crc_detector.verify_crc(data_with_crc)
print(f"Valid: {is_valid}, Original: {original}")
```

#### Error Detection
```python
from crc_detection import CRCDetection, CRCErrorSimulator

# Create CRC detector
crc_detector = CRCDetection('CRC-16')
data = "1101011011001101"
data_with_crc = crc_detector.add_crc(data)

# Introduce error
error_data = CRCErrorSimulator.introduce_single_bit_error(data_with_crc, 5)

# Detect error
has_errors, original, expected_crc = crc_detector.detect_errors(error_data)
print(f"Error detected: {has_errors}")
```

#### Byte-level CRC
```python
from crc_detection import CRCDetection

# Create CRC detector
crc_detector = CRCDetection('CRC-16')

# Calculate CRC for ASCII string
text = "Hello, World!"
text_bytes = text.encode('ascii')
crc_bytes = crc_detector.calculate_crc_bytes(text_bytes)
print(f"CRC checksum: {crc_bytes.hex()}")
```

## Supported CRC Polynomials

| CRC Type | Polynomial | Width | Common Usage |
|----------|------------|-------|--------------|
| CRC-8 | 0x07 | 8 bits | Simple applications |
| CRC-16 | 0x8005 | 16 bits | General purpose |
| CRC-32 | 0x04C11DB7 | 32 bits | Ethernet, ZIP, PNG |
| CRC-CCITT | 0x1021 | 16 bits | X.25, HDLC |
| CRC-ANSI | 0x8005 | 16 bits | Modbus |
| CRC-DNP | 0x3D65 | 16 bits | DNP3 protocol |

## How CRC Works

### 1. Polynomial Representation
CRC uses polynomial arithmetic over GF(2) (Galois Field of 2 elements). The polynomial represents the divisor used in the CRC calculation.

### 2. Calculation Process
1. **Initialize**: Start with a CRC register (usually all zeros)
2. **Process Data**: For each bit/byte in the data:
   - Shift the CRC register
   - XOR with the polynomial if MSB is set
3. **Finalize**: The remaining value in the register is the CRC

### 3. Error Detection
- **Transmission**: Data + CRC is sent
- **Reception**: Receiver calculates CRC on received data
- **Verification**: If calculated CRC matches received CRC, no errors detected

## Example Output

```
CRC (CYCLIC REDUNDANCY CHECK) DEMONSTRATION
============================================================
Original data: 1101011011001101
Data length: 16 bits

--- CRC-8 ---
Polynomial: 0x0007
Width: 8 bits
CRC (bitwise): 10110110
CRC (table):   10110110
Methods match: True
Data with CRC: 110101101100110110110110
CRC verification: Valid
Original data: 1101011011001101

--- CRC-16 ---
Polynomial: 0x8005
Width: 16 bits
CRC (bitwise): 1011011011001101
CRC (table):   1011011011001101
Methods match: True
Data with CRC: 11010110110011011011011011001101
CRC verification: Valid
Original data: 1101011011001101

CRC ERROR DETECTION DEMONSTRATION
============================================================
Original data: 1011010110101101
Data with CRC-16: 10110101101011011011011011001101

--- Single Bit Error ---
Data with error: 10111101101011011011011011001101
Error detected: Yes
Expected CRC: 1011011011001101
Received CRC: 1011011011001101

--- Burst Error (3 bits) ---
Data with burst error: 10110101101100011011011011001101
Error detected: Yes

--- Multiple Random Errors (2 bits) ---
Data with random errors: 10110101101011011011011011001101
Error detected: Yes
```

## Error Detection Capabilities

| Error Type | Detection Rate | Notes |
|------------|----------------|-------|
| Single bit errors | 100% | Always detected |
| Double bit errors | 100% | Always detected |
| Odd number of errors | 100% | Always detected |
| Burst errors ≤ CRC width | 100% | Always detected |
| Burst errors > CRC width | High probability | Depends on polynomial |

## Applications

- **Network Protocols**: Ethernet, Wi-Fi, Bluetooth
- **Storage Systems**: Hard drives, SSDs, RAID
- **File Formats**: ZIP, PNG, MPEG
- **Communication Protocols**: Modbus, DNP3, X.25
- **Data Transmission**: Serial communication, USB

## Advantages of CRC

1. **High Error Detection Rate**: Detects most common transmission errors
2. **Efficient Implementation**: Fast calculation using lookup tables
3. **Flexible**: Different polynomials for different applications
4. **Standardized**: Well-established standards for various protocols
5. **Hardware Support**: Many processors have CRC instructions

## Limitations

1. **Not Cryptographically Secure**: CRC is not suitable for security applications
2. **Polynomial Dependent**: Effectiveness depends on chosen polynomial
3. **Cannot Correct Errors**: Only detects errors, cannot correct them
4. **Burst Error Limits**: Very long burst errors may not be detected

## Files

- `crc_detection.py` - Main CRC implementation with all methods
- `test_crc_detection.py` - Unit tests and demonstrations
- Global `requirements.txt` - Python dependencies for all practicals
- `setup.sh` - Automated setup script
- `README.md` - This documentation file

## Testing

The implementation includes comprehensive unit tests covering:
- CRC calculation for different polynomials
- Error detection and verification
- Byte-level CRC calculation
- Error simulation methods
- Edge cases and error handling

Run tests with:
```bash
python test_crc_detection.py
```

## Interactive Features

The main program provides an interactive menu for:
1. Testing CRC calculation with custom data
2. Testing error detection with simulated errors
3. Testing byte-level CRC with text strings
4. Comparing different CRC polynomials
5. Comprehensive demonstrations
