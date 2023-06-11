@echo off
setlocal

if %cd% neq %~dp0 cd %~dp0
set PYTHONPATH=.

set "TRUE="
IF "%~1"=="-h" goto :printUsage
IF "%~1"=="--help" goto :printUsage
IF "%~1"=="--dev" set TRUE=1
IF "%~1"=="--build" set TRUE=1
IF defined TRUE (
    venv\Scripts\python.exe app\main.py %~1
    goto :EOF
) else (
    echo Error: Invalid argument. Unknown argument %~1
    echo Usage: start.bat [-h] [--dev] [--build]
    goto :EOF
)

:printUsage
    echo usage: start.bat [-h] [--dev] [--build]
    echo:
    echo static site generator and development server.
    echo:
    echo options:
    echo -h, --help  show this help message and exit
    echo --dev       run the development server
    echo --build     bundle for production deployment

endlocal