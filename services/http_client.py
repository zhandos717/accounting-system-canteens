# services/http_client.py
import requests
from config import load_config

class HttpClient:
    def __init__(self):
        # Загружаем URL API и токен из конфигурации
        config = load_config()
        self.base_url = config.get("api_url", "http://localhost:8000")
        self.token = config.get("api_token", None)  # Загружаем токен из конфигурации

    def get_headers(self, additional_headers=None):
        headers = {
            "Content-Type": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"  # Добавляем токен в заголовок
        if additional_headers:
            headers.update(additional_headers)
        return headers

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, headers=self.get_headers(headers))
            response.raise_for_status()  # Поднимаем исключение при неуспешных статусах
            return response.json()  # Возвращаем только JSON
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            return None  # Возвращаем None при ошибке
        except Exception as e:
            print(f"Error: {str(e)}")
            return None  # Возвращаем None при ошибке

    def post(self, endpoint, json=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=json, headers=self.get_headers(headers))
            response.raise_for_status()  # Поднимаем исключение при неуспешных статусах
            return response  # Возвращаем полный объект response
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            return None  # Возвращаем None при ошибке
        except Exception as e:
            print(f"Error: {str(e)}")
            return None  # Возвращаем None при ошибке
