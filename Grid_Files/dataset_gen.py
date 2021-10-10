import random as r
f = open("DataSet2.txt", "w+")
n_datapoints = int(input("Enter the number of random data points to be generated"))
for i in range(n_datapoints):
    id = i + 1
    x = r.randrange(0,400)
    y = r.randrange(0,400)
    output = "%s %s %s" %(id,x, y)
    f.write(output + "\n" )
f.close()
