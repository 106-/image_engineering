#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import math
import copy

sys.path.append("../")
from gray_scale import gray_scale
import interpolation

def main():
    origin_img = gray_scale.load_from_raw(256, 256, "../poppo.raw")

    # Prewittフィルタの適用
    prewitt = copy.deepcopy(origin_img)
    prewitt.prewitt(25)
    prewitt.save_as_pgm("./prewitt.pgm")

    # 回転
    rotate_nn = copy.deepcopy(origin_img)
    rotate_nn.rotate(math.radians(30), interpolation.nearest_neighbor)
    rotate_nn.save_as_pgm("./rotate_30_nn.pgm")
    rotate_bl = copy.deepcopy(origin_img)
    rotate_bl.rotate(math.radians(30), interpolation.bilinear)
    rotate_bl.save_as_pgm("./rotate_30_bl.pgm")

if __name__=='__main__':
    main()