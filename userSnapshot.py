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

class Input(object):
    fp = ""
    plotType = ""
    deltaT = 0.0
    simulationTime = 0
    alongStrike = 0
    downDip = 0
    stepAlongStrike = 0
    stepDownDip = 0
    magSelect = ""
    magnitude = ""
    scale = ""
    cumulative = ""
    snapshots = ""
    numSnapshots = 0
    barChoice = ""
    barMin = 0.0
    barMax = 0.0
    colorChoice = ""
    userColor1 = ""
    userColor2 = ""
    userColor3 = ""
    colorMap = ""

    def __init__(self, fp, plotType, deltaT, simulationTime, alongStrike, downDip, stepAlongStrike, stepDownDip, magSelect, magnitude, scale, cumulative, snapshots, numSnapshots, barChoice, barMin, barMax, colorChoice, userColor1, userColor2, userColor3, colorMap):
        self.fp = fp
        self.plotType = plotType
        self.deltaT = deltaT
        self.simulationTime = simulationTime
        self.alongStrike = alongStrike
        self.downDip = downDip
        self.stepAlongStrike = stepAlongStrike
        self.stepDownDip = stepDownDip
        self.magSelect = magSelect
        self.magnitude = magnitude
        self.scale = scale
        self.cumulative = cumulative
        self.snapshots = snapshots
        self.numSnapshots = numSnapshots
        self.barChoice = barChoice
        self.barMin = barMin
        self.barMax = barMax
        self.colorChoice = colorChoice
        self.userColor1 = userColor1
        self.userColor2 = userColor2
        self.userColor3 = userColor3
        self.colorMap = colorMap

def make_input(fp, plotType, deltaT, simulationTime, alongStrike, downDip, stepAlongStrike, stepDownDip, magSelect, magnitude, scale, cumulative, snapshots, numSnapshots, barChoice, barMin, barMax, colorChoice, userColor1, userColor2, userColor3, colorMap):
    input = Input(fp, plotType, deltaT, simulationTime, alongStrike, downDip, stepAlongStrike, stepDownDip, magSelect, magnitude, scale, cumulative, snapshots, numSnapshots, barChoice, barMin, barMax, colorChoice, userColor1, userColor2, userColor3, colorMap)
    return input

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

def testInput(request_text, error, error_message, identifier, checkChar):

    while True:
        try:
            if identifier == 'i':
                output = int(input(request_text))
                break
            if identifier == 's':
                output = raw_input(request_text)
                output = output.lower()
                for i in range(len(error)):
                    if checkChar == True:
                        if output == error[i][0]:
                            return output
                        if output == error[i]:
                            output = error[i][0]
                            return output
                    else:
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

def testInput_text(textFile, error, error_message, identifier, checkChar):

    try:
        output = textFile.pop(0)

        if identifier == 'i':
            output = int(output)
            return output

        if identifier == 'f':
            output = float(output)
            return output

        if identifier == 's':
            output = output.lower()
            for i in range(len(error)):
                if checkChar == True:
                    if output == error[i][0]:
                        return output
                    if output == error[i]:
                        output = error[i][0]
                        return output
                else:
                    if output == error[i]:
                        return output
            print error_message
            sys.exit()

    except error:
        print error_message
        sys.exit()

''' Test the input when parameters are read from the terminal '''

def testInput_terminal(error, error_message, identifier, inputCount, checkChar):

    try:
        output = sys.argv[inputCount]

        if identifier == 'i':
            output = int(output)

        if identifier == 'f':
            output = float(output)

        if identifier == 's':
            output = output.lower()
            for i in range(len(error)):
                if checkChar == True:
                    if output == error[i][0]:
                        return output
                    if output == error[i]:
                        output = error[i][0]
                        return output
                else:
                    if output == error[i]:
                        return output
            print error_message
            sys.exit()

        return output

    except error:
        print error_message
        sys.exit()


