#!/bin/bash
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


#This script will attempt to automatically find the program paths installed by
#the other helper scripts and generate a template for your 4Pipe4rc file.
#You still have to fill things like the Univec database and the assmebly
#parameters!

workdir=~/Software
datadir=~/Databases

echo "Looking for your programs..."
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
univec=$(find $datadir -name UniVec -type f); echo "."
#nr
nr=$(find $datadir -name nr.pal -type f |sed 's/.pal//'); echo "."
#Templates
templates=$(find $workdir -name Templates -type d |grep 4Pipe4/Templates);echo "."

echo "Done!"
echo "You may add these lines to your 4Pipe4rc file:"
echo "-----Copy from here-----"
echo "[Program paths]"
echo "#Path to seqclean:"
echo "seqclean_path = $seqclean"
echo "#Path to cln2qual:"
echo "cln2qual_path = $cln2qual"
echo "#Path to mira:"
echo "mira_path = $mira"
echo "#Path to EMBOSS getorf:"
echo "GetORF_path = $getorf"
echo "#Path to EMBOSS etandem:"
echo "Etandem_path = $etandem"
echo "#Path to BLAST (works with blast2 and blastx):"
echo "BLAST_path = $blastx"
echo "#Path to 7zip:"
echo "7z_path = $_7z"
echo "#Path to univec database (file of filenames):"
echo "UniVecDB_path = $univec"
echo "#Path to BLAST database (file of filenames):"
echo "BLASTdb_path = $nr"
echo "#Path to Blast2go4pipe:"
echo "Blast2go_path ="
echo "#Path to 4Pipe4's templates directory:"
echo "Templates_path = $templates"
echo "-----End here-----"
echo ""
echo "Don't forget to fill in the rest of the variables in your 4Pipe4rc file!!"
echo ""
