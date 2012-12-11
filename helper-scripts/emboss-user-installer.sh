#!/bin/bash
# Copyright 2011-2012 Francisco Pina Martins <f.pinamartins@gmail.com>
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


#This script will attempt to automatically download, compile and install the
#required emboss programs to run 4Pipe4.

#Define some variables:
emboss_url="ftp://emboss.open-bio.org/pub/EMBOSS/EMBOSS-6.5.7.tar.gz"

#Create a working dir
workdir=~/Software

mkdir -p $workdir/emboss

#Download emboss form the web
echo "Downloading emboss it's respective website... Please wait."
wget $emboss_url -O $workdir/emboss.tar.gz

#Extract the source:
tar xfz $workdir/emboss.tar.gz -C $workdir

#Build the program:
cd $workdir
cd $(ls |grep -i EMBOSS)
./configure --without-x
make
cp emboss/getorf $workdir/emboss/
cp emboss/etandem $workdir/emboss/

