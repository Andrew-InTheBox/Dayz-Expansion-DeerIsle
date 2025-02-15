@echo off
:start
::Name for the CMD window
set serverName=ACBlocal
::Server files location
set serverLocation="C:\Program Files (x86)\Steam\steamapps\common\DayZServerDITrader"
::Server Port
set serverPort=2302
::Server config
set serverConfig=serverDZ.cfg
::Server profile folder
set serverProfile=config
::Logical CPU cores to use (Equal or less than available)
set serverCPU=4
::Sets title for terminal (DONT edit)
title %serverName% batch
::DayZServer location (DONT edit)
cd "%serverLocation%"

::Create mods variable by concatenating directory names starting with "@" in the current directory
setlocal enabledelayedexpansion
set "mods="
for /d %%D in (@*) do (
    if not defined mods ( 
        set "mods=%%~D"
    ) else (
        set "mods=!mods!;%%~D"
    )
)
::echo local Mod list: !mods!

:: Export mods to global scope
endlocal & set "mods=%mods%"

echo Server mod list: %mods%
echo (%time%) %serverName% started.

::Launch parameters (edit end: -config=|-port=|-profiles=|-doLogs|-adminLog|-netLog|-freezeCheck|-filePatching|-BEpath=|-cpuCount=)
start "DayZ Server" /min "DayZServer_x64.exe" -config=%serverConfig% -mod=%mods% "-serverMod=_@DayZ-Dynamic-AI-Addon;_@Heatmap" -port=%serverPort% -profiles=%serverProfile% -cpuCount=%serverCPU% -adminlog -netlog -freezecheck 

::Time in seconds before kill server process (14400 = 4 hours)
timeout 14390
taskkill /im DayZServer_x64.exe /F
::Time in seconds to wait before..
timeout 10
::Go back to the top and repeat the whole cycle again
goto start
