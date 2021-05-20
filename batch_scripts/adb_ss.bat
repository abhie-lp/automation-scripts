@echo off

setlocal
:: Extract date parameters
set dd=%date:~0,2%
set mm=%date:~3,2%
set yyyy=%date:~6,4%
set FILE_DATE=%yyyy%-%mm%-%dd%

:: Extract time parameters
set HH=%time:~0,2%
set MM=%time:~3,2%
set SS=%time:~6,2%

:: Fix the whitespace in hour
if "%HH:~0,1%" == " " set HH=0%HH:~1,1%
set FILE_TIME=%HH%_%MM%_%SS%

set RECORDING_DIRECTORY=%HOMEPATH%\Documents\Screenshots
set FILE_PREFIX=%FILE_DATE%_%FILE_TIME%
set TARGET_FILENAME=%RECORDING_DIRECTORY%\%FILE_PREFIX%
set COMMAND=adb

set DEVICE_ID=""
set FILENAME=""

:loop
if not "%1"=="" (
  if "%1"=="-s" (
    :: Serial number of the device is provided
    set DEVICE_ID=%2
    shift
  ) else if "%1"=="--serial" (
    :: Serial number of the device is provided
    set DEVICE_ID=%2
    shift
  ) else if "%1"=="-f" (
    :: Filename to be used as a suffix
    set FILENAME=%2
    shift
  ) else if "%1"=="--filename" (
    :: Filename to be used as a suffix
    set FILENAME=%2
    shift
  ) else if "%1"=="-d" (
    :: Device name is given and serial_id will be picked fetched from local or global variable
    call set "DEVICE_ID=%%%2%%"
    shift
  ) else if "%1"=="--device" (
    :: Device name is given and serial_id will be picked fetched from local or global variable
    call set "DEVICE_ID=%%%2%%"
    shift
  )
  shift
  goto :loop
)

:: Set the command of there is a device id
if not %DEVICE_ID%=="" (
  set COMMAND=%COMMAND% -s %DEVICE_ID%
  echo Recording will be started for %DEVICE_ID%
)

:: Set the filename of the screenshot
if not %FILENAME%=="" (
  set TARGET_FILENAME=%TARGET_FILENAME%_%FILENAME%.png
) else (
  set TARGET_FILENAME=%TARGET_FILENAME%.png
)

echo Screenshot will be stored in %TARGET_FILENAME%

echo.
set COMMAND=%COMMAND% exec-out screencap -p

%COMMAND% > %TARGET_FILENAME%
endlocal