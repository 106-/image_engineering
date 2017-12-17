# -*- coding:utf-8 -*-

from gray_scale import gray_scale
import math

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
        orig_x = orig_coord[0]
        orig_y = orig_coord[1]
        x = int(trans_coord[0])
        y = int(trans_coord[1])

        # 四方の座標
        ul = [int(math.floor(orig_y)), int(math.floor(orig_x))] # 左上
        ur = [int(math.floor(orig_y)), int(math.ceil(orig_x))]  # 右上
        dl = [int(math.ceil(orig_y)), int(math.floor(orig_x))]  # 左下
        dr = [int(math.ceil(orig_y)), int(math.ceil(orig_x))]   # 右下
        if res_img.isin(ul) and res_img.isin(ur) and res_img.isin(dl) and res_img.isin(dr):
            # ((2つの画素の差)*(座標の小数点以下成分))+(引いたほうの画素)
            upper_color = (origin_image[ur[0]][ur[1]]-origin_image[ul[0]][ul[1]])*(orig_x-math.floor(orig_x))+origin_image[ul[0]][ul[1]]
            downer_color = (origin_image[dr[0]][dr[1]]-origin_image[dl[0]][dl[1]])*(orig_x-math.floor(orig_x))+origin_image[dl[0]][dl[1]]
            color = (downer_color-upper_color)*(orig_y-math.floor(orig_y))+upper_color
            res_img[y][x] = color
    return res_img