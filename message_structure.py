import binary_helper as bh

def structure_message(blocks,ec_blocks,version):
    structured_blocks = []
    for i in range(len(blocks[-1])):
        for j in range(len(blocks)):
            if len(blocks[j]) > i:
                structured_blocks.append(blocks[j][i])

    for i in range(len(ec_blocks[-1])):
        for j in range(len(ec_blocks)):
            if len(ec_blocks[j]) > i:
                structured_blocks.append(ec_blocks[j][i])

    structured_string = ""
    for word in structured_blocks:
        structured_string += bh.left_pad(bh.dec_to_bin(word),8,"0")

    if version >= 2  and version <= 6:  structured_string += "0"*7
    if version >= 14 and version <= 20: structured_string += "0"*3
    if version >= 21 and version <= 27: structured_string += "0"*4
    if version >= 28 and version <= 34: structured_string += "0"*3

    return structured_string
 
 
 
