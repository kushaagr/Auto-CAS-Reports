import os
DEBUG_MODE = False
DBNAME      = "entries.db"
DBLOC       = f"{os.environ['USERPROFILE']}\\.survey-data\\"
DB          = DBLOC + DBNAME
REPORTSFOL  = f"{os.environ['USERPROFILE']}\\.survey-data\\reports"
RAWFOL      = f"{os.environ['USERPROFILE']}\\.survey-data\\raw"
TEMPDIR     = f"{os.environ['USERPROFILE']}\\.survey-data\\TEMP"
LOGDIR      = f"{os.environ['USERPROFILE']}\\.survey-data\\logs"
LOGFILE     = f"{LOGDIR}\\simple-log.txt"