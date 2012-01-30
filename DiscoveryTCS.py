#!/usr/bin/python3
# Copyright 2011 Francisco Pina Martins <f.pinamartins@gmail.com>
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

def TCSParser(infile):
    #Parses the TCS file and returns a short list of interesting sites
    if infile.readline().startswith("#TCS"):
        shortlist = []
        TCS = tuple(infile.readlines()[3:])
        infile.close()
        count = 0
        for lines in TCS:
            line=lines.split('|')
            if "!" in line[-2]:
                shortlist.append(lines)
            else:
                count += 1
        print("Skipped " + str(count) + " lines that were not interesting for SNP detection.")
        return shortlist
    else:
        quit("Invalid input file. Use a TCS file as input.")

def ListParser(shortlist,minqual,mincov):
    #Turns the short lists into shorter lists, discarding everything below mincov
    hiqual = []
    lowqual = []
    for lines in shortlist:
        line = lines.split('|')
        coverage=re.split("\D*",line[2])
        del coverage[0:2]
        del coverage[-1]
        intcoverage=list(map(int, coverage))
        if sum(intcoverage) >= mincov: #Discard positions with less then mincov
            try:
                quals = line[3].replace('--','0')
            except:
                quals = line[3]
            qualgroup = re.split(" +",quals)
            del qualgroup[0]
            del qualgroup[-1]
            intquals=list(map(int, qualgroup))
            intquals.sort()
            if intquals[-2] >= minqual:#Toss overall low quality positions to lowqual; this will also force gaps into lowquals
                hiqual.append(lines)
            else:
                lowqual.append(lines)
    detlists = [hiqual, lowqual]
    return detlists

def ListWriter(infile_name,detlists):
    #Write the selected list into a file.
    round = 0
    for detlist in detlists:
        round = round + 1
        outfile = open((infile_name[0:-4] + '.short' + str(round) + '.tcs'),'w')
        outfile.write("#TCS V1.0\n")
        outfile.write("#\n")
        outfile.write("# contig name\t\t\tpadPos\tupadPos| B  Q |\ttcov covA covC covG covT cov* | qA qC qG qT q* |  S |\tTags\n")
        outfile.write("#\n")
        for lines in detlist:
            outfile.write(lines)
        outfile.close()

def RunModule(infile_name,minqual,mincov):
    infile = open(infile_name,'r')
    SNPList = TCSParser(infile)
    ShortList = ListParser(SNPList,minqual,mincov)
    ListWriter(infile_name,ShortList)
