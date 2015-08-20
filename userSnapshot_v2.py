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
from userInput import *

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

def cumulativePeak(peak, magnitude):
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

def plot(peak, userInput, index):
	# if userInput.colorChoice == 'c':
	# 	c = colors.ColorConverter().to_rgb
	# 	userInput.colorMap = make_colormap(
	# 	[c(userInput.userColor1), c(userInput.userColor2), 0.5,
	# 	c(userInput.userColor2), c(userInput.userColor3), 1,
	# 	c(userInput.userColor3)])

	if userInput.barChoice:
		im = plt.imshow(peak, vmin=userInput.barMin,
			vmax=userInput.barMax, cmap=userInput.colorMap)
	else:
		im = plt.imshow(peak, cmap=userInput.colorMap)

	# im = plt.imshow(peak)

	plt.axis('off')
	plt.gca().invert_yaxis()

	plt.colorbar(im)
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.suptitle('t = ' + (str)(index*userInput.numSnapshots), fontsize=20)
	plt.axis('scaled')
	saveImage(index, userInput.plotType)
	plt.show()
# end of plot

def saveImage(index, plotType):
	type_dict = {'a': 'acceleration', 'v': 'velocity', 'd': 'displacement'}
	plt.savefig(type_dict[plotType] + str(index) + ".png")
# end of saveImage

def userSnapshot(userInput):
	simulationTime = userInput.simulationTime
	deltaT = userInput.deltaT
	runtime = int(simulationTime/deltaT)
	plotType = userInput.plotType
	magSelect = userInput.magSelect
	snapshots = userInput.snapshots
	numSnapshots = userInput.numSnapshots
	magnitude = userInput.magnitude
	cumulative = userInput.cumulative

	# initializing data
	zeros = zero_matrix(1000, 136, 1000, 181)
	disX0, disY0, disZ0 = zeros, zeros, zeros
	velX0, velY0, velZ0 = zeros, zeros, zeros

	plotType_dict = {}
	index = 0
	for i in range(0, runtime):
		disX, disY, disZ = readFile(userInput.fp, 181, 136)

		# signed / unsigned
		if magnitude:
			disX =  np.absolute(disX)
			disY =  np.absolute(disY)
			disZ =  np.absolute(disZ)

		velX = derivative(disX0, disX, deltaT)
		velY = derivative(disY0, disY, deltaT)
		velZ = derivative(disZ0, disZ, deltaT)

		accX = derivative(velX0, velX, deltaT)
		accY = derivative(velY0, velY, deltaT)
		accZ = derivative(velZ0, velZ, deltaT)

		dis_mag = components(magSelect, disX, disY, disZ)
		vel_mag = components(magSelect, velX, velY, velZ)
		acc_mag = components(magSelect, accX, accY, accZ)

		if i == 0 or not cumulative: # initialize peak
			dis_peak = dis_mag
			vel_peak = vel_mag
			acc_peak = acc_mag

		if cumulative:
			dis_peak = cumulativePeak(dis_peak, dis_mag)
			vel_peak = cumulativePeak(vel_peak, vel_mag)
			acc_peak = cumulativePeak(acc_peak, acc_mag)

		# update dictionary for different plotType
		plotType_dict['a'] = acc_peak
		plotType_dict['v'] = vel_peak
		plotType_dict['d'] = dis_peak

		if snapshots == 'm' and ((i*deltaT)%numSnapshots == 0):
			index += 1
			plot(plotType_dict[userInput.plotType], userInput, index)

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
	if snapshots == 's':
		plot(plotType_dict[userInput.plotType], userInput)
	sys.stdout.write('\n')
# end of userSnapshot


if __name__ == "__main__":
	if len(sys.argv) > 1:
		argument = tuple(sys.argv[1:])
		userInput = Input(*argument)
	else:
		userInput = Input()

	userSnapshot(userInput)


