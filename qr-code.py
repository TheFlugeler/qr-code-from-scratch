from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import version_selector as vs
import encoding as en
import binary_helper as bh


# Generating Version 1-M QR Codes with alphanumeric
# Has to be 16 data code words 

def binary_to_RGB(binary):
    rgb = np.zeros(shape=(binary.shape[0],binary.shape[1],3),dtype=np.uint8)
    for i in range(binary.shape[0]):
        for j in range(binary.shape[1]):
            if binary[i,j] == 0:
                rgb[i,j] = [0,0,0]
            else:
                rgb[i,j] = [255,255,255]
    return rgb

mode = "0010"
pad_bytes = ["11101100","00010001"]

character_count = 0 #Must be 9 bits long
encoding = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 10,
    "B": 11,
    "C": 12,
    "D": 13,
    "E": 14,
    "F": 15,
    "G": 16,
    "H": 17,
    "I": 18,
    "J": 19,
    "K": 20,
    "L": 21,
    "M": 22,
    "N": 23,
    "O": 24,
    "P": 25,
    "Q": 26,
    "R": 27,
    "S": 28,
    "T": 29,
    "U": 30,
    "V": 31,
    "W": 32,
    "X": 33,
    "Y": 34,
    "Z": 35,
    " ": 36,
    "$": 37,
    "%": 38,
    "*": 39,
    "+": 40,
    "-": 41,
    ".": 42,
    "/": 43,
    ":": 44
}

def encode(message):
    global character_count 
    character_count = len(message)
    encoded_message = ""
    for i in range(0,len(message),2):
        if((i+1) >= len(message)):
            encoded_message += left_pad(dec_to_bin(encoding[message[i]]),6,"0")
            break
        numeric_value = (45*encoding[message[i]]) + encoding[message[i+1]]
        encoded_message += left_pad(dec_to_bin(numeric_value),11,"0")
    return encoded_message
        

def dec_to_bin(number):
    bit_string = ""
    while number != 0:
        bit_string += str(int(number%2))
        number -= number%2
        number /= 2
    return bit_string[::-1]

def left_pad(message, length, character):
    return character*(length-len(message)) + message

def right_pad(message, length, character):
    return message + character*(length-len(message))

def data_section(message):
    data = ""
    data += mode
    data += left_pad(dec_to_bin(len(message)),9,"0")
    data += encode(message)
    data += (8-len(data)%8)*"0"
    no_pad_bytes = 16 - int(len(data)/8)
    print(no_pad_bytes)
    for i in range(no_pad_bytes):
        print(i)
        print(f"added pad byte {i%2}")
        data += pad_bytes[i%2]
    return data


print(data_section("HELLO WORLD"))


#plt.imsave("output.png",binary_to_RGB(binary))
#print("Image Saved")

message = "this is quite a complex issue @:(£)"
ec_level = "Q"

encoding_type = vs.select_type(message)
version = vs.select_version(message,encoding_type,ec_level)
data_code_words = en.encode_message(message,encoding_type,version,ec_level)
for i in range(0,len(data_code_words),8):
    print(data_code_words[i:i+8])
