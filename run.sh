#!/bin/bash
# Скрипт запуска игры "Подземелье" для Linux/Mac
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Создаю виртуальное окружение..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

python3 main.py

deactivate
