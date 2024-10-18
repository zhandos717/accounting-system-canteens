import flet as ft

def SearchComponent(on_search):
    return ft.TextField(
        label="Поиск продуктов",
        prefix_icon=ft.icons.SEARCH,
        width=600,
        on_change=lambda e: on_search(e.control.value),
        border_radius=ft.border_radius.all(12),
        height=60,
        text_size=20
    )
