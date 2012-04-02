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

XIXI
import subprocess
import os
import sys
import shutil
import time
import configparser
import DiscoveryTCS as TCS
import SNPgrabber as SNPg
import ORFmaker
import Reporter
import ssr
import Metrics

def StartUp():
    arguments = {}
    for args in range(1,len(sys.argv),2):
        try:
            if sys.argv[args].startswith('-'):
                arguments[sys.argv[args]] = sys.argv[args + 1]
            else:
                print("\nERROR:Bad arguments\n")
                quit(Usage())
        except:
            print("\nERROR:Bad arguments\n")
            quit(Usage())
    if '-i' not in arguments or '-o' not in arguments:
        print("\nERROR:Missing agruments\n")
        quit(Usage())

    basefile = arguments['-o']
    sff = arguments['-i']
    if '-c' in arguments:
        rcfile = arguments['-c']
    elif os.path.isfile('4Pipe4rc'):
        rcfile = '4Pipe4rc'
        print("No config file provided, falling back to current working dir 4Pipe4rc")
    elif os.path.isfile('~/.config/4Pipe4rc'):
        rcfile = '~/.config/4Pipe4rc'
        print("No config file provided, falling back to ~/.config/4Pipe4rc")
    else:
        print("\nERROR:No config file provided.\n")
        quit(Usage())
    run_list = [1,2,3,4,5,6,7,8,9]
    if '-n' in arguments:
        exclude = eval(arguments['-n'])
        run_list = list(x for x in run_list if x not in exclude)
    try:
        config = configparser.ConfigParser()
        config.read(rcfile)
    except:
        print("\nERROR: Invalid configuration file\n")
        quit(Usage())

    return basefile,sff,config,run_list

def Usage():
    print('''Program usage:
    "python3 4Pipe4.py -i sff_file -o basefile [-c configfile] [-n [1,2,...,8,9]]"
    Where:
    "sff_file" is the full path to your target sff file;
    "basefile" is the full path to your results directory, plus the name you 
want to give your results;
    "configfile" is optional and is the full path to your configuration file.
If none is provided, the program will look in the current working directory and 
then in ~/.config/4Pipe4rc (in this order) for one. If none is found the 
program will stop;
    The list after "-n" must be given inside square brackets, and each number 
must be separated with a ",". The numbers are the pipeline steps that will NOT 
be run. This is an optional argument. The numbers, from 1 to 9 represent the 
following steps:
    1 - SFF extraction
    2 - SeqClean
    3 - Mira
    4 - DiscoveryTCS
    5 - SNP grabber
    6 - ORF finder
    7 - Blast2go
    8 - SSR finder
    9 - 7zip the report
    The idea here is that to resume an analysis that was interrupted for 
example after the assembling process you should issue "-n [1,2,3]". Note that 
some steps depend on the output of previous steps, thus, using some combinations 
of exceptions can cause errors.

    The arguments can be given in any order.\n''')

def SysPrep(basefile):
    #Function for prepairing the system for the pipeline.
    basepath=os.path.split(basefile)
    if os.path.isdir(basepath[0]):
        os.chdir(basepath[0])
        return basepath[1]
    else:
        print("\nThe directory path used for the basefile does not exist.\n")
        quit(Usage())

