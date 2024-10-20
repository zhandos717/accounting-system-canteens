import flet as ft
import threading


def BannerComponent(page):
    def show_success(message):
        banner = ft.Banner(
            bgcolor=ft.colors.GREEN_500,
            content=ft.Text('Успех', color=ft.colors.WHITE, size=18),
            actions=[
                ft.TextButton(text="Закрыть", style=ft.ButtonStyle(color=ft.colors.WHITE),
                              on_click=lambda e: close_banner(page)),
            ]
        )

        banner.content.value = message
        page.banner = banner
        page.banner.open = True
        page.update()

        # Закрытие баннера через 3 секунды
        threading.Timer(3.0, lambda: close_banner(page)).start()

    def show_error(message):
        error_banner = ft.Banner(
            bgcolor=ft.colors.RED_500,
            content=ft.Text("Ошибка", color=ft.colors.WHITE, size=18),
            actions=[
                ft.TextButton(text="Закрыть", style=ft.ButtonStyle(color=ft.colors.WHITE),
                              on_click=lambda e: close_banner(page)),
            ],
            leading=ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE, size=40),
        )

        error_banner.content.value = message
        print(message)

        page.banner = error_banner
        page.banner.open = True
        page.update()

        # Закрытие баннера через 3 секунды
        threading.Timer(3.0, lambda: close_banner(page)).start()

    def close_banner(page):
        page.banner.open = False
        page.update()

    return show_error, show_success