def getInput(count, userInput):

    if count == 0:
        while True:
            try:
                fp = open(raw_input("Enter filename: "), 'r')
                break
            except IOError:
                print "File not found!"

        checkList = (["displacement", "velocity", "acceleration"])
        plotType = testInput("displacement, velocity, or acceleration plot? ", checkList,
             "Invalid input for plotType", 's', True)

        deltaT = testInput("Enter a value for deltaT: ", NameError, 
            "Parameter is of incorrect type", 'f', False)

        simulationTime = testInput("Enter a value for the simulationTime: ", 
            NameError, "Parameter is of incorrect type", 'i', False)

        alongStrike = testInput("Enter an integer value for alongStrike: ",
            NameError, "Parameter is of incorrect type", 'i', False)

        downDip = testInput("Enter an integer value for downDip: ",
            NameError, "Parameter is of incorrect type", 'i', False)

        stepAlongStrike = testInput("Enter an integer value for stepAlongStrike: ",
            NameError, "Parameter is of incorrect type", 'i', False)

        stepDownDip = testInput("Enter an integer value for stepDownDip: ",
            NameError, "Parameter is of incorrect type", 'i', False)

        while True:
            magSelect = raw_input("Enter the axis to plot: ")
            magSelect = magSelect.lower()
            if 'x' in magSelect or 'y' in magSelect or 'z' in magSelect:
                magSelect = define_mag(magSelect)
                break
            else:
                print "Invalid input for magSelect"

        if len(magSelect) == 1:
            checkList = (["yes", "no"])
            magnitude = testInput("Would you like to plot the magnitude? ",
                checkList, """ Please enter "yes" or "no" """, 's', True)
        else:
            magnitude = "y"
            
    if len(userInput.magSelect) == 1:
        checkList = (["yes", "no"])
        magnitude = testInput("Would you like to plot the magnitude? ",
            checkList, """ Please enter "yes" or "no" """, 's', True)
    else:
        magnitude = "y"

    checkList = (["linear", "log", "logarithmic"])
    scale = testInput("Plot using linear scale or logarithmic scale? ", 
        checkList, """ Please enter "linear" or logarithmic """, 's', False)

    checkList = (["yes", "no"])
    cumulative = testInput("Is this a cumulative plot? ", checkList,
        """ Please enter "yes" or "no" """, 's', True)

    checkList = (["final", "multiple"])
    snapshots = testInput("Display only the final snapshot or multiple snapshots? ",
        checkList, """Please enter "final" or "multiple" """, 's', True)

    if snapshots == "m":
        numSnapshots = testInput("How many snapshots to take? ", checkList,
            "Please enter an integer", 'i', False)
    else:
        numSnapshots = 0

    checkList = (["yes", "no"])
    barChoice = testInput("Set colorbar minimum and maximum? ", checkList,
        """ Please enter "yes" or "no" """, 's', True)

    if barChoice == "yes" or barChoice == "y":
        barMin = testInput("Enter the minimum value for the colorbar: ",
            NameError, "Parameter is of incorrect type", 'f', False)
        barMax = testInput("Enter the maximum value for the colorbar: ",
            NameError, "Parameter is of incorrect type", 'f', False)
    else:
        barMin = 0.0
        barMax = 0.0

    checkList = (["color map", "custom colors", "map", "colors", "custom"])
    colorChoice = testInput("Use a color map or custom colors? ", checkList, 
        """ Please enter "map" or "custom" """, 's', False)

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

    if count == 9:
        userInput = make_input(userInput.fp, userInput.plotType, userInput.deltaT, userInput.simulationTime, userInput.alongStrike, userInput.downDip, userInput.stepAlongStrike, userInput.stepDownDip, userInput.magSelect, magnitude, scale, cumulative, snapshots, numSnapshots, barChoice, barMin, barMax, colorChoice, userColor1, userColor2, userColor3, colorMap)
    else:
        userInput = make_input(fp, plotType, deltaT, simulationTime, alongStrike, downDip, stepAlongStrike, stepDownDip, magSelect, magnitude, scale, cumulative, snapshots, numSnapshots, barChoice, barMin, barMax, colorChoice, userColor1, userColor2, userColor3, colorMap)
    return userInput

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

        # if len(params) < 13 and len(params) > 16:
        #     print "Text file has an invalid number of parameters"
        #     sys.exit()

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
            "Invalid input for plotType", 's', True)

        deltaT = testInput_text(params, ValueError, 
            "Parameter deltaT is of incorrect type", 'f', False)

        simulationTime = testInput_text(params, ValueError,
            "Parameter simulationTime is of incorrect type", 'i', False)

        alongStrike = testInput_text(params, ValueError, 
            "Parameter alongStrike is of incorrect type", 'i', False)

        downDip = testInput_text(params, ValueError, 
            "Parameter downDip is of incorrect type", 'i', False)

        stepAlongStrike = testInput_text(params, ValueError, 
            "Parameter stepAlongStrike is of incorrect type", 'i', False)

        stepDownDip = testInput_text(params, ValueError, 
            "Parameter stepDownDip is of incorrect type", 'i', False)

        while True:
            magSelect = params.pop(0)
            magSelect = magSelect.lower()
            if 'x' in magSelect or 'y' in magSelect or 'z' in magSelect:
                magSelect = define_mag(magSelect)
                break
            else:
                print "Invalid input for magSelect"
                sys.exit()

        if len(magSelect) == 1:
            checkList = (["yes", "no"])
            magnitude = testInput_text(params, checkList,
                "Invalid input for magnitude", 's', True)
        else:
            magnitude = "y"

        checkList = (["linear", "logarithmic", "log"])
        scale = testInput_text(params, checkList, 
            "Invalid input for plotType", 's', False)

        checkList = (["yes", "no"])
        cumulative = testInput_text(params, checkList,
            "Invalid input for cumulative", 's', True)

        checkList = (["final", "multiple"])
        snapshots = testInput_text(params, checkList,
            "Invalid input for snapshots", 's', True)

        if snapshots == "multiple":
            numSnapshots = testInput_text(params, ValueError,
                "Parameter numSnapshots is of incorrect type", 'i', False)
        else:
            numSnapshots = 0

        checkList = (["yes", "no"])
        barChoice = testInput_text(params, checkList,
            "Invalid input for barChoice", 's', True)

        if barChoice == "yes":
            barMin = testInput_text(params, ValueError,
                "Parameter barMin is of incorrect type", 'f', False)
            barMax = testInput_text(params, ValueError,
                "Parameter barMax is of incorrect type", 'f', False)
        else:
            barMin = 0.0
            barMax = 0.0

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

        userInput = make_input(fp, plotType, deltaT, simulationTime, alongStrike, downDip, stepAlongStrike, stepDownDip, magSelect, magnitude, scale, cumulative, snapshots, numSnapshots, barChoice, barMin, barMax, colorChoice, userColor1, userColor2, userColor3, colorMap)

    if count == 0:
        userInput = make_input("", "", 0.0, 0, 0, 0, 0, 0, "", "", "", "", "", 0, "", 0.0, 0.0, "", "", "", "", "")
        userInput = getInput(count, userInput)

    if count == 9:
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
            "Invalid input for plotType", 's', 2, True)

        deltaT = testInput_terminal(ValueError, 
            "deltaT is of incorrect type", 'f', 3, False)

        simulationTime = testInput_terminal(ValueError,
            "simulationTime is of incorrect type", 'i', 4, False)

        alongStrike = testInput_terminal(ValueError, 
            "alongStrike is of incorrect type", 'i', 5, False)

        downDip = testInput_terminal(ValueError,
            "downDip is of incorrect type", 'i', 6, False)

        stepAlongStrike = testInput_terminal(ValueError,
            "stepAlongStrike is of incorrect type", 'i', 7, False)

        stepDownDip = testInput_terminal(ValueError,
            "stepDownDip is of incorrect type", 'i', 8, False)

        while True:
            magSelect = sys.argv[9]
            magSelect = magSelect.lower()
            if 'x' in magSelect or 'y' in magSelect or 'z' in magSelect:
                magSelect = define_mag(magSelect)
                break
            else:
                print "Invalid input for magSelect"
                sys.exit()

        userInput = make_input(fp, plotType, deltaT, simulationTime, alongStrike, downDip, stepAlongStrike, stepDownDip, magSelect, "", "", "", "", 0, "", 0.0, 0.0, "", "", "", "", "")
        userInput = getInput(count, userInput)

    if count != 0 and count != 1 and count != 9:
        print "Invalid input"
        sys.exit()

    return userInput

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

