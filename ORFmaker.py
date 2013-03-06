#!/usr/bin/python3
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

import re

def DealWithSNPS(List):
    #Recalculates the SNP position in the protein and if necessary R&C's the SNP.
    majororfs = {}
    for keys in List:
        snps = re.search('#.*_',keys).group(0)[1:-1].split('#')
        ref = {}
        v1 = int(re.search('\[.* - ',keys).group(0)[1:-3])
        v2 = int(re.search(' - .*\]',keys).group(0)[3:-1])
        values = [v1,v2]
        if values[0] < values[1]:
            for i in snps:
                if int(re.search('^\d*',i).group(0)) >= values[0] and int(re.search('^\d*',i).group(0)) <= values[1]:
                    ref[int(re.search('^\d*',i).group(0))-values[0] + 1] = re.search('\D*$',i).group(0)
            newpos = str(ref)
            majororfs[keys + ' ' + newpos] = List[keys]
        else:
            for i in snps:
                if int(re.search('^\d*',i).group(0)) >= values[1] and int(re.search('^\d*',i).group(0)) <= values[0]:
                    reversible=re.search('\D*$',i).group(0)
                    for k,v in {'A':'t', 'G':'c', 'T':'a', 'C':'g'}.items():
                         if k in reversible:
                             reversible = reversible.replace(k,v)
                    reversible = reversible.upper()
                    ref[abs(int(re.search('^\d*',i).group(0))-values[0]) + 1 ]=reversible
            newpos = str(ref)
            majororfs[keys + ' ' + newpos] = List[keys]
    return(majororfs)

def BestORF(orffasta):
    #Creates a FASTA file with only the best ORFs found.
    #This means the longest ORF that contains at least a SNP.
    #It also discards ORFs that did not contain SNPs and SNPs that are not in ORFs.
    orftuple=tuple(orffasta.readlines())
    orffasta.close()
    orfs = {}
    for lines in orftuple:
        if lines.startswith('>'):
            valid = 0
            title = lines.strip('>\n ')
            step1 = re.search('#.*_',lines).group(0)[:-1]
            snps = list(map(int,re.sub('[A-Z]','',step1)[1:].split('#')))
            v1 = int(re.search('\[.* - ',lines).group(0)[1:-3])
            v2 = int(re.search(' - .*\]',lines).group(0)[3:-1])
            values = [v1,v2]
            for i in snps:
                if i >= min(values) and i <= max(values):
                    valid = 1
                    orfs[title] = ''
        elif valid == 1:
            orfs[title] = orfs[title] + lines
    return(orfs)

def ORFwriter(Dict,orffasta_file):
    #Writes down the BestOrf file after all the selections and trims are done.
    outfile = (re.match('^.*\.',orffasta_file).group(0)[0:-8]) + 'BestORF.fasta'
    print(outfile)
    bestorf = open(outfile, 'w')
    for k, v in Dict.items():
        k = re.sub('#.*_\d*', '', k)
        bestorf.write('>' + k + '\n')
        bestorf.write(v + '\n')

def RunModule(orffasta_file):
    orffasta=open(orffasta_file,'r')
    List = BestORF(orffasta)
    ImprovedList = DealWithSNPS(List)
    ORFwriter(ImprovedList,orffasta_file)
