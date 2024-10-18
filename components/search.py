import flet as ft

def SearchComponent(on_search):
    return ft.TextField(
        label="Поиск продуктов",
        prefix_icon=ft.icons.SEARCH,
        on_change=lambda e: on_search(e.control.value),
        border_radius=ft.border_radius.all(12),
        text_size=20
    )
