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

from math import ceil

def TCSParser(infile_name):
    #Parses the TCS file
    infile = open(infile_name,'r')
    if infile.readline().startswith("#TCS") == False:
        quit("Invalid input file. Use a TCS file as input.")
    else:
        TCS = []
        for i in range(3): infile.readline() #Skip header
    
        for lines in infile:
            TCS.append(lines)

    infile.close()
    return TCS

def ListParser(TCS,minqual,mincov):
    #Discards every line in the TCS file with a coverage below mincov and a qual
    #below minqual
    passed = []
    for lines in TCS:
        line = lines.split('|')
        tcov = int(line[2][:5])
        covs = line[2][5:].strip().split()
        covs = sorted(list(map(int, covs)))
        if tcov < mincov: #Discard positions with less then mincov
            pass
        elif covs[-2] < (ceil(mincov*0.2)):
            pass
        else:
            quals = line[3].replace('--','0')
            quallist = quals.strip().split()
            quallist = sorted(list(map(int, quallist)))
            if quallist[-2] >= minqual: #Filter by quality
                passed.append(lines)
                
    return passed

def ListWriter(infile_name,passed):
    #Write the selected list into a file.
    outfile = open((infile_name[0:-4] + '.short.tcs'),'w')
    outfile.write("#TCS V1.0\n")
    outfile.write("#\n")
    outfile.write("# contig name\t\t\tpadPos\tupadPos| B  Q |\ttcov covA covC covG covT cov* | qA qC qG qT q* |  S |\tTags\n")
    outfile.write("#\n")
    for lines in passed:
        outfile.write(lines)
    outfile.close()

def RunModule(infile_name,minqual,mincov):
    
    TCS = TCSParser(infile_name)
    ShortList = ListParser(TCS,minqual,mincov)
    ListWriter(infile_name,ShortList)

#RunModule("/home/francisco/Desktop/4PipeTest/TestData_assembly/TestData_d_results/TestData_out.tcs", 70, 15)
