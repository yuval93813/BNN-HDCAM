from hdcamV2 import Controller as HDCAM
import random
from typing import List
from run_PS_hdcam import run_class
import os

def process_weights_and_voltages(weights, voltages, activation, one_word, zero_word, hdcam, powerSupply, MnistLable):
    andOfRes_counts = {}
    hdcam_array =   one_word * 480
    hdcam.write(hdcam_array)
    for sub_array in weights:
        label = sub_array[0]  # First value is the label
        print(f"Label: {label}")

        # Initialize the count for the label if not already in the dictionary
        if label not in andOfRes_counts:
            andOfRes_counts[label] = 0
        
        high_32 = (activation[0][0] >> 32) & 0xFFFFFFFF
        low_32 = activation[0][0] & 0xFFFFFFFF
        active1 = (low_32)
        active2 = (high_32)
        high_32 = (activation[0][1] >> 32) & 0xFFFFFFFF
        low_32 = activation[0][1] & 0xFFFFFFFF
        active3 = (low_32)
        active4 = (high_32)
        activationlow1 = [active1] * 4 + [~active1] * 16
        activationhigh1 = [active2] * 4 + [~active2] * 16
        activationlow2 = [active3] * 4 + [~active3] * 16
        activationhigh2 = [active4] * 4 + [~active4] * 16

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
            high_32 = (sub_array[1] >> 32) & 0xFFFFFFFF
            low_32 = sub_array[1] & 0xFFFFFFFF
            weightlow = (low_32)
            weighthigh = (high_32)
            hdcam_array = [weightlow] * 480 
            hdcam.write(hdcam_array)
            firstRes = hdcam.read(activationlow1)
            hdcam_array = [weighthigh] * 408
            secRes = 0
            if  firstRes != 4:
                hdcam.write(hdcam_array)
                secRes = hdcam.read(activationhigh1)

            # Process the first part of hdcam
            high_32 = (sub_array[2] >> 32) & 0xFFFFFFFF
            low_32 = sub_array[2] & 0xFFFFFFFF
            weightlow = (low_32)
            weighthigh = (high_32)
            hdcam_array = [weightlow] * 480 #+ one_word * 4
            tridRes = 0
            if firstRes != 4 or secRes != 4:
                hdcam.write(hdcam_array)
                tridRes = hdcam.read(activationlow2)
            hdcam_array = [weighthigh] * 480 #+ one_word * 4
            if firstRes != 4 or secRes != 4 or tridRes != 4:
                hdcam.write(hdcam_array)
                forthRes = hdcam.read(activationhigh2)

            # Process the second part of hdcam

            # Compute OR result
            orOfRes = 1 if (firstRes in [4] or secRes in [4] or tridRes in [4] or forthRes in [4]) else 0

            # Increment count for the label if `orOfRes == 1`
            if orOfRes == 1:
                print("im here")
                andOfRes_counts[label] += 1

            print(f"Hamming Distance: {hamming_distance}, Vref: {vref}, Veval: {veval}, Vrep: {vrep}, OR results: {orOfRes}")

    file_path = "results.txt"

    # Open the file in append mode if it exists, otherwise create it
    file_mode = "a" if os.path.exists(file_path) else "w"

    with open(file_path, file_mode) as results_file:
        results_file.write("\nOR results counts per label:\n")

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
    



