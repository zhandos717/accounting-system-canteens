import flet as ft
import requests
from config import load_config
from services.http_client import HttpClient

config = load_config()

client = HttpClient()


def home_page(page: ft.Page):
    # Цвета и стили
    primary_color = ft.colors.BLUE_800
    button_color = ft.colors.GREEN_500
    background_color = ft.colors.GREY_100
    accent_color = ft.colors.ORANGE_600
    btn_color = ft.colors.WHITE

    # Ввод ID сотрудника
    employee_id_input = ft.TextField(
        label="Сканируйте QR-код сотрудника",
        prefix_icon=ft.icons.QR_CODE_SCANNER,
        width=500,
        height=60,
        text_size=20,
        filled=True,
        bgcolor=background_color,
        border_radius=ft.border_radius.all(8),
    )

    # Лог для вывода действий
    action_log = ft.ListView(expand=True, spacing=5, padding=ft.Padding(10, 10, 10, 10))

    # Логика для регистрации прихода на работу
    def record_attendance(e):
        employee_id = employee_id_input.value
        if employee_id:
            response = client.post("/attendance", json={"employee_id": employee_id})
            if response.status_code == 200:
                action_log.controls.append(
                    ft.Text(f"Приход записан для {employee_id}", color=ft.colors.GREEN_600, size=18))
            else:
                action_log.controls.append(
                    ft.Text(f"Ошибка: {response.json()['detail']}", color=ft.colors.RED_600, size=18))
        else:
            action_log.controls.append(ft.Text("Пожалуйста, введите ID сотрудника", color=ft.colors.RED_600, size=18))
        page.update()

    # Кнопка для регистрации прихода
    attendance_button = ft.ElevatedButton(
        content=ft.Row(
            controls=[ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.colors.WHITE), ft.Text("Записать приход", size=20)],
            alignment=ft.MainAxisAlignment.CENTER,

        ),
        style=ft.ButtonStyle(
            bgcolor=button_color,
            color=btn_color,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(30, 20, 30, 20),
        ),
        on_click=record_attendance,
    )

    # Кнопка для перехода на страницу медосмотра
    medical_check_button = ft.ElevatedButton(
        adaptive=True,  # a CupertinoButton will be rendered when running on apple-platform
        bgcolor=ft.cupertino_colors.ACTIVE_GREEN,
        content=ft.Row(
            controls=[ft.Icon(ft.icons.MEDICAL_SERVICES, color=ft.colors.WHITE), ft.Text("Медосмотр", size=20)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        style=ft.ButtonStyle(
            color=btn_color,
            bgcolor=accent_color,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 10, 20, 10),
        ),
        on_click=lambda e: page.go("/medical"),
    )

    # Кнопка для перехода на страницу покупки еды
    buy_food_button = ft.ElevatedButton(
        adaptive=True,  # a CupertinoButton will be rendered when running on apple-platform
        bgcolor=ft.cupertino_colors.ACTIVE_GREEN,
        content=ft.Row(
            controls=[ft.Icon(ft.icons.RESTAURANT, color=ft.colors.WHITE), ft.Text("Покупка еды", size=20)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        style=ft.ButtonStyle(
            color=btn_color,
            bgcolor=ft.colors.RED_500,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 10, 20, 10),
        ),
        on_click=lambda e: page.go("/buy_food"),
    )

    # Кнопка для перехода на страницу настроек
    settings_button = ft.ElevatedButton(
        adaptive=True,  # a CupertinoButton will be rendered when running on apple-platform
        bgcolor=ft.cupertino_colors.ACTIVE_GREEN,
        content=ft.Row(
            controls=[ft.Icon(ft.icons.SETTINGS, color=ft.colors.WHITE), ft.Text("Настройки", size=20)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        style=ft.ButtonStyle(
            color=btn_color,
            bgcolor=ft.colors.BLUE_500,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 10, 20, 10),
        ),
        on_click=lambda e: page.go("/settings"),
    )

    # Создаем и возвращаем страницу
    return ft.View(
        "/",
        controls=[
            ft.Container(
                content=ft.Text("Система учета питания сотрудников", size=32, weight=ft.FontWeight.BOLD,
                                color=primary_color),
                alignment=ft.alignment.center,
                padding=ft.Padding(20, 10, 10, 10),
            ),
            ft.Container(employee_id_input, alignment=ft.alignment.center, padding=ft.Padding(20, 10, 10, 10)),
            ft.Container(attendance_button, alignment=ft.alignment.center, padding=ft.Padding(20, 10, 10, 10)),
            ft.Container(
                ft.Row(
                    controls=[medical_check_button, buy_food_button, settings_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                padding=ft.Padding(20, 10, 10, 10),
            ),
            ft.Container(ft.Text("История действий:", size=24, color=primary_color),
                         padding=ft.Padding(10, 10, 10, 10)),
            ft.Container(action_log, padding=ft.Padding(20, 10, 10, 10), bgcolor=background_color),
        ],
    )
