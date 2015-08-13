#!/usr/bin/env python
import numpy as np
def init_peak(stepAlongStrike, alongStrike, stepDownDip, downDip):
	"""initialize peak matrix"""
	y = np.array(range(0, stepAlongStrike*alongStrike, stepAlongStrike))
	x = np.array(range(0, stepDownDip*downDip, stepDownDip))
	x, y = np.meshgrid(x, y)
	peak = np.zeros_like(x)

	for i in range(0, len(peak)):
		for j in range(0, len(peak[i])):
			print peak[i][j]
	print peak.shape
	return peak

# end of init_peak

init_peak(1000, 136, 1000, 181)
