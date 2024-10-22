import flet as ft
import requests

from components.employee_field import EmployeeField
from services.http_client import HttpClient

client = HttpClient()


def medical_page(page: ft.Page):
    primary_color = ft.colors.BLUE_800

    employee_id_input = EmployeeField()

    def medical_check(e):
        employee_id = employee_id_input.value
        if employee_id:
            response = client.post("/medical_check", json={"employee_id": employee_id})

            if response is None:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Не удалось отправить запрос"))
            elif response.status_code == 200:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Медосмотр пройден для {employee_id}"))
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {response.json()['detail']}"))
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Пожалуйста, введите ID сотрудника"))
        page.snack_bar.open = True
        page.update()

    save_button = ft.ElevatedButton(
        adaptive=True,
        content=ft.Text("Допустить", size=20),
        bgcolor=ft.colors.GREEN_500,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN_500,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 10, 20, 10),
        ),
        on_click=medical_check
    )

    # Кнопка для возврата на главную страницу
    back_button = ft.ElevatedButton(
        adaptive=True,
        content=ft.Text("Назад", size=20),
        bgcolor=ft.colors.BLUE_500,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_500,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 10, 20, 10),
        ),
        on_click=lambda e: page.go("/")
    )

    return ft.View(
        "/medical",
        controls=[
            ft.Container(ft.Text("Медосмотр сотрудников", size=32, weight=ft.FontWeight.BOLD, color=primary_color),
                         padding=ft.Padding(20, 10, 10, 10)),
            ft.Container(employee_id_input, alignment=ft.alignment.center, padding=ft.Padding(20, 10, 10, 10)),
            ft.Container(
                ft.Row(
                    controls=[save_button, back_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                padding=ft.Padding(20, 10, 10, 10),
            ),
        ],
    )
