# -*- coding:utf-8 -*-

from gray_scale import gray_scale
import math

def nearest_neighbor(origin_image, origin_coords, trans_coords, default_color=255):
    res_img = gray_scale(height=origin_image.height, width=origin_image.width, default_color=default_color)
    for orig_coord, trans_coord in zip(origin_coords.values, trans_coords.values):
        orig_x = int(orig_coord[0])
        orig_y = int(orig_coord[1])
        x = int(math.floor(trans_coord[0]+0.5))
        y = int(math.floor(trans_coord[1]+0.5))
        if (0 <= orig_y < origin_image.height and 0 <= orig_x < origin_image.width
            and 0 <= y < origin_image.height and 0 <= x < origin_image.width):
            res_img[y][x] = origin_image[orig_y][orig_x]
    return res_img 