''' return the peak value based on magnitude and cumulative inputs '''

def cumulativeMag(peak, userInput, matrix):

    if userInput.magnitude == "y" and userInput.cumulative == "y":
        peak = np.maximum(peak, np.absolute(matrix.transpose()))
    if userInput.magnitude == "y" and userInput.cumulative == "n":
        peak = np.absolute(matrix.transpose())
    if userInput.magnitude == "n" and userInput.cumulative == "y":
        peak = np.maximum(peak, matrix.transpose())
    if userInput.magnitude == "n" and userInput.cumulative == "n":
        peak = matrix.transpose()

    return peak

''' Use the user input to decide which components to use for 
    displacement plots '''

def disComponents(peak, userInput, disX1, disY1, disZ1):

    if userInput.magSelect == [0]:
        peak = cumulativeMag(peak, userInput, disX1)

    if userInput.magSelect == [1]:
        peak = cumulativeMag(peak, userInput, disY1)

    if userInput.magSelect == [2]:
        peak = cumulativeMag(peak, userInput, disZ1)
    
    if userInput.magSelect == [0,1]:
        horizMag = np.sqrt(np.power(disX1, 2) + np.power(disY1, 2))
        peak = np.maximum(peak, horizMag.transpose())

    if userInput.magSelect == [1,2]:
        horizMag = np.sqrt(np.power(disY1, 2) + np.power(disZ1, 2))
        peak = cumulativeMag(peak, userInput, horizMag)

    if userInput.magSelect == [0,2]:
        horizMag = np.sqrt(np.power(disX1, 2) + np.power(disZ1, 2))
        peak = cumulativeMag(peak, userInput, horizMag)

    if userInput.magSelect == [0,1,2]:
        totalMag = np.sqrt(np.power(disX1, 2) + np.power(disY1, 2)
        + np.power(disZ1, 2))
        peak = cumulativeMag(peak, userInput, totalMag)

    return peak

