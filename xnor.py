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
bin1 = "10110001000110110000001000101111"
bin2 = "1010001010110011001001000011101"

bitwise_xnor(bin1, bin2)


