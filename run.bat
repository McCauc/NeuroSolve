@echo off
setlocal
set "NEUROSOLVE_DEV=1"
set "SCRIPT_DIR=%~dp0"
set "REQUIREMENTS=%SCRIPT_DIR%requirements.txt"

where py >nul 2>nul
if %errorlevel%==0 (
    echo Checking dependencies...
    py -3 -m pip install --user -q --disable-pip-version-check -r "%REQUIREMENTS%"
    if errorlevel 1 (
        echo Failed to install project dependencies.
        exit /b %errorlevel%
    )
    echo Launching NeuroSolve...
    py -3 -m src.ui.app
    exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel%==0 (
    echo Checking dependencies...
    python -m pip install --user -q --disable-pip-version-check -r "%REQUIREMENTS%"
    if errorlevel 1 (
        echo Failed to install project dependencies.
        exit /b %errorlevel%
    )
    echo Launching NeuroSolve...
    python -m src.ui.app
    exit /b %errorlevel%
)

echo No suitable Python runtime found.
echo Install Python 3.10+ and try again.
exit /b 1
