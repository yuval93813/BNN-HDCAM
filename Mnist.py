from hdcamV2 import Controller as HDCAM
import random
from typing import List
from run_PS_hdcam import run_class


zero_word = [0x0000000000000000]
one_word = [0x00000000ffffffff]

voltages = [
    {"Hamming Distance": 0, "Vref": 1200, "Veval": 1200, "Vrep": 1200},
    {"Hamming Distance": 1, "Vref": 1100, "Veval": 1200, "Vrep": 1200},
    {"Hamming Distance": 2, "Vref": 950, "Veval": 1200, "Vrep": 1200},
    {"Hamming Distance": 3, "Vref": 800, "Veval": 1200, "Vrep": 1200},
    {"Hamming Distance": 4, "Vref": 750, "Veval": 950, "Vrep": 1200},
    {"Hamming Distance": 5, "Vref": 750, "Veval": 700, "Vrep": 1200},
    {"Hamming Distance": 6, "Vref": 800, "Veval": 600, "Vrep": 1200},
    {"Hamming Distance": 7, "Vref": 750, "Veval": 650, "Vrep": 700}
]

activation = [[0,0x0f0f00f00f00f0f0]]


weights = [
    [0, 0x0f0f00f00f00f0f0, 0x0f0f00f00f00f0f1],
    [1, 0x0f0f00f00f00f0f2, 0x0f0f00f00f00f0f3],
    [2, 0x0f0f00f00f00f0f4, 0x0f0f00f00f00f0f5],
]
hdcam = HDCAM()
a=run_class(0)
print(a)
a.init_PS()

# Initialize a dictionary to count `andOfRes = 1` for each label
andOfRes_counts = {}

for sub_array in weights:
    label = sub_array[0]  # First value is the label
    print(f"Label: {label}")
    
    # Initialize the count for the label if not already in the dictionary
    if label not in andOfRes_counts:
        andOfRes_counts[label] = 0

    activationArr = activation * 4 + one_word * 476
    for row in voltages:
        hamming_distance = row["Hamming Distance"]
        vref = row["Vref"]
        veval = row["Veval"]
        vrep = row["Vrep"]
        a.set_vref(vref)
        a.set_veval(veval)
        a.set_vrep(vrep)

        # Process the first part of hdcam
        hdcam_array = [sub_array[1]] + zero_word * 479
        hdcam.write(hdcam_array)
        firstRes = hdcam.read(activationArr)

        # Process the second part of hdcam
        hdcam_array = [sub_array[2]] + zero_word * 479
        hdcam.write(hdcam_array)
        secRes = hdcam.read(activationArr)

        # Compute AND result
        andOfRes = 1 if (firstRes == 4 and secRes == 4) else 0
        
        # Increment count for the label if `andOfRes == 1`
        if andOfRes == 1:
            andOfRes_counts[label] += 1

        print(f"Hamming Distance: {hamming_distance}, Vref: {vref}, Veval: {veval}, Vrep: {vrep}, AND results: {andOfRes}")

# Print the results
print("\nAND results counts per label:")
for label, count in andOfRes_counts.items():
    print(f"Label {label}: {count}")

        
           

a.close_PS()