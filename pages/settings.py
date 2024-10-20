import flet as ft
from config import load_config, save_config
from services.http_client import HttpClient  # Импортируем клиента для обновления

# Инициализируем глобальный клиент
client = HttpClient()


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

    # Поле для ввода API Token
    api_url_token = ft.TextField(
        label="API token",
        value=config.get("api_token", ""),
        width=500,
        text_size=18,
        filled=True,
        border_radius=ft.border_radius.all(8),
    )

    camera_index = ft.TextField(
        label="Введите индекс камеры",
        value=config.get("camera_index", ""),
        width=500,
        text_size=18,
        filled=True,
        border_radius=ft.border_radius.all(8),
    )

    # Логика для сохранения настроек
    def save_settings(e):
        new_api_url = api_url_input.value
        new_api_token = api_url_token.value
        if new_api_url:
            # Сохраняем новые настройки
            save_config({"api_url": new_api_url, "api_token": new_api_token, "camera_index": camera_index.value})

            # Перезагружаем конфигурацию и обновляем глобальный клиент
            client.update_config()

            # Показываем уведомление об успешном сохранении
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Настройки сохранены и обновлены!"))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(content=ft.Text("URL API не может быть пустым!"))
            page.snack_bar.open = True
            page.update()

    # Кнопка для сохранения настроек
    save_button = ft.ElevatedButton(
        adaptive=True,
        content=ft.Text("Сохранить настройки", size=20),
        bgcolor=ft.colors.GREEN_500,
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.GREEN_500,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(20, 10, 20, 10),
        ),
        on_click=save_settings
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
        "/settings",
        controls=[
            ft.Container(
                content=ft.Text("Настройки приложения", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_800),
                alignment=ft.alignment.center,
                padding=ft.Padding(20, 10, 10, 10),
            ),
            ft.Container(api_url_input, alignment=ft.alignment.center, padding=ft.Padding(20, 10, 10, 10)),
            ft.Container(api_url_token, alignment=ft.alignment.center, padding=ft.Padding(20, 10, 10, 10)),
            ft.Container(camera_index, alignment=ft.alignment.center, padding=ft.Padding(20, 10, 10, 10)),
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
