@echo off
chcp 65001 >nul
rem Скрипт запуска игры "Подземелье" для Windows
cd /d "%~dp0"

rem Создаём venv, если его ещё нет
if not exist .venv\Scripts\activate.bat (
    echo Создаю виртуальное окружение...
    python -m venv .venv
)

call .venv\Scripts\activate.bat
pip install -r requirements.txt

python main.py

deactivate
pause
