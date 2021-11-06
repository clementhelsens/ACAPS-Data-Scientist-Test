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
    * [Retrieve the data](#retrieve-the-data)
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
Retrieve the data
-
First we collect the data locally for the 18 last months when possible and we produce merged files, where the ```results``` field are merged.

```
python get_acapsdata.py --type isi_log --merge
```

Then for the inform severity index and the humanitarian access we produce one file per month.

```
python get_acapsdata.py --type isi --nmonths 18
python get_acapsdata.py --type ha --nmonths 18
```

Now that we have the data locally, we can proceed with analysing them.

Question 1
-
To run the code for the first question, just do

```
python question1.py "data/isi_*.json"
```

it will display something like

```
---- data set size original		 2593
---- number of crisis original		 176
---- data set size filter null		 2226
---- number of crisis filter null	 156
---- data set size filter >1		 2222
---- number of crisis filter >1		 152
Over the last 18 months, the following crises have a larger "INFORM Severity Index" at the last update with respect to the first entry in the database
number	id		var(last-first)	max increase	max decrease
1 	 AFG001 	 0.20 		 0.20 		 0.00
2 	 ARM002 	 0.00 		 0.10 		 -0.10
3 	 BDI001 	 0.60 		 0.70 		 -0.10
...
...
...
150 	 ZMB002 	 0.20 		 0.20 		 -0.10
151 	 ZWE001 	 -0.20 		 0.00 		 -0.20
152 	 ZWE003 	 0.00 		 0.00 		 0.00
over the full period the number of crises out of 152 that have: increase=102   decrease=25   stable=25
within each time period 131 crises out of 152 have suffered from an increase of the index

```

Question 1
-
To run the code for the third question, just do

```
python  question3.py  "data/isi_*.json" "data/ha_*.json"
```
it will display something like

```
============ correlation between "INFORM Severity Index" and "Humanitarian ACCESS" using all the crises and all the data:  0.6723865337297351
============ correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id  AFG001   0.8528028654224437
============ can not calculate correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id  ARM002
============ correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id  BDI001   -0.4195465528466834
============ can not calculate correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id  BFA002
============ can not calculate correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id  BFA003
============ can not calculate correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id  BFA004
...
...
...
============ correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id  ZWE001   -0.8770580193070295
============ can not calculate correlation between "INFORM Severity Index" and "Humanitarian ACCESS" for crisis id  ZWE003
unable to calculate correlations for 59 out of 156 crises, list: ['ARM002', 'BFA002', 'BFA003', 'BFA004', 'CAF002', 'CHN002', 'CHN003', 'COD002', 'COG002', 'COG004', 'COL001', 'COL002', 'COL003', 'DJI001', 'DJI002', 'DJI003', 'DJI004', 'ECU002', 'ERI001', 'ESP002', 'ETH004', 'FJI002', 'GTM003', 'HND002', 'HTI002', 'IDN006', 'IDN007', 'IND004', 'ITA002', 'LBN004', 'LSO002', 'MDG004', 'MDG005', 'MEX004', 'MMR004', 'MOZ007', 'NER005', 'NIC002', 'PAK001', 'PHL004', 'PHL009', 'PRK001', 'REG006', 'SDN007', 'SLV001', 'SSD001', 'SWZ001', 'TCD001', 'TCD003', 'TCD004', 'TCD005', 'TLS002', 'TTO002', 'TZA002', 'UGA001', 'UKR002', 'VNM002', 'VUT002', 'ZWE003']
```