zero_word = [0x0000000000000000]
one_word = [0xffffffffffffffff]

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
    # {"Hamming Distance": 17, "Vref": 950, "Veval": 500, "Vrep": 1100},
    # {"Hamming Distance": 18, "Vref": 1100, "Veval": 450, "Vrep": 1200},
    # {"Hamming Distance": 19, "Vref": 1175, "Veval": 400, "Vrep": 1200},
    # {"Hamming Distance": 20, "Vref": 1025, "Veval": 475, "Vrep": 1000},
    # {"Hamming Distance": 21, "Vref": 1025, "Veval": 475, "Vrep": 1075},
    # {"Hamming Distance": 22, "Vref": 1175, "Veval": 400, "Vrep": 1200},
    # {"Hamming Distance": 23, "Vref": 850, "Veval": 525, "Vrep": 1050},
    # {"Hamming Distance": 24, "Vref": 950, "Veval": 500, "Vrep": 1025},
    # {"Hamming Distance": 25, "Vref": 850, "Veval": 525, "Vrep": 1025},
    # {"Hamming Distance": 26, "Vref": 850, "Veval": 525, "Vrep": 1200},
    # {"Hamming Distance": 27, "Vref": 1175, "Veval": 400, "Vrep": 1200},
    # {"Hamming Distance": 28, "Vref": 775, "Veval": 600, "Vrep": 1100},
    # {"Hamming Distance": 29, "Vref": 925, "Veval": 500, "Vrep": 1000},
    # {"Hamming Distance": 30, "Vref": 925, "Veval": 500, "Vrep": 1025},
    # {"Hamming Distance": 31, "Vref": 1175, "Veval": 400, "Vrep": 1000},
    # {"Hamming Distance": 32, "Vref": 1175, "Veval": 400, "Vrep": 1150},
    # {"Hamming Distance": 33, "Vref": 925, "Veval": 500, "Vrep": 975},
    # {"Hamming Distance": 34, "Vref": 925, "Veval": 500, "Vrep": 1000},
    # {"Hamming Distance": 35, "Vref": 925, "Veval": 500, "Vrep": 1025},
    # {"Hamming Distance": 36, "Vref": 1000, "Veval": 475, "Vrep": 725},
    # {"Hamming Distance": 37, "Vref": 925, "Veval": 500, "Vrep": 975},
    # {"Hamming Distance": 38, "Vref": 875, "Veval": 500, "Vrep": 1025},
]

activation = [
    # [0, [0x979da22bb11b022f, 0x5dcc085a532384ab]],
    # [0, [0x93ad330cb81c1273, 0xdd8a624263028d5e]],
    # [0, [0x979da308b91b02b3, 0xdd8a625273038ddf]],
    # [0, [0xc7adbb0a18171277, 0xddaa62d223038d7f]],
    # [0, [0x97bda30a981b1237, 0x5d8a4a5273038d7f]],
    # [1, [0x64ebdc0b62c6653a, 0xf02952cde854994]],
    # [1, [0x7472dc0962e6e55a, 0x1f22bcac5abcd914]],
    # [1, [0xe5404e7b42cd263a, 0x3e12147c7dbd458b]],
    # [1, [0xe9404c7b62cd64a2, 0x3e36907c5dbf410b]],
    #######[1, [0x8f846e7b02dd2436, 0x1e401c7afda905cd]],
    #[2, [0x74d3110c5ef42dea, 0xcc30e6ecbbd69808]],
    # [2, [0xc605269854ed05a2, 0x540666463e50908d]],
    # [2, [0x86a5229adcd801e3, 0x41e5642365400cd]],
    # [2, [0x74f00058c4f46dc2, 0xc30f76e9bd018a8]],
    # [2, [0x56812088dcf8a9ea, 0x9c98664e735089c8]],
    # [3, [0x4e94423c567aa1d2, 0xb020e7eebdf833a1]],
    # [3, [0x4e35421c5e7ca1c2, 0xa820e3ecb99a93e0]],
    # [3, [0x4635d308be1280d0, 0xd920feec3bae99e1]],
    # [3, [0x4635d309be1281d2, 0xc920e2ec3ba799e0]],
    #####[3, [0x66f553081e16f1d2, 0xc938f2e89b8299e2]],
    # [4, [0xafbc6e7b27cbb118, 0x16599b4e63e2b3d3]],
    # [4, [0x8aade7a2bf6d63af, 0x857d540882a6598f]],
    # [4, [0xcbef4b66e1e92527, 0x22257001126c145f]],
    # [4, [0x8baee672725a19fe, 0x97df83c028756467]],
    # [4, [0x8f6d5b8d9eaa9252, 0x2665a26e8daf1b2f]],
    # [5, [0x86e9b692c9574423, 0x4da2a2ba319b16bb]],
    #[5, [0xd6f1f7089e12447b, 0x5d22aaee5bea9930]],
    #[5, [0x9eb576acbb83433f, 0x85e73dcadbe4a2e1]],
    #[5, [0x86fdab4b97534427, 0x5428eeadda74cbb]],
    #[5, [0x94b5770cae93476f, 0xcd06abeadbe698be]],
    [6, [0xb49b34a9b183c37b, 0x898f1412de45e398]],
    [6, [0xb06b1af950a56263, 0xe99e53144f15ed1b]],
    [6, [0x902f109df8a5436b, 0xe99ef3144f15ec1b]],
    [6, [0xb08a14bdf0a1e36b, 0xa09fd504ce55e298]],
    # #[6, [0x952fdaf6ee07c37b, 0xb021d02bfa5f9e98]],
    # #[7, [0x6e5208209221fe72, 0x93ac8eb62da1a5f6]],
    # #[7, [0x5f7800244337289c, 0x7278e9782a240468]],
    # #[7, [0x6c7a092ad72e4c0e, 0x7278e9782a2d7f3a]],
    # #[7, [0xc37a092acf3c78c7, 0xf2e7803502dff93a]],
    # #[7, [0x6f500058401f2442, 0x3a3a7b66a5951443]],
    # #[8, [0x90bd6a3ca2ab432f, 0xc503a98acda5bc9f]],
    # #[8, [0xa8d12c3e42bf076e, 0x1417a8f2ddaa9c8b]],
    # #[8, [0xbc992e3a02af062e, 0x5406ac6addaa1c8b]],
    # #[8, [0xb0992e2c46bb07ae, 0xc406e94adfa29ccb]],
    # #[8, [0x2952a3c06b52186, 0xc40163cafd903ccf]],
    [9, [0x6a3c1bad86a58c35, 0xb014107082c3e7af]],
    [9, [0xef346c3a0e529468, 0x5668a6ba7750d469]],
    [9, [0x6a344e2cc3e8397d, 0x776c7d1a6ac6de39]],
    # [9, [0xdfbc207a249ae63c, 0x79fbd82c21097623]],
    # [9, [0x6e346c2ac7a2e486, 0x977581a60d85702f]]
]

