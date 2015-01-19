#!/usr/bin/python3
# Copyright 2011-2015 Francisco Pina Martins <f.pinamartins@gmail.com>
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


def FASTA_parser(fasta_file):
    """Parse, convert and return fasta files into a dict like: 'name':'seq'."""
    fasta = open(fasta_file, 'r')
    d = {}

    for lines in fasta:
        if lines.startswith('>'):
            name = lines[1:].strip()
            d[name] = ''
        else:
            d[name] += lines.strip().upper()
    fasta.close()

    return d


def Ambiguifier(bases):
    """Take a list or tuple of bases and returns the corresondig ambiguity."""
    ambigs = {"A": "A", "C": "C", "T": "T", "G": "G", "AC": "M", "AG": "R",
              "AT": "W", "CG": "S", "CT": "Y", "GT": "K", "ACG": "V",
              "ACT": "H", "AGT": "D", "CGT": "B", "ACGT": "N", "*": "*"}

    bases.sort()

    return ambigs["".join(bases)]


def ASCII_to_num(qual):
    """Translate a sequence qual values from ASCII to decimal and return it."""
    values = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^\
_`abcdefghijklmnopqrstuvwxyz{|}~"
    num_qual = values.index(qual)

    return num_qual
