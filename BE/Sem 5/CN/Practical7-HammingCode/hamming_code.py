def calculate_parity_bits(data_bits):
    n = len(data_bits)
    m = 0

    # Calculate number of redundant bits needed (2^m >= m + n + 1)
    while (2 ** m) < (m + n + 1):
        m += 1

    total_length = n + m
    hamming_code = ['0'] * (total_length + 1)  # 1-indexed array

    # Place data bits into the correct positions (skip powers of 2)
    j = 0
    for i in range(1, total_length + 1):
        if (i & (i - 1)) != 0:  # Not a power of two
            hamming_code[i] = data_bits[j]
            j += 1

    # Calculate parity bits
    for i in range(m):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, total_length + 1):
            if j & parity_pos:
                parity ^= int(hamming_code[j])
        hamming_code[parity_pos] = str(parity)

    return ''.join(hamming_code[1:])  # Convert back to string and remove 0th index


def detect_and_correct(hamming_code):
    n = len(hamming_code)
    hamming_code = ['0'] + list(hamming_code)  # Make it 1-indexed
    m = 0

    # Calculate how many parity bits
    while (2 ** m) <= n:
        m += 1

    error_pos = 0

    # Check parity bits
    for i in range(m):
        parity_pos = 2 ** i
        parity = 0
        for j in range(1, n + 1):
            if j & parity_pos:
                parity ^= int(hamming_code[j])
        if parity != 0:
            error_pos += parity_pos

    if error_pos != 0:
        print(f"Error detected at position: {error_pos}")
        # Correct the bit
        hamming_code[error_pos] = '1' if hamming_code[error_pos] == '0' else '0'
    else:
        print("No error detected.")

    corrected_code = ''.join(hamming_code[1:])
    return corrected_code, error_pos


def extract_data(corrected_code):
    data_bits = ''
    for i in range(1, len(corrected_code)+1):
        if (i & (i - 1)) != 0:  # Not a power of 2
            data_bits += corrected_code[i-1]
    return data_bits


# === Example Usage ===
def main():
    data = "1011"  # 4-bit data for (7,4) Hamming Code
    encoded = calculate_parity_bits(data)
    print(f"Original Data: {data}")
    print(f"Encoded Hamming Code: {encoded}")

    # Simulate error at position 3 (1-indexed)
    error_code = list(encoded)
    error_code[2] = '1' if error_code[2] == '0' else '0'  # Flip bit
    error_code = ''.join(error_code)
    print(f"Received Code with Error: {error_code}")

    corrected_code, error_pos = detect_and_correct(error_code)
    print(f"Corrected Hamming Code: {corrected_code}")
    print(f"Extracted Data: {extract_data(corrected_code)}")

main()