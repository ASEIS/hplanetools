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
		self.magSelect, self.magnitude = self.get_mag()
		self.scale = self.get_scale()
		self.cumulative = self.get_cum()
		self.snapshots = self.get_snap()
		if self.snapshots == 'm':
			self.numSnapshots = self.get_numsnap()
		self.barChoice = self.get_bar()
		if self.barChoice:
			self.barMin, self.barMax = self.get_min_max()

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

	def get_mag(self):
		magSelect = []
		magList = ['x','y','z']
		while not magSelect:
			magSelect = raw_input("== Enter the axis to plot (x/y/z/xy..): ").lower().split()
			magSelect = list(sorted(magSelect))
			for m in magSelect:
				if m not in magList:
					print "[ERROR]: invalid axis."
					magSelect = []
					break

		# decide whether or not to plot magnitude
		magnitude = True
		bool_dict = {'y':True, 'n':False}
		if len(magSelect) == 1:
			m = ''
			while not m:
				m = raw_input("== Would you like to plot the magnitude? (y/n) ").lower()
				if m:
					if m[0] in bool_dict.keys():
						magnitude = bool_dict[m[0]]
						break
					else:
						print "[ERROR]: invalid input."
						m = ''
		return magSelect, magnitude
	# end of get_mag

	def get_scale(self):
		"""get the plotting scale from user"""
		scale_list = ["linear", "log", "logarithmic"]
		scale = ''
		while not scale:
			scale = raw_input("== Select linear or logarithmic for plot: ").lower()
			if scale in scale_list:
				return scale
			else:
				print "[ERROR]: invalid scale type."
				scale = ''
	# end of get_scale

	def get_cum(self):
		cum = ''
		bool_dict = {'y':True, 'n':False}
		while not cum:
			cum = raw_input("== Is this a cumulative plot? (y/n) ").lower()
			if cum:
				if cum[0] in bool_dict.keys():
					return bool_dict[cum[0]]
				else:
					print "[ERROR]: invalid input."
					cum = ''
	# end of get_cum

	def get_snap(self):
		snapshots =''
		while not snapshots:
			snapshots = raw_input("== Display a single plot or multiple plots? (s/m) ").lower()
			if snapshots:
				if snapshots[0] in ['s', 'm']:
					return snapshots[0]
				else:
					print "[ERROR]: invalid input."
					snapshots = ''
	# end of get_snap

	def get_numsnap(self):
		numSnapshots = 0
		while not numSnapshots:
			num = raw_input("== Enter how many seconds in between each plot: ")
			try:
				numSnapshots = int(num)
				return numSnapshots
			except ValueError:
				print "[ERROR]: invalid input; int ONLY."
	# end of get_numsnap

	def get_bar(self):
		barChoice = ''
		bool_dict = {'y':True, 'n':False}
		while not barChoice:
			barChoice = raw_input("== Set colorbar minimum and maximum? (y/n) ").lower()
			if barChoice:
				if barChoice[0] in bool_dict.keys():
					return bool_dict[barChoice[0]]
				else:
					print "[ERROR]: invalid input."
					barChoice = ''
	# end of get_bar

	def get_min_max(self):
		"""get the minimum and maximum value for colorbar"""
		while True:
			values = raw_input("== Enter the MAX and MIN values for colorbar: ").replace(',', ' ').split()
			try:
				barMin = values[0]
				barMax = values[1]
			except IndexError:
				print "[ERROR]: enter two numbers for min and max values."

			try:
				barMin = float(barMin)
				barMax = float(barMax)
				return barMin, barMax
			except ValueError:
				print "[ERROR]: invalid input type; floats ONLY."
	# end of get_min_max



	def get_color():
		pass




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
print i.magSelect
print i.magnitude
print i.scale
print i.cumulative
print i.snapshots
print i.numSnapshots
print i.barChoice
print i.barMin
print i.barMax

