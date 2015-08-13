#!/usr/bin/env python
# ===================================================================================
# The program contains basic functions what may be used by other programs.
# ===================================================================================
import numpy as np
def derivative(data, dt):
	"""compute derivative of an numpy."""
	data = np.insert(data, 0, data[0])
	data = np.diff(data/dt)
	return data
