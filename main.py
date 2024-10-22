import os
import flet as ft
from pages.home import home_page
from pages.medical import medical_page
from pages.buy_food import buy_food_page
from pages.settings import settings_page
from pages.login import login_page  # Добавляем импорт страницы логина
from config import load_config

# Загрузка конфигурации
config = load_config()

# Функция для настройки параметров окна
def setup_window(page: ft.Page):
    page.title = "Employee Food System"

# Главная функция приложения
def main(page: ft.Page):
    setup_window(page)

    # Обработчик изменения маршрута
    def route_change(route):
        page.views.clear()

        # Обработка маршрутов к страницам
        if page.route == "/":
            page.views.append(home_page(page))
        elif page.route == "/medical":
            page.views.append(medical_page(page))
        elif page.route == "/buy_food":
            page.views.append(buy_food_page(page))
        elif page.route == "/settings":
            page.views.append(settings_page(page))
        elif page.route == "/login":  # Маршрут для страницы логина
            page.views.append(login_page(page))
        else:
            # Обработка неизвестного маршрута
            page.views.append(ft.View("/404", controls=[
                ft.Text("404 - Страница не найдена", size=24)
            ]))

        page.update()

    # Начальная страница — логин
    page.on_route_change = route_change
    page.go("/login")  # Стартовая страница — это "/login"

# Запуск приложения
if __name__ == "__main__":
    ft.app(target=main)
