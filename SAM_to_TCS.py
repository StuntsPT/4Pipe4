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

import pysam
from pipeutils import FASTA_parser
 
#outfile = open("/home/francisco/Desktop/maf_2_tcs/sam/Taes_out.bam","wb")
#outfile.write(pysam.view("-b", "-S", "/home/francisco/Desktop/maf_2_tcs/sam/Taes_out.sam"))

#pysam.sort("/home/francisco/Desktop/maf_2_tcs/sam/Taes_out.bam", "/home/francisco/Desktop/maf_2_tcs/sam/Taes_out_sorted.bam")
#pysam.index("/home/francisco/Desktop/maf_2_tcs/sam/Taes_out_sorted.bam", "/home/francisco/Desktop/maf_2_tcs/sam/Taes_out_sorted.bai")

#samfile = pysam.Samfile("/home/francisco/Desktop/maf_2_tcs/sam/Taes_out_sorted.bam",'rb')

#for pileupcolumn in samfile.pileup( 'Taes_c1', 100, 120):
    #print()
    #print('coverage at base %s = %s' % (pileupcolumn.pos , pileupcolumn.n))
    #for pileupread in pileupcolumn.pileups:
        #print('\tbase in read %s = %s - %s' % (pileupread.alignment.qname, pileupread.alignment.seq[pileupread.qpos], pileupread.alignment.qual[pileupread.qpos]))


def TCSwriter(bamfile_name, fastafile_name):
    '''Converts the bamfile into the TCS format. The writing and the parsing
    are done simultaneusly.'''

    #Set TCS file 'settings'
    tcsfile_name = bamfile[:bamfile.rindex(".")] + ".tcs"
    TCS = open(tcsfile_name,'w')

    #Set bamfile 'settings'
    bamfile = pysam.Samfile(bamfile_name, 'rb')

    #Get reference sequences from FASTA file
    ref_seqs = FASTA_parser(fastafile_name)
    
    #Write TCS Header
    TCS.write("#TCS V1.0\n")
    TCS.write("#\n")
    TCS.write("# contig name            padPos  upadPos| B  Q | tcov covA covC covG covT cov* | qA qC qG qT q* |  S |   Tags\n")
    TCS.write("#\n")

    for refs in bamfile.references:
        refseq = ref_seqs[refs]
        numpads = 0
        for pileupcolumn in bamfile.pileup(refs, 0):
            position = pileupcolumn.pos
            base = refseq[position]
            if base == "*":
                numpads += 1
                unpadPos = -1
            else:
                unpadPos = position - pads
            padPos = position
            tcov = pileupcolumn.n
            bases = {"A" : [], "C" : [], "G" : [], "T" : [], "*" : []}
            
            for pileupread in pileupcolumn.pileups:
                base = pileupread.alignment.seq[pileupread.qpos]
                qual = pileupread.alignment.qual[pileupread.qpos]
                bases[base] += qual

            covs, quals = covs_and_quals(bases)
            
            
def covs_and_quals(bases):
    '''Takes the "bases" dict and converts it into two tuples - one with the
    coverage and one with the average quals of each base (in order)'''
    ordered = ["A","C","G","T","*"]
    covs = []
    quals = []
    for i in ordered:
        covs.append(len(bases[i]))
        try:
            quals.append(str(sum(bases[i])/len(bases[i])))
        except:
            quals.append("--")

    newcovs = covs.copy()
    top_cov = max(covs)
    
    
    return covs, quals

    
    #Use a natural sort on the dictionary. Really ugly!
    sorted_keys = natural_sort(variation.keys())
    sorted_values = []
    for i in sorted_keys:
        sorted_values.append(variation[i])

    for k,v in zip(sorted_keys, sorted_values):
        stretch_name = k + (" " * (24 - len(k) + 1))

        for variants in sorted(v[0].keys()):
            tcov = str(len(v[0][variants]["A"]) + len(v[0][variants]["C"]) + len(v[0][variants]["G"]) + len(v[0][variants]["T"]) + len(v[0][variants]["-"]))
            TCS.write(stretch_name)
            #Padded variation
            TCS.write(" " * (5 - len(str(variants - 1))))
            TCS.write(str(variants - 1))
            #Unpaded variation
            if v[1][variants - 1] == "-":
                TCS.write("      -1")
            else:
                TCS.write(" " * (8 - len(str(variants - v[1][:variants].count("-") - 1))))
                TCS.write(str(variants - v[1][:variants].count("-") - 1))
            #Contig info
            TCS.write(" | ")
            TCS.write(v[1][variants - 1].upper().replace("-","*"))
            TCS.write(" " * (3 - len(str(v[2][variants-1]))))
            TCS.write(str(v[2][variants - 1]))
            #Individual (and total) coverages
            TCS.write(" | ")
            TCS.write(" " * (4 - len(tcov)))
            TCS.write(tcov)
            for base in ["A", "C", "G", "T", "-"]:
                TCS.write(" " * (5 - len(str(len(v[0][variants][base])))))
                TCS.write(str(len(v[0][variants][base])))
            TCS.write(" | ")
            #Write base quals
            for base in ["A", "C", "G", "T", "-"]:
                if v[0][variants][base] == []:
                    TCS.write("-- ")
                elif base != "-":
                    TCS.write(QualityCalc(v[0][variants][base]))
                else:
                    TCS.write(" 1 ")
            #All tags are discarded. They are not necessary for 4Pipe4 anyway
            TCS.write("|  : |")
            TCS.write("\n")

    TCS.close()
