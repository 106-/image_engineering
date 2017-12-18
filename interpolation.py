# -*- coding:utf-8 -*-

from gray_scale import gray_scale
import math
from math import floor, ceil
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
            res_img[y][x] = int(m.values[0][0])
    return res_img

def bicubic(origin_image, origin_coords, trans_coords, default_color=255):
    res_img = gray_scale(height=origin_image.height, width=origin_image.width, default_color=default_color)
    for orig_coord, trans_coord in zip(origin_coords.values, trans_coords.values):
        x = int(trans_coord[0])
        y = int(trans_coord[1])
        orig_x = orig_coord[0]
        orig_y = orig_coord[1]

        # sinc関数を3次関数で近似したもの
        def h(t):
            abs_t = abs(t)
            if abs(t) <= 1:
                return (abs_t**3 - 2*abs_t**2 + 1)
            elif 1 < abs(t) <= 2:
                return (-abs_t**3 + 5*abs_t**2 - 8*abs_t + 4)
            else:
                return 0

        # 周りの座標との差をh(t)にかけて返す  
        def get_around_coord(orig):
            f = floor(orig)
            m = matrix([
                map(h, [1+orig-f, orig-f, f+1-orig, f+2-orig])
            ])
            return m
        mx = get_around_coord(orig_x)
        my = get_around_coord(orig_y).transpose()

        # 周りの画素値を求める
        def get_around_pixels(cx, cy):
            xf = int(floor(cx))
            yf = int(floor(cy))
            # 相対的な座標をつくる
            pixels = [[xf+rx,yf+ry] for rx in range(-1, 3) for ry in range(-1, 3)]
            # 座標がはみ出してないかの確認
            out_range = map(lambda n: res_img.isin(n), pixels)
            if False in out_range:
                return None
            # 画素値を代入する
            pixels = map(lambda n: origin_image[n[1]][n[0]], pixels)
            # 4つずつのタプルにする
            pixels = zip(*[iter(pixels)]*4)
            # タプルをリストにする
            pixels = map(lambda n: list(n), pixels)
            return matrix(pixels)
        mp = get_around_pixels(orig_x, orig_y)
        if mp is None:
            continue
        m = mx*mp*my
        res_img[y][x] = gray_scale.pixel_adjust(int(m.values[0][0]))
    return res_img