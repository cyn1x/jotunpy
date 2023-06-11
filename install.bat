@echo off
setlocal

set "programName=python"

REM Check if Python is installed
%programName% -V

REM Check the errorlevel to determine if the program is installed
if %errorlevel% equ 0 (
    echo Python detected. Proceeding with installation.
    goto :install
) else (
    echo Python not detected. Aborting installation.
    goto :EOF
)

:install
    REM install virtual environment and required dependencies
    echo Configuring virtual environment
    python -m venv %~dp0\venv

    echo Installing required dependencies
    %~dp0\venv\Scripts\pip.exe install -r %~dp0\requirements.txt

    echo:
    if %errorlevel% equ 0 (
        echo Install complete
        goto :success
    ) else (
        echo Errors were encountered during installation. Aborting.
        goto :EOF
    )

:success
    echo Run start.bat to start the development server
    echo Run build.bat to build the site for deployment

endlocal