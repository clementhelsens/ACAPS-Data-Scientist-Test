ACAPS Data Scientist Test
=============

This repository contains the code I used to reply to ACAPS data scientist question November 04-08 2021

Table of contents
=================
  * [ACAPS Data Scientist Test](#ACAPS-Data-Scientist-Test)
  * [Table of contents](#table-of-contents)
  * [RootDataFrame based](#rootdataframe-based)
    * [Getting Started](#getting-started)
    * [Generalities](#generalities)
    * [Pre selection](#pre-selection)
    * [Final selection](#final-selection)
    * [Plotting](#plotting)


RootDataFrame based
=============
Using ROOT dataframe allows a much quicker processing time as it natively supports multithreading. In this implementation, everything from reading EDM4Hep or FCCSW EDM files on eos and producing flat n-tuples, to running a final selection and plotting the results will be explained. ROOT dataframe documentation is availabe [here](https://root.cern/doc/master/classROOT_1_1RDataFrame.html)

Getting Started
============
In order to use ROOT dataframe for the analyses, the dictionary with the analyzers needs to be built and put into  `LD_LIBRARY_PATH` (this happens in `setup.sh`)
