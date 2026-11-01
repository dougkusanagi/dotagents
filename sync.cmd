@echo off
call "%~dp0bin\run-bash.cmd" "%~dp0bin\sync" %*
exit /b %errorlevel%
