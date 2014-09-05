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


#This script will attempt to automatically download and install the programs
#required by 4Pipe4 in user space, except Blast2GO and emboss.
#You may wish to run emboss-user-installer.sh to automatically install emboss.
#Please consult the Readme.md file for more information on the programs used by
#4Pipe4.

#Define some variables:
#system python version
pyver=$(python3 --version |& sed 's/Python //')
#URLs:
seqclean_url="http://sourceforge.net/projects/seqclean/files/seqclean-x86_64.tgz/download"
mira_url="http://sourceforge.net/projects/mira-assembler/files/MIRA/stable/mira_4.0.2_linux-gnu_x86_64_static.tar.bz2/download"
blast_url="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.2.28/ncbi-blast-2.2.28+-x64-linux.tar.gz"
p7zip_url="http://sourceforge.net/projects/p7zip/files/p7zip/9.20.1/p7zip_9.20.1_x86_linux_bin.tar.bz2/download"
#Temporary for pysam:
python_url="https://www.python.org/ftp/python/$pyver/Python-$pyver.tgz"
setuptools_url="https://bootstrap.pypa.io/ez_setup.py"
cython_url="https://github.com/cython/cython/archive/0.18.tar.gz"
pysam_url="https://github.com/pysam-developers/pysam.git"


#Create a dir for your new programs (change this to your preference):
workdir=~/Software
dldir=$workdir/compressed

mkdir -p $workdir/sff_extract
mkdir -p $dldir


#Download the programs form the web
echo "Downloading programs from their respective websites... Please wait."
wget -c $seqclean_url -O $dldir/seqclean-x86_64.tgz
wget -c $mira_url -O $dldir/mira_4.0rc4_linux-gnu_x86_64_static.tar.bz2
wget -c $blast_url -P $dldir/
wget -c $p7zip_url -O $dldir/p7zip_9.20.1_x86_linux_bin.tar.bz2
wget -c $cython_url -P $dldir/
wget -c --no-check-certificate $python_url -O $dldir/Python-$pyver.tar.gz


#Extract and prepare the downloaded programs:
#sff_extract
chmod 755 $workdir/sff_extract/sff_extract
echo "Extracting and locally installing the downloaded programs... Please wait."
#Gzipped:
for i in $(ls $dldir |grep .gz)
do
tar xfz $dldir/$i -C $workdir
done
#Bzipped
for i in $(ls $dldir |grep .bz2)
do
tar xfj $dldir/$i -C $workdir
done


#Temporary for pysam
#Include Python 3 headers
export CPATH=$CPATH:$workdir/Python-$pyver/Include:$workdir/Python-$pyver/PC

#Build setuptools
cd $dldir
wget --no-check-certificate $setuptools_url -O - | python3 - --user

#Build cython
cd $workdir/cython-0.18
python3 setup.py install --user

#Download and build pysam
git clone $pysam_url $workdir/pysam
cd $workdir/pysam
#Patch to disable automated cython
sed -i '/cython/d' setup.py
#install
python3 setup.py install --user


echo ""
echo "If no errors occurred, (dead links, etc..) all of the software required \
to run 4Pipe4 is now installed in userspace (except Blast2GO and emboss). \
Please add the correct paths to your 4Pipe4rc file."
echo "You may now run emboss-user-installer.sh to download, compile and \
install the required emboss programs."
echo ""
