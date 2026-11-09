#!/bin/bash
# Скрипт запуска игры "Подземелье" для Linux/Mac
cd "$(dirname "$0")"

# Создаём venv, если его ещё нет
if [ ! -d "venv" ]; then
    echo "Создаю виртуальное окружение..."
    python3 -m venv venv
fi

# Активируем venv и ставим зависимости
source venv/bin/activate
pip install -r requirements.txt

# Запускаем игру
python3 main.py

deactivate
