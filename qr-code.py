from PIL import Image

import matplotlib.pyplot as plt
import numpy as np



def data_section(message):
    data = ""
    data += mode
    data += left_pad(dec_to_bin(len(message)),9,"0")
    data += encode(message)
    data += (8-(len(data)-(len(data)//8)*8))*"0"


#plt.imsave("output.png",binary_to_RGB(binary))
#print("Image Saved")

