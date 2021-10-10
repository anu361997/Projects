#! /usr/bin/python
import matplotlib.pyplot as plt
import fileinput
import functools
import os.path
from os import path
import random as r
import time
import statistics
grid = []
b = 0
alpha = 100
file = "DataSetB.txt"
bucket_access = 0
x_arr, y_arr = [], []
class Mapper:
    def __init__(self, x1, x2, y1, y2, count, bucket):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.count = count
        self.bucket = bucket
    def update(self, x1, x2, y1, y2, count, bucket):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.count = count
        self.bucket = bucket
    def print_info(self):
        print(str(self.x1) + "<= x < " + str(self.x2) + " , " + str(self.y1) + " <= y < " + str(self.y2) + ", bucket = " + self.bucket.filename)

class Bucket:
    def __init__(self, filename,count):
        self.filename = filename
        self.count = count
    def addpoint(self, point):
        self.count+=1
        self.point = point
        f = open(self.filename, "a+")
        output = "%s %s %s" %(point[0], point[1], point[2])
        f.write(output+"\n")
        f.close()
    def update(self, points):
        self.points = points
        self.count = len(points)
        f = open(self.filename, 'w+')
        for d in points:
            output = "%s %s %s" %(d[0], d[1], d[2])
            f.write(output+"\n")
        f.close()

def main_func():
    data = []
    result = []
    k = [5, 20, 50, 100]
    generate_mapper()
    for line in fileinput.FileInput("TestData.txt"):
        info = line.split()
        data.append((int(info[0]) , int(info[1]) ))
    for qk in k:
        sum_ = 0
        for d in data:
            sum_ = sum_ + knn(d[0], d[1], qk)
        result.append(sum_/10)
    f = open("PlotData.txt", "w+")
    output="%s %s %s %s" %(result[0], result[1], result[2], result[3])
    f.write(output + "\n")
    f.close()
 
    
def split_bucket(m):
    global b
    data = []
    datam = []
    datan = []
    for line in fileinput.FileInput(m.bucket.filename):
        info = line.split()
        data.append((int(info[0]) , int(info[1]) , int(info[2]) ))
    for g in grid:
        if g.bucket == m.bucket:
            n = g
            break
    for d in data:
        if n.x1 <= d[1] <= n.x2 and n.y1 <= d[2] <= n.y2:
            datan.append(d)
        else: datam.append(d)
    b+=1
    n.bucket = Bucket(str(b) + ".txt", 0)    
    m.bucket.update(datam)
    n.bucket.update(datan)
    n.count = n.bucket.count
           
def generate_mapper():
    global grid, b, x_arr, y_arr
    points = []
    axis = 'y'
    c = 0
    x_arr.append(0)
    y_arr.append(0)
    for line in fileinput.FileInput(file):
        info = line.split()
        points.append((int(info[0]) , int(info[1]) , int(info[2]) ))
    bucket = Bucket(str(b) + ".txt", 0)
    grid.append(Mapper(0, 400, 0, 400, 0, bucket))
    for p in points:
        for g in range(len(grid)):
            if grid[g].x1 <= p[1] < grid[g].x2 and grid[g].y1 <= p[2] < grid[g].y2:
                c+=1
                if grid[g].bucket.count <= alpha:
                    grid[g].bucket.addpoint(p)
                    grid[g].count+=1
                else:
                    grid[g].bucket.addpoint(p)
                    grid[g].count+=1
                    if grid[g].count < grid[g].bucket.count:
                        #print("split : ")
                        #grid[g].print_info()
                        split_bucket(grid[g])
                    else:
                        new_m = []
                        data = []
                        for line in fileinput.FileInput(grid[g].bucket.filename):
                            info = line.split()
                            data.append((int(info[0]) , int(info[1]) , int(info[2]) ))
                        if axis == 'y':
                            ny = int(statistics.median(row[2] for row in data))
                            print("y = " + str(ny))
                            y_arr.append(ny)
                            prev = grid[g]
                            #print(" map split : ")
                            #grid[g].print_info()
                            b+=1
                            new_b = Bucket(str(b) + ".txt", 0)
                            data.sort(key = lambda x: x[2])
                            for i in range(len(data)):
                                if data[i][2] >= ny:
                                    index = i
                                    break
                            prev.bucket.update(data[0:i])
                            new_b.update(data[i: ])
                            new_m.append(Mapper(prev.x1, prev.x2, ny, prev.y2, new_b.count, new_b))
                            grid[g].update(prev.x1, prev.x2, prev.y1, ny, prev.bucket.count, prev.bucket)
                            for z in grid:
                                if z.y1 < ny < z.y2:
                                    c1, c2 = 0, 0
                                    curr = z
                                    for line in fileinput.FileInput(z.bucket.filename):
                                        info = line.split()
                                        if int(info[2]) < nx: c1+=1
                                        else: c2+=1
                                    new_m.append(Mapper(curr.x1, curr.x2, ny, curr.y2, c2, curr.bucket))
                                    z.update(curr.x1, curr.x2, curr.y1, ny, c1, curr.bucket)
                                        
                            axis = 'x'
                            grid.extend(new_m)
                            break
                        else:
                            nx = int(statistics.median(row[1] for row in data))
                            print("x = " + str(nx))
                            x_arr.append(nx)
                            prev = grid[g]
                            #print(" map split : ")
                            #grid[g].print_info()
                        
                            b+=1
                            new_b = Bucket(str(b) + ".txt", 0)
                            data.sort(key = lambda x: x[1])
                            for i in range(len(data)):
                                if data[i][1] >= nx:
                                    index = i
                                    break
                            prev.bucket.update(data[0:i])
                            new_b.update(data[i: ])
                            new_m.append(Mapper(nx, prev.x2, prev.y1, prev.y2, new_b.count, new_b))
                            grid[g].update(prev.x1, nx, prev.y1, prev.y2, prev.bucket.count, prev.bucket)
                            for z in grid:
                                if z.x1 < nx < z.x2:
                                    c1, c2 = 0, 0
                                    curr = z
                                    for line in fileinput.FileInput(z.bucket.filename):
                                        info = line.split()
                                        if int(info[1]) < nx: c1+=1
                                        else: c2+=1
                                    new_m.append(Mapper(nx, curr.x2, curr.y1, curr.y2, c2, curr.bucket))
                                    z.update(curr.x1, nx, curr.y1, curr.y2, c1, curr.bucket)
                            axis = 'y'
                            grid.extend(new_m)
                            break
    print("**********")
    for g in grid:
        g.print_info()
    #print("c = " + str(c))
    x_arr.append(400)
    y_arr.append(400)
    
