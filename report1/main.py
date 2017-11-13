#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

sys.path.append("../")
from gray_scale import gray_scale

def main():
    img = gray_scale.load_from_raw_image(256, 256, '../poppo.raw')
    img.stat()
    img.save_as_pgm('./poppo.pgm')

if __name__=='__main__':
    main()