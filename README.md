# CARG (CAS Reports Generator) tool

## Introduction

This psychometric assessment is based upon College Adjustment Scale (CAS).
It is a rapid method of screening college students for common developmental psychological problems.

This tool automates the process of calculating T-scores and generating pdf reports based
on data provided.

## Downloads

Windows setup for compiled application could be found in releases section [(here)](https://github.com/kushaagr/Auto-CAS-Reports/releases).
  
Upon installation the application can be run from start menu or through desktop shortcut.

## How to run code?

Clone git repo to your local machine:  
```
git clone https://github.com/kushaagr/Auto-CAS-Reports.git
```

or  

[Download this code as zip](https://github.com/kushaagr/Auto-CAS-Reports/archive/refs/heads/main.zip)  

After getting code on your local machine, follow either of the two methods.  

### Method 1:
1. Click on setup.bat to install all required python libraries.  
2. Now click on run.bat to execute the python code.  
### Method 2:
1. Open command line and type:
```cmd
pip install -r requirements.txt 
```
2. Then execute python code by typing:
```cmd
python main.py
```

### Compilation command
```
pyinstaller -i ./images/icons8-feather-60.ico -w --noconfirm --add-data "./images/;images" --add-data "./myfonts/;myfonts" main.py
```

### Setup command (if innosetup's program file folder is in path)
```
iscc create-setup.iss
```

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