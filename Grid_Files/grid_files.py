#!/usr/bin/env python3
# 2020CSM1004 ANAMIKA 2020CSM1003 AKSHAY KUMAR DIXIT
# Lab Assignment 5 Grid File Implementation

import random as r
import fileinput
import statistics
import sys

bucket_size = int(input("Enter the bucket size: "))  # Bucket size
grid = []  # global grid structure
split_point_x, split_point_y = [], []  # tracks the split point for x and y axis
b = 0  # Global Bucket Counter for Grid


class MapGrid_Bucket:  # Map Grid class that maps Grid with the respective bucket
    def __init__(self, xcord1, ycord1, count, bucket):
        self.xcord = xcord1
        self.ycord = ycord1
        self.count = count
        self.bucket = bucket

    def update(self, xcord1, ycord1, count, bucket):  # To update the changes in the Grid files
        self.xcord = xcord1
        self.ycord = ycord1
        self.count = count
        self.bucket = bucket


class Bucket:  # Bucket Class that contains filename of the bucket and its count
    def __init__(self, filename, count):
        self.filename = filename
        self.count = count

    def addpoint(self, data_point):  # To add point in the bucket(file) and updating its count
        self.count += 1
        self.point = data_point
        id_point = data_point[0]
        x = data_point[1]
        y = data_point[2]
        buc = open(self.filename, "a+")
        output = "%s %s %s" % (id_point, x, y)
        buc.write(output + "\n")
        buc.close()

    def update(self, data_points):  # Updating the bucket(file) when split is done
        self.points = data_points
        self.count = len(data_points)
        buc = open(self.filename, 'w+')  # Open the file in write mode
        for dp in data_points:
            dp_id = dp[0]
            dp_x = dp[1]
            dp_y = dp[2]
            output = "%s %s %s" % (dp_id, dp_x, dp_y)  # Enter the records
            buc.write(output + "\n")
        buc.close()


def main_func():
    bucket_name = str(b) + ".txt"
    bucket = Bucket(bucket_name, 0)

    x_min = 0            # Starting Grid Co-ordinates
    x_max = 400
    y_min = 0
    y_max = 400
    count = 0
    split_point_x.append(0)
    split_point_y.append(0)
    xcord = [x_min, x_max]
    ycord = [y_min, y_max]
    grid.append(MapGrid_Bucket(xcord, ycord, count, bucket))  # initiating Grid structure with 0.txt as bucket and co-ordinates as (0,400)(0,400)
    Mapper_func(grid, b, split_point_x, split_point_y, bucket_name)  # Mapping Grid with the bucket


def median(data, axis):  # Calculates and return the median
    data_axis = []
    if (axis == 'y'):   # for median of y axis
        for row in data:
            data_axis.append(row[2])
        med = int(statistics.median(data_axis))
    if (axis == 'x'):  # for median of x axis
        for row in data:
            data_axis.append(row[1])
        med = int(statistics.median(data_axis))
    return med


def sort_data(axis, data):  # To sort the data points for ease in splitting
    if (axis == 'x'):
        data.sort(key=lambda x: x[1])
    else:
        data.sort(key=lambda x: x[2])
    return data


def split_bucket(data, axis, split_point):  # Function to split the bucket when it crosses the bucket size
    if (axis == 'x'):   # when split is on x
        data_sorted = sort_data('x', data)
        ax = 1
        l = len(data_sorted)
        i = 0
        while i < l:        # finding records less than med
            if data_sorted[i][ax] >= split_point:
                index = i
                break
            i = i + 1
    else:  # when split is on y
        data_sorted = sort_data('y', data)
        ax = 2
        l = len(data_sorted)
        i = 0
        while i < l:   # finding records less than med
            if data_sorted[i][ax] >= split_point:
                index = i
                break
            i = i + 1
    return index


def increment(split_point, fname, axis):  # finding count of data records on left and right when grid is logically split
    count1, count2 = 0, 0
    if (axis == 'x'):  # For x axis
        for line in fileinput.FileInput(fname):
            info = line.split()
            if int(info[1]) >= split_point:
                count2 = count2 + 1
            else:
                count1 = count1 + 1
    else:   # For y axis
        for line in fileinput.FileInput(fname):
            info = line.split()
            if int(info[2]) >= split_point:
                count2 = count2 + 1
            else:
                count1 = count1 + 1
    return count1, count2


