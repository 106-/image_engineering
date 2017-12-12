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
    rotate = copy.deepcopy(origin_img)
    rotate.rotate(math.radians(30), interpolation.nearest_neighbor)
    rotate.save_as_pgm("./rotate_30_nn.pgm")

if __name__=='__main__':
    main()