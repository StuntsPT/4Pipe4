#!/usr/bin/python3
# Copyright 2011-2012 Francisco Pina Martins <f.pinamartins@gmail.com>
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

def cafParse(infile_name):
	#Parses the .caf file and returns the information we are looking for.
	textfile = open(infile_name,'r')
	datatype = 0
	skip = 0
	reads = {}
	quals = {}
	contigs = {}
	
	for lines in textfile:
		#Define lines to skip
		if skip > 0:
			skip -= 1
			continue
			
		#Datatypes: 0=nothing;1=sequence;2=quality;3=contig;31=contig seq, etc..
		if lines.startswith("DNA"):
			datatype = 1
			readname = lines[lines.rindex(" "):].strip()
			reads[readname] = ""
			continue
		elif lines.startswith("BaseQuality"):
			datatype = 2
			readname = lines[lines.rindex(" "):].strip()
			quals[readname] = []
			continue
		elif lines.startswith("Sequence"):
			datatype = 3
			contigname = lines[lines.rindex(" "):].strip()
			contigs[contigname] = []
			mapping = {}
			skip = 2
			continue

		#Define how to parse each different kind of data
		if datatype == 1:
			reads[readname] += lines.strip()
			if lines.startswith("\n"):
				datatype = 0
		elif datatype == 2:
			for x in lines.strip().split():
				quals[readname].append(x)
			if lines.startswith("\n"):
				datatype = 0
				skip = 2
		elif datatype == 3:
			if lines.startswith("Assembled"):
				assembly_info = lines.strip().split(" ")
				mapping[assembly_info[1]] = min(int(assembly_info[2]), int(assembly_info[3]))
			elif lines.startswith("\n"):
				datatype = 31
				contigs[contigname].append(mapping)
				contigseq = ""
				skip = 1
		elif datatype == 31:
			contigseq += lines.strip()
			if lines.startswith("\n"):
				datatype = 32
				contigs[contigname].append(contigseq)
				contigqual = []
				skip = 1
		elif datatype == 32:
			#This is in fact faster than a list comprehension...
			for x in lines.strip().split():
				contigqual.append(x)
			if lines.startswith("\n"):
				contigs[contigname].append(contigqual)
				skip = 1
			
	return(reads, quals, contigs)

def FindSNPs(reads, quals, contigs):
	

infile_name = "/home/francisco/Desktop/4PipeTest/TestData_assembly/TestData_d_results/TestData_out.caf" #Hardcoded for now
cafParse(infile_name)
