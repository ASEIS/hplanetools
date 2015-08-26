#!/usr/bin/env python
# ==========================================
# The program contians the classes that may be used by other program.
# ==========================================
import os
import sys
class Input(object):
	def __init__(self, *args):
		self.fp = ""
		self.plotType = ""
		self.deltaT = 0.0
		self.simulationTime, self.alongStrike, self.downDip, self.stepAlongStrike, self.stepDownDip = 0, 0, 0, 0, 0
		self.magSelect, self.magnitude = [], False
		self.scale = ""
		self.cumulative = True
		# self.snapshots, self.numSnapshots = "m", 5
		self.snapshots, self.numSnapshots = 's', 0
		self.barMin, self.barMax = 0.0, 0.0
		self.colorChoice, self.userColor1, self.userColor2, self.userColor3, self.colorMap = '', '', '', '', 'hot'

		if len(args) == 1:
			args = self.read_parameter(args[0])[:9]

		filename =''
		if len(args) <= 1:
			# if len(args) == 1: # if file is given with command
			# 	filename = self.set_fp(args[0])

			# elif len(args) == 0:
			# 	filename = self.get_fp()
			filename = self.get_fp()
			self.get_plotType()
			self.get_deltaT()
			self.get_int('simulationTime')
			self.get_int('alongStrike')
			self.get_int('downDip')
			self.check_size(filename)

			self.get_int('stepAlongStrike')
			self.get_int('stepDownDip')
			self.get_magSelect()
			if len(self.magSelect) == 1:
				self.get_magnitude()

			self.get_scale()
			self.get_cum()
			self.get_snap()
			if self.snapshots == 'm':
				self.get_numsnap()
			self.get_bar()
			if self.barChoice:
				self.get_min_max()
			self.get_colors()

		elif len(args) > 1: # if parameters are given with command
			args = list(args)
			filename = self.set_fp(args[0])
			self.set_plotType(args[1])
			self.set_deltaT(args[2])
			self.set_int_fields('simulationTime', args[3])
			self.set_int_fields('alongStrike', args[4])
			self.set_int_fields('downDip', args[5])
			self.check_size(filename)
			self.set_int_fields('stepAlongStrike', args[6])
			self.set_int_fields('stepDownDip', args[7])
			self.set_mag(args[8])
			if len(self.magSelect) == 1:
				self.set_magnitude(args[9])
				del args[9]


			self.set_scale(args[9])
			self.set_cum(args[10])
			self.set_snap(args[11])
			if self.snapshots == 'm':
				self.set_numsnap(args[12])
				del args[12]

			self.set_bar(args[12])
			if self.barChoice:
				print args[13:15]
				self.set_min_max(args[13:15])
				del args[13:15]

			self.set_colors(args[13])
			return

		else:
			print "[ERROR]: invalid parameters."
			sys.exit()

	# end of __init__

	def read_parameter(self, filename):
		"""loads the file contains parameters"""
		try:
			fp = open(filename, 'r')
			for line in fp:
				params = line.split(' ')
				return params
		except IOError:
			print "[ERROR]: file not found."
			sys.exit()
	# end of read_parameter

	def set_fp(self, filename):
		try:
			fp = open(filename, 'r')
			self.fp = fp
			return filename
		except IOError:
			print "[ERROR]: file not found."
			return False
	# end of set_fp

	def get_fp(self):
		fp = ''
		while not fp:
			fp = raw_input("== Enter the filename of plane data: ")
			fp = self.set_fp(fp)
		return fp
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

		magSelect = sorted(list(set(magSelect))) # sort and remove duplicates
		self.magSelect = magSelect
		return magSelect
	# end of set_mag

	def get_magSelect(self):
		magSelect = []
		while not magSelect:
			magSelect = raw_input("== Enter the axis to plot (x/y/z/xy..): ")
			magSelect = self.set_mag(magSelect)

	def set_magnitude(self, magnitude):
		bool_dict = {'y':True, 'n':False}
		if magnitude[0] in bool_dict.keys():
			self.magnitude = bool_dict[magnitude[0]]
			return True
		else:
			print "[ERROR]: invalid choice for plotting magnitude."
			return ''
	# end of set_magnitude

	def get_magnitude(self):
		# decide whether or not to plot magnitude
		m = ''
		while not m:
			m = raw_input("== Would you like to plot the magnitude? (y/n) ").lower()
			m = self.set_magnitude(m)

	def set_scale(self, scale):
		scale_list = ["linear", "log", "logarithmic"]
		if scale in scale_list:
			self.scale = scale
			return scale
		else:
			print "[ERROR]: invalid scale type."
			return ''
	# end of set_scale


	def get_scale(self):
		"""get the plotting scale from user"""
		scale = ''
		while not scale:
			scale = raw_input("== Select linear or logarithmic for plot: ").lower()
			scale = self.set_scale(scale)
	# end of get_scale

	def set_cum(self, cum):
		bool_dict = {'y':True, 'n':False}
		if cum:
			if cum[0] in bool_dict.keys():
				self.cumulative = bool_dict[cum[0]]
				return True
			else:
				print "[ERROR]: invalid input."
				return False
		else:
			print "[ERROR]: missing cumulative choice."
			return False
	# end of set_cum


	def get_cum(self):
		cum = ''
		while not cum:
			cum = raw_input("== Is this a cumulative plot? (y/n) ").lower()
			cum = self.set_cum(cum)
	# end of get_cum

	def set_snap(self, snapshots):
		if snapshots:
			if snapshots[0] in ['s', 'm']:
				self.snapshots = snapshots[0]
				return snapshots[0]
			else:
				print "[ERROR]: invalid snapshot choice."
				return ''
		else:
			print "[ERROR]: missing snapshot choice."
			return ''
	# end of set_snap

	def get_snap(self):
		snapshots =''
		while not snapshots:
			snapshots = raw_input("== Display a single plot or multiple plots? (s/m) ").lower()
			snapshots = self.set_snap(snapshots)
	# end of get_snap

	def set_numsnap(self, num):
		try:
			numSnapshots = int(num)
			if numSnapshots != 0:
				self.numSnapshots = numSnapshots
				return True
			else:
				print "[ERROR]: numSnapshots cannot be 0. "
				return False
		except ValueError:
			print "[ERROR]: invalid input; int ONLY."
			return False
	# end of set_numsnap

	def get_numsnap(self):
		num = 0
		while not num:
			num = raw_input("== Enter how many seconds in between each plot: ")
			num = self.set_numsnap(num)
	# end of get_numsnap

	def set_bar(self, barChoice):
		bool_dict = {'y':True, 'n':False}
		if barChoice:
			if barChoice[0] in bool_dict.keys():
				self.barChoice = bool_dict[barChoice[0]]
				return True
			else:
				print "[ERROR]: invalid barChoice."
				return False
		else:
			print "[ERROR]: missing barChoice."
			return False
	# end of set_bar

	def get_bar(self):
		barChoice = ''
		while not barChoice:
			barChoice = raw_input("== Set colorbar minimum and maximum: (y/n) ").lower()
			barChoice = self.set_bar(barChoice)
	# end of get_bar

	def set_min_max(self, values):
		if len(values) == 2:
			try:
				barMin = float(values[0])
				barMax = float(values[1])
				if barMin < barMax:
					self.barMin = barMin
					self.barMax = barMax
					return True
				else:
					print "[ERROR]: barMax has to be greater than barMin."
					return False
			except IndexError and ValueError:
				print "[ERROR]: enter two floats for min and max values."
				return False
		else:
			print "[ERROR]: enter two floats for min and max values."
			return False
	# end of set_min_max


	def get_min_max(self):
		"""get the minimum and maximum value for colorbar"""
		values = []
		while not values:
			values = raw_input("== Enter the MIN and MAX values for colorbar: ").replace(',', ' ').split()
			values = self.set_min_max(values)
	# end of get_min_max

	def set_colors(self, colorChoice):
		if colorChoice.endswith('.'):
			pass
			# TODO
		else:
			# TODO: check existence of color map
			self.colorChoice = colorChoice
			return True
	# end of set_colors

	def get_colors(self):
		colorChoice = ''
		while not colorChoice:
			colorChoice = raw_input("== Enter a colormap or the path to custom color file: ")
			colorChoice = self.set_colors(colorChoice)
	# end of get_colors





	# def get_color(self):
	# 	choice_list1 = ['color map', 'map']
	# 	choice_list2 = ['custom', 'colors', 'custom colors']
	# 	while True:
	# 		colorChoice = raw_input("== Use a color map or custom colors? ").lower()
	# 		if colorChoice in choice_list1: # choose a color map
	# 			self.colorChoice = 'm'
	# 			self.colorMap = raw_input("== Enter the colormap for the plot: ")
	# 			return
	# 		elif colorChoice in choice_list2: # choose custom colors
	# 			self.colorChoice = 'c'
	# 			self.userColor1 = raw_input("== Enter the first color: ")
	# 			self.userColor2 = raw_input("== Enter the second color: ")
	# 			self.userColor3 = raw_input("== Enter the third color: ")
	# 			return
	# 		else:
	# 			print "[ERROR]: invalid inputs; choose 'map' or 'custom'."
	# end of get_color


	def check_size(self, filename):
		"""compare the size of given file and the estimated size"""
		stat = os.stat(filename)
		act_size = stat.st_size
		est_size = self.alongStrike*self.downDip*self.simulationTime/self.deltaT*64*3/8

		if act_size != est_size:
			print "[ERROR]: the size of given file doesn't match given parameters."
			sys.exit()
	# end of check_size
# end of input

if __name__ == "__main__":
	if len(sys.argv) > 1:
		argument = tuple(sys.argv[1:])
		i = Input(*argument)
	else:
		i = Input()

	print i.__dict__