def split_grid(split_point, grid, g, b, data, axis):  # Function to split the grid
    new_grid = []
    previous_grid = grid[g]
    data_bucket = data
    index = split_bucket(data_bucket, axis, split_point)  # finding the split index
    new_b = Bucket(str(b) + ".txt", 0)
    previous_grid.bucket.update(data[0:index])   # Updating previous bucket
    # print("Count of bucket 1:",previous_grid.bucket.count)
    new_b.update(data[index:])  # Updating new bucket
    if (axis == 'y'):
        xcord_up_y = [previous_grid.xcord[0], previous_grid.xcord[1]]
        ycord_up_y = [split_point, previous_grid.ycord[1]]
        ycord_up2_y = [previous_grid.ycord[0], split_point]
        new_grid.append(MapGrid_Bucket(xcord_up_y, ycord_up_y, new_b.count, new_b)) 
        grid[g].update(xcord_up_y, ycord_up2_y, previous_grid.bucket.count, previous_grid.bucket) #updating older bucket 

        for curr_grid in grid:  # Checking if older grids need splitting
            # print("values:",curr_grid.ycord[1],split_point)
            if curr_grid.ycord[0] < split_point < curr_grid.ycord[1]:
                curr = curr_grid
                c1, c2 = increment(split_point, curr_grid.bucket.filename, axis)
                xcord_curr_y = [curr.xcord[0], curr.xcord[1]]
                ycord_curr_y = [split_point, curr.ycord[1]]
                ycord_curr2_y = [curr.ycord[0], split_point]
                new_grid.append(MapGrid_Bucket(xcord_curr_y, ycord_curr_y, c2, curr.bucket))
                curr_grid.update(xcord_curr_y, ycord_curr2_y, c1, curr.bucket)

    else:  # for y axis
        xcord_up_x = [split_point, previous_grid.xcord[1]]
        ycord_up_x = [previous_grid.ycord[0], previous_grid.ycord[1]]
        xcord_up2_x = [previous_grid.xcord[0], split_point]

        new_grid.append(MapGrid_Bucket(xcord_up_x, ycord_up_x, new_b.count, new_b))
        grid[g].update(xcord_up2_x, ycord_up_x, previous_grid.bucket.count, previous_grid.bucket)

        for curr_grid in grid: # Checking if older grids need splitting
            # print("values:",curr_grid.xcord[1],split_point)
            if curr_grid.xcord[0] < split_point < curr_grid.xcord[1]:
                curr = curr_grid
                c1, c2 = increment(split_point, curr_grid.bucket.filename, axis)
                xcord_curr_x = [split_point, curr.xcord[1]]
                ycord_curr_x = [curr.ycord[0], curr.ycord[1]]
                xcord_curr2_x = [curr.xcord[0], split_point]

                new_grid.append(MapGrid_Bucket(xcord_curr_x, ycord_curr_x, c2, curr.bucket))
                curr_grid.update(xcord_curr2_x, ycord_curr_x, c1, curr.bucket)
    return new_grid


def read_input(fname):  # For reading from the file
    data_points = []
    for row in fileinput.FileInput(fname):
        info = row.split()
        data_points.append((int(info[0]), int(info[1]), int(info[2])))
    return data_points


