def bitwise_xnor(bin1, bin2):
    # Convert binary strings to integers
    num1 = int(bin1, 2)
    num2 = int(bin2, 2)
    
    # Perform bitwise XNOR using ~(num1 ^ num2) and mask with appropriate bit length
    max_length = max(len(bin1), len(bin2))
    xnor_result = ~(num1 ^ num2) & ((1 << max_length) - 1)  # Mask to ensure correct bit length
    
    # Convert result back to binary format, ensuring leading zeros
    xnor_bin = format(xnor_result, f'0{max_length}b')
    
    # Count the number of ones in the XNOR result
    ones_count = xnor_bin.count('1')
    
    # Print results
    print(f"Binary 1:    {bin1}")
    print(f"Binary 2:    {bin2}")
    print(f"XNOR Result: {xnor_bin}")
    print(f"Number of 1s: {ones_count}")
    
# Example usage
bin1 = "00110001100011001010101111100111010100010101100110010010000111010110101111011000001010100001010101100010001000101000110101011110"
bin2 = "11000110000001010010011010011000010101001110110100000101101000100101010000000110011001100100011000111110010100001001000010001101"

bitwise_xnor(bin1, bin2)

