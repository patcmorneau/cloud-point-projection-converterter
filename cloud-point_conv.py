#!/usr/bin/env python3

# Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés

import numpy as np
from pyproj import Transformer
import sys

if __name__ == '__main__':

	if len(sys.argv) != 5:
		sys.stderr.write("Usage: python cloud-point_conv.py inputFilePath outputFilePath code_espg_in code_espg_out\n")
		sys.exit(1)

	inputFilePath = sys.argv[1]
	outputFilePath = sys.argv[2]
	code_espg_in = sys.argv[3]
	code_espg_out = sys.argv[4]

	transformer = Transformer.from_crs(code_espg_in, code_espg_out)
	with open(inputFilePath, 'r') as filein:
		with open(outputFilePath, 'w') as fileout:
			line = filein.readline()
			while line != '':
				line = line.split(' ')
				line[0] = float(line[0])
				line[1] = float(line[1])
				line[0], line[1] = transformer.transform(line[0], line[1])
				line = [str(x) for x in line]
				fileout.write(' '.join(line))
				line = filein.readline()
