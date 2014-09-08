4Pipe4 Test data
================

### Description

The test dataset is an sff file, which was created from a controlled subset of
an original sff file with transcriptomic data obtained from a pool of Quercus
individuals.

The original dataset was obtained via 454 Titanium technology.

This example dataset does not aim to be representative of the original dataset,
but rather a quick and simple way to demonstrate the use of 4Pipe4.

It contains approximately 2600 reads which is more than enough to work as an
example and results in a very quick analysis process.

In this same directory you will find a file named TestData.report.7z with an
example report of a full 4Pipe4 run with default settings.

### Example usage

Using this test file with 4Pipe4 is rather simple. Just follow these steps
(adjust as necessary to your use case):

1. Create a new directory for your test analysis:
    - mkdir ~/4PipeTest
2. Copy your 4Pipe4rc into the test directory:
    - cp /path/to/4pipe4rc ~/4PipeTest/4PipeTestrc
3. Adjust your new configuration file as needed using your favourite text editor
(in this case Vim):
    - vim ~/4PipeTest/4PipeTestrc
4. Copy (or move) the testfile into your test location:
    - cp /path/to/testfile ~/4PipeTest/4PipeTest.sff
5. Run 4Pipe4:
    - python3 /path/to/4Pipe4.py -c ~/4PipeTest/4PipeTestrc -i ~/4PipeTest/4PipeTest.sff -o ~/4PipeTest/test01
6. Your analysis report can now be found in the resulting 7zip file:
    - ~/4PipeTest/test01.report.7z

This will run the whole pipeline. If you wish to skip some steps you can do so
with with the "-s" option.

### Expected results

If running 4Pipe4 with it's default settings you should expect to find around
4 SNPs with different characteristics.

Changing the parameters in the used 4Pipe4 configuration file will result in a
different amount of SNPs being found.