def velComponents(peak, userInput, velX, velY, velZ):

    if userInput.magSelect == [0]:
        peak = peak = cumulativeMag(peak, userInput, velX)

    if userInput.magSelect == [1]:
        peak = cumulativeMag(peak, userInput, velY)

    if userInput.magSelect == [2]:
        peak = cumulativeMag(peak, userInput, velZ)

    if len(userInput.magSelect) == 2:

        if userInput.magSelect == [0,1]:
            horizMag = np.sqrt(np.power(velX, 2) + np.power(velY, 2))

        if userInput.magSelect == [1,2]:
            horizMag = np.sqrt(np.power(velY, 2) + np.power(velZ, 2))

        if userInput.magSelect == [0,2]:
            horizMag = np.sqrt(np.power(velX, 2) + np.power(velZ, 2))

        peak = cumulativeMag(peak, userInput, horizMag)

    if userInput.magSelect == [0,1,2]:
        totalMag = np.sqrt(np.power(velX, 2) + np.power(velY, 2)
        + np.power(velZ, 2))
        peak = cumulativeMag(peak, userInput, totalMag)

    return peak

def accelComponents(peak, userInput, accelX, accelY, accelZ):

    if userInput.magSelect == [0]:
        peak = cumulativeMag(peak, userInput, accelX)

    if userInput.magSelect == [1]:
        peak = cumulativeMag(peak, userInput, accelY)

    if userInput.magSelect == [2]:
        peak = cumulativeMag(peak, userInput, accelZ)

    if len(userInput.magSelect) == 2:
        if userInput.magSelect == [0,1]:
            horizMag = np.sqrt(np.power(accelX, 2) + np.power(accelY, 2))

        if userInput.magSelect == [1,2]:
            horizMag = np.sqrt(np.power(accelY, 2) + np.power(accelZ, 2))

        if userInput.magSelect == [0,2]:
            horizMag = np.sqrt(np.power(accelX, 2) + np.power(accelZ, 2))

        peak = cumulativeMag(peak, userInput, horizMag)

    if userInput.magSelect == [0,1,2]:
        totalMag = np.sqrt(np.power(accelX, 2) + np.power(accelY, 2)
        + np.power(accelZ, 2))
        peak = cumulativeMag(peak, userInput, totalMag)

    return peak

''' Set up our arrays and matrices '''

def matrices(userInput):

    y = np.array(range(0, userInput.stepAlongStrike*userInput.alongStrike, userInput.stepAlongStrike))
    x = np.array(range(0, userInput.stepDownDip*userInput.downDip, userInput.stepDownDip))
    x, y = np.meshgrid(x, y)
    peak = np.zeros_like(x)

    return peak

''' Read the binary file input by the user, take the X, Y, and Z
    values and reshape into a matrix '''

def readFile(userInput):

    dis = np.fromfile(userInput.fp, np.float64, userInput.downDip*userInput.alongStrike*3)

    X = dis[::3] #take every third element starting at index 0
    Y = dis[1::3] #...starting at index 1
    Z = dis[2::3] #...starting at index 2

    disX = np.reshape(X, (userInput.downDip, userInput.alongStrike), order='F')
    disY = np.reshape(Y, (userInput.downDip, userInput.alongStrike), order='F')
    disZ = np.reshape(Z, (userInput.downDip, userInput.alongStrike), order='F')

    return disX, disY, disZ

