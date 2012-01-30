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

def ReadReference(reffile):
    infile = open(reffile,'r')
    tempreference = []
    tcs = tuple(infile.readlines())
    infile.close()
    for lines in tcs:
        templine = re.sub('\s+',';',lines,count=1)
        tempreference.append(re.sub('\s.*$','',templine))
    reference = tuple(tempreference)
    references = [tcs, reference]
    return references

def ReadList(listfile):
    infile = open(listfile,'r')
    list = tuple(infile.readlines())
    infile.close()
    return list

def Indexer(reference, list):
    shorts = tuple(map(mapper,list))
    list_set = set(shorts)
    matches = [i for i, j in enumerate(reference) if j in list_set]
    return matches

def mapper(item):
    titles = item.split('\t')[0:2]
    call = ';'.join(titles)
    return call

def ShortLister(tcs, indeces, mincov):
    shortTCS = []
    for items in indeces:
        verifyer = re.sub('\s+','\t',tcs[items])
        verifyer = verifyer.split('\t')
        coverage = sum(map(int,verifyer[8:13]))
        if coverage > mincov:
            shortTCS.append(tcs[items])
    return shortTCS


reference = ReadReference('/home/francisco/tests/step3_out.tcs')
list = ReadList('/home/francisco/tests/snps_info_snplist.txt')
indeces = Indexer(reference[1], list)
smallTCS = ShortLister(reference[0], indeces, 15)

outfile = open('SNPs_Shortlist_V5.tcs','w')
for lines in smallTCS:
    outfile.write(lines)
