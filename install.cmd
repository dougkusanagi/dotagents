@echo off
call "%~dp0bin\run-bash.cmd" "%~dp0install.sh" %*
exit /b %errorlevel%
