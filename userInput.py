#!/usr/bin/env python
# ==========================================
# The program contians the classes that may be used by other program.
# ==========================================
import os
import sys
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


	def __init__(self, *args):
		if len(args) <= 1:
			if len(args) == 1: # if file is given with command
				self.set_fp(args[0])

			elif len(args) == 0:
				self.get_fp()
			self.get_plotType()
			self.get_deltaT()
			self.get_int('simulationTime')
			self.get_int('alongStrike')
			self.get_int('downDip')
			self.get_int('stepAlongStrike')
			self.get_int('stepDownDip')
			self.get_mag()

			self.scale = self.get_scale()
			self.cumulative = self.get_cum()
			self.snapshots = self.get_snap()
			if self.snapshots == 'm':
				self.numSnapshots = self.get_numsnap()
			self.barChoice = self.get_bar()
			if self.barChoice:
				self.barMin, self.barMax = self.get_min_max()

		elif len(args) == 9: # if parameters are given with command
			self.set_fp(args[0])
			self.set_plotType(args[1])
			self.set_deltaT(args[2])
			self.set_int_fields('simulationTime', args[3])
			self.set_int_fields('alongStrike', args[4])
			self.set_int_fields('downDip', args[5])
			self.set_int_fields('stepAlongStrike', args[6])
			self.set_int_fields('stepDownDip', args[7])
			self.set_mag(args[8])
			return

		else:
			print "[ERROR]: invalid parameters."
			return

	# end of __init__

	def set_fp(self, filename):
		try:
			fp = open(filename, 'r')
			self.fp = fp
			return True
		except IOError:
			print "[ERROR]: file not found."
			return False
	# end of set_fp

	def get_fp(self):
		fp = ''
		while not fp:
			filename = raw_input("== Enter the filename of plane data: ")
			fp = set_fp(filename)
	# end of get_fp

	def set_plotType(self, ptype):
		type_list = ['a', 'v', 'd']
		try:
			ptype = ptype.lower()[0]
			if ptype not in type_list:
				print "[ERROR]: invalid plot type."
				return False
			else:
				self.plotType = ptype
				return True
		except IndexError:
				print "[ERROR]: invalid plot type."
				return False
	# end of set_plotType

	def get_plotType(self):
		ptype = ''
		while not ptype:
			p = raw_input("== Select displacement, velocity, or acceleration (d/v/a) for plot: ")
			ptype = self.set_plotType(p)
	# end of get_plotType

	def set_deltaT(self, dt):
		try:
			dt = float(dt)
		except ValueError:
			print "[ERROR]: invalid deltaT; float ONLY."
			return False

		if dt <= 0.0:
			print "[ERROR]: invalid deltaT; positive float ONLY."
			return False
		self.deltaT = dt
		return True
	# end of set_deltaT


	def get_deltaT(self):
		dt = 0.0
		while not dt:
			dt = raw_input("== Enter dt: ")
			dt = self.set_deltaT(dt)
	# end of get_deltaT

	def set_int_fields(self, varName, value):
		try:
			value = int(value)
			self.__dict__[varName] = value
			return value

		except ValueError:
			print "[ERROR]: invalid value for " + varName + "."
			return 0
	# end of set_int_fields


	def get_int(self, varName):
		"""get simulationTime, alongStrike, downDip, stepAlongStrike, and stepDownDip from user."""
		value = 0
		while not value:
			value = raw_input("== Enter the value of " + varName + " : ")
			value = self.set_int_fields(varName, value)
	# end of get_int

	def set_mag(self, mag):
		magSelect = []
		magList = ['x','y','z']
		mag = mag.lower().strip()
		for m in mag:
			if m in magList:
				magSelect.append(m)
			elif m not in [' ', ',']:
				print "[ERROR]: invalid axis; x/y/z or their combinations ONLY."
				return []

		if not magSelect:
			print "[ERROR]: invalid axis; x/y/z or their combinations ONLY."
			return []

		magSelect = list(set(magSelect)) # remove duplicates
		self.magSelect = magSelect
		return magSelect
	# end of set_mag

	def get_mag(self):
		magSelect = []
		while not magSelect:
			magSelect = raw_input("== Enter the axis to plot (x/y/z/xy..): ")
			magSelect = self.set_mag(magSelect)

		# decide whether or not to plot magnitude
		magnitude = True
		bool_dict = {'y':True, 'n':False}
		if len(magSelect) == 1:
			m = ''
			while not m:
				m = raw_input("== Would you like to plot the magnitude? (y/n) ").lower()
				if m:
					if m[0] in bool_dict.keys():
						self.magnitude = bool_dict[m[0]]
						break
					else:
						print "[ERROR]: invalid input."
						m = ''
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

if __name__ == "__main__":
	if len(sys.argv) > 1:
		argument = tuple(sys.argv[1:])
		i = Input(*argument)
	else:
		i = Input()

	print i.__dict__

	# print i.plotType
	# print i.deltaT
	# print i.simulationTime
	# print i.alongStrike
	# print i.downDip
	# print i.alongStrike
	# print i.stepAlongStrike
	# print i.stepDownDip
	# print i.magSelect
	# print i.magnitude
	# print i.scale
	# print i.cumulative
	# print i.snapshots
	# print i.numSnapshots
	# print i.barChoice
	# print i.barMin
	# print i.barMax

