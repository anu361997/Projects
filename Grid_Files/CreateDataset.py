#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  5 03:31:02 2021

@author: anamika
"""

import random

file = open("/home/anamika/Desktop/PG_Lab5/DataSet.txt", "w+")

print("Enter the number of points to be generated: ")

n = int(input())

for i in range(n):
	x = random.randint(0,400)
	y = random.randint(0,400)
	file.write(str(i+1)+" "+str(x)+" "+str(y)+"\n")
