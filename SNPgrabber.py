#!/usr/bin/python3
# Copyright 2011-2013 Francisco Pina Martins <f.pinamartins@gmail.com>
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

def TCStoDict(tcs_file):
    #Turns the TCS short list into a Dictionary with names:positionsBases
    tcs=open(tcs_file,'r')
    names = {}
    for i in range(4): tcs.readline() #Skip header
    
    for lines in tcs:
        name = re.match('^\w*',lines).group(0) #Contig name
        #quals = re.search('\|.{16}\|', lines).group(0)[2:-2].split(' ')
        quals = re.split(' *', re.search('\|.{16}\|', lines).group(0)[2:-2].strip())
        SNP = ''
        for q, b in zip(quals[:-1], ['A','C','G','T']):
            try:
                if int(q) >= 70:
                    SNP = SNP + b
            except:
                b = 0
        if name not in names:
            names[name]=str(int(re.search('\d{1,5} [|]', lines).group(0)[:-2]) + 1) + SNP #makes it look like - Contig : position
        else:
            names[name]=names[name] + '#' + str(int(re.search('\d{1,5} [|]', lines).group(0)[:-2]) + 1) + SNP # add another SNP to the contig

    tcs.close()

    return(names)

def FASTAtoDict(fasta_file):
    #This will convert the fasta file into a dict like: "name":"seq" and return it
    fasta=open(fasta_file,'r')
    Dict={}
    for lines in fasta:
        if lines.startswith('>'):
            lines=lines.replace('>','')
            name=lines.replace('\n','')
            Dict[name]= '' 
        else:
            Dict[name] = Dict[name] + lines.upper()
    fasta.close()
    return Dict

def ShortListFASTA(names,fasta,tcs_file):
    #Grabs the contig names and SNP positions from the TCS file and trims the fasta to match only these.
    shortfasta = {}
    for name in names:
        if name in fasta.keys():
            namepos = name + '#' + names[name] #namepos = contigname + #positions
            shortfasta[namepos] = fasta[name] #shortfasta = namepos : sequence from fasta file
    newfile = re.match('^.*\.', tcs_file).group(0) + 'fasta'
    outfile=open(newfile,'w')
    for k in shortfasta:
        outfile.write('>' + k + '\n')
        outfile.write(shortfasta[k] + '\n')
    outfile.close()

def RunModule(tcs_file,fasta_file):
    #Function to run the whole module:
    Names=TCStoDict(tcs_file)
    Sequences=FASTAtoDict(fasta_file)
    ShortListFASTA(Names,Sequences,tcs_file)
