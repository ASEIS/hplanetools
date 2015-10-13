# /*
#  ============================================================================
# Loads the plane displacement data to produce acceleration signals at each grid
# point, then generates a response spectra map of signals.
# Version: Oct 05, 2015.
#  ============================================================================
#  */
import numpy as np
import sys
sys.path.insert(0, '/Users/kelicheng/seismtools') # insert the path to seismtools to import stools program.
from stools import *
from htools import *
np.seterr(divide='ignore', invalid='ignore')

def loadFile(filename, numGridX, numGridY, num_layers, x_coor, y_coor, block_size):
	"""load the displacement data at given grid point"""
	dis = np.array([], float)
	base = numGridX*numGridY*3*num_layers # number of data in past layers
	# index = base + (numGridY*x_coor+y_coor)*3 # number of data in past layers + postion in current layer
	# index = base + (136*x_coor+y_coor)*3
	index = base + (136*y_coor+x_coor)*3
	# index = base + (181*x_coor+y_coor)*3
	# index = base + (181*y_coor+x_coor)*3

	offset = index*8 # offset measured in byte

	try:
		dis = np.memmap(filename, np.float64, 'r', offset, (3*block_size)) # load three numbers for three orientations
		return dis
	except ValueError:
		# return np.zeros((3*block_size))
		# pass
		print x_coor, y_coor, num_layers
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
	block_size = 136

	simulationTime = 50
	deltaT = 0.1
	period = 20
	component = 'x'
	responseType = 'a'
	colorMap = 'hot'


	numLayer = int(simulationTime/deltaT)
	numGridX = dimensionX/spaceX+1
	numGridY = dimensionY/spaceY+1
	# numGridX = int(dimensionX/outSpaceX)
	# numGridY = int(dimensionY/outSpaceY)


	response = np.empty((numGridY, numGridX))
	dis = np.empty((numLayer, block_size))
	# iterate through each grid points
	for i in range(0, numGridX):
		j = 0
		while j < numGridY:
			x_coor = i
			y_coor = j

			for k in range(0, numLayer):
				# data = loadFile(filename, 136, 181, k, x_coor, y_coor, block_size)
				data = loadFile(filename, 136, 181, k, y_coor, x_coor, block_size)

				dis[k] = data[::3]


			for k in range(0, block_size):
				response[j+k][i] = dis[:,k][490]
				# acc = dis_to_acc(dis[:,k], deltaT)
				# response[j+k][i] = max_osc_response(acc, deltaT, 0.05, period, 0, 0)[typeDic[responseType]]
				# response[j+block_size-k-1][numGridX-i-1] = max_osc_response(acc, deltaT, 0.05, period, 0, 0)[typeDic[responseType]]
				# try:
				# 	response[j+block_size-k][i] = max_osc_response(acc, deltaT, 0.05, period, 0, 0)[typeDic[responseType]]
				# except IndexError:
				# 	pass
			j+=block_size
		show_progress(i, numGridX)
	sys.stdout.write('\n')
	plot(response, colorMap)




