@echo off
:: Przekierowanie Outputu konsoli (STDOUT) oraz  błędów(STDERR) do nul
net session >nul 2>&1 
if %errorLevel% == 0 (
    echo Posiadasz Uprawnienia Administratora! 
) else (
    echo Nie posiadasz uprawnien administratora!
)