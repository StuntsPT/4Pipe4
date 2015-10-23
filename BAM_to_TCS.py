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

import pysam
from pipeutils import ASCII_to_num, FASTA_parser


def TCSwriter(bamfile_name, fasta_d, minqual, mincov):
    """Convert the bamfile into the TCS format. The writing and the parsing
    are done simultaneously."""

    # Set TCS file 'settings'
    tcsfile_name = bamfile_name[:bamfile_name.rindex(".")] + ".tcs"
    TCS = open(tcsfile_name, 'w')

    # Set bamfile 'settings'
    bamfile = pysam.Samfile(bamfile_name, 'rb')

    # Set basetrans variable
    basetrans = "ACGT*"

    # Write TCS Header
    TCS.write("#TCS V1.0\n")
    TCS.write("#\n")
    TCS.write("# contig name            padPos  upadPos| B  Q | tcov covA ")
    TCS.write("covC covG covT cov* | qA qC qG qT q* |  S |   Tags\n")
    TCS.write("#\n")

    for refs in bamfile.references:
        numpads = 0
        for pileupcolumn in bamfile.pileup(refs):
            # Define usefull variables that need to be reset
            bases = {"A": [], "C": [], "G": [], "T": [], "*": []}
            position = pileupcolumn.pos
            keepline = True
            tcov = 0  # Workaround
            # Define total coverage (AKA "Tcov")
            # tcov = pileupcolumn.n #TODO - submit bug for wrong counting

            # Define base coverages and qualities
            for pileupread in pileupcolumn.pileups:
                if str(pileupread).startswith("*"):
                    continue
                if str(pileupread.alignment.
                       seq[pileupread.query_position]) not in basetrans:
                    tcov += 1  # Workaround
                    continue

                if pileupread.is_del:
                    bases["*"].append(1)

                else:
                    base = pileupread.alignment.seq[pileupread.
                                                    query_position].upper()
                    qual = pileupread.alignment.qual[pileupread.query_position]
                    if pileupread.alignment.is_reverse:
                        bases[base].append(ASCII_to_num(qual) * -1)
                    else:
                        bases[base].append(ASCII_to_num(qual))

            covs, quals = covs_and_quals(bases)

            tcov += sum(covs)  # Workaround

            if tcov < mincov: # Discard position from TCS in this case
                keepline = False

            # Define reference base (AKA "B") and qual (AKA "Q")

            refbase = fasta_d[refs][position]

            refqual = quals[basetrans.find(refbase)]

            # Define padded and unpadded positions (AKA "padPos" and "upadPos")
            if refbase == "*":
                numpads += 1
                unpadPos = -1
            else:
                unpadPos = position - numpads
            padPos = position

            # Write TCS lines #
            if keepline == True:
                # Contig name
                TCS_line = refs
                TCS_line += " " * (24 - len(refs))
                # padPos
                TCS_line += " " * (5 - len(str(padPos)))
                TCS_line += str(padPos)
                # unpadPos
                TCS_line += " " * (8 - len(str(unpadPos)))
                TCS_line += str(unpadPos)
                # "B" and "Q"
                TCS_line += " | "
                TCS_line += refbase
                TCS_line += " " * (3 - len(str(refqual)))
                TCS_line += str(refqual)
                # Coverages
                TCS_line += " | "
                TCS_line += " " * (6 - len(str(tcov)))
                TCS_line += str(tcov)
                for c in covs:
                    TCS_line += " " * (6 - len(str(c)))
                    TCS_line += str(c)
                # Qualities
                TCS_line += " | "
                for q in quals:
                    TCS_line += " " * (2 - len(str(q)))
                    TCS_line += str(q) + " "
                # Discard all tags (not necessary for 4Pipe4 anyway)
                TCS_line += "|  : |\n"
                TCS.write(TCS_line)

    TCS.close()
    bamfile.close()


def covs_and_quals(bases):
    """Take the "bases" dict and returns two lists - one with the
    coverage and one with the average quals of each base (in order)."""
    ordered = ["A", "C", "G", "T", "*"]
    covs = []
    quals = []
    for i in ordered:
        covs.append(len(bases[i]))
        if len(bases[i]) > 0:
            quals.append(QualityCalc(bases[i]))
        else:
            quals.append("--")

    return covs, quals


def QualityCalc(quals):
    """Calculate and return individual bases qualities, just like mira does,
    as seen here:
    http://www.freelists.org/post/mira_talk/Quality-Values,4 ."""
    quals.sort()
    min1 = quals[0]
    if min1 > 0:
        min1 = 0
    max1 = quals[-1]
    if max1 < 0:
        max1 = 0
    if len(quals) > 1:
        max2 = quals[-2]
        if max2 < 0:
            max2 = 0
        min2 = quals[1]
        if min2 > 0:
            min2 = 0
    else:
        max2 = 0
        min2 = 0

    qual = (max1 + round(max2 * 0.1)) - (min1 + round(min2 * 0.1))

    return qual


def RunModule(bamfile_name, padded_fasta_name):
    """Run the module."""
    TCSwriter(bamfile_name, FASTA_parser(padded_fasta_name))

if __name__ == "__main__":
    # Usage: python3 BAM_to_TCS.py file.bam file_out.padded.fasta
    from sys import argv
    RunModule(argv[1], argv[2])
