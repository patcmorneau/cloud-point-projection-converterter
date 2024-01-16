#!/usr/bin/env python3

# Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés

import argparse
from pyproj import Transformer
import sys, os
import fileinput

def is_header(line:str, delimiter:str):
	values = line.split(delimiter)
	try:
		lat = float(values[0])
		lon = float(values[1])
		z = float(values[2])
	
	except ValueError:
		return True
	
	else:
		return False


parser=argparse.ArgumentParser(description="change coordinate system".format(os.linesep))
parser.add_argument("inputFilePath", type=str, nargs='*', help='files to read, if empty, stdin is used')
parser.add_argument("--delim", type=str)
parser.add_argument("--latPos", type=int)
parser.add_argument("--longPos", type=int)
parser.add_argument("--depthPos", type=int)
parser.add_argument("epsg_in", type=int)
parser.add_argument("epsg_out", type=int)

args = parser.parse_args()

if len(args.inputFilePath) > 1:
	sys.stderr.write("Only one file can be specyfied{}".format(os.linesep))
	sys.exit(1)

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
for line in fileinput.input(inputFilePath):
	if is_header(line, delimiter):
		continue;
	line = line.split(delimiter)
	line[0] = float(line[latPos])
	line[1] = float(line[longPos])
	line[2] = float(line[depthPos])
	line[latPos], line[longPos] = transformer.transform(line[latPos], line[longPos])
	sys.stdout.write("{}{}{}{}{}{}".format(line[latPos], delimiter, line[longPos], delimiter, line[depthPos], os.linesep))
