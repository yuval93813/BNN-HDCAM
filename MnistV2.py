from hdcamV2 import Controller as HDCAM
import random
from typing import List
from run_PS_hdcam import run_class
import os

def process_weights_and_voltages(weights, voltages, activation, one_word, zero_word, hdcam, powerSupply, MnistLable):
    andOfRes_counts = {}

    for sub_array in weights:
        label = sub_array[0]  # First value is the label
        print(f"Label: {label}")

        # Initialize the count for the label if not already in the dictionary
        if label not in andOfRes_counts:
            andOfRes_counts[label] = 0
        print(activation[0][0])
        activationArr1 = [activation[0][0]] * 4 + [~activation[0][0]] * 16
        activationArr2 = [activation[0][1]] * 4 + [~activation[0][1]] * 16

        for row in voltages:
            hamming_distance = row["Hamming Distance"]
            vref = row["Vref"]
            veval = row["Veval"]
            vrep = row["Vrep"]

            # Set voltages
            powerSupply.set_vref(vref)
            powerSupply.set_veval(veval)
            powerSupply.set_vrep(vrep)

            # Process the first part of hdcam
            hdcam_array = [sub_array[1]]*480 #+ one_word * 4
            hdcam.write(hdcam_array)
            firstRes = hdcam.read(activationArr1)

            # Process the second part of hdcam
            hdcam_array = [sub_array[2]]*480 #+ one_word * 4
            hdcam.write(hdcam_array)
            secRes = hdcam.read(activationArr2)

            # Compute AND result
            andOfRes = 1 if (firstRes == 4 or secRes == 4) else 0

            # Increment count for the label if `andOfRes == 1`
            if andOfRes == 1:
                print("im here")
                andOfRes_counts[label] += 1

            print(f"Hamming Distance: {hamming_distance}, Vref: {vref}, Veval: {veval}, Vrep: {vrep}, AND results: {andOfRes}")

    file_path = "results.txt"

    # Open the file in append mode if it exists, otherwise create it
    file_mode = "a" if os.path.exists(file_path) else "w"

    with open(file_path, file_mode) as results_file:
        results_file.write("\nAND results counts per label:\n")

        for label, count in andOfRes_counts.items():
            result_line = f"Label {label}: {count}\n"
            print(result_line, end="")  # Print to console
            results_file.write(result_line)  # Write to file

        # Find the label with the highest count
        predicted_label = max(andOfRes_counts, key=andOfRes_counts.get)
        prediction_result = f"Predicted Label: {predicted_label}, MNIST Label: {MnistLable}\n"
        print(prediction_result, end="")
        results_file.write(prediction_result)

        # Compare labels
        if predicted_label == MnistLable:
            match_result = "The predicted label matches the MNIST label.\n"
        else:
            match_result = "The predicted label does not match the MNIST label.\n"

        print(match_result, end="")
        results_file.write(match_result)

    # Print the results
    # print("\nAND results counts per label:")
    # for label, count in andOfRes_counts.items():
    #     print(f"Label {label}: {count}")

    # # Find the label with the highest count
    # predicted_label = max(andOfRes_counts, key=andOfRes_counts.get)
    # print(f"Predicted Label: {predicted_label}, MNIST Label: {MnistLable}")

    # if predicted_label == MnistLable:
    #     print("The predicted label matches the MNIST label.")
    # else:
    #     print("The predicted label does not match the MNIST label.")

    # return andOfRes_counts


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
    {"Hamming Distance": 7, "Vref": 775, "Veval": 625, "Vrep": 1200},
    {"Hamming Distance": 8, "Vref": 775, "Veval": 600, "Vrep": 1200},
    {"Hamming Distance": 9, "Vref": 750, "Veval": 675, "Vrep": 1200},
    {"Hamming Distance": 10, "Vref": 775, "Veval": 550, "Vrep": 1200},
    {"Hamming Distance": 11, "Vref": 775, "Veval": 525, "Vrep": 1200},
    {"Hamming Distance": 12, "Vref": 1175, "Veval": 350, "Vrep": 1150},
    {"Hamming Distance": 13, "Vref": 1175, "Veval": 350, "Vrep": 1175},
    {"Hamming Distance": 14, "Vref": 1175, "Veval": 350, "Vrep": 1200},
    {"Hamming Distance": 15, "Vref": 1025, "Veval": 475, "Vrep": 1200},
    {"Hamming Distance": 16, "Vref": 950, "Veval": 525, "Vrep": 1100},
    {"Hamming Distance": 17, "Vref": 950, "Veval": 500, "Vrep": 1100},
    {"Hamming Distance": 18, "Vref": 1100, "Veval": 450, "Vrep": 1200},
    {"Hamming Distance": 19, "Vref": 1175, "Veval": 400, "Vrep": 1200},
    {"Hamming Distance": 20, "Vref": 1025, "Veval": 475, "Vrep": 1000},
    {"Hamming Distance": 21, "Vref": 1025, "Veval": 475, "Vrep": 1075},
    {"Hamming Distance": 22, "Vref": 1175, "Veval": 400, "Vrep": 1200},
    {"Hamming Distance": 23, "Vref": 850, "Veval": 525, "Vrep": 1050},
    {"Hamming Distance": 24, "Vref": 950, "Veval": 500, "Vrep": 1025},
    {"Hamming Distance": 25, "Vref": 850, "Veval": 525, "Vrep": 1025},
    {"Hamming Distance": 26, "Vref": 850, "Veval": 525, "Vrep": 1200},
    {"Hamming Distance": 27, "Vref": 1175, "Veval": 400, "Vrep": 1200},
    {"Hamming Distance": 28, "Vref": 775, "Veval": 600, "Vrep": 1100},
    {"Hamming Distance": 29, "Vref": 925, "Veval": 500, "Vrep": 1000},
    {"Hamming Distance": 30, "Vref": 925, "Veval": 500, "Vrep": 1025},
    {"Hamming Distance": 31, "Vref": 1175, "Veval": 400, "Vrep": 1000},
    {"Hamming Distance": 32, "Vref": 1175, "Veval": 400, "Vrep": 1150},
    {"Hamming Distance": 33, "Vref": 925, "Veval": 500, "Vrep": 975},
    {"Hamming Distance": 34, "Vref": 925, "Veval": 500, "Vrep": 1000},
    {"Hamming Distance": 35, "Vref": 925, "Veval": 500, "Vrep": 1025},
    {"Hamming Distance": 36, "Vref": 1000, "Veval": 475, "Vrep": 725},
    {"Hamming Distance": 37, "Vref": 925, "Veval": 500, "Vrep": 975},
    {"Hamming Distance": 38, "Vref": 875, "Veval": 500, "Vrep": 1025},
]

