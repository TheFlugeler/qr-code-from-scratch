from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import version_selector as vs
import encoding as en
import binary_helper as bh

message = "this is quite a complex issue @:(£)"
ec_level = "Q"

encoding_type = vs.select_type(message)
version = vs.select_version(message,encoding_type,ec_level)
data_code_words = en.encode_message(message,encoding_type,version,ec_level)
for i in range(0,len(data_code_words),8):
    print(data_code_words[i:i+8])
