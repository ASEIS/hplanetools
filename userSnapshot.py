#!/usr/bin/env python

import numpy as np
import sys
import array
import time
import math
from mpl_toolkits.mplot3d import proj3d
import matplotlib.pyplot as plt 
import matplotlib.mlab as ml
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import colors

''' Check how many arguments the user inputs '''

def countArguments():
	count = 0
	for i in range(0, 10000):
		try:
			check = sys.argv[i]
			count = i
		except IndexError:
			break
	return count

''' Test the input when parameters are input by the user individually '''

def testInput(request_text, error, error_message, identifier):

	while True:
		try:
			if identifier == 'i':
				output = int(input(request_text))
				break
			if identifier == 's':
				output = raw_input(request_text)
				for i in range(len(error)):
					if output == error[i]:
						return output
				print error_message

			if identifier == 'f':
				output = float(input(request_text))
				break

		except error:
			print error_message

	return output

''' Test the input when parameters are read from a text file '''

def testInput_text(textFile, error, error_message, identifier):

	try:
		output = textFile.pop(0)

		if identifier == 'i':
			output = int(output)
			return output

		if identifier == 'f':
			output = float(output)
			return output

		if identifier == 's':
			for i in range(len(error)):
				if output == error[i]:
					return output
			print error_message
			sys.exit()

	except error:
		print error_message
		sys.exit()

''' Test the input when parameters are read from the terminal '''

def testInput_terminal(error, error_message, identifier, inputCount):

	try:
		output = sys.argv[inputCount]

		if identifier == 'i':
			output = int(output)

		if identifier == 'f':
			output = float(output)

		if identifier == 's':
			for i in range(len(error)):
				if output == error[i]:
					return output
			print error_message
			sys.exit()

		return output

	except error:
		print error_message
		sys.exit()

''' Decide how to collect the data through user input, a text file
	for if it's already been input through the terminal. This is
	decided by how many arguments the user input '''

