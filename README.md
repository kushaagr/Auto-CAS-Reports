# CARG (CAS Reports Generator) tool

## Introduction

This psychometric assessment is based upon College Adjustment Scale (CAS).
It is a rapid method of screening college students for common developmental psychological problems.

This tool automates the process of calculating T-scores and generating pdf reports based
on data provided.


## Application input

* The data could be provided either in form of excel sheet (first sheet should contain the data) or csv.
* The sheet in excel file which contains data should be named 'Raw Data' (case sensitive), or the 
    first sheet in excel file should contain the data.
* First 13 columns are about student details and next 108 columns identify the survey questions or fields.
* A row must contain students' response, where the answer to survey questions could be one of the four choices:  
``` 
'False'
'Slightly True'  
'Mainly True'  
'Very True'
```

| Timestamp | Email Address | Score | NAME | EMAIL ID | GUARDIAN NAME | AGE | GENDER | MOBILE NUMBER | NAME OF INSTITUTE | STREAM | YEAR | MONTHLY FAMILY INCOME | ... |
| :-------- | :------------ | :---- | :--- | :------- | :------------ | :-- | :----- | :------------ | :---------------- | :----- | :--- | :-------------------- | :-- |

Required an excel or csv file where columns should be:

* TIMESTAMP
* EMAIL ADDRESS
* SCORE
* NAME
* EMAIL ID
* GUARDIAN NAME
* AGE
* GENDER
* MOBILE NUMBER
* NAME OF INSTITUTE
* STREAM
* YEAR
* MONTHLY FAMILY INCOME
* followed by 108 columns of questions defined by CAS ..

---

## Contributors:

* Ashutosh Dubey      (IMCA 2021 batch)
* Durva Shinde        (IMCA 2021 batch)
* Kushagra Mehrotra   (IMCA 2019 batch)
Made by students at Acropolis FCA Department