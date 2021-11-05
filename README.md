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
First we collect the data locally for the 18 last months when possible and we produce merged files, where the ```results``` field are merged.

```
python get_acapsdata.py --type isi --nmonths 18 --merge
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
To run the first approach for the first question, just do
```
python question1_1.py data/isi_18months.json 
```

it will display something like

```
Over the last 18 months, the following crises have a larger "INFORM Severity Index" at the last update with respect to the first entry in the database
id	date begin	date end	duration	isi begin	isi end		isi diff
AFG001 	 2020-04-29 	 2021-09-15 	 504 		 4.5 		 4.7 		 0.20
BDI001 	 2020-04-28 	 2021-06-09 	 407 		 3.3 		 3.8 		 0.50
BFA002 	 2020-03-22 	 2021-06-30 	 465 		 3.4 		 3.9 		 0.50
BGD002 	 2020-04-29 	 2021-10-20 	 539 		 3.1 		 3.2 		 0.10
BRA002 	 2020-04-29 	 2021-06-11 	 408 		 2.2 		 2.5 		 0.30
CAF001 	 2020-03-30 	 2021-09-28 	 547 		 4.0 		 4.3 		 0.30
```

and 

```
Over the last 18 months, the following crises have an "INFORM Severity Index" that has increased wrt a previous minimum, and thus shows a larger increase with respect to first - last entry
id	date min	date max	duration	isi min		isi max		isi diff
BDI001 	 2020-05-28 	 2021-06-09 	 377 		 3.2 		 3.9 		 0.70
BFA002 	 2020-03-22 	 2021-06-30 	 465 		 3.4 		 4.1 		 0.70
BGD002 	 2020-04-29 	 2020-06-05 	 37 		 3.1 		 3.3 		 0.20
BRA002 	 2020-04-29 	 2021-06-11 	 408 		 2.2 		 2.6 		 0.40
CMR001 	 2020-05-28 	 2021-06-07 	 375 		 3.5 		 4.2 		 0.70
CMR002 	 2020-08-26 	 2021-10-26 	 426 		 3.1 		 3.7 		 0.60
```

To run the second approach for the first question, just do
```
python question1_2.py data/isi_*.json 
```
