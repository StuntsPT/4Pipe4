#!/usr/bin/python3
# Copyright 2011 Francisco Pina Martins <f.pinamartins@gmail.com>
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

def FASTAtoDict(fasta):
    #This converts the fasta file into a dict like: "name":"seq" and returns it
    Dict={}
    for lines in fasta:
        if lines.strip().startswith('>'):
            Dict[line[1:-1]]= '' 
        else:
            Dict[name[1:-1]] += lines.upper()
    fasta.close()
    return(Dict)

def Read_metrics(fasta_file):
    #Calculate metrics from fasta files.
    fasta = open(fasta_file,'r')
    fasta_dict = FASTAtoDict(fasta)
    values = list(map(len,fasta_dict.values()))
    max_len = max(values)
    avg_len = "%.2f" % (sum(values)/len(values))
    values.sort()
    medianpos = len(values) / 2
    if len(values) % 2 == 0:
        median = (values[int(medianpos)] + values[int(medianpos - 1)]) / 2 
    else:
        median = values[int(medianpos - 0.5)]
    return(avg_len,max_len,median)

def Read_qual_metrics(qual_file):
    #Gather original fasta.qual info.
    qual = open(qual_file,'r')
    quals = []
    for lines in qual:
        if lines[0].isdigit():
            quals.append(lines)
    quals = re.split('\D*',str(quals))
    quals = quals[1:-1]
    quals = list(map(int,quals))
    qual_avg = "%.2f" % (sum(quals)/len(quals))
    return(qual_avg)

def Dataset_gather(seqclean_report_file,origin_fasta_file,clean_fasta_file,origin_qual_file,clean_qual_file):
    #Gather the relevant parts from seqclean report.
    clean_report=open(seqclean_report_file,'r')
    marker = 0
    text = []
    for lines in clean_report:
        if lines.startswith("*****"):
            marker = 1
        if lines.strip().startswith("by 'UniVec'"):
            text.append(lines)
            break
        if marker == 1:
            text.append(lines)

    origin_metrics = Read_metrics(origin_fasta_file)
    clean_metrics = Read_metrics(clean_fasta_file)

    origin_qual_avg = Read_qual_metrics(origin_qual_file)
    clean_qual_avg = Read_qual_metrics(clean_qual_file)

    return(text, origin_metrics, clean_metrics, origin_qual_avg, clean_qual_avg)

def Contig_gather(mira_report):
    #Gather contig data from the mira report:
    report = open(mira_report,'r')
    total_contigs = []
    total_consensus = []
    N50 = []
    N90 = []
    N95 = []
    max_coverage = []
    avg_qual = []
    for lines in report:
        if lines.startswith("Num. reads assembled:"):
            reads_assembled = re.search('\d*$',lines).group()
        if lines.strip().startswith("Avg. total coverage:"):
            total_cov = re.search('\d.*$',lines).group()
        if lines.strip().startswith("Number of contigs:"):
            total_contigs.append(re.search('\d.*$',lines).group())
        if lines.strip().startswith("Total consensus:"):
            total_consensus.append(re.search('\d*$',lines).group())
        if lines.strip().startswith("Largest contig:"):
            largest_contig = re.search('\d.*$',lines).group()
        if lines.strip().startswith("N50 contig size:"):
            N50.append(re.search('\d*$',lines).group())
        if lines.strip().startswith("N90 contig size:"):
            N90.append(re.search('\d*$',lines).group())
        if lines.strip().startswith("N95 contig size:"):
            N95.append(re.search('\d*$',lines).group())
        if lines.strip().startswith("Max coverage (total):"):
            max_coverage.append(re.search('\d*$',lines).group())
        if lines.strip().startswith("Average consensus quality:"):
            avg_qual.append(re.search('\d*$',lines).group())

    report.close()

    return(reads_assembled, total_cov, total_contigs, total_consensus, largest_contig, N50, N90, N95, max_coverage, avg_qual)

def SNP_gather(snp_file,orf_file):
    #Gather SNP data from the fasta files:
    snp_file = open(snp_file,'r')
    snps = FASTAtoDict(snp_file)
    ammount = 0
    for titles in snps.keys():
        ammount += titles.count("#")
    num_contigs = len(snps)
    avg_snps_per_contig = "%.2f" % (ammount/num_contigs)
    contig_sizes = list(map(len,snps.values()))
    max_contig_size = max(contig_sizes)
    min_contig_size = min(contig_sizes)
    avg_contig_size = "%.2f" % (sum(contig_sizes)/len(contig_sizes))
    
    #This part counts how many SNPs are inside ORFs
    orf_file = open(orf_file,'r')
    orfs = FASTAtoDict(orf_file)
    contig_names = []
    for contigs in orfs.keys():
        if "REVERSE" in contigs:
            start = int(re.search('\[\d*',contigs).group()[1:])
            end = re.findall('\d+(?=:)',contigs)
            end = list(map(int,end))
            for items in end:
                suffix = str(start-items+2)
                contig = re.sub(' .*$','',contigs) + ';' + suffix
                contig_names.append(contig)
        else:
            start = int(re.search('\[\d*',contigs).group()[1:])
            end = re.findall('\d+(?=:)',contigs)
            end = list(map(int,end))
            for items in end:
                suffix = str(start+items)
                contig = re.sub(' .*$','',contigs) + ';' + suffix
                contig_names.append(contig)
    snps_in_orfs = len(set(contig_names))

    return(ammount, num_contigs, avg_snps_per_contig, max_contig_size, min_contig_size, avg_contig_size, snps_in_orfs)