def readInput(count):

	if count == 1:
		while True:
			try:
				inFile = sys.argv[1]
				file = open(inFile)
				for line in file:
					params = line.split(' ')
				if open(inFile): break
			except IOError:
				print "File not found!"
				sys.exit()

		if len(params) != 13 and len(params) != 15:
			print "Text file has an invalid number of parameters"
			sys.exit()

		while True:
			try:
				binaryFile = params.pop(0)
				fp = open(binaryFile, 'r')
				break
			except IOError: 
				print "Binary file not found"
				sys.exit

		checkList = (["displacement", "velocity", "acceleration"])
		plotType = testInput_text(params, checkList, 
			"Invalid input for plotType", 's')

		deltaT = testInput_text(params, ValueError, 
			"Parameter deltaT is of incorrect type", 'f')

		simulationTime = testInput_text(params, ValueError,
			"Parameter simulationTime is of incorrect type", 'i')

		alongStrike = testInput_text(params, ValueError, 
			"Parameter alongStrike is of incorrect type", 'i')

		downDip = testInput_text(params, ValueError, 
			"Parameter downDip is of incorrect type", 'i')

		stepAlongStrike = testInput_text(params, ValueError, 
			"Parameter stepAlongStrike is of incorrect type", 'i')

		stepDownDip = testInput_text(params, ValueError, 
			"Parameter stepDownDip is of incorrect type", 'i')

		while True:
			magSelect = params.pop(0)
			if 'x' in magSelect or 'y' in magSelect or 'z' in magSelect:
				magSelect = define_mag(magSelect)
				break
			else:
				print "Invalid input for magSelect"
				sys.exit()

		checkList = (["linear", "logarithmic", "log"])
		scale = testInput_text(params, checkList, 
			"Invalid input for plotType", 's')

		checkList = (["final", "ten", "10"])
		snapshots = testInput_text(params, checkList,
			"Invalid input for snapshots", 's')

		colorChoice = params.pop(0)

		if colorChoice == 'custom' or colorChoice == 'colors' or colorChoice == 'custom colors':
			userColor1 = params.pop(0)
			userColor2 = params.pop(0)
			userColor3 = params.pop(0)
			colorMap = 0

		else:
			colorMap = params.pop(0)
			userColor1 = 0
			userColor2 = 0
			userColor3 = 0

	if count == 0:

		while True:
			try:
				fp = open(raw_input("Enter filename: "), 'r')
				break
			except IOError:
				print "File not found!"

	 	checkList = (["displacement", "velocity", "acceleration"])
		plotType = testInput("displacement, velocity, or acceleration plot? ", checkList,
			"Invalid input for plotType", 's')

		deltaT = testInput("Enter a value for deltaT: ", NameError, 
			"Parameter is of incorrect type", 'f')

		simulationTime = testInput("Enter a value for the simulationTime: ", 
			NameError, "Parameter is of incorrect type", 'i')

		alongStrike = testInput("Enter an integer value for alongStrike: ",
			NameError, "Parameter is of incorrect type", 'i')

		downDip = testInput("Enter an integer value for downDip: ",
			NameError, "Parameter is of incorrect type", 'i')

		stepAlongStrike = testInput("Enter an integer value for stepAlongStrike: ",
			NameError, "Parameter is of incorrect type", 'i')

		stepDownDip = testInput("Enter an integer value for stepDownDip: ",
			NameError, "Parameter is of incorrect type", 'i')

		while True:
			magSelect = raw_input("Enter the axis to plot: ")
			if 'x' in magSelect or 'y' in magSelect or 'z' in magSelect:
				magSelect = define_mag(magSelect)
				break
			else:
				print "Invalid input for magSelect"

		checkList = (["linear", "log", "logarithmic"])
		scale = testInput("Plot using linear scale or logarithmic scale? ", 
			checkList, """ Please enter "linear" or logarithmic """, 's')

		checkList = (["final", "ten", "10"])
		snapshots = testInput("Display only the final snapshot or ten snapshots? ",
			checkList, """Please enter "final" or "ten" """, 's')

		checkList = (["color map", "custom colors", "map", "colors", "custom"])
		colorChoice = testInput("Use a color map or custom colors? ", checkList, 
			""" Please enter "map" or "custom" """, 's')

		if colorChoice == 'map' or colorChoice == 'color map':
			colorMap = raw_input("Enter the colormap for the plot: ")
			userColor1 = 0
			userColor2 = 0
			userColor3 = 0

		if colorChoice == 'colors' or colorChoice == 'custom colors' or colorChoice == 'custom':
			userColor1 = raw_input("Enter the first color: ")
			userColor2 = raw_input("Enter the second color: ")
			userColor3 = raw_input("Enter the third color: ")
			colorMap = 0

	if count == 12 or count == 13:
		while True:
			try:
				binaryFile = sys.argv[1]
				fp = open(binaryFile, 'r')
				break
			except IOError:
				print "File not found!"
				sys.exit()

		checkList = (["displacement", "velocity", "acceleration"])
		plotType = testInput_terminal(checkList, 
			"Invalid input for plotType", 's', 2)

		deltaT = testInput_terminal(ValueError, 
			"deltaT is of incorrect type", 'f', 3)

		simulationTime = testInput_terminal(ValueError,
			"simulationTime is of incorrect type", 'i', 4)

		alongStrike = testInput_terminal(ValueError, 
			"alongStrike is of incorrect type", 'i', 5)

		downDip = testInput_terminal(ValueError,
			"downDip is of incorrect type", 'i', 6)

		stepAlongStrike = testInput_terminal(ValueError,
			"stepAlongStrike is of incorrect type", 'i', 7)

		stepDownDip = testInput_terminal(ValueError,
			"stepDownDip is of incorrect type", 'i', 8)

		while True:
			magSelect = sys.argv[9]
			if 'x' in magSelect or 'y' in magSelect or 'z' in magSelect:
				magSelect = define_mag(magSelect)
				break
			else:
				print "Invalid input for magSelect"
				sys.exit()

		checkList = (["linear", "log", "logarithmic"])
		scale = testInput_terminal(checkList, 
			""" Please enter "linear" or logarithmic """, 's', 10)

		checkList = (["final", "ten", "10"])
		snapshots = testInput_terminal(checkList, 
			""" Please enter "final" or "ten" """, 's', 11)

		checkList = (["color map", "custom colors", "map", "colors", "custom"])
		colorChoice = testInput_terminal(checkList, 
			""" Please enter "map" or "custom" """, 's', 12)

		if colorChoice == 'map' or colorChoice == 'colormap':
			colorMap = sys.argv[13]
			userColor1 = 0
			userColor2 = 0
			userColor3 = 0

		else:
			userColor1 = sys.argv[13]
			userColor2 = sys.argv[14]
			userColor3 = sys.argv[15]
			colorMap = 0

	if count != 0 and count != 1 and count != 13 and count != 15:
		print "Invalid input"
		sys.exit()

	return fp, plotType, deltaT, simulationTime, alongStrike, downDip, stepAlongStrike, stepDownDip, magSelect, scale, snapshots, colorChoice, userColor1, userColor2, userColor3, colorMap

def define_mag(userString):

	charList = list(userString)
	result = []

	for i in range(len(charList)):
		if charList[i] == 'x':
			result.append(0)
		if charList[i] == 'y':
			result.append(1)
		if charList[i] == 'z':
			result.append(2)

	result = sorted(result)
	return result

''' Use the user input to decide which components to use for 
	displacement plots '''

