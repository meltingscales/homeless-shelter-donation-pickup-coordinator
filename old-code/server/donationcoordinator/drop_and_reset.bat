@setlocal enableextensions
@cd /d "%~dp0"
@ECHO OFF

net session >nul 2>&1
if %errorLevel% == 0 (
        echo Success: Administrative permissions confirmed.

	
	py manage.py reset_db
	py manage.py makemigrations
	py manage.py migrate

) else (
        echo Failure: Current permissions inadequate.
)


PAUSE