# activation = [
#     [5, [0xd6f1f7089e12447b, 0x5d22aaee5bea9930]],
#     [5, [0x9eb576acbb83433f, 0x85e73dcadbe4a2e1]],
#     [5, [0x86fdab4b97534427, 0x5428eeadda74cbb]],
#     [5, [0x94b5770cae93476f, 0xcd06abeadbe698be]],
# ]
# activation = [
    
#     [9, [0x8fb5641b8d5b07e7, 0x3425a9ceb16a96e3]],
#     [9, [0x4f346c3a8f6a2586, 0x1e608aee3daa3423]],
#     #[9, [0x4b344a2ccb20e4c7, 0xb171c1a60d997723]],
#     [9, [0xecb66c2aa3ae4566, 0xae6589aa9cec70af]],
#     [9, [0x4b2c6c9cc128e586, 0xb05141062d90742f]]
# ]
              

activation = [
    [9, [0xd3b5600cccb811c7, 0xd535e1c8e110bc62]],
    [9, [0xcbb6682ec9384447, 0xa561c1e2c5197e2f]],
    [9, [0xefac2cba816b4407, 0x346dc112c4096627]],
]




weights = [
    [0, 0x318cabe75159921d, 0x6bd82a1562228d5e],
    [1, 0xbd42dd336accb758, 0x1f2a347d74bd4974],
    [2, 0x744120958579b580, 0x4e18f6447254a2af],
    [3, 0x4e1dc3954fd7a670, 0xa029e7e5b9e2d3c1],
    [4, 0x09a64de2edaa7ffd, 0x46fd1a58862d4607],
    [5, 0xdae1b7c7d6705a2d, 0x81ebadea8bf66010],
    [6, 0xb12ab4f5b3a3da39, 0xe98f3d17ce44de18],
    [7, 0xed5a0962fd2e3cc6, 0x3af8d6b6357ccfd0],
    [8, 0x60d3a811061f100c, 0x94193dea85249c8e],
    [9, 0x5b354cb08522d4c4 , 0x52ed091f2628e607]
]

hdcam = HDCAM()
powerSupply=run_class(0)
print(powerSupply)
powerSupply.init_PS()
for active in activation:
    #print(active[1])
    process_weights_and_voltages(weights, voltages, [active[1]], one_word, zero_word, hdcam, powerSupply, active[0])





powerSupply.close_PS()