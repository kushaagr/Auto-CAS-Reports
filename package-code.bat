@echo off
ECHO Update AppVersion in .iss script
rem TIMEOUT 3
@pause
@echo on
notepad "C:\git\Auto-CAS-Reports\create-setup.iss"
pyinstaller -i ./images/icons8-feather-60.ico -w --noconfirm --add-data "./images/;images" --add-data "./myfonts/;myfonts" main.py
iscc create-setup.iss