def Metrics_writer(dataset_info, contig_info, snp_info, metrics_file):
    metrics_file = open(metrics_file,'w')
    metrics_file.write('<HTML>\n    <HEAD>\n        <META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=utf-8">\n        <TITLE>4Pipe4 Metrics Report</TITLE>            \n        <STYLE>\n        <!-- \n        BODY,DIV,TABLE,THEAD,TBODY,TFOOT,TR,TH,TD,P { font-family:"Arial"; font-size:small }\n        -->\n        </STYLE>\n    </HEAD>\n<BODY>\n')
    metrics_file.write("<H1>4Pipe4 metrics report:</H1>\n")
    metrics_file.write("<H2>Dataset metrics:</H2>\n")
    metrics_file.write("<p>Average read length (before cleaning): " + str(dataset_info[1][0]) + "</p>\n")
    metrics_file.write("<p>Maximum read length (before cleaning): " + str(dataset_info[1][1]) + "</p>\n")
    metrics_file.write("<p>Median of read length (before cleaning): " + str(dataset_info[1][2]) + "</p>\n")
    metrics_file.write("<p>Average base quality (before cleaning): " + str(dataset_info[3]) + "</p>\n")
    metrics_file.write("<H3>SeqClean report:</H3>")
    for lines in dataset_info[0]:
        metrics_file.write("<p>" + lines + "</p>")
    metrics_file.write("<p>Average read length (after cleaning): " + str(dataset_info[2][0]) + "</p>\n")
    metrics_file.write("<p>Maximum read length (after cleaning): " + str(dataset_info[2][1]) + "</p>\n")
    metrics_file.write("<p>Median of read length (after cleaning): " + str(dataset_info[2][2]) + "</p>\n")
    metrics_file.write("<p>Average base quality (after cleaning): " + str(dataset_info[4]) + "</p>\n")

    metrics_file.write("<H2>Contig metrics:</H2>\n")
    metrics_file.write("<p>Number of reads assembled: " + str(contig_info[0]) + "</p>\n")
    metrics_file.write("<p>Total coverage: " + str(contig_info[1]) + "</p>\n")
    metrics_file.write("<p>Length of largest contig: " + str(contig_info[4]) + "</p>\n")
    metrics_file.write("<H3>Contigs with a length of at least 1000 bp:</H3>\n")
    metrics_file.write("<p>Total number of contigs formed: " + str(contig_info[2][0]) + "</p>\n")
    metrics_file.write("<p>Total sum of consesnus bases: " + str(contig_info[3][0]) + "</p>\n")
    metrics_file.write("<p>N50: " + str(contig_info[5][0]) + "</p>\n")
    metrics_file.write("<p>N90: " + str(contig_info[6][0]) + "</p>\n")
    metrics_file.write("<p>N95: " + str(contig_info[7][0]) + "</p>\n")
    metrics_file.write("<p>Depth of maximum coverage zone: " + str(contig_info[8][0]) + "</p>\n")
    metrics_file.write("<p>Average quality of bases: " + str(contig_info[9][0]) + "</p>\n")
    metrics_file.write("<H3>All contigs:</H3>\n")
    metrics_file.write("<p>Total number of contigs formed: " + str(contig_info[2][1]) + "</p>\n")
    metrics_file.write("<p>Total sum of consesnus bases: " + str(contig_info[3][1]) + "</p>\n")
    metrics_file.write("<p>N50: " + str(contig_info[5][1]) + "</p>\n")
    metrics_file.write("<p>N90: " + str(contig_info[6][1]) + "</p>\n")
    metrics_file.write("<p>N95: " + str(contig_info[7][1]) + "</p>\n")
    metrics_file.write("<p>Depth of maximum coverage zone: " + str(contig_info[8][1]) + "</p>\n")
    metrics_file.write("<p>Average quality of bases: " + str(contig_info[9][1]) + "</p>\n")

    metrics_file.write("<H2>SNP metrics:</H2>\n")
    metrics_file.write("<p>Number of SNPs found: " + str(snp_info[0]) + "</p>\n")
    metrics_file.write("<p>Number of contigs with SNPs: " + str(snp_info[1]) + "</p>\n")
    metrics_file.write("<p>Average SNPs per contig with SNPs: " + str(snp_info[2]) + "</p>\n")
    metrics_file.write("<p>Largest contig length with at least one SNP: " + str(snp_info[3]) + "</p>\n")
    metrics_file.write("<p>Shortest contig length with at least one SNP: " + str(snp_info[4]) + "</p>\n")
    metrics_file.write("<p>Average length of contigs containing SNPs: " + str(snp_info[5]) + "</p>\n")
    metrics_file.write("<p>Number of SNPs in ORFs: " + str(snp_info[6]) + "</p>\n")
    metrics_file.write("</BODY>\n</HTML>\n")
    metrics_file.close()

def Run_module(seqclean_log_file, original_fasta_file, clean_fasta_file, original_fasta_qual_file, clean_fasta_qual_file, info_assembly_file, snps_fasta_file, bestorf_fasta_file, metrics_file):
    #Run the module
    dataset_info = Dataset_gather(seqclean_log_file, original_fasta_file, clean_fasta_file, original_fasta_qual_file, clean_fasta_qual_file)
    contig_info = Contig_gather(info_assembly_file)
    snp_info = SNP_gather(snps_fasta_file, bestorf_fasta_file)
    Metrics_writer(dataset_info, contig_info, snp_info, metrics_file)
