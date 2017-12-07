#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import math
import copy

sys.path.append("../")
from gray_scale import gray_scale

def main():
    origin_img = gray_scale.load_from_raw(256, 256, "../poppo.raw")

    # Prewittフィルタの適用
    prewitt = copy.deepcopy(origin_img)
    prewitt.prewitt(25)
    prewitt.save_as_pgm("./prewitt.pgm")

if __name__=='__main__':
    main()