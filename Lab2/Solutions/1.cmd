@echo off
set msg=%~1*.%2
echo Files in dir: %msg%
dir "%msg%" /b

