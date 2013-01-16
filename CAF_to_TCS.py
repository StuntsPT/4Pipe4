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

import re

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
            contigreads[readname][0] += lines.upper().strip()
            if lines.startswith("\n"):
                datatype = 0
        elif datatype == 2:
            for x in lines.strip().split():
                contigreads[readname][1].append(int(x))
            if lines.startswith("\n"):
                datatype = 0
                skip = 2
        elif datatype == 3:
            if lines.startswith("Assembled"):
                assembly_info = lines.strip().split()
                #RevComp the sequences if required (and quals too)
                if int(assembly_info[2]) < int(assembly_info[3]):
                    contigreads[assembly_info[1]][2] = int(assembly_info[2])
                else:
                    contigreads[assembly_info[1]][2] = int(assembly_info[3])
                    contigreads[assembly_info[1]][0] = RevComp(contigreads[assembly_info[1]][0])
                    contigreads[assembly_info[1]][1].reverse()
                    contigreads[assembly_info[1]][1][:] = [-1 * i for i in contigreads[assembly_info[1]][1]]
                    #This line will remove "N"s from the start of a sequence.
                    #Apparently they are silently removed from the .caf file...
                    if contigreads[assembly_info[1]][0].startswith("N"):
                        contigreads[assembly_info[1]][0] = contigreads[assembly_info[1]][0][1:]
                        contigreads[assembly_info[1]][1] = contigreads[assembly_info[1]][1][1:]

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
            contigseq += lines.upper().strip()
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
                if len(contigqual) % 25 != 0:
                    skip = 1
                else:
                    skip = 2

    caffile.close()

    #We return the following dictionary:
    #{contig_name:[{read_name:[sequence, [qualities], position]}, contig_seq, [contig quals]]}
    #The sequences are already returned in R&C position if necessary.
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

        for read_info in contig_map.values():
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
    infile_name = infile_name[:infile_name.rindex(".")] + ".tcs"

    outfile = open(infile_name,'w')
    outfile.write("#TCS V1.0\n")
    outfile.write("#\n")
    outfile.write("# contig name            padPos  upadPos| B  Q | tcov covA covC covG covT cov* | qA qC qG qT q* |  S |   Tags\n")
    outfile.write("#\n")

    #Use a natural sort on the dictionary. Really ugly!
    sorted_keys = natural_sort(variation.keys())
    sorted_values = []
    for i in sorted_keys:
        sorted_values.append(variation[i])

    for k,v in zip(sorted_keys, sorted_values):
        stretch_name = k + (" " * (24 - len(k) + 1))

        for variants in sorted(v[0].keys()):
            tcov = str(len(v[0][variants]["A"]) + len(v[0][variants]["C"]) + len(v[0][variants]["G"]) + len(v[0][variants]["T"]) + len(v[0][variants]["-"]))
            outfile.write(stretch_name)
            #Padded variation
            outfile.write(" " * (5 - len(str(variants - 1))))
            outfile.write(str(variants - 1))
            #Unpaded variation
            if v[1][variants - 1] == "-":
                outfile.write("      -1")
            else:
                outfile.write(" " * (8 - len(str(variants - v[1][:variants].count("-") - 1))))
                outfile.write(str(variants - v[1][:variants].count("-") - 1))
            #Contig info
            outfile.write(" | ")
            outfile.write(v[1][variants - 1].upper().replace("-","*"))
            outfile.write(" " * (3 - len(str(v[2][variants-1]))))
            outfile.write(str(v[2][variants - 1]))
            #Individual (and total) coverages
            outfile.write(" | ")
            outfile.write(" " * (4 - len(tcov)))
            outfile.write(tcov)
            for base in ["A", "C", "G", "T", "-"]:
                outfile.write(" " * (5 - len(str(len(v[0][variants][base])))))
                outfile.write(str(len(v[0][variants][base])))
            outfile.write(" | ")
            #Write base quals
            for base in ["A", "C", "G", "T", "-"]:
                if v[0][variants][base] == []:
                    outfile.write("-- ")
                elif base != "-":
                    outfile.write(QualityCalc(v[0][variants][base]))
                else:
                    outfile.write(" 1 ")
            #All tags are discarded. They are not necessary for 4Pipe4 anyway
            outfile.write("|  : |")
            outfile.write("\n")

    outfile.close()

def QualityCalc(quals):
    #Calculate individual bases qualities, just like mira does, as seen here:
    #http://www.freelists.org/post/mira_talk/Quality-Values,4
    quals.sort()
    min1 = quals[0]
    if min1 > 0: min1 = 0
    max1 = quals[-1]
    if max1 < 0: max1 = 0
    if len(quals) > 1:
        max2 = quals[-2]
        if max2 < 0: max2 = 0
        min2 = quals[1]
        if min2 > 0: min2 = 0
    else:
        max2 = 0
        min2 = 0

    qual = (max1 + round(max2 * 0.1)) - (min1 + round(min2 * 0.1))
    #Return the already formatted string
    return (" " * (2 - (len(str(qual))))) + str(qual) + " "

def natural_sort(l):
    #Sort values in a 'natural' way taken form stack overflow
    #http://stackoverflow.com/questions/4836710
    #does-python-have-a-built-in-function-for-string-natural-sort?
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

def RunModule(infile_name):
    #Run the necessary module functions
    contigs = cafParse(infile_name)
    variation = FindSNPs(contigs)
    TCSwriter(infile_name, variation)

RunModule("/home/francisco/Desktop/4PipeTest/TestData_assembly/TestData_d_results/TestData_out.caf")
