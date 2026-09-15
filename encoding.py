import sys
import binary_helper as bh
import version_selector as vs

ALHPANUMERIC_ENCODING = {
    "0": 0,"1": 1,"2": 2,"3": 3,"4": 4,"5": 5,"6": 6,"7": 7,"8": 8,"9": 9,
    "A": 10,"B": 11,"C": 12,"D": 13,"E": 14,"F": 15,"G": 16,"H": 17,"I": 18,
    "J": 19,"K": 20,"L": 21,"M": 22,"N": 23,"O": 24,"P": 25,"Q": 26,"R": 27,
    "S": 28,"T": 29,"U": 30,"V": 31,"W": 32,"X": 33,"Y": 34,"Z": 35," ": 36,
    "$": 37,"%": 38,"*": 39,"+": 40,"-": 41,".": 42,"/": 43,":": 44
}
TOTAL_BYTE_LIMITS = {
    1:  {'L': 19,  'M': 16,  'Q': 13,  'H': 9},
    2:  {'L': 34,  'M': 28,  'Q': 22,  'H': 16},
    3:  {'L': 55,  'M': 44,  'Q': 34,  'H': 26},
    4:  {'L': 80,  'M': 64,  'Q': 48,  'H': 36},
    5:  {'L': 108, 'M': 86,  'Q': 62,  'H': 46},
    6:  {'L': 136, 'M': 108, 'Q': 76,  'H': 60},
    7:  {'L': 156, 'M': 124, 'Q': 88,  'H': 66},
    8:  {'L': 194, 'M': 154, 'Q': 110, 'H': 86},
    9:  {'L': 232, 'M': 182, 'Q': 132, 'H': 100},
    10: {'L': 274, 'M': 216, 'Q': 154, 'H': 122},
    11: {'L': 324, 'M': 254, 'Q': 180, 'H': 140},
    12: {'L': 370, 'M': 290, 'Q': 206, 'H': 158},
    13: {'L': 428, 'M': 334, 'Q': 244, 'H': 180},
    14: {'L': 461, 'M': 365, 'Q': 261, 'H': 197},
    15: {'L': 523, 'M': 415, 'Q': 295, 'H': 223},
    16: {'L': 589, 'M': 453, 'Q': 325, 'H': 253},
    17: {'L': 647, 'M': 507, 'Q': 367, 'H': 283},
    18: {'L': 721, 'M': 563, 'Q': 397, 'H': 313},
    19: {'L': 795, 'M': 627, 'Q': 445, 'H': 341},
    20: {'L': 861, 'M': 669, 'Q': 485, 'H': 385},
    21: {'L': 932, 'M': 714, 'Q': 512, 'H': 406},
    22: {'L': 1006,'M': 782, 'Q': 568, 'H': 442},
    23: {'L': 1094,'M': 860, 'Q': 614, 'H': 464},
    24: {'L': 1174,'M': 914, 'Q': 664, 'H': 514},
    25: {'L': 1276,'M': 1000,'Q': 718, 'H': 538},
    26: {'L': 1370,'M': 1062,'Q': 754, 'H': 596},
    27: {'L': 1468,'M': 1128,'Q': 808, 'H': 628},
    28: {'L': 1531,'M': 1193,'Q': 871, 'H': 661},
    29: {'L': 1631,'M': 1267,'Q': 911, 'H': 701},
    30: {'L': 1735,'M': 1373,'Q': 985, 'H': 745},
    31: {'L': 1843,'M': 1455,'Q': 1033,'H': 793},
    32: {'L': 1955,'M': 1541,'Q': 1115,'H': 845},
    33: {'L': 2071,'M': 1631,'Q': 1171,'H': 901},
    34: {'L': 2191,'M': 1725,'Q': 1231,'H': 961},
    35: {'L': 2306,'M': 1812,'Q': 1286,'H': 986},
    36: {'L': 2434,'M': 1914,'Q': 1354,'H': 1054},
    37: {'L': 2566,'M': 1992,'Q': 1426,'H': 1096},
    38: {'L': 2702,'M': 2102,'Q': 1502,'H': 1142},
    39: {'L': 2812,'M': 2216,'Q': 1582,'H': 1222},
    40: {'L': 2956,'M': 2334,'Q': 1666,'H': 1276},
}
PAD_BYTES = ["11101100", "00010001"]

def encode_message(message,type,version,ec_level):
    global TOTAL_BYTE_LIMITS
    global PAD_BYTES
    data_words = ""
    message_binary = ""
    if type == "N":
        data_words += "0001"
        message_binary = encode_numeric(message)
    elif type == "A":
        data_words += "0010"
        message_binary = encode_alphanumeric(message)
    else:
        data_words += "0100"
        message_binary = encode_byte(message)
    data_words += bh.left_pad(bh.dec_to_bin(len(message)),character_count_length(version,type),"0") #character count
    data_words += message_binary
    data_words += "0"*(8-(len(data_words)%8))
    bytes_remaining = int(TOTAL_BYTE_LIMITS[version][ec_level] - (len(data_words)/8))
    for i in range(bytes_remaining):
        data_words += PAD_BYTES[i%2]
    return data_words

def encode_numeric(message):
    print("Using numeric encoding")
    data = ""
    for i in range(0,len(message),3):
        if i+2 >= len(message):
            number = int(message[i:])
            binary_length = 7
            if len(str(number)) < 2: binary_length = 4
            binary_number = bh.left_pad(bh.dec_to_bin(number),binary_length,"0")
            data += binary_number
        else:       
            number = int(message[i:i+3])
            binary_number = bh.left_pad(bh.dec_to_bin(number),10,"0")
            data += binary_number
    return data

def encode_alphanumeric(message):
    print("Using alphanumeric encoding")
    global ALHPANUMERIC_ENCODING
    data = ""
    for i in range(0,len(message),2):
        if i+1 >= len(message):
            binary_number = bh.left_pad(bh.dec_to_bin(ALHPANUMERIC_ENCODING[message[i]]),6,"0")
            data += binary_number
        else:
            number = ALHPANUMERIC_ENCODING[message[i]]*45 + ALHPANUMERIC_ENCODING[message[i+1]]
            binary_number = bh.left_pad(bh.dec_to_bin(number),11,"0")
            data += binary_number
    return data

def encode_byte(message):
    print("Using byte encoding")
    data = ""
    for i in range(len(message)):
        data += bh.left_pad(bh.dec_to_bin(ord(message[i])),8,"0")
    return data

def character_count_length(version, type):
    type_index = 0
    if type == "A": type_index = 1
    elif type == "B": type_index = 2
    if version < 10: return [10,9,8][type_index]
    elif version < 27: return [12,11,16][type_index]
    else: return [14,13,16][type_index]
