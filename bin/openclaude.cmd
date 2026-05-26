@echo off
setlocal

set "OPENCLAUDE_BIN=%~dp0"
if not defined OPENCLAUDE_HOME set "OPENCLAUDE_HOME=%OPENCLAUDE_BIN%.."

node "%OPENCLAUDE_BIN%openclaude" %*
exit /b %ERRORLEVEL%
