@echo off
rem Скрипт запуска игры "Подземелье" для Windows
cd /d "%~dp0"

rem Создаём venv, если его ещё нет
if not exist venv\Scripts\activate.bat (
    echo Создаю виртуальное окружение...
    python -m venv venv
)

rem Активируем venv и ставим зависимости (пока их нет, но на будущее)
call venv\Scripts\activate.bat
pip install -r requirements.txt

rem Запускаем игру
python main.py

deactivate
pause
