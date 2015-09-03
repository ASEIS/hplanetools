#!/usr/bin/env python
import numpy as np
import os
import sys
# stat = os.stat('planedisplacements.0')
# size = stat.st_size
# print size

# def x(a):
# 	print "--"
# 	a = 5

# 	return a


# def y():
# 	print "~~~"
# 	return 1

# a = 0
# b = 0
# c = 10
# l = [x(a), y(), 'print c']

# for i in l:
# 	i

# # print a
# # print b

def getMultiple(path, numSnapshots):
	filename = path.split('/')[-1]
	dirpath = path.replace(filename, '')
	time = filename.split('-')[-1]
	filelist = []
	index = 0
	while True:
		try:
			index = int(time.replace('s.dat', ''))
		except ValueError:
			print "[ERROR]: not a data file from multiple snapshots."
			sys.exit()
		new_time = str(index+numSnapshots) + 's.dat'

		target = dirpath + filename.replace(time, new_time)
		time = new_time

		# if os.path.isfile(f)
		# os.path.isfile(f)

getMultiple('dis-z-mag-cum-0s.dat', 5)
