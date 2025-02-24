from hdcamV2 import Controller as HDCAM
import random
from typing import List
from run_PS_hdcam import run_class

def flip_bits_in_array(word_array,num_of_bits):
 
    flipped_array = []
    
    for i, word in enumerate(word_array):
        # Generate X unique random bit positions to flip
        bit_positions = random.sample(range(64), num_of_bits)
        
        # Create a mask with the selected bits set to 1
        mask = sum(1 << pos for pos in bit_positions)
        
        # Flip the bits in the word using XOR
        flipped_word = word ^ mask
        
        # Append the flipped word to the result array
        flipped_array.append(flipped_word)
        
        # # Print results
        # print(f"Word {i + 1}:")
        # print(f"  Original: {word:#018x}")
        # print(f"  Mask:     {mask:#018x}")
        # print(f"  Flipped:  {flipped_word:#018x}")
        # print(f"  Flipped Bits: {bit_positions}")
        # print("-" * 30)
    
    return flipped_array

zero_word = [0x0000000000000000]
one_word = [0x00000fffffffffff]

hdcam = HDCAM()
qurry = [0x0fffffffffffffff] 
hdcam_array = qurry + zero_word * 479
print(hdcam_array)
hdcam.write(hdcam_array)
#hamming_dist = 1
#print(f"{hamming_dist} errors")
a=run_class(0)
print(a)
a.init_PS()


hd_results = {}

log_file = open("log.txt", "a", buffering=1)  # Line-buffering enabled

def log_and_print(message):
    """Prints the message to the screen and writes it to a log file instantly."""
    print(message)
    log_file.write(message + "\n")
    log_file.flush()  # Ensure immediate writing to disk

for hamming_dist in range(33, 41):  # Adjust the range as needed
    found = False  # Flag to check if a new combination is found
    flipped_array = flip_bits_in_array(qurry, hamming_dist)
    qurryArr = flipped_array* 4 + one_word * 16
    
    for Vrep in range(1025, 0, -50):
        a.set_vrep(Vrep)
        for Veval in range(500, 501, 25):
            a.set_veval(Veval)
            for Vref in range(900, 24, -25):
                a.set_vref(Vref)

                # Check hits (assuming `hdcam.read` compares flipped array and calculates hits)
                hits = hdcam.read(qurryArr)

                # Check if hits match the tolerance (e.g., hits == hamming_dist)
                if hits == 4:
                    hd_results[hamming_dist] = (Vref, Veval, Vrep)
                    log_and_print(f"HD {hamming_dist}: Found new combo - Vref: {Vref}, Veval: {Veval}, Vrep: {Vrep}")
                    found = True
                    break  # Stop searching for this Hamming distance
            if found:
                break
        if found:
            break

    # If no new combination is found, attempt to reuse the previous one
    if not found:
        log_and_print(f"HD {hamming_dist}: No valid combination exists, and no previous combo to reuse.")

# Close the power supply
a.close_PS()

# Save or print the final results
log_and_print("\nFinal Results:")
for hd, combo in hd_results.items():
    log_and_print(f"Hamming Distance {hd}: Vref: {combo[0]}, Veval: {combo[1]}, Vrep: {combo[2]}")

# Close the log file
log_file.close()