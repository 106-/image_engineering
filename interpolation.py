# -*- coding:utf-8 -*-

from gray_scale import gray_scale
import math
from matrix import matrix

def nearest_neighbor(origin_image, origin_coords, trans_coords, default_color=255):
    res_img = gray_scale(height=origin_image.height, width=origin_image.width, default_color=default_color)
    for orig_coord, trans_coord in zip(origin_coords.values, trans_coords.values):
        orig_x = int(math.floor(orig_coord[0]+0.5))
        orig_y = int(math.floor(orig_coord[1]+0.5))
        x = int(trans_coord[0])
        y = int(trans_coord[1])
        if res_img.isin([orig_x,orig_y]):
            res_img[y][x] = origin_image[orig_y][orig_x]
    return res_img 

def bilinear(origin_image, origin_coords, trans_coords, default_color=255):
    res_img = gray_scale(height=origin_image.height, width=origin_image.width, default_color=default_color)
    for orig_coord, trans_coord in zip(origin_coords.values, trans_coords.values):
        x = int(trans_coord[0])
        y = int(trans_coord[1])

        orig_x = orig_coord[0]
        orig_y = orig_coord[1]
        xf = int(math.floor(orig_x))
        yf = int(math.floor(orig_y))
        xc = xf+1 
        yc = yf+1
        if res_img.isin([yf,xf]) and res_img.isin([yf,xc]) and res_img.isin([yc,xf]) and res_img.isin([yc,xc]):
            ma = matrix([
                [xc-orig_x, orig_x-xf]
            ])
            mb = matrix([
                [origin_image[yf][xf], origin_image[yf][xc]],
                [origin_image[yc][xf], origin_image[yc][xc]],
            ])
            mc = matrix([
                [yc-orig_y, orig_y-yf]
            ]).transpose()
            m = ma*mb*mc
            color = m.values[0][0] if 0 <= m.values[0][0] < 256 else default_color
            res_img[y][x] = color 
    return res_img