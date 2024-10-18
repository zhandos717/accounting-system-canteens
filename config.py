import json
import os

# Путь к файлу конфигурации
CONFIG_FILE = "config.json"

# Функция для сохранения настроек
def save_config(data):
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(data, config_file)

# Функция для загрузки настроек
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.load(config_file)
    return {"api_url": "http://localhost:8000"}  # Значение по умолчанию
