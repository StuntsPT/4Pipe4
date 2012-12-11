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


#This script will attempt to automatically download and install the programs
#required by 4Pipe4 in user space, except Blast2GO.
#Please consult the Readme.md file for more information on the programs used by
#4Pipe4.

#Define some variables:
#URLs:
sff_extract_url="http://bioinf.comav.upv.es/_downloads/sff_extract_0_3_0"
seqclean_url="http://sourceforge.net/projects/seqclean/files/seqclean-x86_64.tgz/download"
mira_url="http://sourceforge.net/projects/mira-assembler/files/MIRA/stable/mira_3.4.1.1_prod_linux-gnu_x86_64_static.tar.bz2/download"
#Please select the correct one for your distribution
emboss_url="" #Deb
#emboss_url="" #RPM
blast_url="ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ncbi-blast-2.2.27+-x64-linux.tar.gz"
p7zip_url="http://sourceforge.net/projects/p7zip/files/p7zip/9.20.1/p7zip_9.20.1_x86_linux_bin.tar.bz2/download"

#Create a dir for your new programs (change this to your preference):
mkdir -p ~/Software/sff_extract

#Download the programs form the web
echo "Downloading programs from theire respective websites... Please wait."
wget $sff_extract_url -O ~/Software/sff_extract/sff_extract
wget $seqclean_url -O ~/Software/seqclean.tar.gz
wget $mira_url -O ~/Software/mira.tar.bz2
wget $emboss_url -O ~/Software/emboss.gz #TODO
wget $blast_url -O ~/Software/blast.tar.gz
wget $p7zip_url -O ~/Software/p7z.tar.bz2

#Extract and prepare the downloaded programs:
#sff_extract
chmod 755 ~/Software/sff_extract/sff_extract
echo "Extracting and locally installing the downloaded programs... Please wait."
#Gzipped:
for i in $(ls ~/Software |grep .gz)
do
tar xfz ~/Software/$i -C ~/Software
done
#Bzipped
for i in $(ls ~/Software |grep .bz2)
do
tar xfj ~/Software/$i -C ~/Software
done
#Deb
for i in $(ls ~/Software |grep .deb)
do
ar vx ~/Software/$i data.tar.gz | tar xz -C ~/Software
done
#RPM
for i in $(ls ~/Software |grep .rpm)
do
~/Software/p7zip/7z x ~/Software/$i -o ~/Software/
done

echo "If no errors accurred, (dead links, etc..) all of the software required\
run 4Pipe4 is now installed in userspace. Please add the correct paths to \
your 4Pipe4rc file."

getorf (http://emboss.sourceforge.net/apps/cvs/emboss/apps/getorf.html)
etandem (http://helixweb.nih.gov/emboss/html/etandem.html)
