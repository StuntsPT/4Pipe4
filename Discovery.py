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
	contigreads = {}
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
			contigreads[readname] = ["",[],""]
			continue
		elif lines.startswith("BaseQuality"):
			datatype = 2
			readname = lines[lines.rindex(" "):].strip()
			continue
		elif lines.startswith("Sequence"):
			datatype = 3
			contigname = lines[lines.rindex(" "):].strip()
			contigs[contigname] = []
			#contigreads = {}
			skip = 2
			continue

		#Define how to parse each different kind of data
		if datatype == 1:
			contigreads[readname][0] += lines.strip()
			if lines.startswith("\n"):
				datatype = 0
		elif datatype == 2:
			for x in lines.strip().split():
				contigreads[readname][1].append(x)
			if lines.startswith("\n"):
				datatype = 0
				skip = 2
		elif datatype == 3:
			if lines.startswith("Assembled"):
				assembly_info = lines.strip().split(" ")
				#Slice the read according the assembly (what a mess)
				contigreads[assembly_info[1]][0] = contigreads[assembly_info[1]][0][int(assembly_info[4])-1:int(assembly_info[5])]
				if int(assembly_info[2]) < int(assembly_info[3]):
					contigreads[assembly_info[1]][2] = int(assembly_info[2])
				else:
					contigreads[assembly_info[1]][2] = int(assembly_info[3])
					contigreads[assembly_info[1]][0] = RevComp(contigreads[assembly_info[1]][0])
			elif lines.startswith("\n"):
				datatype = 31
				contigs[contigname].append(contigreads)
				contigreads = {}
				contigseq = ""
				skip = 1
		elif datatype == 31:
			contigseq += lines.strip()
			if lines.startswith("\n"):
				datatype = 32
				contigs[contigname].append(contigseq)
				contigqual = []
				if len(contigseq) % 60 != 0:
					skip = 1
				else:
					skip = 2
		elif datatype == 32:
			#This is in fact faster than a list comprehension...
			for x in lines.strip().split():
				contigqual.append(x)
			if lines.startswith("\n"):
				contigs[contigname].append(contigqual)
				skip = 1
	#We return the following dictionary:
	#{contig_name:[{read_name:[sequence, [qualities], position]}, contig_seq, [contig quals]]}
	#The sequences are already returned in R&C position if necessary.
	return contigs

def FindSNPs(contigs):
	for k,v in contigs.items():
		contig_name = k
		contig_map = v[0]
		contig_seq = v[1]
		contig_qual = v[2]
		padded_var = set()
		unpadded_var = set()
		contig_variants = {}
		#print(contig_name)
		for names,read_info in contig_map.items():
			padded, unpadded = StringCompare(contig_seq.upper(), read_info[0], read_info[2])
			for i,j in zip(padded, unpadded):
				padded_var.add(i)
				unpadded_var.add(j)
			if contig_name.endswith("_c35"):
				print(names)
				print(padded_var)
				print(contig_seq[read_info[2]-1:])
				print(read_info[0])
		#print(padded_var)
			#for position in padded_var:
				#if reads[2] <= position and reads[2] + len(reads[0]) >= position:
					#contig_variants[position] = {"A":[],"C":[],"G":[],"T":[],"-":[]}
					#if position in variants:
						#contig_variants[position] = 
					#else:
						#variants[position] = reads[0][position]
	
def StringCompare(contig, read, position):
	#Compares the contig and read sequence and returns the variant positions
	pad_var = [i + position for i in range(len(read)) if contig[i + position -1] != read[i]]
	unpad_var = []
	for i in pad_var:
		j = read.count("-",0,i)
		unpad_var.append(i-j)
	return pad_var, unpad_var

def RevComp(sequence):
	#Reverses and complements a DNA sequence
	comp_table = str.maketrans("ACGT","TGCA")
	rc_seq = str.translate(sequence,comp_table)[::-1]
	return rc_seq

infile_name = "/home/francisco/Desktop/4PipeTest/TestData_assembly/TestData_d_results/TestData_out.caf" #Hardcoded for now
contigs = cafParse(infile_name)
FindSNPs(contigs)
