import os

import flet as ft
from pages.home import home_page
from pages.medical import medical_page
from pages.buy_food import buy_food_page
from pages.settings import settings_page
from config import load_config

# Загрузка настроек при запуске приложения
config = load_config()

def main(page: ft.Page):
    page.title = "Employee Food System"
    # Используем новые свойства вместо устаревших
    page.window.width = 800
    page.window.height = 600
    # Управление маршрутами
    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(home_page(page))
        elif page.route == "/medical":
            page.views.append(medical_page(page))
        elif page.route == "/buy_food":
            page.views.append(buy_food_page(page))
        elif page.route == "/settings":
            page.views.append(settings_page(page))

        page.update()

    # Старт с главной страницы
    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
