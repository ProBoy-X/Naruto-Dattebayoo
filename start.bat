@echo off
TITLE phantom Robot
rem This next line removes any fban csv files if they exist in root when bot restarts. 
del *.csv
py -3.9 --version
IF "%ERRORLEVEL%" == "0" (
    py -3.9 -m Naruto
) ELSE (
    py -m Naruto
)

pause
