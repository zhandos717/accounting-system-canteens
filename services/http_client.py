# services/http_client.py
import requests
from config import load_config

class HttpClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HttpClient, cls).__new__(cls)
            config = load_config()
            cls._instance.base_url = config.get("api_url", "http://localhost:8000")
            cls._instance.token = config.get("api_token", None)
        return cls._instance

    def update_config(self):
        config = load_config()
        self.base_url = config.get("api_url", "http://localhost:8000")
        self.token = config.get("api_token", None)

    def get_headers(self, additional_headers=None):
        headers = {
            "Content-Type": "application/json"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if additional_headers:
            headers.update(additional_headers)
        return headers

    def get(self, endpoint, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, headers=self.get_headers(headers))
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def post(self, endpoint, json=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=json, headers=self.get_headers(headers))
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            print(f"HTTP Error: {err}")
            return None
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

# Создание глобального экземпляра
client = HttpClient()
