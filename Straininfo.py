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


#Usage:Straininfo.py /path/to/target/folder

import sys
import glob
import os
import shutil

#Fasta files location
#This folder should contain all the fasta and fasta.qual files
basedir=sys.argv[1]

def cat(match_extension, output_name): 
    #Implement a function similar to Unix 'cat'
    infiles = os.listdir(basedir)
    outfile = open(output_name, 'wb') 
    for f in infiles:
        if f.endswith(match_extension):
            shutil.copyfileobj(open(f,'rb'), outfile)
    outfile.close()

def FastaLister(basedir,extensions):
    os.chdir(basedir)
    fastas=glob.glob(extensions)
    return(fastas)

def StrainNamer(basedir):
    fastas=FastaLister(basedir,'*.fasta')
    outfile=open('straindata_in.txt','w')
    for files in fastas:
        infile = open(files,'r')
        strain = files[0:files.index('.')]
        for lines in infile:
            if lines.startswith('>'):
                outfile.write(lines.replace('>','').strip('\n') + ' ' + strain + '\n')
        infile.close()
    outfile.close()
                
def FastaConcat(basedir):
    os.chdir(basedir)
    cat('.qual', 'all.fasta.qual')
    cat('.fasta', 'all.fasta')

StrainNamer(basedir)
FastaConcat(basedir)
