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

import subprocess
import re
import os 

def FASTAtoDict(fasta):
    #This converts the fasta file into a dict like: "name":"seq" and returns it
    Dict={}
    for lines in fasta:
        if lines.startswith('>'):
            lines=lines.replace('>','')
            name=lines.replace('\n','')
            Dict[name]= '' 
        else:
            Dict[name] += lines.upper()
    fasta.close()
    return(Dict)

def FASTA_qualtoDict(fasta_qual):
    #This converts the fasta file into a dict like: "name":"qual values" and returns it
    Dict={}
    for lines in fasta_qual:
        if lines.startswith('>'):
            lines=lines.replace('>','')
            name=lines.replace('\n','')
            Dict[name]= '' 
        else:
            Dict[name] += ' ' + lines.replace(' \n','')
    fasta_qual.close()
    return(Dict)

def SmallFiles(FDict,QDict,etandem,endreport,minqual):
    final = {}
    for k,v in FDict.items():
        qlist = list(map(int,QDict[k][1:].split(' ')))
        if sum(qlist)/len(qlist) >= int(minqual):
            filename=str(os.getpid())
            outfile = open('/tmp/' + filename + '.fasta','w')
            outfile.write('>' + k + '\n')
            outfile.write(v + '\n')
            outfile.close()
            cli = [etandem, '/tmp/' + filename + '.fasta', '/tmp/report.' + filename, '-minrepeat' , '2' , '-maxrepeat' , '5' , '-auto']
            eqt_run = subprocess.Popen(cli, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            eqt_run_Stdout = eqt_run.stdout.readlines()
            reportgrabber = open('/tmp/report.' + filename,'r')
            report = reportgrabber.readlines()
            reportgrabber.close()
            for lines in report:
                if re.match('^# *Sequence',lines):
                    seq = re.search(': \w*',lines).group(0)[2:]
                elif re.match('^ *\d',lines):
                    lines = lines.replace('+','')
                    final[seq] = re.sub(' +','</TD><TD>',lines.strip())
    endreport.write('''<HTML>
    <HEAD>
        <META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=utf-8">
        <TITLE>Putative SSR Table</TITLE>            
        <STYLE>
        <!-- 
        BODY,DIV,TABLE,THEAD,TBODY,TFOOT,TR,TH,TD,P { font-family:"Arial"; font-size:small }
        -->
        </STYLE>                                               
    </HEAD>\n''')
    endreport.write('<BODY>\n<TABLE CELLSPACING=1 BORDER=1>\n<TBODY>\n<TR>\n')
    endreport.write('''<TD ALIGN=CENTER>Contig</TD>
<TD ALIGN=CENTER>SSR start</TD>
<TD ALIGN=CENTER>SSR end</TD>
<TD ALIGN=CENTER>Score</TD>
<TD ALIGN=CENTER>Size</TD>
<TD ALIGN=CENTER>Tandem Count</TD>
<TD ALIGN=CENTER>Identity</TD>
<TD ALIGN=CENTER>Tandem Pattern</TD>
</TR>\n''')
    for k in final:
        endreport.write('<TR><TD>' + k + '</TD><TD>' + final[k] + '</TR>\n')
    endreport.write('</TBODY>\n</TABLE>\n</BODY>\n</HTML>')
    endreport.close()

def RunModule(fasta_file,fasta_qual_file,endreport_file,etandem,minqual):
    infile = open(fasta_file,'r')
    infile_qual = open(fasta_qual_file,'r')
    endreport = open(endreport_file,'w')

    FDict = FASTAtoDict(infile)
    QDict = FASTA_qualtoDict(infile_qual)
    SmallFiles(FDict,QDict,etandem,endreport,minqual)
