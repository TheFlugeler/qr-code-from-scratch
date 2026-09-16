import numpy as np
import copy


def zero(row,col): return ((row+col)%2 == 0)
def one(row,col): return (row%2 == 0)
def two(row,col): return (col%3 == 0)
def three(row,col): return ((row+col)%3 == 0)
def four(row,col): return(((row//2) + (col//3))%2 == 0)
def five(row,col): return(((row*col)%2)+((row*col)%3) == 0)
def six(row,col): return((((row*col)%2)+((row*col)%3))%2 == 0)
def seven(row,col): return((((row+col)%2)+((row*col)%3))%2 == 0)

MASK_CONDITIONS = [zero,one,two,three,four,five,six,seven]

def mask_code(qr_code,reserved):
    global MASK_CONDITIONS
    size = qr_code.shape[0]
    scores = [0]*8
    masked_codes = []
    for i in range(8):
        mask = copy.deepcopy(qr_code)
        for row in range(size):
            for col in range(size):
                if(reserved[row,col] != 1):
                    if MASK_CONDITIONS[i](row,col):
                        if mask[row,col] == 1: mask[row,col] = 0
                        elif mask[row,col] == 0: mask[row,col] = 1
        masked_codes.append(mask)
        scores[i] = score_mask(mask)

    smallest = 0
    for i in range(8):
        if scores[i] < scores[smallest]:
            smallest = i

    return (masked_codes[smallest],smallest)


def score_mask(mask):
    score = 0
    score += score_condition_1(mask)
    score += score_condition_2(mask)
    score += score_condition_3(mask)
    score += score_condition_4(mask)
    return score


def score_condition_1(mask):
    size = mask.shape[0]
    score = 0
    counter = 0
    bit = 1
    for i in range(size):
        for j in range(size):
            if mask[i,j] == bit:
                counter += 1
                if  counter == 5: score += 3
                elif counter > 5: score += 1
            else:
                counter = 1
                bit = mask[i,j]
        counter = 0
    for i in range(size):
        for j in range(size):
            if mask[j,i] == bit:
                counter += 1
                if  counter == 5: score += 3
                elif counter > 5: score += 1
            else:
                counter = 1
                bit = mask[j,i]
        counter = 0
    #print(f"Condition 1: {score}")
    return score

def score_condition_2(mask):
    size = mask.shape[0]
    score = 0
    for i in range(size-1):
        for j in range(size-1):
            bit = mask[i,j]
            if mask[i,j+1] == bit and mask[i+1,j] == bit and mask[i+1,j+1] == bit:
                score += 3
    #print(f"Condition 2: {score}")
    return score

def score_condition_3(mask):
    score = 0
    size = mask.shape[0]
    patterns = [[1,0,1,1,1,0,1,0,0,0,0],[0,0,0,0,1,0,1,1,1,0,1]]
    for i in range(size):
        for j in range(size-11):
            if np.array_equal(mask[i,j:j+11],patterns[0]) or np.array_equal(mask[i,j:j+11],patterns[1]):
                score += 40

    for i in range(size):
        for j in range(size-11):
            if np.array_equal(mask[j:j+11,i],patterns[0]) or np.array_equal(mask[j:j+11,i],patterns[1]):
                score += 40

    #print(f"Condition 3: {score}")
    return score

def score_condition_4(mask):
    size = mask.shape[0]
    dark = 0
    total = size*size
    for i in range(size):
        for j in range(size):
            if mask[i,j] == 1: dark += 1
    percentage = (dark/total)*100
    bounds = [percentage-percentage%5,percentage-percentage%5+5]
    for i in range(2):
        bounds[i] = abs(bounds[i]-50)/5
    smaller = bounds[0]
    if bounds[0] > bounds[1]: smaller = bounds[1]

    score = smaller*10
    #print(f"Condition 4: {score}")
    return score


    