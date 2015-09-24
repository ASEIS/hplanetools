#!/usr/bin/env python
import numpy as np
import os
import sys
def load_by_index(alongStrike, downDip, x_coor, y_coor):
	"""load plane data file, return the values of four points around the station"""
	dis = np.fromfile('planedisplacements2.0', np.float64, downDip*alongStrike*3)
	values_x, values_y, values_z = np.array([], float), np.array([], float), np.array([], float)
	for i in range(0, len(x_coor)):
		x = x_coor[i]
		y = y_coor[i]
		index_x = (downDip*x+y)*3 + 0
		index_y = (downDip*x+y)*3 + 1
		index_z = (downDip*x+y)*3 + 2

		values_x = np.append(values_x, dis[index_x])
		values_y = np.append(values_y, dis[index_y])
		values_z = np.append(values_z, dis[index_z])

		print "%.7f" % dis[index_x]
		print "%.7f" % dis[index_y]
		print "%.7f" % dis[index_z]

		# print values_x
		# print values_y
		# print values_z


def test_mem(x_coor, y_coor):
	for i in range(0, len(x_coor)):
		x = x_coor[i]
		y = y_coor[i]
		index_x = (181*x+y)*3 + 1
		offset = index_x*64*8
		a = np.memmap('planedisplacements2.0', np.float64, 'r', offset, (3))
		print a


x_coor = [60, 60, 61, 61]
y_coor = [90, 91, 90, 91]
runtime = int(50/0.1)
for i in range(0, runtime):
	print str(i) + '----------------------------'
	# load_by_index(181, 136, x_coor, y_coor)
	test_mem(x_coor, y_coor)