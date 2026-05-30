import numpy as np

def binary_to_RGB(binary):
    rgb = np.zeros(shape=(binary.shape[0],binary.shape[1],3),dtype=np.uint8)
    for i in range(binary.shape[0]):
        for j in range(binary.shape[1]):
            if binary[i,j] == 0:
                rgb[i,j] = [0,0,0]
            else:
                rgb[i,j] = [255,255,255]
    return rgb

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
