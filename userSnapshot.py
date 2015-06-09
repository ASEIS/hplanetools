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
	for i in range(0, 10000):
		try:
			global count
			check = sys.argv[i]
			count = i
		except IndexError:
			break

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

def readInput():
	global fp
	global deltaT
	global simulationTime
	global alongStrike
	global downDip
	global stepAlongStrike
	global stepDownDip
	global magSelect
	global iterations
	global runtime
	global plotType
	global colorMap
	global colorChoice
	global userColor1
	global userColor2
	global userColor3
	global scale

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

		if len(params) != 12 and len(params) != 14:
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

		checkList = (["x", "y", "z", "xy", "xz", "yz", "xyz"])
		magSelect = testInput_text(params, checkList, 
			"Invalid input for magSelect", 's')

		checkList = (["linear", "logarithmic", "log"])
		scale = testInput_text(params, checkList, 
			"Invalid input for plotType", 's')

		colorChoice = params.pop(0)

		if colorChoice == 'custom' or colorChoice == 'colors' or colorChoice == 'custom colors':
			userColor1 = params.pop(0)
			userColor2 = params.pop(0)
			userColor3 = params.pop(0)

		else:
			colorMap = params.pop(0)

	if count == 0:

		while True:
			try:
				fp = open(raw_input("Enter filename: "), 'r')
				break
			except IOError:
				print "File not found!"

		checkList = (["displacement", "velocity", "acceleration"])
		plotType = ("displacement, velocity, or acceleration plot?", checkList,
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

		checkList = (["x", "y", "z", "xy", "xz", "yz", "xyz"])
		magSelect = testInput("Enter the axis to plot: ", checkList, 
			"Invalid input for magSelect", 's')

		checkList = (["linear", "log", "logarithmic"])
		scale = testInput("Plot using linear scale or logarithmic scale? ", 
			checkList, """ Please enter "linear" or logarithmic """, 's')

		checkList = (["color map", "custom colors", "map", "colors", "custom"])
		colorChoice = testInput("Use a color map or custom colors? ", checkList, 
			""" Please enter "map" or "custom" """, 's')

		if colorChoice == 'map' or colorChoice == 'color map':
			colorMap = raw_input("Enter the colormap for the plot: ")

		if colorChoice == 'colors' or colorChoice == 'custom colors' or colorChoice == 'custom':
			userColor1 = raw_input("Enter the first color: ")
			userColor2 = raw_input("Enter the second color: ")
			userColor3 = raw_input("Enter the third color: ")

	if count == 11 or count == 12:
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

		checkList = (["x", "y", "z", "xy", "xz", "yz", "xyz"])
		magSelect = testInput(checkList, 
			"Invalid input for magSelect", 's', 9)

		checkList = (["linear", "log", "logarithmic"])
		scale = testInput(checkList, 
			""" Please enter "linear" or logarithmic """, 's', 10)

		checkList = (["color map", "custom colors", "map", "colors", "custom"])
		colorChoice = testInput(checkList, 
			""" Please enter "map" or "custom" """, 's', 11)

		if colorChoice == 'map' or colorChoice == 'colormap':
			colorMap = sys.argv[12]
			print colorMap

		else:
			userColor1 = sys.argv[12]
			userColor2 = sys.argv[13]
			userColor3 = sys.argv[14]


	if count != 0 and count != 1 and count != 12 and count != 14:
		print "Invalid input"
		sys.exit()

	iterations = int(simulationTime/deltaT)
	runtime = iterations-1

''' Read the binary file input by the user, take the X, Y, and Z
	values and reshape into a matrix '''

def readFile():
	global dis
	global X
	global Y
	global Z
	global disX1
	global disY1
	global disZ1
	global disX2
	global disY2
	global disZ2

	dis = np.fromfile(fp, np.float64, downDip*alongStrike*3)

	X = dis[::3] #take every third element starting at index 0
	Y = dis[1::3] #...starting at index 1
	Z = dis[2::3] #...starting at index 2

	disX1 = np.reshape(X, (downDip, alongStrike), order='F')
	disY1 = np.reshape(Y, (downDip, alongStrike), order='F')
	disZ1 = np.reshape(Z, (downDip, alongStrike), order='F')

	if plotType == 'acceleration':

		dis = np.fromfile(fp, np.float64, downDip*alongStrike*3)

		X = dis[::3] #take every third element starting at index 0
		Y = dis[1::3] #...starting at index 1
		Z = dis[2::3] #...starting at index 2

		disX2 = np.reshape(X, (downDip, alongStrike), order='F')
		disY2 = np.reshape(Y, (downDip, alongStrike), order='F')
		disZ2 = np.reshape(Z, (downDip, alongStrike), order='F')

''' Use the user input to decide which components to plot '''

def components():
	global peak
	global velX
	global velY
	global velZ
	global accelX
	global accelY
	global accelZ

	if magSelect == "x" and plotType == "displacement":
		peak = np.maximum(peak, np.absolute(disX1.transpose()))

	if magSelect == "x"	and plotType == "velocity":
		peak = np.maximum(np.absolute(velX.transpose()), peak)

	if magSelect == "x"	and plotType == "acceleration":
		peak = np.maximum(np.absolute(accelX.transpose()), peak)

	if magSelect == "y" and plotType == "displacement":
		peak = np.maximum(peak, np.absolute(disY1.transpose()))

	if magSelect == "y" and plotType == "velocity":
		peak = np.maximum(np.absolute(velY.transpose()), peak)

	if magSelect == "y" and plotType == "acceleration":
		peak = np.maximum(np.absolute(accelY.transpose()), peak)

	if magSelect == "z" and plotType == "displacement":
		peak = np.maximum(peak, np.absolute(disZ1.transpose()))

	if magSelect == "z" and plotType == "velocity":
		peak = np.maximum(np.absolute(velZ.transpose()), peak)

	if magSelect == "z" and plotType == "acceleration":
		peak = np.maximum(np.absolute(accelZ.transpose()), peak)
	
	if magSelect == "xy" and plotType == "displacement":
		horizMag = np.sqrt(np.power(disX1, 2) + np.power(disY1, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == "xy" and plotType == "velocity":
		horizMag = np.sqrt(np.power(velX, 2) + np.power(velY, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == "xy" and plotType == "acceleration":
		horizMag = np.sqrt(np.power(accelX, 2) + np.power(accelY, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == "yz" and plotType == "displacement":
		horizMag = np.sqrt(np.power(disY1, 2) + np.power(disZ1, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == "yz" and plotType == "velocity":
		horizMag = np.sqrt(np.power(velY, 2) + np.power(velZ, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == "yz" and plotType == "acceleration":
		horizMag = np.sqrt(np.power(accelY, 2) + np.power(accelZ, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == "xz" and plotType == "displacement":
		horizMag = np.sqrt(np.power(disX1, 2) + np.power(disZ1, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == "xz" and plotType == "velocity":
		horizMag = np.sqrt(np.power(velX, 2) + np.power(velZ, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == "xz" and plotType == "acceleration":
		horizMag = np.sqrt(np.power(accelX, 2) + np.power(accelZ, 2))
		peak = np.maximum(peak, horizMag.transpose())

	if magSelect == "xyz" and plotType == "displacement":
		totalMag = np.sqrt(np.power(disX1, 2) + np.power(disY1, 2)
		+ np.power(disZ1, 2))
		peak = np.maximum(peak, totalMag.transpose())

	if magSelect == "xyz" and plotType == "velocity":
		totalMag = np.sqrt(np.power(velX, 2) + np.power(velY, 2)
		+ np.power(velZ, 2))
		peak = np.maximum(peak, totalMag.transpose())

	if magSelect == "xyz" and plotType == "acceleration":
		totalMag = np.sqrt(np.power(accelX, 2) + np.power(accelY, 2)
		+ np.power(accelZ, 2))
		peak = np.maximum(peak, totalMag.transpose())

''' Set up our arrays and matrices '''

def matrices():
	global peak

	y = np.array(range(0, stepAlongStrike*alongStrike, stepAlongStrike))
	x = np.array(range(0, stepDownDip*downDip, stepDownDip))
	x, y = np.meshgrid(x, y)
	peak = np.zeros_like(x)

''' For velocity plots '''

def readVelocity():
	global disX1
	global disY1
	global disZ1
	global peak
	global velX
	global velY
	global velZ

	dis = np.fromfile(fp, np.float64, downDip*alongStrike*3)

	X = dis[::3] #take every third element starting at index 0
	Y = dis[1::3] #...starting at index 1
	Z = dis[2::3] #...starting at index 2

	disX2 = np.reshape(X, (downDip, alongStrike), order='F')
	disY2 = np.reshape(Y, (downDip, alongStrike), order='F')
	disZ2 = np.reshape(Z, (downDip, alongStrike), order='F')

	velX = (1/deltaT)*(disX2-disX1)
	velY = (1/deltaT)*(disY2-disY1)
	velZ = (1/deltaT)*(disZ2-disZ1)

	components()
	disX1 = disX2

''' For acceleration plots '''

def readAcceleration():
	global disX1
	global disY1
	global disZ1
	global disX2
	global disY2
	global disZ2
	global accelX
	global accelY
	global accelZ

	dis = np.fromfile(fp, np.float64, downDip*alongStrike*3)

	X = dis[::3] #take every third element starting at index 0
	Y = dis[1::3] #...starting at index 1
	Z = dis[2::3] #...starting at index 2

	disX3 = np.reshape(X, (downDip, alongStrike), order='F')
	disY3 = np.reshape(Y, (downDip, alongStrike), order='F')
	disZ3 = np.reshape(Z, (downDip, alongStrike), order='F')

	accelX = (disX3-(2*disX2)-disX1)/(np.power(deltaT, 2))
	accelY = (disY3-(2*disY2)-disY1)/(np.power(deltaT, 2))
	accelZ = (disZ3-(2*disZ2)-disZ1)/(np.power(deltaT, 2))

	components()

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

''' Create the plot '''

def plot():
	global colorMap
	global counting

	counting = counting + 1

	if colorChoice == 'colors' or colorChoice == 'custom colors' or colorChoice == 'custom':
		c = colors.ColorConverter().to_rgb
		colorMap = make_colormap(
    	[c(userColor1), c(userColor2), 0.33, c(userColor2), 
    	c(userColor3), 0.66, c(userColor3)])

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

counting = 0
countArguments()
readInput()
if plotType == 'velocity' or plotType == 'acceleration':
	readFile()
matrices()

if plotType == 'displacement' or plotType == 'velocity':
	for i in range(0, runtime):
		if plotType == 'velocity' and i == 0:
			i = i+1

		if plotType == 'displacement':
			readFile()
			components()

			# if i == int(runtime*0.1) or i == int(runtime*0.2):
			# 	plot()
			# if i == int(runtime*0.3) or i == int(runtime*0.4):
			# 	plot()
			# if i == int(runtime*0.5) or i == int(runtime*0.6):
			# 	plot()
			# if i == int(runtime*0.7) or i == int(runtime*0.8):
			# 	plot()
			# if i == int(runtime*0.9):
			# 	plot()

		if plotType == 'velocity':
			readVelocity()

			# if i == int(runtime*0.1) or i == int(runtime*0.2):
			# 	plot()
			# if i == int(runtime*0.3) or i == int(runtime*0.4):
			# 	plot()
			# if i == int(runtime*0.5) or i == int(runtime*0.6):
			# 	plot()
			# if i == int(runtime*0.7) or i == int(runtime*0.8):
			# 	plot()
			# if i == int(runtime*0.9):
			# 	plot()

if plotType == 'acceleration':
	for i in range(2, runtime):
		readAcceleration()

		# if i == int(runtime*0.1) or i == int(runtime*0.2):
		# 	plot()
		# if i == int(runtime*0.3) or i == int(runtime*0.4):
		# 	plot()
		# if i == int(runtime*0.5) or i == int(runtime*0.6):
		# 	plot()
		# if i == int(runtime*0.7) or i == int(runtime*0.8):
		# 	plot()
		# if i == int(runtime*0.9):
		# 	plot()


plot()
plt.show()