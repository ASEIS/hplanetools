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

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.grid(False)

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

		if len(params) != 8:
			print "Text file has an invalid number of parameters"
			sys.exit()

		while True:
			try:
				binaryFile = params.pop(0)
				fp = open(binaryFile, 'r')
				break
			except IOError: 
				print "Binary file not found"
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


	if count == 0:
		while True:
			try:
				fp = open(raw_input("Enter filename: "), 'r')
				break
			except IOError:
				print "File not found!"
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

	if count == 8:
		while True:
			try:
				binaryFile = sys.argv[1]
				fp = open(binaryFile, 'r')
				break
			except IOError:
				print "File not found!"
				sys.exit()

		while True:
			try:
				deltaT = sys.argv[2]
				deltaT = float(deltaT)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				simulationTime = sys.argv[3]
				simulationTime = int(simulationTime)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				alongStrike = sys.argv[4]
				alongStrike = int(alongStrike)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				downDip = sys.argv[5]
				downDip = int(downDip)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				stepAlongStrike = sys.argv[6]
				stepAlongStrike = int(stepAlongStrike)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			try:
				stepDownDip = sys.argv[7]
				stepDownDip = int(stepDownDip)
				break
			except ValueError:
				print "Parameter is of incorrect type"
				sys.exit()

		while True:
			magSelect = sys.argv[8]

			if magSelect == 'x' or magSelect == 'y' or magSelect == 'z' or magSelect == 'xy' or magSelect == 'xz' or magSelect == 'yz' or magSelect == 'xyz':
				break
			else:
				print "Invalid input for magSelect"
				sys.exit()

	if count != 0 and count != 1 and count != 8:
		print "Invalid input"
		sys.exit()

	iterations = int(simulationTime/deltaT)

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

	dis = np.fromfile(fp, np.float64, downDip*alongStrike*3)

	X = dis[::3] #take every third element starting at index 0
	Y = dis[1::3] #...starting at index 1
	Z = dis[2::3] #...starting at index 2

	disX1 = np.reshape(X, (downDip, alongStrike), order='F')
	disY1 = np.reshape(Y, (downDip, alongStrike), order='F')
	disZ1 = np.reshape(Z, (downDip, alongStrike), order='F')

''' Use the user input to decide which components to plot '''

def components():
	global peakDis

	if magSelect == "x":
		peakDis = np.maximum(peakDis, np.absolute(disX1.transpose()))

	if magSelect == "y":
		peakDis = np.maximum(peakDis, np.absolute(disY1.transpose()))

	if magSelect == "z":
		peakDis = np.maximum(peakDis, np.absolute(disZ1.transpose()))
	
	if magSelect == "xy":
		horizMag = np.sqrt(np.power(disX1, 2) + np.power(disY1, 2))
		peakDis = np.maximum(peakDis, horizMag.transpose())

	if magSelect == "yz":
		horizMag = np.sqrt(np.power(disY1, 2) + np.power(disZ1, 2))
		peakDis = np.maximum(peakDis, horizMag.transpose())

	if magSelect == "xz":
		horizMag = np.sqrt(np.power(disX1, 2) + np.power(disZ1, 2))
		peakDis = np.maximum(peakDis, horizMag.transpose())

	if magSelect == "xyz":
		totalMag = np.sqrt(np.power(disX1, 2) + np.power(disY1, 2)
		+ np.power(disZ1, 2))
		peakDis = np.maximum(peakDis, totalMag.transpose())

''' Create the plot '''

def plot():
	for a in (ax.w_xaxis, ax.w_yaxis, ax.w_zaxis):
		for t in a.get_ticklines()+a.get_ticklabels():
			t.set_visible(False)
		a.line.set_visible(False)
		a.pane.set_visible(False)\

	surf = ax.plot_surface(x, y, peakDis, cmap=cm.seismic, linewidth=0,
		antialiased=False, vmin=0, vmax=0.04, cstride=1, rstride=1, shade=True)
	ax.view_init(azim=-90, elev=90)

	m = cm.ScalarMappable(cmap=cm.seismic)
	m.set_array(peakDis)
	plt.colorbar(m)
	plt.xlabel('X')
	plt.ylabel('Y')
	plt.axis('scaled')

countArguments()
readInput()

y = np.array(range(0, stepAlongStrike*alongStrike, stepAlongStrike))
x = np.array(range(0, stepDownDip*downDip, stepDownDip))
x, y = np.meshgrid(x, y)
peakDis = np.zeros_like(x)

for i in range(0, iterations-1):

	readFile()
	components()

plot()
plt.show()