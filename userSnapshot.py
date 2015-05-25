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

for i in range(0, 10000):
	try:
		check = sys.argv[i]
		count = i
	except IndexError:
		break

if count == 1:
	inFile = sys.argv[1]
	file = open(inFile)
	for line in file:
		params = line.split(' ')

	binaryFile = params.pop(0)
	fp = open(binaryFile, 'r')

	deltaT = params.pop(0)
	deltaT = float(deltaT)

	simulationTime = params.pop(0)
	simulationTime = int(simulationTime)

	alongStrike = params.pop(0)
	alongStrike = int(alongStrike)

	downDip = params.pop(0)
	downDip = int(downDip)

	stepAlongStrike = params.pop(0)
	stepAlongStrike = int(stepAlongStrike)

	stepDownDip = params.pop(0)
	stepDownDip = int(stepDownDip)

	magSelect = params.pop(0)

if count == 0:
	fp = file(raw_input("Enter filename: "), 'r')

	deltaT = float(input("Enter a value for deltaT: "))
	simulationTime = int(input("Enter a value for the simulationTime: "))

	alongStrike = int(input("Enter an integer value for alongStrike: "))
	downDip = int(input("Enter an integer value for downDip: "))

	stepAlongStrike = int(input("Enter an integer value for stepAlongStrike: "))
	stepDownDip = int(input("Enter an integer value for stepDownDip: "))

	# magSelect = raw_input("singleComponent, horizontalMagnitude, or totalMagnitude plot? ")
	magSelect = raw_input("Enter the type of plot: ")

if count == 8:
	binaryFile = sys.argv[1]
	fp = open(binaryFile, 'r')

	deltaT = sys.argv[2]
	deltaT = float(deltaT)

	simulationTime = sys.argv[3]
	simulationTime = int(simulationTime)

	alongStrike = sys.argv[4]
	alongStrike = int(alongStrike)

	downDip = sys.argv[5]
	downDip = int(downDip)

	stepAlongStrike = sys.argv[6]
	stepAlongStrike = int(stepAlongStrike)

	stepDownDip = sys.argv[7]
	stepDownDip = int(stepDownDip)

	magSelect = sys.argv[8]

if count != 0 and count != 1 and count != 8:
	print "invalid input"

y = np.array(range(0, stepAlongStrike*alongStrike, stepAlongStrike))
x = np.array(range(0, stepDownDip*downDip, stepDownDip))
x, y = np.meshgrid(x, y)
peakDis = np.zeros_like(x)

iterations = int(simulationTime/deltaT)

for i in range(0, iterations-1):

	dis = np.fromfile(fp, np.float64, downDip*alongStrike*3)

	X = dis[::3] #take every third element starting at index 0
	Y = dis[1::3] #...starting at index 1
	Z = dis[2::3] #...starting at index 2

	disX1 = np.reshape(X, (downDip, alongStrike), order='F')
	disY1 = np.reshape(Y, (downDip, alongStrike), order='F')
	disZ1 = np.reshape(Z, (downDip, alongStrike), order='F')

	totalMag = np.sqrt(np.power(disX1, 2) + np.power(disY1, 2)
		+ np.power(disZ1, 2))

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
		peakDis = np.maximum(peakDis, totalMag.transpose())

for a in (ax.w_xaxis, ax.w_yaxis, ax.w_zaxis):
	for t in a.get_ticklines()+a.get_ticklabels():
		t.set_visible(False)
	a.line.set_visible(False)
	a.pane.set_visible(False)

surf = ax.plot_surface(x, y, peakDis, cmap=cm.seismic, linewidth=0,
	antialiased=False, vmin=0, vmax=0.04, cstride=1, rstride=1, shade=True)
ax.view_init(azim=-90, elev=90)

m = cm.ScalarMappable(cmap=cm.seismic)
m.set_array(peakDis)
plt.colorbar(m)
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('scaled')
time.sleep(0.1)

plt.show()