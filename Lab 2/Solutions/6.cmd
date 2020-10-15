@echo off
chcp 65001
setlocal ENABLEDELAYEDEXPANSION 
call :Print_All_Files "%1"
Exit /b 0

:Print_All_Files
    
    call :Print_Files_With_Level %~1 1
    
    for /f %%B in ('dir "%~1" /ad /b') do (
        echo %%B
        call :Print_Dir_Recursive %~1\%%B 1
    )
    Exit /B 0
:Print_Files_With_Level

    set "str=─"
    for /L %%X in (1,1,%~2) do set "str=!str!─"
    set "white= "
    for /L %%X in (1,1,%nextLevel%) do set "white=!white!  "
    
    for /f "usebackq delims=?" %%A in (`dir "%~1" /a-d-h-o-i /b`) do (
        if %~2 == 1 (echo ─%%A) else (echo %white%└!str!%%A)
    )


    Exit /b 0
:Print_Dir_Recursive

    set /a nextLevel=%~2+1
    call :Print_Files_With_Level "%~1" %nextLevel%

    set "white= "
    for /L %%X in (1,1,%nextLevel%) do set "white=!white!  "
        
    for /f "usebackq delims=?" %%B in (`dir "%~1" /ad /b`) do (
        
        echo !white!%%B
        
        call :Print_Dir_Recursive "%~1\%%B" %nextLevel%
        
    )
    Exit /b 0
