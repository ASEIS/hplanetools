#!/usr/bin/env python
# ==========================================
# The program contians the classes that may be used by other program.
# ==========================================
import os
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


	def __init__(self):
		self.fp = self.get_fp()
		self.plotType = self.get_plotType()
		self.deltaT = self.get_deltaT()
		self.simulationTime = self.get_int('simulationTime')
		self.alongStrike = self.get_int('alongStrike')
		self.downDip = self.get_int('downDip')
		self.stepAlongStrike = self.get_int('stepAlongStrike')
		self.stepDownDip = self.get_int('stepDownDip')


		pass
	# def __init__(self, fp, plotType, deltaT, simulationTime, alongStrike, downDip, stepAlongStrike, stepDownDip, magSelect,
	# 	magnitude, scale, cumulative, snapshots, numSnapshots, barChoice, barMin, barMax, colorChoice, userColor1, userColor2, userColor3, colorMap):
	# 	self.fp = fp
	# 	self.plotType = plotType
	# 	self.deltaT = deltaT
	# 	self.simulationTime = simulationTime
	# 	self.alongStrike = alongStrike
	# 	self.downDip = downDip
	# 	self.stepAlongStrike = stepAlongStrike
	# 	self.stepDownDip = stepDownDip
	# 	self.magSelect = magSelect
	# 	self.magnitude = magnitude
	# 	self.scale = scale
	# 	self.cumulative = cumulative
	# 	self.snapshots = snapshots
	# 	self.numSnapshots = numSnapshots
	# 	self.barChoice = barChoice
	# 	self.barMin = barMin
	# 	self.barMax = barMax
	# 	self.colorChoice = colorChoice
	# 	self.userColor1 = userColor1
	# 	self.userColor2 = userColor2
	# 	self.userColor3 = userColor3
	# 	self.colorMap = colorMap
	# end of __init__

	def get_fp(self):
		fp = ''
		while not fp:
			filename = raw_input("== Enter the filename of plane data: ")
			try:
				fp = open(filename, 'r')
				return fp
			except IOError:
				print "[ERROR]: file not found."
	# end of get_fp

	def get_plotType(self):
		type_list = ['a', 'v', 'd']
		ptype = ''
		while not ptype:
			p = raw_input("== Select displacement, velocity, or acceleration (d/v/a) for plot: ")
			try:
				ptype = p.lower()[0]
				if ptype not in type_list:
					print "[ERROR]: invalid plot type."
					ptype = ''
				else:
					return ptype
			except IndexError:
				print "[ERROR]: invalid plot type."
	# end of get_plotType

	def get_deltaT(self):
		dt = 0.0
		while not dt:
			d = raw_input("== Enter dt: ")
			try:
				dt = float(d)
				return dt
			except ValueError:
				print "[ERROR]: invalid deltaT."
	# end of get_deltaT

	def get_int(self, varName):
		"""get simulationTime, alongStrike, downDip, stepAlongStrike, and stepDownDip from user."""
		value = 0
		while not value:
			i = raw_input("== Enter the value of " + varName + " : ")
			try:
				value = int(i)
				return value
			except ValueError:
				print "[ERROR]: invalid input."
	# end of get_int

	def check_size(self, filename):
		"""compare the size of given file and the estimated size"""
		stat = os.stat(filename)
		act_size = stat.st_size
		est_size = self.alongStrike*self.downDip #TODO

		if act_size != est_size:
			# TODO
			pass
	# end of check_size
# end of input

i = Input()
# print i.fp[0]
print i.plotType
print i.deltaT
print i.simulationTime
print i.alongStrike
print i.downDip
print i.alongStrike
print i.stepAlongStrike
print i.stepDownDip

