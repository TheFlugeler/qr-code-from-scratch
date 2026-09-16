from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import version_selector as vs
import encoding as en
import binary_helper as bh
import block_creator as bc
import error_correction as ec
import message_structure as ms
import pattern_generator as pg
import data_write as dw
import data_mask as dm

#message = "https://www.geeksforgeeks.org/python/get-the-logical-xor-of-two-variables-in-python/"
message = "This should use multiple blocks if i really drag on and on and on and on and on you're taking the piss now OH MY DAYS"
ec_level = "L"

encoding_type = vs.select_type(message)

version = vs.select_version(message,encoding_type,ec_level)

data_string = en.encode_message(message,encoding_type,version,ec_level)

data_code_words = []
for i in range(0,len(data_string),8):
    data_code_words.append(bh.bin_to_dec(data_string[i:i+8]))

print(f"Number of code words: {len(data_code_words)}")

blocks = bc.message_to_blocks(data_code_words,version,ec_level)

print("BLOCK SIZES:")
for block in blocks:
    print(f"\t{len(block)}")

ec_blocks = ec.generate_ec_code_words(blocks,version,ec_level)

print("EC_BLOCK SIZES:")
for ec_block in ec_blocks:
    print(f"\t{len(ec_block)}")

final_data_string = ms.structure_message(blocks,ec_blocks,version)

print(f"Final data string no bytes: {len(final_data_string)/8}")

(qr_code,reserved_areas) = pg.generate_base(version)

qr_code = dw.write_data(qr_code,reserved_areas,final_data_string)

(qr_code, mask_number) = dm.mask_code(qr_code,reserved_areas)

print(f"Mask number: {mask_number}")

qr_code = dw.write_format_info(qr_code,ec_level,mask_number)

if version >= 7:
    qr_code = dw.write_version_info(qr_code,version)

def binary_to_RGB(binary):
    rgb = np.zeros(shape=(binary.shape[0],binary.shape[1],3),dtype=np.uint8)
    for i in range(binary.shape[0]):
        for j in range(binary.shape[1]):
            if binary[i,j] == 1:
                rgb[i,j] = [0,0,0]
            else:
                rgb[i,j] = [255,255,255]
    return rgb


plt.imsave("outputs/output.png",binary_to_RGB(qr_code))
plt.imsave("outputs/reserved.png",binary_to_RGB(reserved_areas))