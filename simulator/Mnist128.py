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
    
    return ones_count

def run_last_layer(weights, activation, MnistLable, max_hd):
    histogram_Arr = {}
    for weight in weights:
        label = weight[0]  # First value is the label

        # Initialize the count for the label if not already in the dictionary
        if label not in histogram_Arr:
            histogram_Arr[label] = 0

        for hd in range(max_hd+1):
            result = bitwise_xnor(format(activation, '0128b'), format(weight[1], '0128b'))
            resultFinel = 1 if (128 - result) <= hd else 0

            if resultFinel == 1:
                histogram_Arr[label] += 1

    # Get the top 2 labels with the highest counts
    top_2_labels = sorted(histogram_Arr.items(), key=lambda item: (-item[1], item[0]))[:2]
    top_2_labels = [label for label, count in top_2_labels]
    predicted_label = top_2_labels[0]
    top_2_correct = MnistLable in top_2_labels
    
    # Check for tie in the top 2
    if top_2_correct and not(predicted_label == MnistLable) :
        # Check if there are more ties that can enter the top 2
        tied_labels = [label for label, count in histogram_Arr.items() if count == histogram_Arr[top_2_labels[1]]]
        if len(tied_labels) > 2:
            top_2_correct = False
        else:
            top_2_correct = MnistLable in tied_labels
       
    prediction_result = f"Predicted Label: {predicted_label:<2}, MNIST Label: {MnistLable:<2}, top_2_correct = {top_2_correct}, Top 2 Labels: {top_2_labels} \n"
    # print(prediction_result, end="")

    return predicted_label == MnistLable, top_2_correct

weightsMnist = [
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


weightsHG = [
    [0, 0xdcf98b43aac413620c64705e439aace8],
    [1, 0x251470a24d3fcdfd57b01db34e6d5717],
    [2, 0xd95e2f6afb016421f598438fc9880c6c],
    [3, 0x7aabf54fbbfc20fb82e54d6647f43968],
    [4, 0xeb9e785aef9472f149d68a58cdd1c724],
    [5, 0xa550a720b20ce8a0df23dd9865b3dfa7],
    [6, 0x363be447aac4920b08665ae210922390],
    [7, 0x4e7899936fc47a302cd622b9a2131b34],
    [8, 0x54f43ecb35975dcf3d80752f72a00fd9],
    [9, 0x6eee9e0580d200dab2f6037b468af467],
    [10, 0xf3efb1bf7458c65fe677e7a191c360fb],
    [11, 0xed4f017a11155e06b749e25b6210eb6e],
    [12, 0x0435be5a1d08eaf559b9096a98adff1d],
    [13, 0x00c10f6ac3e10e70c049651108307877],
    [14, 0xbfb0d8d7bfbe658410357da6ded52d03],
    [15, 0x56ff2c34514538eb5c7e6210c51f48bc],
    [16, 0x30394e2b70b26c9877e5f3a4785861eb],
    [17, 0xaf0d8679a74d9c6192216b543fdb24a1],
    [18, 0x7d9f8774d60bc315828d8a6953e727c8],
    [19, 0xad50f0b584c3762ca3717e292f7b8e23]
]

activation = []
csv_Mnist = f"Mnist_data\mnist_Test_data.csv"
csv_HG = f"HG_data\hg_Test_data.csv"
for row in csv.reader(open(csv_HG)):
    active = int(row[0], 2)
    label = int(row[1])
    activation.append([label, active])

os.makedirs(os.path.dirname("C:/Users/User/Desktop/BNN-HDCAM/HG128Results.txt"), exist_ok=True)
with open("C:/Users/User/Desktop/BNN-HDCAM/HG128Results.txt", "w") as result_file:
    for hd in range(0,70,2):
        labelmiss = {}
        count_res = 0
        top_2_count = 0

        for active in activation:
            correct, top_2_correct = run_last_layer(weightsMnist, active[1], active[0], hd)
            
            if correct:
                count_res += 1
            else:
                if active[0] not in labelmiss:
                    labelmiss[active[0]] = 1
                else:
                    labelmiss[active[0]] += 1
            if top_2_correct:
                top_2_count += 1
        print(f"HD: {hd}")
        print(f"Total correct predictions: {count_res/len(activation)}")
        print(f"Total top 2 accuracy: {top_2_count/len(activation)}")
        print(f"Label miss counts: {labelmiss}\n")
        result_file.write(f"HD: {hd}\n")
        result_file.write(f"Total correct predictions: {count_res/len(activation)}\n")
        result_file.write(f"Total top 2 accuracy: {top_2_count/len(activation)}\n")
        result_file.write(f"Label miss counts: {labelmiss}\n\n")