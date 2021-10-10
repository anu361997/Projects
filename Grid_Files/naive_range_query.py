#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 21:23:22 2021

@author: anamika
"""
import fileinput

def read_input(fname):
    data_points=[]
    for row in fileinput.FileInput(fname):
        info = row.split()
        data_points.append((int(info[0]) , int(info[1]) , int(info[2])))
    return data_points

def naive_range(x1,y1,x2,y2,data):
    in_range_data =[]
    for d in data:
        if d[1]>=x1 and d[2] >=y1 and d[1]<=x2 and d[2]<=y2:
            in_range_data.append((int(d[0]),int(d[1]),int(d[2])))
            
    return in_range_data

def main():
    data = read_input("DataSet.txt")
    print("Enter the Lower left coordinates of the query rectangle:")
    x1,y1 = int(input("Enter x coordinate: ")),int(input("Enter y coordinate: "))
    print("Enter the upper right coordinates of the query rectangle:")
    x2,y2 = int(input("Enter x coordinate: ")),int(input("Enter y coordinate: "))
    in_range_points = naive_range(x1,y1,x2,y2,data)
    print("------------------------------------------")
    print("points present in the query rectangle are:")
    print(in_range_points)
    
main()