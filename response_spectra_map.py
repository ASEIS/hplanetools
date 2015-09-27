# /*
#  ============================================================================
# Loads the plane displacement data to produce acceleration signals at each grid
# point, then generates a response spectra map of signals.
# Version: Sep 25, 2015.
#  ============================================================================
#  */
import numpy as np
import sys
sys.path.insert(0, '/Users/kelicheng/seismtools')
from stools import *
from htools import *
np.seterr(divide='ignore', invalid='ignore')
def loadData(fp, alongStrike, downDip, x_coor, y_coor, num_layers):
	"""load plane data file by index, return the values of four points around the station"""
	dis = np.array([], float)
	values_x, values_y, values_z = np.array([], float), np.array([], float), np.array([], float)
	base = alongStrike*downDip*3*num_layers # number of data in past layers

	for i in range(0, len(x_coor)):
		x = x_coor[i]
		y = y_coor[i]

		# index = number of data in past layers + postion in current layer
		index = base + (downDip*x+y)*3
		offset = index*8 # offset measured in byte
		try:
			dis = np.memmap(filename, np.float64, 'r', offset, (3)) # load three numbers for x/y/z
		except ValueError:
			print "[ERROR]: unable to load file."
			sys.exit()

		values_x = np.append(values_x, dis[0])
		values_y = np.append(values_y, dis[1])
		values_z = np.append(values_z, dis[2])
	return values_x, values_y, values_z
# end of load_by_index

def loadFile(filename, numGridX, numGridY, num_layers, x_coor, y_coor):
	"""load the displacement data at given grid point"""
	dis = np.array([], float)
	base = numGridX*numGridY*3*num_layers
	index = base + (numGridY*x_coor+y_coor)*3
	offset = index*8

	try:
		dis = np.memmap(filename, np.float64, 'r', offset, (3)) # load three numbers for three orientations
		return dis
	except ValueError:
		print "[ERROR]: unable to load file."
		sys.exit()
# end of loadFile

def dis_to_acc(dis, deltaT):
	vel = derivative(dis, deltaT)
	acc = derivative(vel, deltaT)
	return acc
# end of dis_to_acc



if __name__ == "__main__":
	compoDic = {'x':0, 'y':1, 'z':2}
	typeDic = {'a':2, 'v':'1', 'd':0}
	filename = 'planedisplacements2.0'
	dimensionX = 180000
	dimensionY = 135000
	spaceX = 1000
	spaceY = 1000
	simulationTime = 50
	deltaT = 0.1
	period = 2
	component = 'x'
	responseType = 'a'
	colorMap = 'hot'


	runtime = int(simulationTime/deltaT)
	numGridX = dimensionX/spaceX+1
	numGridY = dimensionY/spaceY+1

	print numGridX, numGridY


	response = np.empty((numGridX, numGridX))
	# iterate through each grid points
	for i in range(0, numGridX):
		for j in range(0, numGridY):
			dis = np.array([],float)

			# read the same grid point at different layer
			for k in range(0, runtime):
				data = loadFile(filename, numGridX, numGridY, k, i, j)
				dis = np.append(dis, data[compoDic[component]])
			acc = dis_to_acc(dis, deltaT)

			# calculate response and put into the matrix
			# response[i][j] = max_osc_response(acc, deltaT, 0.05, period, 0, 0)[typeDic[responseType]]
			response[i][j] = acc[15]
			# showing progress on terminal

		show_progress(i, numGridX)

	# plot response spectra
	plot(response, colorMap)

