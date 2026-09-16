import binary_helper as bh

EC_LEVEL_VALUE = {
    "L":1,
    "M":0,
    "Q":3,
    "H":2
}

def write_data(qr_code,reserved_areas,data_string):
    size = qr_code.shape[0]
    direction = "UP"
    reader_index = 0
    column = size-1
    while column > 0:
        if column == 6:
            column -= 1
        if direction == "UP":
            for row in range(size-1,-1,-1):
                if(reserved_areas[row,column] != 1):
                    qr_code[row,column] = int(data_string[reader_index])
                    #print(f"Writing row:{row}, col:{column}")
                    reader_index += 1
                if(reserved_areas[row,column-1] != 1):
                    qr_code[row,column-1] = int(data_string[reader_index])
                    #print(f"Writing row:{row}, col:{column-1}")
                    reader_index += 1
            direction = "DOWN"
        elif direction == "DOWN":
            for row in range(0,size):
                if(reserved_areas[row,column] != 1):
                    qr_code[row,column] = int(data_string[reader_index])
                    #print(f"Writing row:{row}, col:{column}")
                    reader_index += 1
                if(reserved_areas[row,column-1] != 1):
                    qr_code[row,column-1] = int(data_string[reader_index])
                    #print(f"Writing row:{row}, col:{column-1}")
                    reader_index += 1
            direction = "UP"
        column -=2
    return qr_code

def write_format_info(qr_code,ec_level,mask_pattern):
    size = qr_code.shape[0]
    generator = "10100110111"
    ec_bits = bh.left_pad(bh.dec_to_bin(EC_LEVEL_VALUE[ec_level]),2,"0")
    mask_bits = bh.left_pad(bh.dec_to_bin(mask_pattern),3,"0")
    bit_string = bh.right_pad(ec_bits + mask_bits,15,"0")

    bit_string = bh.trim_left(bit_string,"0")
    while len(bit_string) >= 11:
        padded_generator = bh.right_pad(generator,len(bit_string),"0")
        bit_string = bh.dec_to_bin(bh.bin_to_dec(bit_string)^bh.bin_to_dec(padded_generator))
        bit_string = bh.trim_left(bit_string,"0")

    bit_string = bh.left_pad(bit_string,10,"0")
    bit_string = ec_bits + mask_bits + bit_string

    mask_string = "101010000010010"
    bit_string = bh.left_pad(bh.dec_to_bin(bh.bin_to_dec(bit_string)^bh.bin_to_dec(mask_string)),15,"0")

    for i in range(6):
        qr_code[8,i] = bit_string[i]

    qr_code[8,7] = bit_string[6]
    qr_code[8,8] = bit_string[7]
    qr_code[7,8] = bit_string[8]

    for i in range(6):
        qr_code[5-i,8] = bit_string[9+i]

    for i in range(7):
        qr_code[size-1-i,8] = bit_string[i]

    for i in range(8):
        qr_code[8,size-8+i] = bit_string[7+i]

    return qr_code


def write_version_info(qr_code,version):
    size = qr_code.shape[0]
    generator = "1111100100101"
    version_bits = bh.left_pad(bh.dec_to_bin(version),6,"0")
    bit_string = bh.right_pad(version_bits,18,"0")
    bit_string = bh.trim_left(bit_string,"0")

    while len(bit_string) >= 13:
        padded_generator = bh.right_pad(generator,len(bit_string),"0")
        bit_string = bh.dec_to_bin(bh.bin_to_dec(bit_string)^bh.bin_to_dec(padded_generator))
        bit_string = bh.trim_left(bit_string,"0")

    bit_string = bh.left_pad(bit_string,12,"0")
    bit_string = version_bits + bit_string

    for i in range(6):
        for j in range(3):
            qr_code[size-11+j,i] = bit_string[i*3+j]
            qr_code[i,size-11+j] = bit_string[i*3+j]

    return qr_code