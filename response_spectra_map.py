# /*
#  ============================================================================
# Loads the plane displacement data to produce acceleration signals at each grid
# point, then generates a response spectra map of signals.
# Version: Sep 25, 2015.
#  ============================================================================
#  */
import numpy as np
import sys
sys.path.insert(0, '/Users/kelicheng/seismtools') # insert the path to seismtools to import stools program.
from stools import *
from htools import *
from userInput import *
np.seterr(divide='ignore', invalid='ignore')

def loadFile(fp, alongStrike, downDip, num_layers, x_coor, y_coor):
	"""load the displacement data at given grid point"""
	dis = np.array([], float)
	base = alongStrike*downDip*3*num_layers # number of data in past layers
	index = base + (downDip*x_coor+y_coor)*3 # number of data in past layers + postion in current layer
	offset = index*8 # offset measured in byte

	try:
		dis = np.memmap(fp, np.float64, 'r', offset, (3)) # load three numbers for three orientations
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

def saveDat(userInput, plotData):
	"""print the response data in a separate file"""
	try:
		f = open(userInput.out_path, 'w')
	except IOError, e:
		print e

	descriptor = '{:>12}'*2 + '{:>12.7f}' + '\n'
	x = np.arange(0, userInput.dimensionX+1, userInput.outspaceX, dtype=np.int)
	for i in range(0, len(plotData)):
		y = np.empty(len(plotData[i]), dtype = np.int)
		y.fill(i*userInput.outspaceY)
		values = plotData[i]
		for c0, c1, c2 in zip(x, y, values):
			f.write(descriptor.format(c0, c1, c2))
	f.close()
# end of saveDat

if __name__ == "__main__":
	if len(sys.argv) > 1:
		argument = tuple(sys.argv[1:])
		userInput = ResponseInput(*argument)
	else:
		userInput = ResponseInput()
	compoDic = {'x':0, 'y':1, 'z':2}
	typeDic = {'a':2, 'v':1, 'd':0}
	fp = userInput.fp
	dimensionX = userInput.dimensionX
	dimensionY = userInput.dimensionY
	spaceX = userInput.spaceX
	spaceY = userInput.spaceY
	outSpaceX = userInput.outspaceX
	outSpaceY = userInput.outspaceY

	simulationTime = userInput.simulationTime
	deltaT = userInput.deltaT
	period = userInput.period
	component = userInput.component
	responseType = userInput.plotType
	colorMap = userInput.colorMap


	numLayer = int(simulationTime/deltaT)
	downDip = dimensionX/spaceX+1
	alongStrike = dimensionY/spaceY+1
	numGridX = int(dimensionX/outSpaceX)+1
	numGridY = int(dimensionY/outSpaceY)+1


	response = np.empty((numGridY, numGridX))
	# iterate through each grid points
	for i in range(0, numGridX):
		for j in range(0, numGridY):
			dis = np.array([],float)

			# read the same grid point at different layer
			for k in range(0, numLayer):
				x_coor = i * (outSpaceX/spaceX)
				y_coor = j * (outSpaceY/spaceY)

				data = loadFile(fp, alongStrike, downDip, k, y_coor, x_coor)
				dis = np.append(dis, data[compoDic[component]])
			acc = dis_to_acc(dis, deltaT)

			# calculate response and put into the matrix
			response[j][i] = max_osc_response(acc, deltaT, 0.05, period, 0, 0)[typeDic[responseType]]
			# print max_osc_response(acc, deltaT, 0.05, period, 0, 0)[typeDic[responseType]]
			# response[j][i] = acc[480]

		show_progress(i, numGridX)

	sys.stdout.write('\n')
	if userInput.printDat:
		saveDat(userInput, response)
	plot(response, colorMap)

