#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import pylab

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

while True:
    try:
        fp = open(raw_input("Enter filename of output file: "), 'r')
        break
    except IOError:
        print "File not found!"

alongStrike = testInput("Enter an integer value for alongStrike: ",
	NameError, "Parameter is of incorrect type", 'i', False)

downDip = testInput("Enter an integer value for downDip: ",
	NameError, "Parameter is of incorrect type", 'i', False)


data = []
readFile = fp.read()

getNumbers = readFile.split(" ")

for i in range(0, len(getNumbers)):
	data.append(getNumbers[i])

data = np.resize(data, [alongStrike, downDip])
data = data.astype(np.float)

im = plt.imshow(data, cmap="seismic")
plt.axis('off')
plt.gca().invert_yaxis()

plt.colorbar(im)
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('scaled')
plt.savefig("output.png")

plt.show()
