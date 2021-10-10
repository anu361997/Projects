#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 00:33:30 2021

@author: anamika
"""
import random as r
import fileinput
import statistics
import sys

bucket_size = int(input("Enter the bucket size: "))
grid = []
split_point_x , split_point_y = [], []
b=0

class MapGrid_Bucket:
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
    bucket_name = str(b) + ".txt" 
    bucket = Bucket(bucket_name, 0)
    
    x_min =0
    x_max = 400
    y_min = 0
    y_max = 400
    count = 0
    split_point_x.append(0)
    split_point_y.append(0)
    grid.append(MapGrid_Bucket(x_min, x_max, y_min, y_max, count, bucket)) #xy plane
    Mapper_func(grid, b, split_point_x, split_point_y,bucket_name)
    
def median(data,axis):
    data_axis=[]
    if(axis == 'y'):
        for row in data:
            data_axis.append(row[2])
        med = int(statistics.median(data_axis))
    if(axis == 'x'):
        for row in data:
            data_axis.append(row[1])
        med = int(statistics.median(data_axis))
    return med
    
def sort_data(axis,data):
    if(axis == 'x'):
        data.sort(key=lambda x:x[1])
    else:
        data.sort(key=lambda x:x[2])
    return data
    
         
def split_bucket(data,axis,split_point):
    if (axis == 'x'):
        data_sorted = sort_data('x',data)
        ax =1
        l = len(data_sorted)
        i=0
        while i < l:
            if data_sorted[i][ax] >= split_point:
                index = i
                break
            i=i+1
    else:
        data_sorted = sort_data('y', data)
        ax =2
        l = len(data_sorted)
        i=0
        while i < l:
            if data_sorted[i][ax] >= split_point:
                index = i
                break
            i=i+1
    return index

def increment(split_point,fname,axis):
    count1,count2 = 0,0 
    if(axis == 'x'):
        for line in fileinput.FileInput(fname):
            info = line.split()
            if int(info[1]) >= split_point:
                count2 = count2+1
            else: 
                count1 = count1+1
    else:
        for line in fileinput.FileInput(fname):
            info = line.split()
            if int(info[2]) >= split_point:
                count2 = count2+1
            else: 
                count1 = count1+1
    return count1,count2


def split_grid(split_point,grid,g,b,data,axis):
    new_m = []
    previous_grid = grid[g]
    data_bucket = data
    index = split_bucket(data_bucket,axis,split_point)
    new_b =  Bucket(str(b) + ".txt", 0)
    previous_grid.bucket.update(data[0:index])
    print("Count of bucket 1:",previous_grid.bucket.count)
    new_b.update(data[index: ])
    if(axis == 'y'):
        new_m.append(MapGrid_Bucket(previous_grid.x1, previous_grid.x2, split_point, previous_grid.y2, new_b.count, new_b))
        grid[g].update(previous_grid.x1, previous_grid.x2, previous_grid.y1, split_point, previous_grid.bucket.count, previous_grid.bucket)
        
        for curr_grid in grid:
            print("values:",curr_grid.y2,split_point)
            if curr_grid.y1 < split_point < curr_grid.y2:
                curr = curr_grid
                c1,c2 = increment(split_point,curr_grid.bucket.filename,axis)
                
                new_m.append(MapGrid_Bucket(curr.x1, curr.x2, split_point, curr.y2, c2, curr.bucket))
                curr_grid.update(curr.x1, curr.x2, curr.y1, split_point, c1, curr.bucket)
                                        
    else:
        new_m.append(MapGrid_Bucket(split_point, previous_grid.x2, previous_grid.y1, previous_grid.y2, new_b.count, new_b))
        grid[g].update(previous_grid.x1, split_point, previous_grid.y1, previous_grid.y2 , previous_grid.bucket.count, previous_grid.bucket)
        
        for curr_grid in grid:
            print("values:",curr_grid.x2,split_point)
            if curr_grid.x1 < split_point < curr_grid.x2:
                curr = curr_grid
                c1,c2 = increment(split_point,curr_grid.bucket.filename,axis)
                
                new_m.append(MapGrid_Bucket(split_point, curr.x2, curr.y1, curr.y2, c2, curr.bucket))
                curr_grid.update(curr.x1, split_point, curr.y1, curr.y2, c1, curr.bucket)
    return new_m            

def read_input(fname):
    data_points=[]
    for row in fileinput.FileInput(fname):
        info = row.split()
        data_points.append((int(info[0]) , int(info[1]) , int(info[2])))
    return data_points
           
def Mapper_func(grid, b, split_point_x, split_point_y,bucket_name):
    points = read_input("DataSet.txt")
    axis = 'y'
    c = 0
    for p in points:
        for g in range(len(grid)):
            if grid[g].x1 <= p[1] < grid[g].x2 and grid[g].y1 <= p[2] < grid[g].y2:
                c+=1
               
                if grid[g].bucket.count < bucket_size:
                    print("Count of grid :"+ str(g) + " "+str(grid[g].bucket.count))
                    grid[g].bucket.addpoint(p)
                    grid[g].count+=1
                    print("Contents: "+str(g)+" "+ str(grid[g].bucket.filename))
                    for i in fileinput.FileInput(grid[g].bucket.filename):
                        info = i.split()
                        print(info,end = '')
                    print("\n")
                else:
                    print("else")
                    grid[g].bucket.addpoint(p)
                    grid[g].count+=1
                    print(grid[g].count)
                    print(grid[g].bucket.count)
                    print("Contents: "+str(g)+" "+ str(grid[g].bucket.filename))
                    for i in fileinput.FileInput(grid[g].bucket.filename):
                        info = i.split()
                        
                        print(info,end = '')
                        
                    print("\n")
                    
                    data = []
                    for line in fileinput.FileInput(grid[g].bucket.filename):
                        info = line.split()
                        data.append((int(info[0]) , int(info[1]) , int(info[2]) ))
                    if axis == 'y':
                        split_y = median(data,axis)#split point on y axis
                        split_point_y.append(split_y)
                        print("y = " + str(split_y))
                        b=b+1
                        new_bucket = split_grid(split_y,grid,g,b,data,axis)
                        axis = 'x'
                        grid.extend(new_bucket)
                        break
        
                    else:
                        split_x = median(data,axis)
                        split_point_x.append(split_x) #appending the split points of x axis
                        print("x = " + str(split_x))
                        b=b+1
                        new_bucket = split_grid(split_x,grid,g,b,data,axis)
                        axis = 'y'
                        grid.extend(new_bucket)
                        break
                            
    print("**********")
    for g in grid:
        g.print_info()
    split_point_x.append(400)
    split_point_y.append(400)

if __name__ == '__main__':
	main_func()
