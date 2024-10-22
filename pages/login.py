import flet as ft

from config import save_config, load_config
from services.http_client import HttpClient

client = HttpClient()


# Страница логина
def login_page(page: ft.Page):
    # Функция для обработки нажатия кнопки "Войти"
    def login(e):
        username = username_input.value
        password = password_input.value

        response = client.post(endpoint='/login', json={
            "username": username,
            "password": password
        })

        if response is None:
            error_text.value = "Не удалось отправить запрос"
            page.update()
        elif response.status_code == 200:

            config = load_config()

            url = config.get('api_url')
            camera_index = config.get('camera_index')
            token = response.json()['token']

            save_config({"api_url": url, "api_token": token, "camera_index": camera_index})
            client.update_config()

            page.go("/")  # Переход на главную страницу после успешного входа
        else:
            error_text.value = "Неверные имя пользователя или пароль"
            page.update()

    # Поля ввода для имени пользователя и пароля
    username_input = ft.TextField(label="Имя пользователя", width=300)
    password_input = ft.TextField(label="Пароль", password=True, width=300)

    # Текст ошибки
    error_text = ft.Text(value="", color=ft.colors.RED, size=14)

    # Кнопка "Войти"
    login_button = ft.CupertinoButton(text="Войти",
                                      bgcolor=ft.cupertino_colors.PRIMARY,
                                      opacity_on_click=0.3,
                                      on_click=login)

    # Компоновка элементов на странице
    return ft.View(
        "/login",
        controls=[
            ft.Column(
                controls=[
                    ft.Text("Вход в систему", size=24, weight=ft.FontWeight.BOLD),
                    error_text,
                    username_input,
                    password_input,
                    login_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