activation = [[0,[0x979da22bb11b022f,0x5dcc085a932384ab]],[9,[0xef346c3a072a4526,0x166589ae9dea3427]]]
activation = [[0,[0x979da22bb11b022f,0x5dcc085a932384ab]]]


weights = [
    [0, 0x318cabe75159921d, 0x6bd82a1562228d5e]#,
    # [1, 0xbd42dd336accb758, 0x1f2a347d74bd4974],
    # [2, 0x744120958579b580, 0x4e18f6447254a2af],
    # [3, 0x4e1dc3954fd7a670, 0xa029e7e5b9e2d3c1],
    # [4, 0x09a64de2edaa7ffd, 0x46fd1a58862d4607],
    # [5, 0xdae1b7c7d6705a2d, 0x81ebadea8bf66010],
    # [6, 0xb12ab4f5b3a3da39, 0xe98f3d17ce44de18],
    # [7, 0xed5a0962fd2e3cc6, 0x3af8d6b6357ccfd0],
    # [8, 0x60d3a811061f100c, 0x94193dea85249c8e],
    # [9, 0x52ed091f2628e607, 0x5b354cb08522d4c4]
]
hdcam = HDCAM()
powerSupply=run_class(0)
print(powerSupply)
powerSupply.init_PS()
for active in activation:
    #print(active[1])
    process_weights_and_voltages(weights, voltages, [active[1]], one_word, zero_word, hdcam, powerSupply, active[0])





powerSupply.close_PS()