def RunProgram(cli, requires_output):
    #Function for running external programs and dealing with their output.
    program_stdout = []
    try:
        program = subprocess.Popen(cli, bufsize=64,shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for lines in program.stdout:
            lines = lines.decode("utf-8").strip()
            print(lines)
            program_stdout.append(lines)
    except:
        quit("\nERROR:Program not found... exiting. Check your configuration file.\n")
    if requires_output == 1:
        return program_stdout
    time.sleep(5)

def SffExtract(sff, clip):
    #Function for using the sff_extract program. The function returns the 'clip' value recommended by sff_extract. If run sequentially, the recommendations should be added.
    cli = [config.get('Program paths','sff_extract_path'), '-c', '--min_left_clip=' + str(clip), '-o', basefile, sff]
    print("\nRunning sff_extract using the folowing command:")
    print(' '.join(cli))
    sff_extract_stdout = RunProgram(cli,1)
    if len(sff_extract_stdout) == 20:
        for lines in sff_extract_stdout:
            if "Probably" in str(lines): 
                warning = str(lines)
                number = ''
                for letters in warning:
                    if letters.isdigit():
                        number = number + letters
                return number
    else:
        print("The found value seems acceptable. If this message is displayed twice in a row you have found your min_left_clip.\n")
        return "OK"

def MinClip(basefile):
    #Function for calling the SffExtract function and adding 1 to the 'clip' value until the ideal value is found. Depends on SffExtract.
    OK = 0
    clip = 0
    while OK < 2:
        turner = SffExtract(sff, clip)
        if turner == "OK":
            OK = OK + 1
            clip = clip + 1
            if OK == 2:
                clip= clip - 2
        else:
            OK = 0
            clip = clip + int(turner)
    print("Sff_extract finished with a min_left_clip=" + str(clip) + ".\n")

def SeqClean(basefile):
    #Function for using seqclean and clean2qual.
    #seqclean
    cli = [config.get('Program paths','seqclean_path'), basefile + '.fasta', '-r', basefile + '.clean.rpt', '-l', config.get('Variables','min_len'), '-o', basefile + '.clean.fasta', '-c', config.get('Variables','seqcores'), '-v', config.get('Program paths','UniVecDB_path')]
    print("\nRunning Seqclean using the folowing command:")
    print(' '.join(cli))
    RunProgram(cli,0)
    #cln2qual
    cli = [config.get('Program paths','cln2qual_path'), basefile + '.clean.rpt', basefile + '.fasta.qual']
    print("\nRunning cln2qual using the folowing command:")
    print(' '.join(cli))
    RunProgram(cli,0)
    shutil.move(basefile + '.fasta.qual.clean', basefile + '.clean.fasta.qual')

def MiraRun(basefile):
    #Assemble the sequences
    mira_dir = os.path.split(config.get('Program paths','mira_path'))[0] + '/'
    os.symlink(basefile + '.clean.fasta', basefile + '_in.454.fasta')
    os.symlink(basefile + '.clean.fasta.qual', basefile + '_in.454.fasta.qual')
    #Keep these 2 lines in case 4Pipe4 is used in windows (no symlink support).
    #shutil.copy(basefile + '.clean.fasta', basefile + '_in.454.fasta')
    #shutil.copy(basefile + '.clean.fasta.qual', basefile + '_in.454.fasta.qual')
    cli = [config.get('Program paths','mira_path'), '-project=' + miraproject]
    for items in config.get('Mira Parameters','miraparms').split(' '):
        cli.append(items)
    print("\nRunning Mira using the following command:")
    print(' '.join(cli))
    RunProgram(cli,0)
    os.unlink(basefile + '_in.454.fasta')
    os.unlink(basefile + '_in.454.fasta.qual')

def DiscoveryTCS(basefile):
    #Discovers SNPs in the TCS output file of Mira. Use only if trying to find SNPs. Output in TCS format.
    os.chdir(os.path.split(basefile)[0])
    print("\nRunning SNP Discovery tool module...")
    TCS.RunModule(basefile + '_assembly/' + miraproject + '_d_results/' + miraproject + '_out.tcs',int(config.get('Variables','minqual')),int(config.get('Variables','mincov')))

def SNPgrabber(basefile):
    #Grabs suitable SNPs in the short TCS output DiscoveryTCS and outputs a fasta with only the relevant contigs, tagged with SNP info.
    os.chdir(os.path.split(basefile)[0])
    print("\nRunning SNP Grabber tool module...")
    SNPg.RunModule(basefile + '_assembly/' + miraproject + '_d_results/' + miraproject + '_out.short1.tcs',basefile + '_assembly/' + miraproject + '_d_results/' + miraproject + '_out.unpadded.fasta')
    shutil.move(miraproject + '_assembly/' + miraproject + '_d_results/' + miraproject + '_out.short1.fasta', basefile + '.SNPs.fasta')

def ORFliner(basefile):
    #This will run EMBOSS 'getorf' and use 2 scripts to filter the results and write a report. The paramters for 'getorf' are changed here.
    os.chdir(os.path.split(basefile)[0])
    cli = [config.get('Program paths','GetORF_path'), '-sequence', basefile + '.SNPs.fasta', '-outseq', basefile + '.allORFs.fasta', '-find', '3']
    print("\nRunning EMBOSS 'getorf' using the folowing command:")
    print(' '.join(cli))
    RunProgram(cli,0)
    #After this we go to ORFmaker.py:
    print("\nRunning ORFmaker module...")
    ORFmaker.RunModule(basefile + '.allORFs.fasta')
    #Next we BLAST the resulting ORFs against the local 'nr' database:
    cli = [config.get('Program paths','BLAST_path'), '-p', 'blastx', '-d', config.get('Program paths','BLASTdb_path'), '-i', basefile + '.BestORF.fasta', '-H', 'T', '-a', config.get('Variables','seqcores'), '-o', basefile + '.ORFblast.html']
    print("\nRunning NCBI 'blastx' using the folowing command:")
    print(' '.join(cli))
    RunProgram(cli,0)
    #Then we write the metrics report:
    print("\nRunning the metrics calculator module...")
    seqclean_log_path =  os.path.split(basefile)[0] + "/seqcl_" + miraproject + ".fasta.log" 
    Metrics.Run_module(seqclean_log_path, basefile + '.fasta', basefile + '.clean.fasta', basefile + '.fasta.qual', basefile + '.clean.fasta.qual', basefile + '_assembly/' + miraproject + '_d_info/' + miraproject + '_info_assembly.txt', basefile + '.SNPs.fasta', basefile + '.BestORF.fasta', basefile + '.Metrics.html')
    #Finally we write down our report using the data gathered so far:
    print("\nRunning Reporter module...")
    Reporter.RunModule(basefile + '.BestORF.fasta', basefile + '.SNPs.fasta', basefile + '.ORFblast.html', basefile + '.Report.html')

def B2G(basefile):
    #This will make all necessary runs to get a B2go anottation ready for the GUI aplication. Bummer...
    #We start by blasting all the contigs against the NCBI's 'nr'.
    os.chdir(os.path.split(basefile)[0])
    cli = [config.get('Program paths','BLAST_path'), '-p', 'blastx', '-d', config.get('Program paths','BLASTdb_path'), '-i', basefile + '.SNPs.fasta', '-m', '7', '-a', config.get('Variables','seqcores'), '-o', basefile + '.shortlistblast.xml']
    print("\nRunning NCBI 'blastx' using the folowing command:")
    print(' '.join(cli))
    RunProgram(cli,0)
    #After 'blasting' we run b2g4pipe:
    if os.path.isfile(config.get('Program paths','Blast2go_path')):
        cli = ['java', '-jar', config.get('Program paths','Blast2go_path'), '-in', basefile + '.shortlistblast.xml', '-prop', os.path.split(config.get('Program paths','Blast2go_path'))[0] + '/b2gPipe.properties', '-out', basefile + '.b2g', '-a']
        print("\nRunning b2g4pipe using the folowing command:")
        print(' '.join(cli))
        RunProgram(cli,0)
    else:
        quit("\nERROR:Program not found... exiting. Check your configuration file.\n")

def SSRfinder(basefile):
    #Runs the SSR finder in batch mode and generates an HTML. It's mostly disk I/O stress and not CPU intensive:
    print("\nRunning SSR finder module...")
    ssr.RunModule(basefile + '_assembly/' + miraproject + '_d_results/' + miraproject + '_out.unpadded.fasta',basefile + '_assembly/' + miraproject + '_d_results/' + miraproject + '_out.unpadded.fasta.qual',basefile + '.SSR.html',config.get('Program paths','Etandem_path'),config.get('Variables','min_ssr_qual'))

def TidyUP(basefile):
    #Tidy up the report folder:
    os.chdir(os.path.split(basefile)[0])
    try:
        os.mkdir('Report')
    except:
        print('Directory tree already exists - beware!')
    try:
        os.rename(basefile + '.SSR.html','Report/SSRs.html')
    except:
        print(basefile + '.SSR.html does not exist')
    try:
        os.rename('html_files','Report/html_files')
    except:
        print(basefile + 'html_files directory does not exist')
    try:
        os.rename(basefile + '.ORFblast.html','Report/html_files/ORFblast.html')
    except:
        print(basefile + '.ORFblast.html does not exist')
    try:
        os.rename(basefile + '.Report.html','Report/SNPs.html')
    except:
        print(basefile + '.Report.html does not exist')
    try:    
        os.rename(basefile + '.b2g.annot','Report/B2g.annot')
    except:
        print(basefile + '.b2g.annot does not exist')
    try:
        shutil.copy(basefile + '.SNPs.fasta', 'Report/B2g.fasta')
    except:
        print(basefile + '.SNPs.fasta does not exist.')
    try:
        os.rename(basefile + '.Metrics.html','Report/Metrics.html')
    except:
        print(basefile + '.Metrics.html does not exist')
    shutil.copy(config.get('Program paths','Templates_path') + '/Report.html', 'Report/Report.html')
    #7zip it
    cli = [config.get('Program paths','7z_path'), 'a', '-y', '-bd', basefile + '.report.7z', 'Report']
    print("\n7ziping the Report folder for sending using the folowing command:")
    print(' '.join(cli))
    RunProgram(cli,0)

def RunMe(run_list):
    #Function to parse which parts of 4Pipe4 will run.
    if 1 in run_list:
        MinClip(basefile)
    if 2 in run_list:
        SeqClean(basefile)
    if 3 in run_list:
        MiraRun(basefile)
    if 4 in run_list:
        DiscoveryTCS(basefile)
    if 5 in run_list:
        SNPgrabber(basefile)
    if 6 in run_list:
        ORFliner(basefile)
    if 7 in run_list:
        B2G(basefile)
    if 8 in run_list:
        SSRfinder(basefile)
    if 9 in run_list:
        TidyUP(basefile)
    print("\nPipeline finished.\n")
basefile,sff,config,run_list = StartUp()
miraproject = SysPrep(basefile)
RunMe(run_list)