''' For velocity plots '''

def readVelocity(peak, userInput, disX1, disY1, disZ1):

    disX2, disY2, disZ2 = readFile(userInput)

    velX = (1/userInput.deltaT)*(disX2-disX1)
    velY = (1/userInput.deltaT)*(disY2-disY1)
    velZ = (1/userInput.deltaT)*(disZ2-disZ1)

    peak = velComponents(peak, userInput, velX, velY, velZ)
    disX1 = disX2
    disY1 = disY2
    disZ1 = disZ2

    return peak, disX1, disY1, disZ1

''' For acceleration plots '''

def readAcceleration(peak, userInput, disX1, disY1, disZ1, disX2, disY2, disZ2):

    disX3, disY3, disZ3 = readFile(userInput)

    accelX = (disX3-(2*disX2)-disX1)/(np.power(userInput.deltaT, 2))
    accelY = (disY3-(2*disY2)-disY1)/(np.power(userInput.deltaT, 2))
    accelZ = (disZ3-(2*disZ2)-disZ1)/(np.power(userInput.deltaT, 2))

    peak = accelComponents(peak, userInput, accelX, accelY, accelZ)
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

def createSnapshots(time, peak, counting, userInput):

    if i > 1:
        if i%(time/userInput.numSnapshots) == 0:
            counting = plot(peak, counting, userInput)

    return counting

''' Create the plot '''

def plot(peak, counting, userInput):

    counting = counting + 1

    if userInput.colorChoice == 'colors' or userInput.colorChoice == 'custom colors' or userInput.colorChoice == 'custom':
        c = colors.ColorConverter().to_rgb
        userInput.colorMap = make_colormap(
        [c(userInput.userColor1), c(userInput.userColor2), 0.5, 
        c(userInput.userColor2), c(userInput.userColor3), 1, 
        c(userInput.userColor3)])

    if userInput.barChoice == "y":
        im = plt.imshow(peak, vmin=userInput.barMin, 
            vmax=userInput.barMax, cmap=userInput.colorMap)
    else:
        im = plt.imshow(peak, cmap=userInput.colorMap)

    plt.axis('off')
    plt.gca().invert_yaxis()

    plt.colorbar(im)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.suptitle('t = ' + (str)((int)(i*userInput.deltaT)), fontsize=20)
    plt.axis('scaled')

    if userInput.plotType == 'd':
        plt.savefig("displacement" + str(counting) + ".png")
    if userInput.plotType == 'v':
        plt.savefig("velocity" + str(counting) + ".png")
    if userInput.plotType == 'a':
        plt.savefig("acceleration" + str(counting) + ".png")

    plt.show()
    return counting

counting = 0
count = countArguments()
userInput = readInput(count)

iterations = int(userInput.simulationTime/userInput.deltaT)
runtime = iterations-1

if userInput.plotType == 'd':
    start = 0
if userInput.plotType == 'v':
    start = 1

if userInput.plotType == 'v' or userInput.plotType == 'a':
    disX1, disY1, disZ1 = readFile(userInput)
    if userInput.plotType == 'a':
        disX2, disY2, disZ2 = readFile(userInput)
        start = 2

peak = matrices(userInput)

for i in range(start, runtime):

    if userInput.plotType == 'd':
        disX1, disY1, disZ1 = readFile(userInput)
        peak = disComponents(peak, userInput, disX1, disY1, disZ1)

    if userInput.plotType == 'v':
        peak, disX1, disY1, disZ1 = readVelocity(peak, userInput, disX1, disY1, disZ1)

    if userInput.plotType == 'a':
        peak, disX1, disY1, disZ1, disX2, disY2, disZ2 = readAcceleration(peak, userInput, disX1, disY1, disZ1, disX2, disY2, disZ2)

    if userInput.numSnapshots != 0:
        counting = createSnapshots(runtime, peak, counting, userInput)

    percent = float(i)/runtime
    hashes = '#'*int(round(percent*20))
    spaces = ' '*(20-len(hashes))
    sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes+spaces, int(round(percent*100))))
    sys.stdout.flush()

if userInput.numSnapshots == 0:
    plot(peak, counting, userInput)