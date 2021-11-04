ACAPS Data Scientist Test
=============

This repository contains the code I used to reply to ACAPS data scientist question November 04-08 2021

Table of contents
=================
  * [ACAPS Data Scientist Test](#ACAPS-Data-Scientist-Test)
  * [Table of contents](#table-of-contents)
  * [Questions](#questions)
  * [Setup](#setup)
  * [How to run the code](#how-to-run-the-code)
    * [Get the data](#get-the-data)
    * [Question 1](#question-1)
    * [Question 2](#question-2)
    * [Question 3](#question-3)

Questions
-
Below are the questions asked 
1. Which crises show a deterioration in severity, as measured by theINFORM Severity Index, during the last 18 months?  
   *Use the /api/v1/inform-severity-index/{date}/ endpoint of ACAPS API, where {date} is in the format MMMYYYY, e.g., Nov2021. The "INFORM Severity Index" field gives the overall score.*
2. Explore the indicators of the INFORM Severity Index model. Are
   there indicators which show a particularly strong increase or
   decrease, or an interesting change, over the last 18 months? Pick
   out some interesting features for some crises.  
*Use the /api/v1/inform-severity-index/log/ endpoint of ACAPS API.*
3. Is there a correlation between the severity of a crisis, as measured by the INFORM Severity Index, and the humanitarian access score?  
*Use the /api/v1/humanitarian-access/{date}/ endpoint to access the humanitarian access scores.*

Setup
=============
To run you need python 3, the request package, pandas and other
things. On my local machine I am using anaconda to create a dedicated
virtual environement with python 3.7.11. Then on top of this just
install with pip:
```
pip install pandas
pip install requests
pip install matplotlib
```

How to run the code
============
Get the data
-
First we collect the data locally for the 18 last months when possible (the last request will take some time)
```
python get_acapsdata.py --type isi --nmonths 18
python get_acapsdata.py --type ha --nmonths 18
python get_acapsdata.py --type isi_log

```
Now that we have the data locally, we can proceed with analysing them.

Question 1
-
