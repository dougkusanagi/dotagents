@echo off
rem Executa um script Bash com o Git Bash (nunca o bash.exe do WSL).
rem Uso: run-bash.cmd <script> [argumentos...]
setlocal
set "BASH="
for %%P in ("%ProgramFiles%\Git\bin\bash.exe" "%ProgramW6432%\Git\bin\bash.exe" "%LOCALAPPDATA%\Programs\Git\bin\bash.exe") do if not defined BASH if exist "%%~P" set "BASH=%%~P"
if not defined BASH for /f "delims=" %%G in ('where git.exe 2^>nul') do if not defined BASH (
  if exist "%%~dpG..\bin\bash.exe" set "BASH=%%~dpG..\bin\bash.exe"
  if not defined BASH if exist "%%~dpG..\usr\bin\bash.exe" set "BASH=%%~dpG..\usr\bin\bash.exe"
)
if not defined BASH (
  echo erro: Git para Windows nao encontrado. Instale em https://git-scm.com/download/win 1>&2
  exit /b 1
)
"%BASH%" %*
exit /b %errorlevel%
