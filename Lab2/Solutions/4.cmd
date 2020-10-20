@echo off
::Enabledelayedexpansion pozwala na !var! przez co wartos odczytywana jest w momencie gdy jest potrzebna
SETLOCAL ENABLEDELAYEDEXPANSION 
set /a n=%1
set /a n=%n-1
set num1=0
set num2=1
echo %num1%

FOR /L %%A IN (1,1,!n!) DO (
    set /a next=!num1!+!num2!
    set /a num1=!num2!
    set /a num2=!next!
    echo !num1!
)