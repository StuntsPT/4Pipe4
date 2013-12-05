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


#This script will attempt to automatically download the Univec and the nr
#databases from NCBI for use with 4Pipe4.
#Please consult the Readme.md file for more information on the programs used by
#4Pipe4 that require these databases.

#Define some variables:
univec_url="ftp://ftp.ncbi.nih.gov/pub/UniVec/UniVec"
nr_url="ftp://ftp.ncbi.nlm.nih.gov/blast/db/"

#Set datbase directory:
datadir=~/Databases

#Download Univec and create a dir for it
echo "Downloading the Univec database..."
mkdir -p $datadir/Univec
wget -c univec_url -O $datadir/Univec/Univec

#Download nr and create a dir for it
mkdir -p $datadir/nr
echo "Downloading the nr databse... This *will* take a while, please be patient."
wget -c $nr_url/nr* -P $datadir/nr/

#Uncompress the files
chmod 744 $datadir/nr -R
for i in $datadir/nr/*
do
	tar xfvz $i -C $datadir/nr
done

echo ""
echo "If no errors occurred, (dead links, etc..) both the nr and Univec \
databases are now readt to use in your system."
echo "Please add the correct paths to your 4Pipe4rc file."
echo ""