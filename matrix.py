# -*- coding:utf-8 -*-

import copy

class matrix:
    
    def __init__(self, values):
        self.height = len(values)
        self.width = len(values[0])
        self.is_square = self.height == self.width
        self.values = values

    # 掛け算の定義 
    def __mul__(self, m):
        if self.width != m.height:
            print(self.width)
            print(m.height)
            raise ValueError("columb and row must have same size.")
        
        res = [[None for x in range(m.width)] for y in range(self.height)]

        for i in range(m.width):
            for j in range(self.height):
                sum = 0
                for n in range(self.width):
                    sum += self[j][n] * m[n][i]
                res[j][i] = sum
        return matrix(res)

    # 行列式
    def determinant(self):
        if not self.is_square:
            raise ValueError("square matrix only have determinant.")
        c = copy.deepcopy(self)
        for row in range(self.height-1):
            for y in range(row+1, self.height):
                if c[y][row] == 0:
                    continue
                a = float(c[y][row])/float(c[row][row])
                for x in range(row, self.width):
                    c[y][x] -= c[row][x] * a
        det = 1
        for row in range(self.height):
            det *= c[row][row]
        return det

    # 逆行列
    def inverse(self):
        if not self.is_square:
            raise ValueError("square matrix only have inverse matrix.")
        # 単位行列を代入しておく
        inverse = [[1.0 if x==y else 0.0 for y in range(self.height)] for x in range(self.width)]
        
        # 元データから隔離するためコピーを作ってそっちをいじる
        c = copy.deepcopy(self)

        for row in range(self.height):
            # 対角部分の成分の逆数を求める 
            recip = 1.0/c[row][row]
            
            # 対角部分の成分を1にするための計算
            for x in range(self.width):
                c[row][x] *= recip
                inverse[row][x] *= recip
            
            # 1にした行を他の行にかけて引く
            for y in range(self.height):
                if row == y:
                    continue
                # aは上で1にした列の成分と同じ列にある成分
                a = c[y][row]
                for x in range(self.width):
                    c[y][x] -= c[row][x] * a
                    inverse[y][x] -= inverse[row][x] * a
        return matrix(inverse)

    # 転置行列
    def transpose(self):
        m = matrix([[None for x in range(self.height)] for y in range(self.width)])
        for y in range(self.width):
            for x in range(self.height):
                m[y][x] = self[x][y]
        return m

    def __getitem__(self, key):
        return self.values[key]
