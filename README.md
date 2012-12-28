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
* CAF_to_TCS.py - Module for locating variation in .caf files. Outputs a TCS.
* TCSfilter.py - Module for SNP filtering in TCS files;
* LICENSE - License file;
* Metrics.py - Module for generating dataset metrics;
* ORFmaker.py - Module for finding ORFs;
* README.md - This file;
* Reporter.py - Module for generating putative SNP reports;
* SNPgrabber.py - Module for organizing SNP information;
* SSRfinder.py - Module for finding SSRs;
* Templates/Report.html - Template for report "front page";
* Testdata/4Pipe4_test.sff - Test data file;
* Testdata/README.md - Documentation on the test data;

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
* mira 3.4.x series (http://mira-assembler.sourceforge.net/) 
* getorf (http://emboss.sourceforge.net/apps/cvs/emboss/apps/getorf.html)
* blast (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
* blast2go4pipe (http://bioinfo.cipf.es/aconesa/software.html)
* etandem (http://helixweb.nih.gov/emboss/html/etandem.html)
* 7zip (http://www.7-zip.org/)

These programs are mentioned as "optinal" since you can have for example an
already assembled dataset and just want to run the SNP detection routines,
starting the pipeline from step #4. This would not require sff_extract, seqclean
nor mira to be installed.
All of these programs aer required if you wish to run all the steps in 4Pipe4.
Beware the 4Pipe4 currentlly relies on the stable version of mira, and not the
development version. When the current development branch (3.9.x series at the
time of writing) sees a stable release 4Pipe4 will be updated to work with this
new version, which radically changes the user interface.

You should also have a local database of NCBI's
Univec (http://www.ncbi.nlm.nih.gov/VecScreen/UniVec.html)
and nr (ftp://ftp.ncbi.nlm.nih.gov/blast/db/) or equivalent.
Once again, if you are using linux remember that some of these programs are
likely in your distribution's repositories (such as 7zip or blast).

### HELPER SCRIPTS

Inside the directory "helper-scripts" you will find 4 shell scripts:

* user-installer.sh
* emboss-user-installer.sh
* database-downloader.sh
* rc-generator.sh

If they are run in the order they are shown here, they will:

1. Download and locally install the programs: "sff_extract", "seqclean", "mira",
"blast" and "p7zip".
2. Download, compile and locally install emboss' "getorf" and "etandem". (This
script requires build tools such as "make" and "gcc". They should be readily
available on any *nix machine you have access to but don't have root access.)
3. Download local copies of NCBI's "Univec" and "nr" databases.
4. Generate pre-configured entries for all of the above ready to be copied &
pasted into 4Pipe4rc.

These scripts should significantlly speed up the instalation process of these
external 4Pipe4 programs.

By default these scripts will install all the software to "~/Software", but this
can be easily changed in the scripts themselves.

### USAGE

Using 4Pipe4 should be relatively simple. Simply calling "4Pipe4.py -h" or
"4Pipe4.py --help" should printthe following help message:

--------------------------------------------

```

usage: 4Pipe4 [-h] -i sff_file -o basefile [-c configfile] [-s [RUN_LIST]]

optional arguments:
  -h, --help     show this help message and exit
  -i sff_file    Provide the full path to your target sff file
  -o basefile    Provide the full path to your results directory, plus the name you want to give your results
  -c configfile  Provide the full path to your configuration file. If none is provided, the program will look in the current working directory and  then in ~/.config/4Pipe4rc (in this order) for one. If none is found the  program will stop
  -s [RUN_LIST]  Specify the numbers corresponding to the pipeline steps that will be run. The string after -s must be given inside quotation marks, and numbers can be joined together or separated by any symbol. The numbers are the pipeline steps that should be run. This is an optional argument and it's omission will run all steps by default'. The numbers, from 1 to 9 represent the following steps:
                        1 - SFF extraction
                        2 - SeqClean
                        3 - Mira
                        4 - DiscoveryTCS
                        5 - SNP grabber
                        6 - ORF finder
                        7 - Blast2go
                        8 - SSR finder
                        9 - 7zip the report

The idea here is that to resume an analysis that was interrupted for example after the assembling process you should issue -s '4,5,6,7,8,9' or -s '456789'. Note that some steps depend on the output of previous steps, so using some combinations can cause errors. The arguments can be given in any order.
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
