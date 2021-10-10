#! /usr/bin/python
import fileinput
import functools
import os.path
from os import path
import random as r
import time
grid = []
alpha = 100
size = None
bucket_access = 0
file = "DataSetB.txt"
class Mapper:
    def __init__(self, x1, x2, y1, y2, bucket):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.bucket = bucket
    def print_info(self):
        print(str(self.x1) + "<= x < " + str(self.x2) + " , " + str(self.y1) + " <= y < " + str(self.y2))
        for b in self.bucket:
            print(str(b.filename))
    

class Bucket:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        f = open(filename, 'a+')
        for d in data:
            output = "%s %s %s" %(d[0], d[1], d[2])
            f.write(output+"\n")
                
def main_func():
    global grid, bucket_access
    data = []
    result = []
    k = [5, 20, 50, 100]
    generate_mapper()
    generate_buckets()
    print("*****Mapper Info*****")
    for g in grid:
        g.print_info()
    for line in fileinput.FileInput("TestData.txt"):
        info = line.split()
        data.append((int(info[0]) , int(info[1]) ))
    for qk in k:
        sum_ = 0
        for d in data:
            sum_ = sum_ + knn(d[0], d[1], qk)
        result.append(sum_/10)
    f = open("PlotData.txt", "a+")
    output="%s %s %s %s" %(result[0], result[1], result[2], result[3])
    f.write(output + "\n")
    f.close()
            
def generate_mapper():
    global grid, size
    size = int(input("Enter size of the cell : "))
    n = int(400/size)
    #b = []
    for i in range(n):
        x1 = i*size
        x2 = (i+1)*size
        for j in range(n):
            y1 = j*size
            y2 = (j+1)*size
            grid.append(Mapper(x1, x2, y1, y2, []))
    #generate_buckets()

def generate_buckets():
    global grid, alpha
    points = []
    countb = 0
    b = [[] for _ in range(len(grid))]
    for line in fileinput.FileInput(file):
        info = line.split()
        points.append((int(info[0]) , int(info[1]) , int(info[2]) ))
    for p in points:
        for g in range(len(grid)):
            if grid[g].x1 <= p[1] < grid[g].x2 and grid[g].y1 <= p[2] < grid[g].y2:
                if len(b[g]) < alpha:
                    b[g].append(p)
                    break
                else:
                    if grid[g].bucket is [None]:
                        grid[g].bucket = b[g]
                    else: grid[g].bucket.append(Bucket(str(countb) + '.txt', b[g]))
                    countb+=1
                    b[g].clear()
                    b[g].append(p)
                    break
                    

    for x in range(len(b)):
        grid[x].bucket.append(Bucket(str(countb) + '.txt', b[x]))
        countb+=1

def knn(qpointx, qpointy, qk):
    global grid, bucket_access
    #qpointx = int(input("Enter x(abscissa) : "))
    #qpointy = int(input("Enter y(ordinate) : "))
    #qk = int(input("Enter k value : "))
    data = []
    rad_grid = []
    bucket_access = 0
    for g in grid:
        if (g.x1 <= qpointx <= g.x2) and (g.y1 <= qpointy <= g.y2):
            z = g
            rad_grid.append(z)
            break
    for b in z.bucket:
        for line in fileinput.FileInput(b.filename):
            info = line.split()
            dist2 = ((int(info[1]) - qpointx) ** 2) + ((int(info[1]) - qpointy) ** 2)
            data.append((int(info[0]) , int(info[1]) , int(info[2]), dist2 ))
        bucket_access+=1
    if len(data) < qk:
        goto_neighbors(z.x1, z.x2, z.y1, z.y2, data, rad_grid, qpointx, qpointy, qk)
    else:
        data.sort(key = lambda x: x[3])
        radius = data[qk-1][3]
        radialcheck(radius, qpointx, qpointy, qk, rad_grid, data[0:qk])
    return bucket_access
    

def goto_neighbors(a, b, c, d, data, rad_grid, qpointx, qpointy, qk):
    global grid, size, bucket_access
    buckets = []
    if (a-size) < 0: p = 0
    else: p = a-size
    if (b+size) > 400: q = 400
    else: q = b + size
    if (c-size) < 0: r = 0
    else: r = c-size
    if (d+size) > 400: s = 400
    else: s = d + size
    for g in grid:
        if (g.x1 == p and g.x2 == a) or (g.x1 == b and g.x2 == q) or (g.y1 == r and g.y2 == c) or (g.y1 == d and g.y2 == s):
            rad_grid.append(g)
            for b in g.bucket:
                for line in fileinput.FileInput(b.filename):
                    info = line.split()
                    dist2 = ((int(info[1]) - qpointx) ** 2) + ((int(info[1]) - qpointy) ** 2)
                    data.append((int(info[0]) , int(info[1]) , int(info[2]), dist2 ))
                bucket_access+=1
    if len(data) < qk:
        goto_neighbors(p, q, r, s, data, rad_grid, qpointx, qpointy, qk)
    else:
        data.sort(key = lambda x: x[3])
        radius = data[qk-1][3] 
        radialcheck(radius, qpointx, qpointy, qk, rad_grid, data[0:qk])

def radialcheck(radius, qpointx, qpointy, qk, rad_grid, data):
    global grid, bucket_access
    buckets = []
    for g in grid:
        if not g in rad_grid:
            dist2 = ((g.x1 - qpointx) ** 2) + ((g.y1 - qpointy) ** 2)
            if dist2 <= radius:
                buckets.extend(g.bucket)
                continue
            dist2 = ((g.x1 - qpointx) ** 2) + ((g.y2 - qpointy) ** 2)
            if dist2 <= radius:
                buckets.extend(g.bucket)
                continue
            dist2 = ((g.x2 - qpointx) ** 2) + ((g.y1 - qpointy) ** 2)
            if dist2 <= radius:
                buckets.extend(g.bucket)
                continue
            dist2 = ((g.x2 - qpointx) ** 2) + ((g.y2 - qpointy) ** 2)
            if dist2 <= radius:
                buckets.extend(g.bucket)
                continue
    for b in buckets:
        for line in fileinput.FileInput(b.filename):
                info = line.split()
                dist2 = ((int(info[1]) - qpointx) ** 2) + ((int(info[1]) - qpointy) ** 2)
                if dist2 <= radius:
                    data.append((int(info[0]) , int(info[1]) , int(info[2]), dist2 ))
        bucket_access+=1
    data = list(set(data))
    data.sort(key = lambda x: x[3])
    """print("K nearest neighbors : ")
    if len(data) > qk:
        points = data[0:qk]
    else:
        points = data
    for k in points:
        print(str(k[0]) + " " + str(k[1]) + " " + str(k[2]))"""


if __name__ == '__main__':
	main_func()

