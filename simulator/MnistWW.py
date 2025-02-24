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
    high_32 = (activation[0][0] >> 32) & 0xFFFFFFFF
    low_32 = activation[0][0] & 0xFFFFFFFF
    active1_low = (low_32 << 32) | low_32
    active1_high = (high_32 << 32) | high_32
    high_32 = (activation[0][1] >> 32) & 0xFFFFFFFF
    low_32 = activation[0][1] & 0xFFFFFFFF
    active2_low = (low_32 << 32) | low_32
    active2_high = (high_32 << 32) | high_32
    
    for weight in weights:
        label = weight[0]  # First value is the label

        # Initialize the count for the label if not already in the dictionary
        if label not in histogram_Arr:
            histogram_Arr[label] = 0

        for hd in range(max_hd+1):
            high_32 = (weight[1] >> 32) & 0xFFFFFFFF
            low_32 = weight[1] & 0xFFFFFFFF
            weight1low = (low_32 << 32) | low_32
            weight1high = (high_32 << 32) | high_32
            high_32 = (weight[2] >> 32) & 0xFFFFFFFF
            low_32 = weight[2] & 0xFFFFFFFF
            weight2low = (low_32 << 32) | low_32
            weight2high = (high_32 << 32) | high_32

            result1low = bitwise_xnor(format(active1_low, '032b'), format(weight1low, '032b'))
            result1high = bitwise_xnor(format(active1_high, '032b'), format(weight1high, '032b'))
            result2low = bitwise_xnor(format(active2_low, '032b'), format(weight2low, '032b'))
            result2high = bitwise_xnor(format(active2_high, '032b'), format(weight2high, '032b'))
            resultFinel = 1 if ((64 - result1low) <= hd or (64 - result1high) <= hd or (64 - result2low) <= hd or (64 - result2high) <= hd) else 0

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
    print(prediction_result, end="")

    return predicted_label == MnistLable, top_2_correct

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
    [9, 0x5b354cb08522d4c4, 0x52ed091f2628e607]
]

activation = []
csv_name = f"Mnist_data\mnist_Test_data.csv"
for row in csv.reader(open(csv_name)):
    first_active = int(row[0], 2) >> 64
    second_active = int(row[0], 2) & 0xFFFFFFFFFFFFFFFF
    label = int(row[1])
    activation.append([label, [first_active, second_active]])

labelmiss = {}
count_res = 0
top_2_count = 0

for active in activation:
    correct, top_2_correct = run_last_layer(weights, [active[1]], active[0], 30)
    
    if correct:
        count_res += 1
    else:
        if active[0] not in labelmiss:
            labelmiss[active[0]] = 1
        else:
            labelmiss[active[0]] += 1
    if top_2_correct:
        top_2_count += 1
    

print(f"Total correct predictions: {count_res/len(activation)}")
print(f"Total top 2 accuracy: {top_2_count/len(activation)}")
print(labelmiss)
