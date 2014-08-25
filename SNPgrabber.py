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

import re
from pipeutils import FASTA_parser


def TCStoDict(tcs_file, minqual):
    '''Turns the TCS short list into a Dictionary with names:positionsBases'''
    tcs = open(tcs_file, 'r')
    names = {}
    for i in range(4):
        tcs.readline()  # Skip header

    for lines in tcs:
        name = re.match('^\w*', lines).group(0)  # Contig name
        quals = re.split(' *', re.search('\|.{16}\|', lines).
                         group(0)[2:-2].strip())
        SNP = ''
        for q, b in zip(quals[:-1], ['A', 'C', 'G', 'T']):
            try:
                if int(q) >= minqual:
                    SNP = SNP + b
            except:
                b = 0
        if name not in names:
            names[name] = str(int(re.search('\d{1,5} [|]', lines).
                              group(0)[:-2]) + 1) + SNP  # Contig : position
        else:
            names[name] += '#' + str(int(re.search('\d{1,5} [|]', lines).
                                     group(0)[:-2]) + 1) + SNP  # add SNP

    tcs.close()

    return(names)


def ShortListFASTA(names, fasta, tcs_file, snp_fasta):
    '''Grabs the contig names and SNP positions from the TCS file and trims the
     fasta to match only these.'''
    shortfasta = {}
    for name in names:
        if name in fasta.keys():
            namepos = name + '#' + names[name]
            shortfasta[namepos] = fasta[name]
    outfile = open(snp_fasta, 'w')
    for k in shortfasta:
        outfile.write('>' + k + '\n')
        outfile.write(shortfasta[k] + '\n')
    outfile.close()


def RunModule(tcs_file, fasta_file, snp_fasta, minqual):
    '''Runs the module:'''
    Names = TCStoDict(tcs_file, minqual)
    Sequences = FASTA_parser(fasta_file)
    ShortListFASTA(Names, Sequences, tcs_file, snp_fasta)

if __name__ == "__main__":
    from sys import argv
    # Usage: python3 SNPgrabber.py file.tcs file.fasta file.SNPs.fasta minqual
    RunModule(argv[1:])
