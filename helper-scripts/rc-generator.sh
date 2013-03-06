#!/bin/bash
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


#This script will attempt to automatically find the program paths installed by
#the other helper scripts and generate a template for your 4Pipe4rc file.
#You still have to fill things like the Univec database and the assmebly
#parameters!

workdir=~/Software
datadir=~/Databases

echo "Looking for your programs..."
#sff_extract
sff_extract=$(find $workdir -executable -name sff_extract -type f);echo "."
#seqclean
seqclean=$(find $workdir -executable -name seqclean -type f);echo "."
#clean2qual
cln2qual=$(find $workdir -executable -name cln2qual -type f);echo "."
#mira
mira=$(find $workdir -executable -name mira -type f);echo "."
#etandem
etandem=$(find $workdir/emboss -executable -name etandem -type f);echo "."
#getorf
getorf=$(find $workdir/emboss -executable -name getorf -type f);echo "."
#blast
blastx=$(find $workdir -executable -name blastx -type f);echo "."
#7zip
_7z=$(find $workdir -executable -name 7z -type f);echo "."
#Univec
univec=$(find $datadir -name Univec -type f); echo "."
#nr
nr=$(find $datadir -name nr -type f); echo "."

echo "Done!"
echo "You may add these lines to your 4Pipe4rc file:"
echo "sff_extract_path = $sff_extract"
echo "seqclean_path = $seqclean"
echo "cln2qual_path = $cln2qual"
echo "mira_path = $mira"
echo "GetORF_path = $getorf"
echo "Etandem_path = $etandem"
echo "BLAST_path = $blastx"
echo "7z_path = $_7z"
echo "UniVecDB_path = $univec"
echo "BLASTdb_path = $nr"
echo ""
echo "Don't forget to fill in the rest of the variables in your 4Pipe4rc file!!"
echo ""
