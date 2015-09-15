# /*
#  ============================================================================
# Loads the plane displacement data at given coordinates, generates corresponding
# velocity and acceleration data, in order to print the hercules file.
# Version: Sep 10, 2015
#  ============================================================================
#  */
from __future__ import division
import sys
import numpy as np
from htools import *
from scipy import interpolate
# from scipy.interpolate import griddata

def readFile(fp, downDip, alongStrike):
	"""read the binary file to get the X, Y, Z values and reshape each
	into a 2D matrix"""
	dis = np.fromfile(fp, np.float64, downDip*alongStrike*3)

	X = dis[::3] #take every third element starting at index 0
	Y = dis[1::3] #...starting at index 1
	Z = dis[2::3] #...starting at index 2

	disX = np.reshape(X, (downDip, alongStrike), order='F')
	disY = np.reshape(Y, (downDip, alongStrike), order='F')
	disZ = np.reshape(Z, (downDip, alongStrike), order='F')

	disX = disX.transpose()
	disY = disY.transpose()
	disZ = disZ.transpose()

	# dis = Data('d', disX, disY, disZ)
	return disX, disY, disZ
	# return dis

def bilinear_interp(x, y, data):
	"""perform bilinear interpolation"""
	values = np.array([], float)
	x0 = int(x)
	x1 = x0+1
	y0 = int(y)
	y1 = y0+1
	x_coor = np.array([x0, x1, x0, x1], dtype = int)
	y_coor = np.array([y0, y0, y1, y1], dtype = int)
	for i in range(0, x_coor.size):
		values = np.append(values, data[x_coor[i], y_coor[i]])
	f = interpolate.interp2d(x_coor, y_coor, values, kind='linear')
	new_value = f(x, y)
	return new_value
# end of bilinear_interp

def print_her(filename, dt, disData, velData, accData):
	filename = filename.split('.')[0]+'.her'
	try:
		f = open(filename, 'w')
	except IOError, e:
		print e
	dis_x = disData[0].tolist()
	vel_x = velData[0].tolist()
	acc_x = accData[0].tolist()
	dis_y = disData[1].tolist()
	vel_y = velData[1].tolist()
	acc_y = accData[1].tolist()
	dis_z = disData[2].tolist()
	vel_z = velData[2].tolist()
	acc_z = accData[2].tolist()


	# get a list of time incremented by dt
	time = [0.000]
	samples = disData[0].size
	tmp = samples

	while tmp > 1:
		time.append(time[len(time)-1] + dt)
		tmp -= 1

	# f.write('# '+str(dt)+'\n')

	descriptor = '{:>12}' + '  {:>12}'*9 + '\n'
	f.write(descriptor.format("# time", "dis_x", "dis_y", "dis_z", "vel_x", "vel_y", "vel_z", "acc_x", "acc_y", "acc_z")) # header

	descriptor = '{:>12.3f}' + '  {:>12.7f}'*9 + '\n'
	for c0, c1, c2, c3, c4, c5, c6, c7, c8, c9 in zip(time, dis_x, dis_y, dis_z, vel_x, vel_y, vel_z, acc_x, acc_y, acc_z):
		f.write(descriptor.format(c0, c1, c2, c3, c4, c5, c6, c7, c8, c9 ))
	f.close()
# end of print_her


if __name__ == "__main__":
	# initialization
	filename = 'planedisplacements.0'
	simulationTime = 100
	deltaT = 0.025
	alongStrike = 136
	downDip = 181
	stepAlongStrike = 1000
	stepDownDip = 1000

	# random coordinates to test
	x = 118524
	y = 123356

	index_x = x/stepAlongStrike
	index_y = y/stepDownDip

	# loading plane data file
	try:
		fp = open(filename, 'r')
	except IOError:
		print "[ERROR]: unable to load data file."

	runtime = int(simulationTime/deltaT)
	disX = np.array([],float)
	disY = np.array([],float)
	disZ = np.array([],float)
	for i in range(0, runtime):
		dataX, dataY, dataZ = readFile(fp, downDip, alongStrike)
		disX = np.append(disX, bilinear_interp(index_x, index_y, dataX))
		disY = np.append(disY, bilinear_interp(index_x, index_y, dataY))
		disZ = np.append(disZ, bilinear_interp(index_x, index_y, dataZ))

		# showing progress on terminal
		percent = float(i)/runtime
		hashes = '#'*int(round(percent*20))
		spaces = ' '*(20-len(hashes))
		sys.stdout.write("\rProgress: [{0}] {1}%".format(hashes+spaces, int(round(percent*100))))
		sys.stdout.flush()

	velX = derivative(disX, deltaT)
	velY = derivative(disY, deltaT)
	velZ = derivative(disZ, deltaT)

	accX = derivative(velX, deltaT)
	accY = derivative(velY, deltaT)
	accZ = derivative(velZ, deltaT)

	print_her(filename, deltaT, [disX, disY, disZ], [velX, velY, velZ], [accX, accY, accZ])
	sys.stdout.write('\n')
# end of __main__
