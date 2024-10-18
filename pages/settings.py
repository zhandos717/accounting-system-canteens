import flet as ft
from config import load_config, save_config


def settings_page(page: ft.Page):
    # Загрузка текущих настроек
    config = load_config()

    # Поле для ввода API URL
    api_url_input = ft.TextField(
        label="API URL",
        value=config.get("api_url", ""),
        width=500,
        text_size=18,
        filled=True,
        border_radius=ft.border_radius.all(8),
    )

    # Логика для сохранения настроек
    def save_settings(e):
        new_api_url = api_url_input.value
        if new_api_url:
            save_config({"api_url": new_api_url})
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Настройки сохранены!"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("URL API не может быть пустым!"))
            page.snack_bar.open = True
            page.update()

    # Кнопка для сохранения настроек
    save_button = ft.ElevatedButton(
        content=ft.Text("Сохранить настройки", size=20),
        bgcolor=ft.colors.GREEN_500,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN_500,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 10, 20, 10),
        ),
        on_click=save_settings
    )

    # Кнопка для возврата на главную страницу
    back_button = ft.ElevatedButton(
        content=ft.Text("Назад", size=20),
        bgcolor=ft.colors.BLUE_500,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_500,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 10, 20, 10),
        ),
        on_click=lambda e: page.go("/")
    )

    return ft.View(
        "/settings",
        controls=[
            ft.Container(
                content=ft.Text("Настройки приложения", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                alignment=ft.alignment.center,
                padding=ft.Padding(20, 10, 10, 10),
            ),
            ft.Container(api_url_input, alignment=ft.alignment.center, padding=ft.Padding(20, 10, 10, 10)),
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
