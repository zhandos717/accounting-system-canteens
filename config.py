import json
import os

# Путь к файлу конфигурации
CONFIG_FILE = "config.json"

# Функция для сохранения настроек
def save_config(data):
    # Открываем файл в режиме записи ('w') и с указанием кодировки
    with open(CONFIG_FILE, 'w', encoding='utf-8') as config_file:
        json.dump(data, config_file, ensure_ascii=False, indent=4)  # Записываем данные в файл с форматированием

# Функция для загрузки настроек
def load_config():
    if os.path.exists(CONFIG_FILE):
        # Открываем файл в режиме чтения ('r') и с указанием кодировки
        with open(CONFIG_FILE, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)  # Загружаем данные из файла
    # Если файл не существует, возвращаем значение по умолчанию
    return {"api_url": "http://localhost:8000"}
