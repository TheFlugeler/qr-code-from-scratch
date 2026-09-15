from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import version_selector as vs
import encoding as en
import binary_helper as bh
import block_creator as bc

message = "This is a test message that should mean that I can test my blocks really really well!!"
ec_level = "Q"

encoding_type = vs.select_type(message)

version = vs.select_version(message,encoding_type,ec_level)

data_string = en.encode_message(message,encoding_type,version,ec_level)

data_code_words = []
for i in range(0,len(data_string),8):
    data_code_words.append(bh.bin_to_dec(data_string[i:i+8]))

print(f"Number of code words: {len(data_code_words)}")

blocks = bc.message_to_blocks(data_code_words,version,ec_level)

print("Block sizes:")
for block in blocks:
    print(f"\t {len(block)}")

