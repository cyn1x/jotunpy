@echo off
setlocal

if %cd% neq %~dp0 cd %~dp0
set PYTHONPATH=.
venv\Scripts\python.exe app\main.py

endlocal