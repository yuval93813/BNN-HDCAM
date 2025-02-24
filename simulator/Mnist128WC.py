import csv
import os

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
    # print(f"Binary 1:    {bin1}")
    # print(f"Binary 2:    {bin2}")
    # print(f"XNOR Result: {xnor_bin}")
    # print(f"Number of 1s: {ones_count}")

    return ones_count


def run_last_layer(weights, activation,MnistLable, max_hd):
    histogram_Arr = {}
    for weight in weights:
        label = weight[0]  # First value is the label

        # Initialize the count for the label if not already in the dictionary
        if label not in histogram_Arr:
            histogram_Arr[label] = 0

        min_xor_result = 128
        for i in range(128):
            # Flip the i-th bit of the weight
            modified_weight = weight[1] ^ (1 << i)
            result = bitwise_xnor(format(active[1], '0128b'), format(modified_weight, '0128b'))
            
            if result < min_xor_result:
                min_xor_result = result

        for hd in range(max_hd+1):
            resultFinel = 1 if (128 - min_xor_result) <= hd else 0

            if resultFinel == 1:
                histogram_Arr[label] += 1

    # Find the label with the highest count
    
    predicted_label = max(histogram_Arr, key=histogram_Arr.get)
    prediction_result = f"Predicted Label: {predicted_label}, MNIST Label: {MnistLable}\n"
    print(prediction_result, end="")
    
    return predicted_label == MnistLable
        


weights = [
    [0, 0x318cabe75159921d6bd82a1562228d5e],
    [1, 0xbd42dd336accb7581f2a347d74bd4974],
    [2, 0x744120958579b5804e18f6447254a2af],
    [3, 0x4e1dc3954fd7a670a029e7e5b9e2d3c1],
    [4, 0x09a64de2edaa7ffd46fd1a58862d4607],
    [5, 0xdae1b7c7d6705a2d81ebadea8bf66010],
    [6, 0xb12ab4f5b3a3da39e98f3d17ce44de18],
    [7, 0xed5a0962fd2e3cc63af8d6b6357ccfd0],
    [8, 0x60d3a811061f100c94193dea85249c8e],
    [9, 0x5b354cb08522d4c452ed091f2628e607]
]

# activation = [
#     [0, [0x979da22bb11b022f, 0x5dcc085a532384ab]],
#     [0, [0x93ad330cb81c1273, 0xdd8a624263028d5e]],
#     [0, [0x979da308b91b02b3, 0xdd8a625273038ddf]],
#     [0, [0xc7adbb0a18171277, 0xddaa62d223038d7f]],
#     [0, [0x97bda30a981b1237, 0x5d8a4a5273038d7f]],
#     [1, [0x64ebdc0b62c6653a, 0xf02952cde854994]],
#     [1, [0x7472dc0962e6e55a, 0x1f22bcac5abcd914]],
#     [1, [0xe5404e7b42cd263a, 0x3e12147c7dbd458b]],
#     [1, [0xe9404c7b62cd64a2, 0x3e36907c5dbf410b]],
#     [1, [0x8f846e7b02dd2436, 0x1e401c7afda905cd]],##
#     [2, [0x74d3110c5ef42dea, 0xcc30e6ecbbd69808]],
#     [2, [0xc605269854ed05a2, 0x540666463e50908d]],
#     [2, [0x86a5229adcd801e3, 0x41e5642365400cd]],
#     [2, [0x74f00058c4f46dc2, 0xc30f76e9bd018a8]],
#     [2, [0x56812088dcf8a9ea, 0x9c98664e735089c8]],
#     [3, [0x4e94423c567aa1d2, 0xb020e7eebdf833a1]],
#     [3, [0x4e35421c5e7ca1c2, 0xa820e3ecb99a93e0]],
#     [3, [0x4635d308be1280d0, 0xd920feec3bae99e1]],
#     [3, [0x4635d309be1281d2, 0xc920e2ec3ba799e0]],
#     [3, [0x66f553081e16f1d2, 0xc938f2e89b8299e2]],##
#     [4, [0xafbc6e7b27cbb118, 0x16599b4e63e2b3d3]],
#     [4, [0x8aade7a2bf6d63af, 0x857d540882a6598f]],
#     [4, [0xcbef4b66e1e92527, 0x22257001126c145f]],
#     [4, [0x8baee672725a19fe, 0x97df83c028756467]],
#     [4, [0x8f6d5b8d9eaa9252, 0x2665a26e8daf1b2f]],
#     [5, [0x86e9b692c9574423, 0x4da2a2ba319b16bb]],
#     [5, [0xd6f1f7089e12447b, 0x5d22aaee5bea9930]],
#     [5, [0x9eb576acbb83433f, 0x85e73dcadbe4a2e1]],
#     [5, [0x86fdab4b97534427, 0x5428eeadda74cbb]],
#     [5, [0x94b5770cae93476f, 0xcd06abeadbe698be]],
#     [6, [0xb49b34a9b183c37b, 0x898f1412de45e398]],
#     [6, [0xb06b1af950a56263, 0xe99e53144f15ed1b]],
#     [6, [0x902f109df8a5436b, 0xe99ef3144f15ec1b]],
#     [6, [0xb08a14bdf0a1e36b, 0xa09fd504ce55e298]],
#     [6, [0x952fdaf6ee07c37b, 0xb021d02bfa5f9e98]],
#     [7, [0x6e5208209221fe72, 0x93ac8eb62da1a5f6]],
#     [7, [0x5f7800244337289c, 0x7278e9782a240468]],
#     [7, [0x6c7a092ad72e4c0e, 0x7278e9782a2d7f3a]],
#     [7, [0xc37a092acf3c78c7, 0xf2e7803502dff93a]],
#     [7, [0x6f500058401f2442, 0x3a3a7b66a5951443]],
#     [8, [0x90bd6a3ca2ab432f, 0xc503a98acda5bc9f]],
#     [8, [0xa8d12c3e42bf076e, 0x1417a8f2ddaa9c8b]],
#     [8, [0xbc992e3a02af062e, 0x5406ac6addaa1c8b]],
#     [8, [0xb0992e2c46bb07ae, 0xc406e94adfa29ccb]],
#     [8, [0x2952a3c06b52186, 0xc40163cafd903ccf]],
#     [9, [0x6a3c1bad86a58c35, 0xb014107082c3e7af]],##
#     [9, [0xef346c3a0e529468, 0x5668a6ba7750d469]],##
#     [9, [0x6a344e2cc3e8397d, 0x776c7d1a6ac6de39]],##
#     [9, [0xdfbc207a249ae63c, 0x79fbd82c21097623]],
#     [9, [0x6e346c2ac7a2e486, 0x977581a60d85702f]]
# ]
activation = []
csv_name = "mnistLL.csv"
for row in csv.reader(open(csv_name)):
    active = int(row[0], 2)
    label = int(row[1])
    activation.append([label, active])
  




labelmiss = {}
count_res = 0
for active in activation:

    if run_last_layer(weights, [active[1]], active[0], 64):
        count_res += 1
    else:
        if active[0] not in labelmiss:
            labelmiss[active[0]] = 0
        else:
            labelmiss[active[0]] += 1
print(count_res)
print(labelmiss)
