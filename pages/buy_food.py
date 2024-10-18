import flet as ft
import requests
from config import load_config

config = load_config()
API_URL = config.get("api_url", "http://localhost:8000")

def buy_food_page(page: ft.Page):
    primary_color = ft.colors.BLUE_800
    background_color = ft.colors.GREY_100

    employee_id_input = ft.TextField(
        label="Сканируйте QR-код для покупки еды",
        prefix_icon=ft.icons.QR_CODE_SCANNER,
        width=500,
        height=60,
        text_size=20,
        filled=True,
        bgcolor=background_color,
        border_radius=ft.border_radius.all(8),
    )

    def buy_food(e):
        employee_id = employee_id_input.value
        amount = 1000  # Пример суммы покупки
        if employee_id:
            response = requests.post(f"{API_URL}/buy_food", json={"employee_id": employee_id, "amount": amount})
            if response.status_code == 200:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Покупка успешна для {employee_id}"))
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {response.json()['detail']}"))
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("Пожалуйста, введите ID сотрудника"))
        page.snack_bar.open = True
        page.update()

    back_button = ft.ElevatedButton("Назад", on_click=lambda e: page.go("/"))

    return ft.View(
        "/buy_food",
        controls=[
            ft.Container(ft.Text("Покупка еды", size=32, weight=ft.FontWeight.BOLD, color=primary_color), padding=ft.Padding(20, 10, 10, 10)),
            ft.Container(employee_id_input, alignment=ft.alignment.center, padding=ft.Padding(20, 10, 10, 10)),
            ft.ElevatedButton("Подтвердить покупку", on_click=buy_food),
            back_button,
        ],
    )