def disComponents(peak, magSelect):

	if magSelect == [0]:
		peak = np.maximum(peak, np.absolute(disX1.transpose()))

	if magSelect == [1]:
		peak = np.maximum(peak, np.absolute(disY1.transpose()))

	if magSelect == [2]:
		peak = np.maximum(peak, np.absolute(disZ1.transpose()))
	
	if magSelect == [0,1]:
		horizMag = np.sqrt(np.power(disX1, 2) + np.power(disY1, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == [1,2]:
		horizMag = np.sqrt(np.power(disY1, 2) + np.power(disZ1, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == [0,2]:
		horizMag = np.sqrt(np.power(disX1, 2) + np.power(disZ1, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == [0,1,2]:
		totalMag = np.sqrt(np.power(disX1, 2) + np.power(disY1, 2)
		+ np.power(disZ1, 2))
		peak = np.maximum(peak, totalMag.transpose())

	return peak

def velComponents(peak, magSelect, velX, velY, velZ):

	if magSelect == [0]:
		peak = np.maximum(np.absolute(velX.transpose()), peak)

	if magSelect == [1]:
		peak = np.maximum(np.absolute(velY.transpose()), peak)

	if magSelect == [2]:
		peak = np.maximum(np.absolute(velZ.transpose()), peak)

	if len(magSelect) == 2:

		if magSelect == [0,1]:
			horizMag = np.sqrt(np.power(velX, 2) + np.power(velY, 2))

		if magSelect == [1,2]:
			horizMag = np.sqrt(np.power(velY, 2) + np.power(velZ, 2))

		if magSelect == [0,2]:
			horizMag = np.sqrt(np.power(velX, 2) + np.power(velZ, 2))

		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == [0,1,2]:
		totalMag = np.sqrt(np.power(velX, 2) + np.power(velY, 2)
		+ np.power(velZ, 2))
		peak = np.maximum(peak, totalMag.transpose())

	return peak

def accelComponents(peak, magSelect, accelX, accelY, accelZ):

	if magSelect == [0]:
		peak = np.maximum(np.absolute(accelX.transpose()), peak)

	if magSelect == [1]:
		peak = np.maximum(np.absolute(accelY.transpose()), peak)

	if magSelect == [2]:
		peak = np.maximum(np.absolute(accelZ.transpose()), peak)

	if len(magSelect) == 2:
		if magSelect == [0,1]:
			horizMag = np.sqrt(np.power(accelX, 2) + np.power(accelY, 2))

		if magSelect == [1,2]:
			horizMag = np.sqrt(np.power(accelY, 2) + np.power(accelZ, 2))

		if magSelect == [0,2]:
			horizMag = np.sqrt(np.power(accelX, 2) + np.power(accelZ, 2))

		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == [0,1,2]:
		totalMag = np.sqrt(np.power(accelX, 2) + np.power(accelY, 2)
		+ np.power(accelZ, 2))
		peak = np.maximum(peak, totalMag.transpose())

	return peak

''' Set up our arrays and matrices '''

def matrices(stepAlongStrike, alongStrike, downDip, stepDownDip):

	y = np.array(range(0, stepAlongStrike*alongStrike, stepAlongStrike))
	x = np.array(range(0, stepDownDip*downDip, stepDownDip))
	x, y = np.meshgrid(x, y)
	peak = np.zeros_like(x)

	return peak

''' Read the binary file input by the user, take the X, Y, and Z
	values and reshape into a matrix '''

def readFile(fp, downDip, alongStrike):

	dis = np.fromfile(fp, np.float64, downDip*alongStrike*3)

	X = dis[::3] #take every third element starting at index 0
	Y = dis[1::3] #...starting at index 1
	Z = dis[2::3] #...starting at index 2

	disX = np.reshape(X, (downDip, alongStrike), order='F')
	disY = np.reshape(Y, (downDip, alongStrike), order='F')
	disZ = np.reshape(Z, (downDip, alongStrike), order='F')

	return disX, disY, disZ

''' For velocity plots '''

def readVelocity(peak, magSelect, fp, downDip, alongStrike, disX1, disY1, disZ1):

	disX2, disY2, disZ2 = readFile(fp, downDip, alongStrike)

	velX = (1/deltaT)*(disX2-disX1)
	velY = (1/deltaT)*(disY2-disY1)
	velZ = (1/deltaT)*(disZ2-disZ1)

	peak = velComponents(peak, magSelect, velX, velY, velZ)
	disX1 = disX2
	disY1 = disY2
	disZ1 = disZ2

	return peak, disX1, disY1, disZ1

''' For acceleration plots '''

def readAcceleration(peak, magSelect, fp, downDip, alongStrike, disX1, disY1, disZ1, disX2, disY2, disZ2):

	disX3, disY3, disZ3 = readFile(fp, downDip, alongStrike)

	accelX = (disX3-(2*disX2)-disX1)/(np.power(deltaT, 2))
	accelY = (disY3-(2*disY2)-disY1)/(np.power(deltaT, 2))
	accelZ = (disZ3-(2*disZ2)-disZ1)/(np.power(deltaT, 2))

	peak = accelComponents(peak, magSelect, accelX, accelY, accelZ)
	return peak, disX1, disY1, disZ1, disX2, disY2, disZ2

''' for custom color maps '''

def make_colormap(seq):

    seq = [(None,) * 3, 0.0] + list(seq) + [1.0, (None,) * 3]
    cdict = {'red': [], 'green': [], 'blue': []}
    for i, item in enumerate(seq):
        if isinstance(item, float):
            r1, g1, b1 = seq[i - 1]
            r2, g2, b2 = seq[i + 1]
            cdict['red'].append([item, r1, r2])
            cdict['green'].append([item, g1, g2])
            cdict['blue'].append([item, b1, b2])
    return colors.LinearSegmentedColormap('CustomMap', cdict)

''' Create multiple snapshots '''

def createSnapshots(time, peak, counting, colorMap, colorChoice, plotType, userColor1, userColor2, userColor3):

	if i == int(time*0.1) or i == int(time*0.2):
		counting = plot(peak, counting, colorMap, colorChoice, plotType, userColor1, userColor2, userColor3)
	if i == int(time*0.3) or i == int(time*0.4):
		counting = plot(peak, counting, colorMap, colorChoice, plotType, userColor1, userColor2, userColor3)
	if i == int(time*0.5) or i == int(time*0.6):
		counting = plot(peak, counting, colorMap, colorChoice, plotType, userColor1, userColor2, userColor3)
	if i == int(time*0.7) or i == int(time*0.8):
		counting = plot(peak, counting, colorMap, colorChoice, plotType, userColor1, userColor2, userColor3)
	if i == int(time*0.9):
		counting = plot(peak, counting, colorMap, colorChoice, plotType, userColor1, userColor2, userColor3)

	return counting

''' Create the plot '''

def plot(peak, counting, colorMap, colorChoice, plotType, userColor1, userColor2, userColor3):

	counting = counting + 1

	if colorChoice == 'colors' or colorChoice == 'custom colors' or colorChoice == 'custom':
		c = colors.ColorConverter().to_rgb
		colorMap = make_colormap(
    	[c(userColor1), c(userColor2), 0.5, c(userColor2), 
    	c(userColor3), 1, c(userColor3)])

	fig = plt.imshow(peak, cmap=colorMap)

	plt.axis('off')
	plt.gca().invert_yaxis()

	m = cm.ScalarMappable(cmap=colorMap)
	m.set_array(peak)
	plt.colorbar(m)
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.axis('scaled')

	if plotType == 'displacement':
		plt.savefig("displacement" + str(counting) + ".png")
	if plotType == 'velocity':
		plt.savefig("velocity" + str(counting) + ".png")
	if plotType == 'acceleration':
		plt.savefig("acceleration" + str(counting) + ".png")

	plt.show()
	return counting

counting = 0
count = countArguments()
fp, plotType, deltaT, simulationTime, alongStrike, downDip, stepAlongStrike, stepDownDip, magSelect, scale, snapshots, colorChoice, userColor1, userColor2, userColor3, colorMap = readInput(count)

iterations = int(simulationTime/deltaT)
runtime = iterations-1

if plotType == 'displacement':
	start = 0
if plotType == 'velocity':
	start = 1

if plotType == 'velocity' or plotType == 'acceleration':
	disX1, disY1, disZ1 = readFile(fp, downDip, alongStrike)
	if plotType == 'acceleration':
		disX2, disY2, disZ2 = readFile(fp, downDip, alongStrike)
		start = 2

peak = matrices(stepAlongStrike, alongStrike, downDip, stepDownDip)

for i in range(start, runtime):

	if plotType == 'displacement':
		disX1, disY1, disZ1 = readFile(fp, downDip, alongStrike)
		peak = disComponents(peak, magSelect)

	if plotType == 'velocity':
		peak, disX1, disY1, disZ1 = readVelocity(peak, magSelect, fp, downDip, alongStrike, disX1, disY1, disZ1)

	if plotType == 'acceleration':
		peak, disX1, disY1, disZ1, disX2, disY2, disZ2 = readAcceleration(peak, magSelect, fp, downDip, alongStrike, disX1, disY1, disZ1, disX2, disY2, disZ2)

	if snapshots == "ten" or snapshots == "10":
		counting = createSnapshots(runtime, peak, counting, colorMap, colorChoice, plotType, userColor1, userColor2, userColor3)

plot(peak, counting, colorMap, colorChoice, plotType, userColor1, userColor2, userColor3)
