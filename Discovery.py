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
	caffile = open(infile_name,'r')
	datatype = 0
	skip = 0
	contigreads = {}
	contigs = {}

	for lines in caffile:
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
				#RevComp the sequences if required (and quals too)
				if int(assembly_info[2]) < int(assembly_info[3]):
					contigreads[assembly_info[1]][2] = int(assembly_info[2])
				else:
					contigreads[assembly_info[1]][2] = int(assembly_info[3])
					contigreads[assembly_info[1]][0] = RevComp(contigreads[assembly_info[1]][0])
					contigreads[assembly_info[1]][1].reverse()
					
				#Slice the read according the assembly (what a mess)	
				contigreads[assembly_info[1]][0] = contigreads[assembly_info[1]][0][int(assembly_info[4])-1:int(assembly_info[5])]
				contigreads[assembly_info[1]][1] = contigreads[assembly_info[1]][1][int(assembly_info[4])-1:int(assembly_info[5])]
				
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

	caffile.close()
	
	#We return the following dictionary:
	#{contig_name:[{read_name:[sequence, [qualities], position]}, contig_seq, [contig quals]]}
	#The sequences are already returned in R&C position if necessary.

	print(contigs["TestData_c1"][0]["GXGT5DO01A883I"][0])
	print(contigs["TestData_c1"][0]["GXGT5DO01A883I"][1])
	
	return contigs

def FindSNPs(contigs):
	#Finds tha variation present in the dict that resulted from the parsing of
	#the .caf file.
	#It looks nasty, but wroks well and is relatively fast.
	var_info = {}
	for k,v in contigs.items():
		contig_name = k
		contig_map = v[0]
		contig_seq = v[1]
		contig_qual = v[2]
		contig_variants = {}
		
		for read_info in contig_map.values():
			padded = StringCompare(contig_seq.upper(), read_info[0], read_info[2])
			for i in padded: contig_variants[i] = {"A":[],"C":[],"G":[],"T":[],"-":[]}

		for n,read_info in contig_map.items():
			#Yes, we are looping through the same as before, but I don't see an
			#alternative
			
			for base_pos in range(len(read_info[0])):
				if (base_pos + read_info[2]) in contig_variants.keys():
					try:
						contig_variants[base_pos + read_info[2]][read_info[0][base_pos]].append(read_info[1][base_pos])
					except:
						print("WARNING: Your READS have ambiguities - in this case an \"%s\" in the contig %s in position %s.\n" % (read_info[0][base_pos], contig_name, (base_pos + read_info[2])))

		var_info[contig_name] = [contig_variants, contig_seq, contig_qual]

	#The returned dictionary is something like this:
	#{Contig_name:[{variant_position:{"A":[quals],"C":[quals],"G":[quals],"T":[quals],"-":[quals]}}, contig_seq, [contig_qual]]}
	return var_info
	
def StringCompare(contig, read, position):
	#Compares the contig and read sequence and returns the variant positions
	pad_var = [i + position for i in range(len(read)) if contig[i + position -1] != read[i]]
	return pad_var

def RevComp(sequence):
	#Reverses and complements a DNA sequence. IUPAC codes are NOT considered,
	#but they should not be present in 454 data anyway
	comp_table = str.maketrans("ACGT","TGCA")
	rc_seq = str.translate(sequence,comp_table)[::-1]
	return rc_seq

def TCSwriter(infile_name, variation):
	#Writes the bases with variation to a new TCS file
	#infile_name = infile_name[:infile_name.rindex(".")] + ".short1.tcs"
	#Temporarily write to /tmp to speed things up during testing
	infile_name = "/tmp/" + infile_name[infile_name.rindex("/"):infile_name.rindex(".")] + ".short1.tcs"
	outfile = open(infile_name,'w')
	outfile.write("#TCS V1.0\n")
	outfile.write("#\n")
	outfile.write("# contig name			padPos	upadPos| B  Q |	tcov covA covC covG covT cov* | qA qC qG qT q* |  S |	Tags\n")
	outfile.write("#\n")
	
	name_lens = max(map(len,variation.keys()))

	for k,v in variation.items():
		stretch_name = k + (" " * (name_lens - len(k) + 1))
		sorted_variants = list(v[0].keys())
		sorted_variants.sort()
		
		for variants in sorted_variants:
			tcov = str(len(v[0][variants]["A"]) + len(v[0][variants]["C"]) + len(v[0][variants]["G"]) + len(v[0][variants]["T"]) + len(v[0][variants]["-"]))
			outfile.write(stretch_name)
			outfile.write(" " * (6 - len(str(variants))))
			outfile.write(str(variants))
			#Unpaded variation is not implemented yet. This is a placeholder.
			outfile.write(" " * (6 - len(str(variants))))
			outfile.write(str(variants))
			#End placeholder
			outfile.write(" | ")
			outfile.write(v[1][variants - 1].upper().replace("-","*"))
			outfile.write(" " * (3 - len(str(v[2][variants]))))
			outfile.write(str(v[2][variants - 1]))
			outfile.write(" | ")
			outfile.write(" " * (6 - len(tcov)))
			outfile.write(tcov)
			outfile.write("\n")

	outfile.close()

infile_name = "/home/francisco/Desktop/4PipeTest/TestData_assembly/TestData_d_results/TestData_out.caf" #Hardcoded for now
contigs = cafParse(infile_name)
variation = FindSNPs(contigs)
TCSwriter(infile_name, variation)