def knn(qpointx, qpointy, qk):
    global x_arr, y_arr, grid, bucket_access
    bucket_access = 0
    #qpointx = int(input("Enter x(abscissa) : "))
    #qpointy = int(input("Enter y(ordinate) : "))
    #qk = int(input("Enter k value : "))
    data = []
    rad_grid = []
    for g in grid:
        if (g.x1 <= qpointx <= g.x2) and (g.y1 <= qpointy <= g.y2):
            z = g
            rad_grid.append(z)
            break
    for line in fileinput.FileInput(z.bucket.filename):
        info = line.split()
        dist2 = ((int(info[1]) - qpointx) ** 2) + ((int(info[1]) - qpointy) ** 2)
        data.append((int(info[0]) , int(info[1]) , int(info[2]), dist2 ))
    bucket_access+=1
    if z.bucket.count < qk:
        goto_neighbors(z.x1, z.x2, z.y1, z.y2, data, rad_grid, qpointx, qpointy, qk)
    else:
        data.sort(key = lambda x: x[3])
        radius = data[qk-1][3]
        radialcheck(radius, qpointx, qpointy, qk, rad_grid, data[0:qk])
    return bucket_access
    

def goto_neighbors(a, b, c, d, data, rad_grid, qpointx, qpointy, qk):
    global x_arr, y_arr, grid, bucket_access
    buckets = []
    for i in x_arr:
        if a == 0:
            p = x_arr[1]
            break
        else:
            if i < a:
                p = i
            else: break
    for i in x_arr:
        if b == 400:
            q = x_arr[-2]
            break
        else:
            if i > b:
                q = i
                break
    for i in y_arr:
        if c == 0:
            r = y_arr[1]
            break
        else:
            if i < c: r = i
            else: break
    for i in y_arr:
        if d == 400:
            s = y_arr[-2]
            break
        else:
            if i > d:
                s = i
                break
    for g in grid:
        if (g.x1 == p and g.x2 == a) or (g.x1 == b and g.x2 == q) or (g.y1 == r and g.y2 == c) or (g.y1 == d and g.y2 == s):
            rad_grid.append(g)
            for line in fileinput.FileInput(g.bucket.filename):
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
                buckets.append(g.bucket)
                continue
            dist2 = ((g.x1 - qpointx) ** 2) + ((g.y2 - qpointy) ** 2)
            if dist2 <= radius:
                buckets.append(g.bucket)
                continue
            dist2 = ((g.x2 - qpointx) ** 2) + ((g.y1 - qpointy) ** 2)
            if dist2 <= radius:
                buckets.append(g.bucket)
                continue
            dist2 = ((g.x2 - qpointx) ** 2) + ((g.y2 - qpointy) ** 2)
            if dist2 <= radius:
                buckets.append(g.bucket)
                continue
    bucket_access = bucket_access + len(buckets)
    for b in buckets:
        for line in fileinput.FileInput(b.filename):
                info = line.split()
                dist2 = ((int(info[1]) - qpointx) ** 2) + ((int(info[1]) - qpointy) ** 2)
                if dist2 <= radius:
                    data.append((int(info[0]) , int(info[1]) , int(info[2]), dist2 ))
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
