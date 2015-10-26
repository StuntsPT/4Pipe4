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
from math import ceil


def tcs_writer(bamfile_name, fasta_d, minqual, mincov):
    """
    Convert the bamfile into the TCS format. SNP filtering is done here.
    The TCS writing and BAM parsing are done simultaneously.
    """

    # Set TCS file 'settings'
    tcsfile_name = bamfile_name[:bamfile_name.rindex(".")] + "_out.short.tcs"
    tcs = open(tcsfile_name, 'w')

    # Set bamfile 'settings'
    bamfile = pysam.Samfile(bamfile_name, 'rb')

    # Set basetrans variable
    basetrans = "ACGT*"

    # Write TCS Header
    tcs.write("#TCS V1.0\n")
    tcs.write("#\n")
    tcs.write("# contig name            padPos  upadPos| B  Q | tcov covA ")
    tcs.write("covC covG covT cov* | qA qC qG qT q* |  S |   Tags\n")
    tcs.write("#\n")

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

            # Discard position if below mincov:
            if tcov < mincov:
                keepline = False

            # Discard low freq. second variant:
            elif sorted([int(x) for x in covs])[-2] <= (ceil(tcov * 0.2)):
                keepline = False

            # Discard low quality variants:
            elif sorted(quals)[-2] < minqual:
                keepline = False

            #Discard positions with excess gaps:
            elif covs[-1]//2 >= tcov:
                keepline = False


            # Define reference base (AKA "B") and qual (AKA "Q")

            refbase = fasta_d[refs][position]

            refqual = quals[basetrans.find(refbase)]

            # Define padded and unpadded positions (AKA "padPos" and "upadPos")
            if refbase == "*":
                numpads += 1
                unpad_pos = -1
            else:
                unpad_pos = position - numpads
            pad_pos = position

            # Write TCS lines #
            if keepline is True:
                tcs_line = tcs_line_composer(refs, pad_pos, unpad_pos, refbase,
                                             refqual, tcov, covs, quals)

                tcs.write(tcs_line)

    tcs.close()
    bamfile.close()


def covs_and_quals(bases):
    """
    Take the "bases" dict and returns two lists - one with the
    coverage and one with the average quals of each base (in order).
    """
    ordered = ["A", "C", "G", "T", "*"]
    covs = []
    quals = []
    for i in ordered:
        covs.append(len(bases[i]))
        if len(bases[i]) > 0:
            quals.append(quality_calc(bases[i]))
        else:
            quals.append(0)

    return covs, quals


def quality_calc(quals):
    """
    Calculate and return individual bases qualities, just like mira does,
    as seen here:
    http://www.freelists.org/post/mira_talk/Quality-Values,4 .
    """
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

def tcs_line_composer(refs, pad_pos, unpad_pos, refbase,
                      refqual, tcov, covs, quals):
    """
    Composes and returns a TCS line based on the data harvested from the BAM
    file.
    """
    # Contig name
    tcs_line = refs
    tcs_line += " " * (24 - len(refs))
    # pad_pos
    tcs_line += " " * (5 - len(str(pad_pos)))
    tcs_line += str(pad_pos)
    # unpad_pos
    tcs_line += " " * (8 - len(str(unpad_pos)))
    tcs_line += str(unpad_pos)
    # "B" and "Q"
    tcs_line += " | "
    tcs_line += refbase
    tcs_line += " " * (3 - len(str(refqual)))
    tcs_line += str(refqual)
    # Coverages
    tcs_line += " | "
    tcs_line += " " * (6 - len(str(tcov)))
    tcs_line += str(tcov)
    for cov in covs:
        tcs_line += " " * (6 - len(str(cov)))
        tcs_line += str(cov)
    # Qualities
    tcs_line += " | "
    for basequal in quals:
        if basequal == 0:
            basequal = "--"
        tcs_line += " " * (2 - len(str(basequal)))
        tcs_line += str(basequal) + " "
    # Discard all tags (not necessary for 4Pipe4 anyway)
    tcs_line += "|  : |\n"

    return tcs_line


def RunModule(bamfile_name, padded_fasta_name, minqual, mincov):
    """
    Run the module.
    """
    tcs_writer(bamfile_name, FASTA_parser(padded_fasta_name), minqual, mincov)

if __name__ == "__main__":
    # Usage: python3 BAM_to_tcs.py file.bam file_out.padded.fasta minqual mincov
    from sys import argv
    RunModule(argv[1], argv[2], int(argv[3]), int(argv[4]))
