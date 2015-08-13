#!/usr/bin/env python
# ==========================================================================
# The program is to load data stored in plantedisplacement file, then to plot
# figures based on user's choises.
# version: August 11, 2015.
# ==========================================================================
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as ml

def components(magSelect, dataX, dataY, dataZ):
	"""decide components to use for displacement plotting"""
	magDic = {'x': dataX, 'y': dataY, 'z': dataZ}
	if len(magSelect) == 1:
		magnitude = magDic[magSelect[0]]
	elif len(magSelect) == 2:
		magnitude = np.sqrt(np.power(magDic[magSelect[0]], 2) + np.power(magDic[magSelect[1]], 2))
	elif len(magSelect) == 3:
		magnitude = np.sqrt(np.power(magDic[magSelect[0]], 2) + np.power(magDic[magSelect[1]], 2)
			+ np.power(magDic[magSelect[2]], 2))
	return magnitude
# end of disComponents

def cumulativeMag(peak, magnitude):
	"""return the peak value based on original peak and given magnitude"""
	peak = np.maximum(peak, magnitude)
	return peak
# end of cumulativeMag

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
	return disX, disY, disZ

def zero_matrix(stepAlongStrike, alongStrike, stepDownDip, downDip):
	"""generate a matrix contains all zeros"""
	y = np.array(range(0, stepAlongStrike*alongStrike, stepAlongStrike))
	x = np.array(range(0, stepDownDip*downDip, stepDownDip))
	x, y = np.meshgrid(x, y)
	zeros = np.zeros_like(x)
	return zeros
# end of init_peak

def derivative(data1, data2, dt):
	data = (data2-data1)/dt
	return data
# end of derivative

def plot(peak):
	im = plt.imshow(peak)

	plt.axis('off')
	plt.gca().invert_yaxis()

	plt.colorbar(im)
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.suptitle('t = ' + (str)((int)(i*0.025)), fontsize=20)
	plt.axis('scaled')

	plt.show()
# end of plot


if __name__ == "__main__":
	try:
		fp = open('planedisplacements.0', 'r')
	except IOError:
		print "[ERROR]: No such file."
	simulationTime = 100
	deltaT = 0.025
	runtime = int(simulationTime/deltaT)
	plotType = 'd'
	magSelect = ['x']
	# magSelect = ['x', 'z']
	# magSelect = ['x', 'y', 'z']
	numSnapshots = 's'

	zeros = zero_matrix(1000, 136, 1000, 181)
	disX0, disY0, disZ0 = zeros, zeros, zeros
	velX0, velY0, velZ0 = zeros, zeros, zeros

	for i in range(0, runtime):
		disX, disY, disZ = readFile(fp, 181, 136)

		velX = derivative(disX0, disX, deltaT)
		velY = derivative(disY0, disY, deltaT)
		velZ = derivative(disZ0, disZ, deltaT)

		accX = derivative(velX0, velX, deltaT)
		accY = derivative(velY0, velY, deltaT)
		accZ = derivative(velZ0, velZ, deltaT)

		dis_mag = components(magSelect, disX, disY, disZ)
		vel_mag = components(magSelect, velX, velY, velZ)
		acc_mag = components(magSelect, accX, accY, accZ)

		if i == 0: # initialize peak
			dis_peak = dis_mag
			vel_peak = vel_mag
			acc_peak = acc_mag
		dis_peak = cumulativeMag(dis_peak, dis_mag)
		vel_peak = cumulativeMag(vel_peak, vel_mag)
		acc_peak = cumulativeMag(acc_peak, acc_mag)

		if numSnapshots == 'm':
			plot(dis_peak)
			# plot(vel_peak)
			# plot(acc_peak)

		# showing progress on terminal
		percent = float(i)/runtime
		hashes = '#'*int(round(percent*20))
		spaces = ' '*(20-len(hashes))
		sys.stdout.write("\rProgress: [{0}] {1}%".format(hashes+spaces, int(round(percent*100))))
		sys.stdout.flush()

		# update initial values for next iteration
		disX0, disY0, disZ0 = disX, disY, disZ
		velX0, velY0, velZ0 = velX, velY, velZ

	# plotting cumulative values
	if numSnapshots == 's':
		plot(dis_peak)
		plot(vel_peak)
		plot(acc_peak)
	sys.stdout.write('\n')