def Mapper_func(grid, b, split_point_x, split_point_y, bucket_name):  # Main Mapper function that reads points one by one and add to GRID and BUCKET
    points = read_input("DataSet.txt")  # Name of the DatSet
    axis = 'y'
    c = 0
    for record in points:
        for g in range(len(grid)):
            if grid[g].xcord[0] <= record[1] < grid[g].xcord[1] and grid[g].ycord[0] <= record[2] < grid[g].ycord[1]:
                c += 1

                if grid[g].bucket.count < bucket_size:
                    # print("Count of grid :"+ str(g) + " "+str(grid[g].bucket.count))
                    print("Adding point: " + str(record[0]))
                    grid[g].bucket.addpoint(record)
                    grid[g].count += 1
                    break
                else:
                    # print("else")
                    print("Adding point: " + str(record[0]))
                    grid[g].bucket.addpoint(record)
                    grid[g].count += 1

                    data = []
                    for line in fileinput.FileInput(grid[g].bucket.filename): # adding all the points
                        info = line.split()
                        data.append((int(info[0]), int(info[1]), int(info[2])))
                    if axis == 'y':
                        split_y = median(data, axis)  # split point on y axis
                        split_point_y.append(split_y)
                        print("Splitting at y = " + str(split_y))
                        b = b + 1
                        new_bucket = split_grid(split_y, grid, g, b, data, axis)  # checking if old grid needs to be updated
                        axis = 'x'
                        grid.extend(new_bucket) # adding new grid to the grid data structure
                        break

                    else:  # when split is on x asis
                        split_x = median(data, axis)
                        split_point_x.append(split_x)  # appending the split points of x axis
                        print("Splitting at x = " + str(split_x))
                        b = b + 1
                        new_bucket = split_grid(split_x, grid, g, b, data, axis) # checking if old grid needs to be updated
                        axis = 'y'
                        grid.extend(new_bucket)  # adding new grid to the grid data structure
                        break
    split_point_x.append(400)
    split_point_y.append(400)


def print_content(fname):    # To print the content of the file
    for i in fileinput.FileInput(fname):
        info = i.split()
        print(info, end='')
    print("\n")


def print_final_grid():  # For printing the final Grid data structure
    print("Printing the final contents of the grid: ")
    bucket_names = []
    for g in grid:
        bucket_names.append(g.bucket.filename)
    grid_buckets = set(bucket_names)
    sorted(grid_buckets)
    print(grid_buckets)
    # g.print_info()
    for i in grid_buckets:  # prints the bucket contents
        b_name = i
        print("Contents of bucket: ", b_name)
        print("\n")
        print_content(b_name)


def print_splitpoints():  # For printing the final split scales of x and y
    print("split points on x-axis:")
    for i in split_point_x:
        print(i, end=' ')
    print("\n")
    print("split points on y-axis:")
    for i in split_point_y:
        print(i, end=' ')
    print("\n")


def print_grid():  # For Printing Grid and its bucket name
    logical_counter = 0
    for i in grid:
        print("Grid number: ", logical_counter)
        print("Bucket_name: ", i.bucket.filename)
        print("Size of Bucket: ", i.bucket.count)
        print("Lower Coordinates of Grid: ", i.xcord[0], i.ycord[0])
        print("Higher Coordinates of Grid: ", i.xcord[1], i.ycord[1])
        logical_counter += 1


def range_query(q_xmin, q_xmax, q_ymin, q_ymax):  # Implementation of range query
    print(q_xmin, q_xmax, q_ymin, q_ymax)
    logical_counter = 0
    list = []
    for i in grid:  # for all grids check if it lies inside the range query rectangle
        if (q_xmin <= i.xcord[0] <= q_xmax and q_ymin <= i.ycord[0] <= q_ymax) or (
                q_xmin <= i.xcord[1] <= q_xmax and q_ymin <= i.ycord[1] <= q_ymax):
            for line in fileinput.FileInput(i.bucket.filename):
                info = line.split()
                if q_xmin <= int(info[1]) <= q_xmax and q_ymin <= int(info[2]) <= q_ymax:
                    flag = False
                    for i in list:  # Checking if the record is already been added in the list
                        # print(i[0])
                        if i[0] == int(info[0]):
                            flag = True
                            break
                    if not flag:
                        list.append((int(info[0]), int(info[1]), int(info[2])))
            logical_counter += 1
    print(list) # printing final list


main_func()
print_final_grid()
print("--------------------------------------------")
print_splitpoints()
print("--------------------------------------------")
print_grid()
print("---For Range Query -----------------")
print("Enter the Lower left coordinates of the query rectangle:")
q_xmin = int(input("Enter the xmin for Range Query: "))
q_ymin = int(input("Enter the ymmin for Range Query: "))
print("Enter the Upper Right coordinates of the query rectangle:")
q_xmax = int(input("Enter the xmax for Range Query: "))
q_ymax = int(input("Enter the ymax for Range Query: "))
range_query(q_xmin, q_xmax, q_ymin, q_ymax)
