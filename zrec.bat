:: This script starts firefox with a (Zoom) url and the appropriate OBS Studio shortcut (.lnk) 
:: to start recording the screen
:: USAGE
:: zrec.bat SHORTCUT_PATH URL
@echo off

set shortcut_path=%1
set url=%2

cd "C:\Program Files\Mozilla Firefox\"
start firefox.exe %url%

start "" %shortcut_path%
exit