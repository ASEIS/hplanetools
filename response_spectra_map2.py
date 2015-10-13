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
from userInput import *
from response_spectra_map import *
np.seterr(divide='ignore', invalid='ignore')

# def loadFile(fp, numGridX, numGridY, num_layers, x_coor, y_coor, size):
# 	"""load the displacement data at given grid point"""
# 	fp = userInput.fp
# 	numGridX = userInput.numGridX
# 	numGridY = userInput.numGridY
# 	try:
# 		size = userInput.size
# 	except AttributeError:
# 		size = 1
# 	dis = np.array([], float)
# 	base = numGridX*numGridY*3*num_layers # number of data in past layers
# 	index = base + (numGridX*x_coor+y_coor)*3 # number of data in past layers + postion in current layer
# 	offset = index*8 # offset measured in byte

# 	try:
# 		dis = np.memmap(fp, np.float64, 'r', offset, (3*size)) # load three numbers for three orientations
# 		return dis
# 	except ValueError:
# 		print "[ERROR]: unable to load file."
# 		sys.exit()
# # end of loadFile

# def saveDat(dimensionX, spaceX, spaceY, plotData):
#   """print the response data in a separate file"""
#   try:
#     f = open(userInput.out_path, 'w')
#   except IOError, e:
#     print e

#   descriptor = '{:>12}'*2 + '{:>12.7f}' + '\n'
#   x = np.arange(0, dimensionX+1, spaceX, dtype=np.int)
#   for i in range(0, len(plotData)):
#     y = np.empty(len(plotData[i]), dtype = np.int)
#     y.fill(i*spaceY)
#     values = plotData[i]
#     for c0, c1, c2 in zip(x, y, values):
#       f.write(descriptor.format(c0, c1, c2))
#   f.close()
# # end of saveDat


if __name__ == "__main__":
	if len(sys.argv) > 1:
		argument = tuple(sys.argv[1:])
		userInput = ResponseInput2(*argument)
	else:
		userInput = ResponseInput2()

	compoDic = {'x':0, 'y':1, 'z':2}
	typeDic = {'a':2, 'v':'1', 'd':0}
	fp = userInput.fp
	dimensionX = userInput.dimensionX
	dimensionY = userInput.dimensionY
	spaceX = userInput.spaceX
	spaceY = userInput.spaceY
	block_size = userInput.size

	simulationTime = userInput.simulationTime
	deltaT = userInput.deltaT
	period = userInput.period
	component = userInput.component
	responseType = userInput.plotType
	colorMap = userInput.colorMap


	numLayer = int(simulationTime/deltaT)
	numGridX = dimensionX/spaceX+1
	numGridY = dimensionY/spaceY+1

	response = np.empty((numGridY, numGridX))
	dis = np.empty((numLayer, block_size))
	# iterate through each grid points
	for i in range(0, numGridY):
		j = 0
		while j < numGridX:
			if j + block_size > numGridX:
				tmp_size = numGridX-j
			else:
				tmp_size = block_size

			# load the data at each time stamp
			for k in range(0, numLayer):
				data = loadFile(fp, numGridY, numGridX, k, i, j, tmp_size)
				dis[k] = data[compoDic[component]::3]

			# for each signal, generate acceleration signal and calculate response
			for k in range(0, tmp_size):
				acc = dis_to_acc(dis[:,k], deltaT)
				response[i][j+k] = max_osc_response(acc, deltaT, 0.05, period, 0, 0)[typeDic[responseType]]
			j+=block_size
		show_progress(i, numGridY)
	sys.stdout.write('\n')
	if userInput.printDat:
		saveDat(userInput.out_path, dimensionX, spaceX, spaceY, response)
	plot(response, colorMap)



