### INTRODUCTION

First of all, thank for downloading CoBiG² 4Pipe4 analysis pipeline. We hope you
find it useful. 4Pipe4 allows you to automate NGS data analysis process into a
simple script run. It is designed to be as simple to use as possible.
4Pipe4 can now be used with illumina data, however, keep in mind that 4Pipe4 was
designed for 454 data, and although everything should run using illumina data,
it's performance was not nearly was tested as the performance with 454 data.
Therefore, the software is usable, but YMMV with the default values for illumina
data. In fact, any feedback with this sort of data is **very** appreciated.

### INSTALLING

4Pipe4 currently has no installing system. It is simply a set of scripts that
you can run from anywhere you want. Although it is recommended
(for simplicity's sake) that you either copy them into somewhere in your $PATH
or add 4Pipe4's directory to your $PATH.

```
PATH=$PATH:/path/to/4Pipe4/
```

Please check the README.md section on the helper scripts for a semi-automatic
way to install all of 4Pipe4's dependencies.

### FILES

4Pipe4 contains the following files (in alphabetical order):

* 4Pipe4.py - Main file: this is the script you want to run;
* 4Pipe4rc - Configuration file;
* BAM_to_TCS.py - Module to convert .bam files into the TCS format.
* LICENSE - License file;
* Metrics.py - Module for generating dataset metrics;
* ORFmaker.py - Module for finding ORFs;
* pipeutils.py - Module with code common to several other modules.
* README.md - This file;
* Reporter.py - Module for generating putative SNP reports;
* SAM_to_BAM.py - Module for converting the .sam files into .bam files.
* sff_extractor.py - Module for extracting fasta and fasta.qual from sff files. Originally developed by José Blanca, but forked and ported to python 3 since it was removed from the original website.
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
it from the website (http://python.org/download/). Also required are the python3
header files (the package name in Ubuntu is python3-dev).
Due to the latest release of pysam, python >= 3.4 is now required.
Not strictly required, but highly recommended to for best results are the
external programs that 4Pipe4 uses in it's processes. By default, these are:

* seqclean (http://compbio.dfci.harvard.edu/tgi/software/)
* mira 4.x series (http://mira-assembler.sourceforge.net/)
* getorf (http://emboss.sourceforge.net/apps/cvs/emboss/apps/getorf.html)
* blast (ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/)
* blast2go4pipe (http://www.blast2go.com/data/blast2go/b2g4pipe_v2.5.zip)  - *Seems to have been discontinued*
* etandem (http://helixweb.nih.gov/emboss/html/etandem.html)
* 7zip (http://www.7-zip.org/)
* pysam (https://github.com/pysam-developers/pysam)

These programs are mentioned as "optinal" since you can have for example an
already assembled dataset and just want to run the SNP detection routines,
starting the pipeline from step #4. This would not require sff_extract, seqclean
nor mira to be installed.
All of these programs aer required if you wish to run all the steps in 4Pipe4.
Beware that 4Pipe4 currently relies on the 4.x version of mira, and is not
backward compatible with 3.x versions. If you wish to use a 3.x version of
mira for your assembly you can use an older version of 4Pipe4 (v1.1.3 and
below).

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
"blast", "p7zip", "pysam", "cython" and "setuptools".
2. Download, compile and locally install emboss' "getorf" and "etandem". (This
script requires build tools such as "make" and "gcc". They should be readily
available on any \*nix machine you have access to but don't have root access.)
3. Download local copies of NCBI's "Univec" and "nr" databases.
4. Generate pre-configured entries for all of the above ready to be copied &
pasted into 4Pipe4rc.

These scripts should significantly speed up the installation process of these
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
  -i input_file    Provide the full path to your target input file
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

  -d 454/solexa    Declare the type of data being used. Currentlly suported are 454 (454) and Illumina (solexa). Default is 454.
  -p [True/False]  Is the data paired end? True/False, default is                     False.

The idea here is that to resume an analysis that was interrupted for example after the assembling process you should issue -s '4,5,6,7,8,9' or -s '456789'. Note that some steps depend on the output of previous steps, so using some combinations can cause errors. The arguments can be given in any order.
```

--------------------------------------------

If you wish to run the entire pipeline on 454 data, just issue something like

```
python3 4Pipe4.py -i /path/to/file.sff -o /path/to/results/basefilename
```

However, if you wish to run the pipeline with Illumina data, skip steps 1 and 2,
and add the "-d solexa" switch:

```
python3 4Pipe4.py -i /path/to/reads.fastq -o /path/to/results/basefilename\
-d solexa -s 3,4,5,6,7,8,9
```

Use the -s option to specify only the steps you wish to run from the analysis
and the -c option to point 4Pipe4 to a specific configuration file.

In the directory "Testdata" you will find an example sff file for testing
purposes, as well as documentation on how to do an example run of 4Pipe4.

### CONFIGURATION

The configuration file contains information on every option. You should change
those options to reflect your own system and SNP detection preferences.
Do not forget that the helper scripts will generate most of the config file
for you if you wish.

### CONTACT

If you have questions or feedback you can contact the author by email:
f.pinamartins@gmail.com
For bug reporting, you can use github tracker:
https://github.com/StuntsPT/4Pipe4/issues
For other programs, also please be sure to check out our group's website:
http://cobig2.com

### CITING

[Francisco Pina-Martins, Bruno M. Vieira, Sofia G. Seabra, Dora Batista and Octávio S. Paulo 2016. 4Pipe4 – A 454 data analysis pipeline for SNP detection in datasets with no reference sequence or strain information. BMC Bioinformatics, 17:46.](http://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-016-0892-1)

~~[Old Zenodo DOI](http://dx.doi.org/10.5281/zenodo.13948)~~
