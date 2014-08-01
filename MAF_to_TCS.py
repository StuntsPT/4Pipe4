#!/usr/bin/python3
# Copyright 2011-2014 Francisco Pina Martins <f.pinamartins@gmail.com>
# This file is part of 4Pipe4.
# 4Pipe4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# 4Pipe4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with 4Pipe4.  If not, see <http://www.gnu.org/licenses/>.


class Contig():
	'''A class for storing contig data. Includes contig sequence and quality,
	read sequences, quality and coordinates.'''
	def __init__(self, name):
		#Define contig data
		self.name = name
		self.num_reads = 0
		self.length = 0
		self.sequence = ""
		self.qual = []
		#Define read data
		self.read_seq = {}
		self.read_qual = {}
		self.read_coords = {}


def ASCII_to_num(quals):
	'''Translates the ASCII sequence quality values into numerical ones.'''
	values = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
	num_quals = []

	for i in quals:
		num_quals.append(quals.index(i))

	return num_quals

def MAF_parser(maf_file):
	'''Parses the MAF file and places the results in a dict like this:
	{contig_name: (instance of the Contig class)}'''
	maf = open(maf_file,'r')
	assembly = {}
	readname = ""
	for _ in range(8):
		maf.readline()
	for lines in maf:
		#Parse the contig data
		if lines.startswith("CO"):
			name = lines.split()[1]
			contig = Contig(name)
		elif lines.startswith("NR"):
			contig.num_reads = lines.split()[1]
		elif lines.startswith("CS"):
			contig.sequence = lines.split()[1]
		elif lines.startswith("CQ"):
			contig.qual = ASCII_to_num(lines.split()[1])
		elif lines.startswith("EC"):
			assembly[name] = contig
			
		#Parse the read data
		elif lines.startswith("RD"):
			if readname != "":
