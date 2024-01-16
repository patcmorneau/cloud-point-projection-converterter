#!/usr/bin/env python3

# Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés

import argparse
import numpy as np
from pyproj import Transformer
import sys, os

def is_header(line:str, delimiter:str):
	values = line.split(delimiter)
	try:
		if len(values) == 3:
			lat = values[0]
			lon = values[1]
			z = values[2]
	
	except ValueError:
		return True
	
	else:
		return False


parser=argparse.ArgumentParser(description="change coordinate system".format(os.linesep))
parser.add_argument("inputFilePath", type=str)
parser.add_argument("--delim", type=str)
parser.add_argument("--latPos", type=int)
parser.add_argument("--longPos", type=int)
parser.add_argument("--depthPos", type=int)
parser.add_argument("epsg_in", type=int)
parser.add_argument("epsg_out", type=int)

args = parser.parse_args()

inputFilePath = args.inputFilePath
delimiter = args.delim
code_epsg_in = args.epsg_in
code_epsg_out = args.epsg_out
latPos = args.latPos
longPos = args.longPos
depthPos = args.depthPos

if delimiter == None:
	delimiter = " "

if latPos == None:
	latPos = 0

if longPos == None:
	longPos = 1

if depthPos == None:
	depthPos = 2

transformer = Transformer.from_crs(code_epsg_in, code_epsg_out)
with open(inputFilePath, 'r') as filein:
	line = filein.readline()
	if is_header(line, delimiter):
		line = filein.readline()
	
	while line != '':
		line = line.split(delimiter)
		line[0] = float(line[latPos])
		line[1] = float(line[longPos])
		line[0], line[1] = transformer.transform(line[0], line[1])
		sys.stdout.write("{}{}{}{}{}".format(line[latPos], delimiter, line[longPos], delimiter, line[depthPos]))
		line = filein.readline()
