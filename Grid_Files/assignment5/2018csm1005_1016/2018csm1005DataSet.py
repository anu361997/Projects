import random as r
import fileinput
f = open("DataSetB.txt", "w+")
for i in range(100):
	#id = i + 1
	x = r.randrange(0,400)
	y = r.randrange(0,400)
	output = "%s %s" %(x, y)
	f.write(output + "\n" )
#	print(str(i) + " " + str(x) + " " + str(y))
f.close()


	
