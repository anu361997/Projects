#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 16:40:53 2021

@author: anamika
"""

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
    def __init__(self, xcord1 , ycord1 ,count, bucket):     
        self.xcord = xcord1
        self.ycord = ycord1
        self.count = count
        self.bucket = bucket
    def update(self, xcord1, ycord1, count, bucket):
        self.xcord = xcord1
        self.ycord = ycord1
        self.count = count
        self.bucket = bucket

class Bucket:
    def __init__(self, filename,count):
        self.filename = filename
        self.count = count
    def addpoint(self, data_point):
        self.count+=1
        self.point = data_point
        id_point = data_point[0]
        x = data_point[1]
        y = data_point[2]
        buc = open(self.filename, "a+")
        output = "%s %s %s" %(id_point,x,y)
        buc.write(output+"\n")
        buc.close()
    def update(self, data_points):
        self.points = data_points
        self.count = len(data_points)
        buc = open(self.filename, 'w+')
        for dp in data_points:
            dp_id = dp[0]
            dp_x = dp[1]
            dp_y = dp[2]
            output = "%s %s %s" %(dp_id,dp_x,dp_y)
            buc.write(output+"\n")
        buc.close()

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
    xcord=[x_min, x_max]
    ycord=[y_min, y_max]
    grid.append(MapGrid_Bucket(xcord,ycord, count, bucket)) #xy plane
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
    new_grid = []
    previous_grid = grid[g]
    data_bucket = data
    index = split_bucket(data_bucket,axis,split_point)
    new_b =  Bucket(str(b) + ".txt", 0)
    previous_grid.bucket.update(data_bucket[0:index])
    #print("Count of bucket 1:",previous_grid.bucket.count)
    new_b.update(data_bucket[index: ])
    if(axis == 'y'):
        xcord_up_y = [previous_grid.xcord[0], previous_grid.xcord[1]]
        ycord_up_y = [ split_point, previous_grid.ycord[1]] 
        ycord_up2_y = [previous_grid.ycord[0],split_point]
        new_grid.append(MapGrid_Bucket(xcord_up_y, ycord_up_y, new_b.count, new_b))
        grid[g].update(xcord_up_y, ycord_up2_y, previous_grid.bucket.count, previous_grid.bucket)
        
        for curr_grid in grid:
            #print("values:",curr_grid.ycord[1],split_point)
            if curr_grid.ycord[0] < split_point < curr_grid.ycord[1]:
                curr = curr_grid
                c1,c2 = increment(split_point,curr_grid.bucket.filename,axis)
                xcord_curr_y = [curr.xcord[0], curr.xcord[1]]
                ycord_curr_y = [split_point,curr.ycord[1]]
                ycord_curr2_y = [curr.ycord[0], split_point]
                new_grid.append(MapGrid_Bucket(xcord_curr_y, ycord_curr_y, c2, curr.bucket))
                curr_grid.update(xcord_curr_y, ycord_curr2_y, c1, curr.bucket)
                                        
    else:
        xcord_up_x = [split_point, previous_grid.xcord[1]]
        ycord_up_x = [previous_grid.ycord[0], previous_grid.ycord[1]] 
        xcord_up2_x = [previous_grid.xcord[0],split_point]
        
        new_grid.append(MapGrid_Bucket(xcord_up_x, ycord_up_x, new_b.count, new_b))
        grid[g].update(xcord_up2_x,ycord_up_x, previous_grid.bucket.count, previous_grid.bucket)
        
        for curr_grid in grid:
            #print("values:",curr_grid.xcord[1],split_point)
            if curr_grid.xcord[0] < split_point < curr_grid.xcord[1]:
                curr = curr_grid
                c1,c2 = increment(split_point,curr_grid.bucket.filename,axis)
                xcord_curr_x = [split_point, curr.xcord[1]]
                ycord_curr_x = [curr.ycord[0], curr.ycord[1]] 
                xcord_curr2_x = [curr.xcord[0],split_point]
                
                new_grid.append(MapGrid_Bucket(xcord_curr_x, ycord_curr_x, c2, curr.bucket))
                curr_grid.update(xcord_curr2_x, ycord_curr_x, c1, curr.bucket)
    return new_grid            

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
            if grid[g].xcord[0] <= p[1] < grid[g].xcord[1] and grid[g].ycord[0] <= p[2] < grid[g].ycord[1]:
                c+=1
               
                if grid[g].bucket.count < bucket_size:
                    #print("Count of grid :"+ str(g) + " "+str(grid[g].bucket.count))
                    print("Adding point: "+str(p[0]))
                    grid[g].bucket.addpoint(p)
                    grid[g].count+=1
                    #print("Contents: "+str(g)+" "+ str(grid[g].bucket.filename))
                    #for i in fileinput.FileInput(grid[g].bucket.filename):
                    #    info = i.split()
                    #    print(info,end = '')
                    #print("\n")
                    break
                else:
                    #print("else")
                    print("Adding point: "+str(p[0]))
                    grid[g].bucket.addpoint(p)
                    grid[g].count+=1
                    #print(grid[g].count)
                    #print(grid[g].bucket.count)
                    #print("Contents: "+str(g)+" "+ str(grid[g].bucket.filename))
                    #for i in fileinput.FileInput(grid[g].bucket.filename):
                    #    info = i.split()
                        
                    #    print(info,end = '')
                        
                    #print("\n")
                    
                    data = []
                    for line in fileinput.FileInput(grid[g].bucket.filename):
                        data_p = line.split()
                        data.append((int(data_p[0]) , int(data_p[1]) , int(data_p[2]) ))
                    if axis == 'y':
                        split_y = median(data,axis)#split point on y axis
                        split_point_y.append(split_y)
                        print("Splitting at y = " + str(split_y))
                        b=b+1
                        new_bucket = split_grid(split_y,grid,g,b,data,axis)
                        axis = 'x'
                        grid.extend(new_bucket)
                        break
        
                    else:
                        split_x = median(data,axis)
                        split_point_x.append(split_x) #appending the split points of x axis
                        print("Splitting at x = " + str(split_x))
                        b=b+1
                        new_bucket = split_grid(split_x,grid,g,b,data,axis)
                        axis = 'y'
                        grid.extend(new_bucket)
                        break
    split_point_x.append(400)
    split_point_y.append(400)
    
def print_content(fname):
     for i in fileinput.FileInput(fname):
         info = i.split()
         print(info,end = '')
     print("\n")
    
            
def print_final_grid():                
    print("Printing the final contents of the grid: ")
    bucket_names = []
    for g in grid:
        bucket_names.append(g.bucket.filename)
    grid_buckets = set(bucket_names)
    sorted(grid_buckets)
    #print(grid_buckets)
        
    for i in grid_buckets:
        b_name = i
        print("Contents of bucket: ",b_name)
        print("\n")
        print_content(b_name)
 
def print_splitpoints():
    print("split points on x-axis:")
    for i in split_point_x:
        print(i,end=' ')
    print("\n")
    print("split points on y-axis:")
    for i in split_point_y:
        print(i,end=' ')
    print("\n")

def print_grid():
    logical_counter=0
    for i in grid:
        
        print("Grid number: ",logical_counter)
        print("Bucket_name: ", i.bucket.filename )
        print("Size of Bucket: ", i.bucket.count)
        print("Lower Coordinates of Grid: ", i.xcord[0],i.ycord[0])
        print("Higher Coordinates of Grid: ",i.xcord[1],i.ycord[1])
        logical_counter+=1
    

main_func()
print_final_grid()
print("--------------------------------------------")
print_splitpoints()
print("--------------------------------------------")
print_grid()
