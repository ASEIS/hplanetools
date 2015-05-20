#!/usr/bin/env python

import numpy as np
import sys
import array
import time
#import json
import matplotlib.pyplot as plt 
import matplotlib.mlab as ml
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.grid(False)

try: 
	if ".txt" not in sys.argv[1]:
		userSelection = 3
	else:
		inFile = sys.argv[1]
		userSelection = 1
except IndexError:
	print "no text file" 
	userSelection = 2

if userSelection == 1:
	file = open(inFile)
	for line in file:
		params = line.split(',')

	binaryFile = params.pop(0)
	fp = open(binaryFile, 'r')


	deltaT = params.pop(0)
	deltaT = float(deltaT)

	iTimeReal = params.pop(0)
	iTimeReal = float(iTimeReal)

	alongStrike = params.pop(0)
	alongStrike = int(alongStrike)

	downDip = params.pop(0)
	downDip = int(downDip)

	stepAlongStrike = params.pop(0)
	stepAlongStrike = int(stepAlongStrike)

	stepDownDip = params.pop(0)
	stepDownDip = int(stepDownDip)

if userSelection == 2:
	fp = file(raw_input("Enter filename: "), 'r')

	deltaT = float(input("Enter a value for deltaT: "))
	iTimeReal = float(input("Enter a value for iTimeReal: "))

	alongStrike = int(input("Enter an integer value for alongStrike: "))
	downDip = int(input("Enter an integer value for downDip: "))

	stepAlongStrike = int(input("Enter an integer value for stepAlongStrike: "))
	stepDownDip = int(input("Enter an integer value for stepDownDip: "))

if userSelection == 3:
	binaryFile = sys.argv[1]
	fp = open(binaryFile, 'r')

	deltaT = sys.argv[2]
	deltaT = float(deltaT)

	iTimeReal = sys.argv[3]
	iTimeReal = float(iTimeReal)

	alongStrike = sys.argv[4]
	alongStrike = int(alongStrike)

	downDip = sys.argv[5]
	downDip = int(downDip)

	stepAlongStrike = sys.argv[6]
	stepAlongStrike = int(stepAlongStrike)

	stepDownDip = sys.argv[7]
	stepDownDip = int(stepDownDip)

y = np.array(range(0, stepAlongStrike*alongStrike, stepAlongStrike))
x = np.array(range(0, stepDownDip*downDip, stepDownDip))
x, y = np.meshgrid(x, y)
peakDis = np.zeros_like(x)

for i in range(0, 899):

	dis = np.fromfile(fp, np.float64, downDip*alongStrike*3)

	X = dis[::3] #take every third element starting at index 0
	Y = dis[1::3] #...starting at index 1
	Z = dis[2::3] #...starting at index 2

	disX1 = np.reshape(X, (downDip, alongStrike), order='F')
	disY1 = np.reshape(Y, (downDip, alongStrike), order='F')
	disZ1 = np.reshape(Z, (downDip, alongStrike), order='F')

	peakDis = np.maximum(peakDis, np.absolute(disX1.transpose()))

for a in (ax.w_xaxis, ax.w_yaxis, ax.w_zaxis):
	for t in a.get_ticklines()+a.get_ticklabels():
		t.set_visible(False)
	a.line.set_visible(False)
	a.pane.set_visible(False)

surf = ax.plot_surface(x, y, peakDis, cmap=cm.seismic, linewidth=0,
	antialiased=False, vmin=0, vmax=0.02, cstride=1, rstride=1, shade=True)
ax.view_init(azim=-90, elev=90)

m = cm.ScalarMappable(cmap=cm.seismic)
m.set_array(peakDis)
plt.colorbar(m)
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('scaled')
time.sleep(0.1)

plt.show()