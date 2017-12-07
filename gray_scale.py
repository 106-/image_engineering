# -*- coding:utf-8 -*-

import struct
from itertools import chain
import math
import copy

class gray_scale:
    def __init__(self):
      self.height = 0
      self.width = 0
      self.pixel = []
    
    # gray_scale同士の足し算を定義
    def __add__(self, other, **args):
        def func(img, x, y, add_img):
            return img.pixel[y][x] + add_img.pixel[y][x]
        # gray_scale + gray_scale
        if isinstance(other, gray_scale):
            if self.height != other.height or self.width != other.width:
                raise ValueError("Images must be same size.")
            self.map(func, add_img=other, **args)
            return self
        else:
            raise ValueError("Canno3x3t add gray_scale with %s" % type(other))
    
    def __iadd__(self, other, **args):
        return self.__add__(other, **args)        

    # 画像の2重リストを一つのリストにまとめる
    def _flatted(self):
        return list(chain.from_iterable(self.pixel))

    # 画像の情報を一括表示
    def stat(self):
        #print("合計: {}".format(self.sum()))
        print("最大値: {}".format(self.max()))
        print("最小値: {}".format(self.min()))
        print("平均値: {}".format(self.average()))
        print("分散: {}".format(self.variance()))
        print("標準偏差: {}".format(self.deviation()))
        print("中央値: {}".format(self.median()))
        print("最頻値: {}".format( ', '.join(map(lambda x:str(x), self.mode())) ))

    # 合計
    def sum(self):
        sum = 0
        for i in self._flatted():
            sum += i
        return sum

    # 最大値
    def max(self):
        max = 0
        for i in self._flatted():
            if i > max:
                max = i
        return max

    # 最小値
    def min(self):
        min = 255
        for i in self._flatted():
            if i < min:
                min = i
        return min

    # 平均値
    def average(self):
        return float(self.sum()) / float(self.height * self.width)

    # 分散
    def variance(self):
        ave = self.average()
        sum = 0
        for i in self._flatted():
            sum += (i - ave) ** 2
        return float(sum) / float(self.height * self.width)

    # 標準偏差
    def deviation(self):
        return math.sqrt(self.variance())

    # 中央値
    def median(self):
        lst = self._flatted()
        lst.sort()
        if len(lst)%2==0:
            center = len(lst)/2
            return (lst[center] + lst[center-1]) /2
        else:
            return lst[(len(lst)+1)/2]

    # 最瀕値
    def mode(self):
        histogram = [0 for x in range(256)]
        for i in self._flatted():
            histogram[i] += 1
        
        modes = []
        max_value = max(histogram)
        for i,value in enumerate(histogram):
            if value == max_value:
                modes.append(i)
        return modes

    # 全てのピクセルにfuncの返り値を入れる.
    # funcはgray_scale, x, y, 可変長引数を引数にとる.
    def map(self, func, adjust=True, **args):
        c = copy.deepcopy(self)
        for i,y in enumerate(self.pixel):
            for n,x in enumerate(y):
                self.pixel[i][n] = int(func(c, n, i, **args))
                if adjust:
                    self.pixel[i][n] = self._pixel_adjust(int(func(c, n, i, **args)))

    # トーンカーブを適用する.
    def tone_curve(self, curve, **args):
        self.map(lambda img, x, y: curve(img.pixel[y][x], **args))

    # エンボス処理
    def emboss(self, delta):
        # 画素をdeltaの分だけ右下へ移動するための関数
        def func(img, x, y, delta):
            if y-delta < 0 or x-delta < 0:
                return 127
            else:
                return img.pixel[y-delta][x-delta]
        c = copy.deepcopy(self)
        c.tone_curve(lambda x: 255-x)
        c.map(func, delta=delta)
        self.__add__(c, adjust=False)
        self.tone_curve(lambda x: x-128)

    # Prewittフィルタ
    def prewitt(self, threshold):
        # ２つの画像の2乗,加算,平方根した値を返す
        def func(img, x, y, vert, hori, threshold):
            value = math.sqrt(vert.pixel[y][x]**2+hori.pixel[y][x]**2)
            if value > threshold:
                return 255
            return 0

        filter_vert = [
            [ 1,  1,  1],
            [ 0,  0,  0],
            [-1, -1, -1]
        ]
        filter_hori = [
            [-1,  0,  1],
            [-1,  0,  1],
            [-1,  0,  1]
        ]
        vert = copy.deepcopy(self)
        hori = copy.deepcopy(self)
        vert.filter(filter_vert, adjust=False)
        hori.filter(filter_hori, adjust=False)
        self.map(func, vert=vert, hori=hori, threshold=threshold)

    # フィルタの適用 
    def filter(self, filter_matrix, adjust=True, frame=0):
        def func(img, x, y, filter_matrix):
            size = len(filter_matrix)/2
            # 範囲外の場合
            if y-size < 0 or x-size < 0 or img.height-1 < y+size or img.width-1 < x+size:
                return frame
            # 範囲内なら
            else:
                sum = 0
                for row, dy in zip(filter_matrix, range(-size, size+1)):
                    for value, dx in zip(row, range(-size, size+1)):
                        sum += img.pixel[y+dy][x+dx] * value
                return sum
        self.map(func, filter_matrix=filter_matrix, adjust=adjust)

    # raw形式で出力
    def save_as_raw(self, filename):
        with open(filename, 'wb+') as f:
            for y in self.pixel:
                for x in y:
                    f.write(struct.pack('B', x))

    # pgm形式で出力
    def save_as_pgm(self, filename):
        with open(filename, 'wb+') as f:
            f.write(b'P5\n')
            f.write('{} {}\n'.format(self.width, self.height).encode('ascii'))
            f.write(b'255\n')
            for y in self.pixel:
                for x in y:
                    f.write(struct.pack('B', x))

    # rawファイルからimageオブジェクトを生成する
    @classmethod
    def load_from_raw(cls, width, height, filename):
        img = gray_scale()
        img.height = height
        img.width = width
        with open(filename, 'rb') as f:
            for y in range(img.height):
                line = []
                for x in range(img.width):
                    # バイナリデータを0-255の数値に変換する
                    val = struct.unpack('B', f.read(1))[0]
                    line.append(val)
                img.pixel.append(line)
        return img
    
    # ピクセルを0-255の範囲に収める
    def _pixel_adjust(cls,pixel):
        if pixel < 0:
            return 0
        elif 255 < pixel:
            return 255
        else:
            return pixel