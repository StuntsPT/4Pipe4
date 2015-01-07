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

# Usage: python3 SAM_to_BAM.py samfile bamfile

import pysam
import os


def SAM_to_BAM(samfile_name, bamfile_name):
    '''Converts a SAM file into an ordered and indexed BAM file.'''
    unsortedbamfile_name = samfile_name[:-4] + "_unsorted.bam"

    bamfile = open(unsortedbamfile_name, "wb")
    bamfile.write(pysam.view("-b", "-S", samfile_name))

    if bamfile_name.endswith(".bam"):
        bamfile_name = bamfile_name[:-4]
    pysam.sort(unsortedbamfile_name, bamfile_name)
    pysam.index(bamfile_name + ".bam")


def Cleanup(samfile_name):
    '''Cleans up the unnecessary files left behind by the SAM to BAM
    conversion'''
    os.unlink(samfile_name[:-4] + "_unsorted.bam")


def RunModule(samfile_name, bamfile_name):
    '''Runs the module in order.'''
    SAM_to_BAM(samfile_name, bamfile_name)
    Cleanup(samfile_name)


if __name__ == "__main__":
    from sys import argv
    RunModule(argv[1], argv[2])
