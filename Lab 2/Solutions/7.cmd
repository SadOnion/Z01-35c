@echo off

SETLOCAL ENABLEDELAYEDEXPANSION 
set /a n=%1

set sum=1
echo %num1%

FOR /L %%A IN (1,1,!n!) DO (
    set /a sum=sum*%%A

    
)
echo %sum%