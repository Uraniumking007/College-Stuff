def bit_stuffing(data):
    stuffed_data = ''
    count = 0

    for bit in data:
        stuffed_data += bit
        if bit == '1':
            count += 1
            if count == 5:
                stuffed_data += '0'  # Stuff a '0' after five consecutive '1's
                count = 0
        else:
            count = 0

    return stuffed_data


def bit_de_stuffing(stuffed_data):
    de_stuffed = ''
    count = 0
    i = 0

    while i < len(stuffed_data):
        bit = stuffed_data[i]
        de_stuffed += bit

        if bit == '1':
            count += 1
            if count == 5:
                # Skip the stuffed '0'
                i += 1
                count = 0
        else:
            count = 0

        i += 1

    return de_stuffed


# === Example Usage ===
original_data = "01111110111111011111"
stuffed = bit_stuffing(original_data)
de_stuffed = bit_de_stuffing(stuffed)

print(f"Original Data:      {original_data}")
print(f"Bit Stuffed Data:   {stuffed}")
print(f"De-Stuffed Data:    {de_stuffed}")
