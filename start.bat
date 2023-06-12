@echo off
setlocal

if %cd% neq %~dp0 cd %~dp0
set PYTHONPATH=.

set "ENVIRONMENT="
set "VALID="
IF "%~1"=="-h" goto :printUsage
IF "%~1"=="--help" goto :printUsage
IF "%~1"=="--dev" (
    set VALID=1
    set ENVIRONMENT=DEVELOPMENT
)
IF "%~1"=="--build" (
    set VALID=1
    set ENVIRONMENT=PRODUCTION
)
IF defined VALID (
    venv\Scripts\python.exe app\main.py %~1
    goto :EOF
) else (
    echo Error: Invalid argument. Unknown argument %~1
    echo Usage: start.bat [-h] [dev] [build]
    goto :EOF
)

:printUsage
    echo usage: start.bat [-h] [dev] [build [--optimize] [--no-optimize]]
    echo:
    echo static site generator and development server.
    echo:
    echo options:
    echo -h, --help  show this help message and exit
    echo --dev       run the development server
    echo --build     bundle for production deployment

endlocal