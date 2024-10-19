import flet as ft
import threading

def BannerComponent(page):
    error_banner = ft.Banner(
        bgcolor=ft.colors.RED_500,
        leading=ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE, size=40),
        content=ft.Text("Ошибка", color=ft.colors.WHITE, size=18),
        actions=[
            ft.TextButton(text="Закрыть", style=ft.ButtonStyle(color=ft.colors.WHITE), on_click=lambda e: close_banner(page)),
        ],
    )

    def show_error(message):
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

    return show_error
