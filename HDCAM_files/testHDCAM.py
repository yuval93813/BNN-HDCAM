from hdcamV2 import Controller as HDCAM
import random
from typing import List



def getRandomList(size: int) -> List[int]:
    l = []
    for i in range(size):
        l.append(random.randint(0, (1<<64)))
    return l
    
def insert_errors(binary_string, hamming_distance):
    binary_list = list(binary_string)
    errors_count = 0
    already_used_index = set()
    while errors_count < hamming_distance:
        index = random.randint(0, len(binary_list) - 1)
        while index in already_used_index:
            index = random.randint(0, len(binary_list) - 1)
        if binary_list[index] == "0":
            binary_list[index] = "1"
            errors_count += 1
        elif binary_list[index] == "1":
            binary_list[index] = "0"
            errors_count += 1
        already_used_index.add(index)
    return "".join(binary_list)

def decimal_to_binary_64(decimal_number):
    binary_representation = bin(decimal_number)[2:].zfill(64)
    return binary_representation
    

def binary_to_decimal(binary_number):
    decimal_value = int(binary_number, 2)
    return decimal_value
    
hdcam = HDCAM()
hdcam_array = getRandomList(120)
hdcam_array = hdcam_array*4
#hdcam_array = [0xFFFFFFFFFFFFFFFF] * 480

print(hdcam_array)
#hdcam_array_error1 = [0 for i in range(480)]
#hdcam_array_ones = [1 for i in range(480)]
hdcam.write(hdcam_array)
#hdcam.read(hdcam_array)
#inserting errors with a hamming distance
hamming_dist = 4
print(f"{hamming_dist} errors")


for index in range(0,480):
    hdcam_array_bin=decimal_to_binary_64(hdcam_array[index])
    error_list = insert_errors(hdcam_array_bin,hamming_dist)
    error_hdcam = binary_to_decimal(error_list)
    hdcam_array[index] = error_hdcam


hdcam.read(hdcam_array)