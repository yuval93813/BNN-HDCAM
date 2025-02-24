from hdcamV2 import XBOX  # Import the XBOX class directly
import random

# Constants
XBOX_CAPACITY = 480  # Max words that fit in XBOX SRAM

def get_random_data(size):
    """Generate a list of random 64-bit integers."""
    return [random.randint(0, (1 << 64) - 1) for _ in range(size)]

def compare_data(data1, data2):
    """Compare two lists of integers for equality."""
    return data1 == data2

def test_sram():
    """Test writing to and reading from the XBOX SRAM."""
    # Initialize XBOX instance
    xbox = XBOX(null_value=0x0)  # XBOX SRAM interface

    print("Generating random data to write to SRAM...")
    write_data = get_random_data(XBOX_CAPACITY)

    print("Clearing SRAM...")
    xbox.clear()  # Optional: Clear SRAM to avoid stale data interference

    print("Writing data to SRAM...")
    xbox.write(write_data)  # Write the data to SRAM

    print("Reading data back from SRAM...")
    read_data = [0] * XBOX_CAPACITY  # Placeholder to store read data

    # Read back the data directly from SRAM
    xbox_mem_ptr = xbox.xbox_mem_base_addr  # Start address for reading

    for i in range(XBOX_CAPACITY):
        # Read LSB and MSB parts of each 64-bit word from SRAM
        lsb = xbox.serial_gateway.rd_mem_by_uart(xbox_mem_ptr)
        msb = xbox.serial_gateway.rd_mem_by_uart(xbox_mem_ptr + 4)
        read_data[i] = (msb << 32) | lsb  # Reconstruct the 64-bit word
        xbox_mem_ptr += 8  # Move to the next word address

    print("Comparing written and read data...")
    if compare_data(write_data, read_data):
        print("SRAM write/read test successful!")
    else:
        print("SRAM write/read test failed. Data mismatch detected.")

if __name__ == "__main__":
    test_sram()
