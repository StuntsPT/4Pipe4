### INTRODUCTION

First of all, thank for downloading CoBiG² 4Pipe4 analysis pipeline. We hope you
find it useful. 4Pipe4 allows you to automate NGS data analysis process into a
simple script run. It is designed to be as simple to use as possible.

### INSTALLING

4Pipe4 currently has no installing system. It is simply a set of scripts that
you can run from anywhere you want. Although it is recommended
(for simplicity's sake) that you either copy them into somewhere in your $PATH
or add 4Pipe4's directory to your $PATH.

```
PATH=/path/to/4Pipe4/:$PATH
```

### FILES

4Pipe4 contains the following files (in alphabetical order):

* 4Pipe4.py - Main file: this is the script you want to run;
* 4Pipe4rc - Configuration file;
* DiscoveryTCS.py - Module for SNP discovery in TCS files;
* LICENSE - License file;
* Metrics.py - Module for generating dataset metrics;
* ORFmaker.py - Module for finding ORFs;
* README.md - This file;
* Reporter.py - Module for generating putative SNP reports;
* SNPgrabber.py - Module for organizing SNP information;
* SSRfinder.py - Module for finding SSRs;
* Templates/Report.html - Template for report "front page"

As time progresses and 4Pipe4 sees new development, this list will be updated.

### REQUIREMENTS

4Pipe4 is written in python 3. Therefore an installation of python 3 is required
to run 4Pipe4. If you are using linux you can get python 3 from you
distribution's package manager (sudo apt-get install python3 for Ubuntu) or get
it from the website (http://python.org/download/).
Not strictly required, but highly recommended to for best results are the
external programs that 4Pipe4 uses in it's processes. By default, these are:

* ssf_extract (http://bioinf.comav.upv.es/sff_extract/)
* seqclean (http://compbio.dfci.harvard.edu/tgi/software/)
* mira (http://mira-assembler.sourceforge.net/)
* getorf (http://emboss.sourceforge.net/apps/cvs/emboss/apps/getorf.html)
* blast (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
* blast2go4pipe (http://bioinfo.cipf.es/aconesa/software.html)
* etandem (http://helixweb.nih.gov/emboss/html/etandem.html)
* 7zip (http://www.7-zip.org/)

You should also have a local database of NCBI's
Univec (http://www.ncbi.nlm.nih.gov/VecScreen/UniVec.html)
and nr (ftp://ftp.ncbi.nlm.nih.gov/blast/db/) or equivalent.
Once again, if you are using linux remember that some of these programs are
likely in your distribution's repositories (such as 7zip or blast).

### USAGE

Using 4Pipe4 should be relatively simple. Simply calling "4Pipe4.py -h" or "4Pipe4.py --help" should print
the following help message:

--------------------------------------------

```

usage: "4Pipe4 [-h] -i sff_file -o basefile [-c configfile] [-n [RUN_LIST]]"

  -h, --help     show this help message and exit 
  -i sff_file    Provide the full path to your target sff file  
  -o basefile    Provide the full path to your results directory, plus the name you want to give your results  
  -c configfile  Provide the full path to your configuration file. If none is provided, the program will look 
                 in the current working directory and  then in ~/.config/4Pipe4rc (in this order) for one. If 
                 none is found the  program will stop 
  -n [RUN_LIST]  Pleave specify the numbers corresponding to the pipeline steps that will be run. The string 
                 after "-n" must be given inside quotation marks, and numbers can be joined together or separated 
                 by any symbol. The numbers are the pipeline steps the should be run. This is an optional argument. 
                 This is an optional argument. The numbers, from 1 to 9 represent the following steps:  
                        1 - SFF extraction
                        2 - SeqClean
                        3 - Mira
                        4 - DiscoveryTCS
                        5 - SNP grabber
                        6 - ORF finder
                        7 - Blast2go
                        8 - SSR finder
                        9 - 7zip the report

The idea here is that to resume an analysis that was interrupted for example after the assembling process you 
should issue -n '1,2,3' or -n '123'. Note that some steps depend on the output of previous steps, so using some 
combinations can cause errors. The arguments can be given in any order but the running order is the same.
```

--------------------------------------------

If you wish to run the entire pipeline, just issue something like

```
python3 4Pipe4.py -i /path/to/file.sff -o /path/to/results/basefilename
```

Use the -n option to specify only the steps you wish to run from the analysis
and the -c option to point 4Pipe4 to a specific configuration file.

In the directory "Testdata" you will find an example sff file for testing
purposes, as well as documentation on how to do an example run of 4Pipe4.

### CONFIGURATION

The configuration file contains information on every option. You should change
those options to reflect your own system and SNP detection preferences.

### CONTACT

If you have questions or feedback you can contact the author by email:
f.pinamartins@gmail.com
For other programs, also please be sure to check out our group's website:
http://cobig2.fc.ul.pt
