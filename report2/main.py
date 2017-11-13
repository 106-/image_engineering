#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import math
import copy

sys.path.append("../")
from gray_scale import gray_scale

# ガンマ補正用の関数
def gamma_correction(pixel, gamma):
    if gamma == 0:
        return pixel
    return 255.0 * math.pow((pixel / 255.0), (1.0 / gamma))

# size x sizeかつ値が1/(size^2)な二次元リストを作る
def average_filter(size):
    return [[1.0/size**2 for x in range(size)] for x in range(size)]

def main():
    origin_img = gray_scale.load_from_raw(256, 256, "../poppo.raw")

    gamma = copy.deepcopy(origin_img) 
    gamma.tone_curve(gamma_correction, gamma=0.7 )
    gamma.save_as_pgm("./gamma.pgm")

    emboss = copy.deepcopy(origin_img)
    emboss.emboss(delta=3)
    emboss.save_as_pgm("./emboss.pgm")

    filter_3x3 = average_filter(3)
    avg_3x3 = copy.deepcopy(origin_img)
    avg_3x3.filter(filter_3x3)
    avg_3x3.save_as_pgm("./avg_3x3.pgm")

    filter_5x5 = average_filter(5)
    avg_5x5 = copy.deepcopy(origin_img)
    avg_5x5.filter(filter_5x5)
    avg_5x5.save_as_pgm("./avg_5x5.pgm")

if __name__ == '__main__':
    main()