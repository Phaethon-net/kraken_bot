@echo off
set NSSM=nssm
set SRVNAME=KrakenBot
set SRVDIR=%~dp0..
set PY=python
%NSSM% install %SRVNAME% "%PY%" "%SRVDIR%\main.py"
%NSSM% set %SRVNAME% AppDirectory "%SRVDIR%"
%NSSM% set %SRVNAME% AppEnvironmentExtra ENVIRONMENT=live
%NSSM% set %SRVNAME% Start SERVICE_AUTO_START
%NSSM% start %SRVNAME%
echo Service installed. Check Services.msc for status.
