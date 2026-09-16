import numpy as np
SIZE = 0
ALIGNMENT_LOCATIONS = {
    1:  [],
    2:  [6, 18],
    3:  [6, 22],
    4:  [6, 26],
    5:  [6, 30],
    6:  [6, 34],
    7:  [6, 22, 38],
    8:  [6, 24, 42],
    9:  [6, 26, 46],
    10: [6, 28, 50],
    11: [6, 30, 54],
    12: [6, 32, 58],
    13: [6, 34, 62],
    14: [6, 26, 46, 66],
    15: [6, 26, 48, 70],
    16: [6, 26, 50, 74],
    17: [6, 30, 54, 78],
    18: [6, 30, 56, 82],
    19: [6, 30, 58, 86],
    20: [6, 34, 62, 90],
    21: [6, 28, 50, 72, 94],
    22: [6, 26, 50, 74, 98],
    23: [6, 30, 54, 78, 102],
    24: [6, 28, 54, 80, 106],
    25: [6, 32, 58, 84, 110],
    26: [6, 30, 58, 86, 114],
    27: [6, 34, 62, 90, 118],
    28: [6, 26, 50, 74, 98, 122],
    29: [6, 30, 54, 78, 102, 126],
    30: [6, 26, 52, 78, 104, 130],
    31: [6, 30, 56, 82, 108, 134],
    32: [6, 34, 60, 86, 112, 138],
    33: [6, 30, 58, 86, 114, 142],
    34: [6, 34, 62, 90, 118, 146],
    35: [6, 30, 54, 78, 102, 126, 150],
    36: [6, 24, 50, 76, 102, 128, 154],
    37: [6, 28, 54, 80, 106, 132, 158],
    38: [6, 32, 58, 84, 110, 136, 162],
    39: [6, 26, 54, 82, 110, 138, 166],
    40: [6, 30, 58, 86, 114, 142, 170],
}
VERSION = 0


def generate_base(version):
    global VERSION
    global SIZE
    SIZE = ((version-1)*4)+21
    VERSION = version

    qr_code = np.zeros((SIZE,SIZE))
    reserved_areas = np.zeros((SIZE,SIZE))

    (qr_code, reserved_areas) = add_finder_patterns(qr_code,reserved_areas)

    (qr_code, reserved_areas) = add_alignment_patterns(qr_code,reserved_areas)

    (qr_code, reserved_areas) = add_timing_patterns(qr_code, reserved_areas)

    return (qr_code,reserved_areas)


def add_finder_patterns(qr_code, reserved_areas):
    global SIZE
    (qr_code,reserved_areas) = place_finder_pattern(qr_code, reserved_areas, 0, 0)
    (qr_code,reserved_areas) = place_finder_pattern(qr_code, reserved_areas, SIZE-7, 0)
    (qr_code,reserved_areas) = place_finder_pattern(qr_code, reserved_areas, 0, SIZE-7)
    return (qr_code, reserved_areas)

def place_finder_pattern(qr_code, reserved_areas, x, y):
    for i in range(8):
        for j in range(8):
            if(x == 0 and y == 0): reserved_areas[x+i,y+j] = 1
            elif(x == 0): reserved_areas[x+i,y-1+j] = 1
            elif(y == 0): reserved_areas[x-1+i,y+j] = 1

    for i in range(7):
        qr_code[x+i,y] = 1
        qr_code[x+i,y+6] = 1
        qr_code[x,y+i] = 1
        qr_code[x+6,y+i] = 1

    for i in range(3):
        for j in range(3):
            qr_code[x+i+2,y+j+2] = 1

    return (qr_code, reserved_areas)

def add_alignment_patterns(qr_code, reserved_areas):
    global SIZE
    locations = ALIGNMENT_LOCATIONS[VERSION]
    if(len(locations) == 0): return (qr_code,reserved_areas)

    for x in locations:
        for y in locations:
            (qr_code,reserved_areas) = place_alignment_pattern(qr_code, reserved_areas, x, y)

    return (qr_code,reserved_areas)

def place_alignment_pattern(qr_code, reserved_areas, x, y):
    if reserved_areas[x,y] == 1: return (qr_code, reserved_areas)

    qr_code[x,y] = 1
    for i in range(5):
        qr_code[x-2+i,y-2] = 1
        qr_code[x-2+i,y+2] = 1
        qr_code[x-2,y-2+i] = 1
        qr_code[x+2,y-2+i] = 1
        for j in range(5):
            reserved_areas[x-2+i,y-2+j] = 1

    return (qr_code, reserved_areas)

def add_timing_patterns(qr_code, reserved_areas):
    for i in range(SIZE):
        if reserved_areas[6,i] != 1:
            qr_code[6,i] = (i%2)+1
        reserved_areas[6,i] = 1

        if reserved_areas[i,6] != 1:
            qr_code[i,6] = (i%2)+1
        reserved_areas[i,6] = 1
    return (qr_code, reserved_areas)