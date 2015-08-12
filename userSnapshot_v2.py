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

def disComponents(magSelect, disX, disY, disZ):
	"""decide components to use for displacement plotting"""
	magDic = {0: disX, 1: disY, 2: disZ}
	if len(magSelect) == 1:
		magnitude = magDic[magSelect[0]]
	elif len(magSelect) == 2:
		magnitude = np.sqrt(np.power(magDic[magSelect[0]], 2) + np.power(magDic[magSelect[1]], 2))
		# reverse X and Y
		# if 0 and 1 in magSelect:
		# 	magnitude = horizMag.transpose()
	elif len(magSelect) == 3:
		magnitude = np.sqrt(np.power(magDic[magSelect[0]], 2) + np.power(magDic[magSelect[1]], 2)
			+ np.power(magDic[magSelect[2]], 2))
	return magnitude
# end of disComponents

def cumulativeMag(peak, magnitude):
	"""return the peak value based on original peak and given magnitude"""
	peak = np.maximum(peak, magnitude.transpose())
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
	return disX, disY, disZ

def init_peak(stepAlongStrike, alongStrike, stepDownDip, downDip):
	"""initialize peak matrix"""
	y = np.array(range(0, stepAlongStrike*alongStrike, stepAlongStrike))
	x = np.array(range(0, stepDownDip*downDip, stepDownDip))
	x, y = np.meshgrid(x, y)
	peak = np.zeros_like(x)
	return peak
# end of init_peak

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
	start = 0
	simulationTime = 100
	deltaT = 0.025
	runtime = int(simulationTime/deltaT)
	# peak = init_peak(1000, 136, 1000, 181)

	for i in range(start, runtime):
		disX, disY, disZ = readFile(fp, 181, 136)
		# magnitude = disComponents([0], disX, disY, disZ)
		# magnitude = disComponents([0, 1], disX, disY, disZ)
		magnitude = disComponents([0, 1, 2], disX, disY, disZ)
		if i == start:
			peak = magnitude.transpose()
		peak = cumulativeMag(peak, magnitude)

		# showing progress on terminal
		percent = float(i)/runtime
		hashes = '#'*int(round(percent*20))
		spaces = ' '*(20-len(hashes))
		sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes+spaces, int(round(percent*100))))
		sys.stdout.flush()

	plot(peak)
	pass
