import sys
from binary import *
alphanumeric_encoding = {
    "0": 0,"1": 1,"2": 2,"3": 3,"4": 4,"5": 5,"6": 6,"7": 7,"8": 8,"9": 9,
    "A": 10,"B": 11,"C": 12,"D": 13,"E": 14,"F": 15,"G": 16,"H": 17,"I": 18,
    "J": 19,"K": 20,"L": 21,"M": 22,"N": 23,"O": 24,"P": 25,"Q": 26,"R": 27,
    "S": 28,"T": 29,"U": 30,"V": 31,"W": 32,"X": 33,"Y": 34,"Z": 35," ": 36,
    "$": 37,"%": 38,"*": 39,"+": 40,"-": 41,".": 42,"/": 43,":": 44
}

def encode_message(message):
    numeric = "0123456789"
    alphanumeric = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:"
    if all(c in numeric for c in message):
        return encode_numeric(message)
    elif all(c in alphanumeric for c in message):
        return encode_alphanumeric(message)
    elif all(ord(c) < 256 for c in message):
        return encode_byte(message)
    else:
        print("ERROR: NOT ENCODABLE")
        sys.exit()

def encode_numeric(message):
    data = ""
    for i in range(0,len(message),3):
        if i+2 >= len(message):
            number = int(message[i:])
            binary_length = 7
            if len(str(number)) < 2: binary_length = 4
            binary_number = left_pad(dec_to_bin(number),binary_length,"0")
            data += binary_number
        else:       
            number = int(message[i:i+3])
            binary_number = left_pad(dec_to_bin(number),10,"0")
            data += binary_number
    return data

def encode_alphanumeric(message):
    data = ""
    for i in range(0,len(message),2):
        if i+1 >= len(message):
            binary_number = left_pad(dec_to_bin(alphanumeric_encoding[message[i]]),6,"0")
            data += binary_number
        else:
            number = alphanumeric_encoding[message[i]]*45 + alphanumeric_encoding[message[i+1]]
            binary_number = left_pad(dec_to_bin(number),11,"0")
            data += binary_number
    return data

def encode_byte(message):
    data = ""
    for i in range(len(message)):
        data += left_pad(dec_to_bin(ord(message[i])),8,"0")
    return data