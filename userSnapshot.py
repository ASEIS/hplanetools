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

		if len(params) != 11 and len(params) != 13:
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

		while True:
			plotType = params.pop(0)

			if plotType == 'displacement' or plotType == 'velocity' or plotType == 'acceleration':
				break
			else:
				print "Invalid input for plotType"
				sys.exit()

		while True:
			try:
				deltaT = params.pop(0)
				deltaT = float(deltaT)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				simulationTime = params.pop(0)
				simulationTime = int(simulationTime)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				alongStrike = params.pop(0)
				alongStrike = int(alongStrike)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				downDip = params.pop(0)
				downDip = int(downDip)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				stepAlongStrike = params.pop(0)
				stepAlongStrike = int(stepAlongStrike)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				stepDownDip = params.pop(0)
				stepDownDip = int(stepDownDip)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			magSelect = params.pop(0)

			if magSelect == 'x' or magSelect == 'y' or magSelect == 'z' or magSelect == 'xy' or magSelect == 'xz' or magSelect == 'yz' or magSelect == 'xyz':
				break
			else:
				print "Invalid input for magSelect"
				sys.exit()

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

		while True:
			plotType = raw_input("Displacement, velocity, or acceleration plot?  ")

			if plotType == 'displacement' or plotType == 'velocity' or plotType == 'acceleration':
				break
			else:
				print "Invalid input for plotType"

		while True:
			try:
				deltaT = float(input("Enter a value for deltaT: "))
				break
			except NameError:
				print "Parameter is of incorrect type"

		while True:
			try:
				simulationTime = int(input("Enter a value for the simulationTime: "))
				break
			except NameError:
				print "Parameter is of incorrect type"

		while True:
			try:
				alongStrike = int(input("Enter an integer value for alongStrike: "))
				break
			except NameError:
				print "Parameter is of incorrect type"

		while True:
			try:
				downDip = int(input("Enter an integer value for downDip: "))
				break
			except NameError:
				print "Parameter is of incorrect type"

		while True:
			try:
				stepAlongStrike = int(input("Enter an integer value for stepAlongStrike: "))
				break
			except NameError:
				print "Parameter is of incorrect type"

		while True:
			try:
				stepDownDip = int(input("Enter an integer value for stepDownDip: "))
				break
			except NameError:
				print "Parameter is of incorrect type"

		while True:
			magSelect = raw_input("Enter the type of plot: ")

			if magSelect == 'x' or magSelect == 'y' or magSelect == 'z' or magSelect == 'xy' or magSelect == 'xz' or magSelect == 'yz' or magSelect == 'xyz':
				break
			else:
				print "Invalid input for magSelect"

		while True:
			colorChoice = raw_input("Use a a color map or custom colors? ")

			if colorChoice == 'color map' or colorChoice == 'custom colors' or colorChoice == 'map' or colorChoice == 'colors' or colorChoice == 'custom':
				break
			else:
				print """ Please enter "map" or "custom" """

		if colorChoice == 'map' or colorChoice == 'color map':
			colorMap = raw_input("Enter the colormap for the plot: ")

		if colorChoice == 'colors' or colorChoice == 'custom colors' or colorChoice == 'custom':
			userColor1 = raw_input("Enter the first color: ")
			userColor2 = raw_input("Enter the second color: ")
			userColor3 = raw_input("Enter the third color: ")

	if count == 11 or count == 13:
		while True:
			try:
				binaryFile = sys.argv[1]
				fp = open(binaryFile, 'r')
				break
			except IOError:
				print "File not found!"
				sys.exit()

		while True:
			plotType = sys.argv[2]

			if plotType == 'displacement' or plotType == 'velocity' or plotType == 'acceleration':
				break

			else:
				print "Invalid input for plotType"
				sys.exit()

		while True:
			try:
				deltaT = sys.argv[3]
				deltaT = float(deltaT)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				simulationTime = sys.argv[4]
				simulationTime = int(simulationTime)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				alongStrike = sys.argv[5]
				alongStrike = int(alongStrike)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				downDip = sys.argv[6]
				downDip = int(downDip)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				stepAlongStrike = sys.argv[7]
				stepAlongStrike = int(stepAlongStrike)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				stepDownDip = sys.argv[8]
				stepDownDip = int(stepDownDip)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			magSelect = sys.argv[9]

			if magSelect == 'x' or magSelect == 'y' or magSelect == 'z' or magSelect == 'xy' or magSelect == 'xz' or magSelect == 'yz' or magSelect == 'xyz':
				break
			else:
				print "Invalid input for magSelect"
				sys.exit()
		while True:
			colorChoice = sys.argv[10]

			if colorChoice == 'map' or colorChoice == 'colormap' or colorChoice == 'colors' or colorChoice == 'custom':
				break
			else: 
				print "Invalid input for colorChoice"
				sys.exit()

		if colorChoice == 'map' or colorChoice == 'colormap':
			colorMap = sys.argv[11]
			print colorMap

		else:
			userColor1 = sys.argv[11]
			userColor2 = sys.argv[12]
			userColor3 = sys.argv[13]


	if count != 0 and count != 1 and count != 11 and count != 13:
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

''' Create the plot '''

def plot():
	global colorMap
	global counting

	counting = counting + 1

	if colorChoice == 'colors' or colorChoice == 'custom colors' or colorChoice == 'custom':
		colorMap = colors.ListedColormap([userColor1, userColor2, userColor3])

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

			if i == int(runtime/10) or i == int(runtime/5):
				plot()
			if i == int(runtime/3.3333333) or i == int(runtime/2.5):
				plot()
			if i == int(runtime/2) or i == int(runtime/1.6666667):
				plot()
			if i == int(runtime/1.4285714) or i == int(runtime/1.25):
				plot()
			if i == int(runtime/1.11111112):
				plot()

		if plotType == 'velocity':
			readVelocity()

			if i == int(runtime/10) or i == int(runtime/5):
				plot()
			if i == int(runtime/3.3333333) or i == int(runtime/2.5):
				plot()
			if i == int(runtime/2) or i == int(runtime/1.6666667):
				plot()
			if i == int(runtime/1.4285714) or i == int(runtime/1.25):
				plot()
			if i == int(runtime/1.11111112):
				plot()

if plotType == 'acceleration':
	for i in range(2, runtime):
		readAcceleration()

		if i == int(runtime/10) or i == int(runtime/5):
			plot()
		if i == int(runtime/3.3333333) or i == int(runtime/2.5):
			plot()
		if i == int(runtime/2) or i == int(runtime/1.6666667):
			plot()
		if i == int(runtime/1.4285714) or i == int(runtime/1.25):
			plot()
		if i == int(runtime/1.11111112):
			plot()


plot()
plt.show()