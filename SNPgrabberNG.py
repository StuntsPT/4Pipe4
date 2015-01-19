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

from pipeutils import FASTA_parser


def TCStoDict(variants_file):
    '''Parse the variants.csv list and return a Dictionary with
    names:positionsBases'''
    variants = open(variants_file, 'r')
    names = {}
    
    variants.readline()  # Skip header

    for lines in variants:
        lines=lines.split()
        if int(lines[-1]) > 0:
            try:
                names[lines[0]] += "#" + lines[1] + lines[2] + lines[3]
            except:
                names[lines[0]] = "#" + lines[1] + lines[2] + lines[3]

    variants.close()

    return(names)


def ShortListFASTA(names, fasta, snp_fasta):
    '''Grabs the contig names and SNP positions from the TCS file and trims the
     fasta to match only these.'''
    shortfasta = {}
    for name in names:
        if name in fasta.keys():
            namepos = names[name]
            shortfasta[namepos] = fasta[name]
    outfile = open(snp_fasta, 'w')
    for k in shortfasta:
        outfile.write('>' + k + '\n')
        outfile.write(shortfasta[k] + '\n')
    outfile.close()


def RunModule(variants_file, fasta_file, snp_fasta):
    '''Runs the module:'''
    Names = TCStoDict(variants_file)
    Sequences = FASTA_parser(fasta_file)
    ShortListFASTA(Names, Sequences, variants_file, snp_fasta)

if __name__ == "__main__":
    from sys import argv
    # Usage: python3 SNPgrabber.py variants.csv file.fasta file.SNPs.fasta
    RunModule(argv[1], argv[2], argv[3], argv[4], argv[5])
