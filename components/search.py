import flet as ft


def SearchComponent(on_search, width=600, height=60):
    """Компонент для поиска с заданными размерами и placeholder текстом"""
    return ft.TextField(
        label="Поиск продуктов",

        prefix_icon=ft.icons.SEARCH,
        width=width,
        height=height,
        on_change=lambda e: on_search(e.control.value),
        border_radius=ft.border_radius.all(12),
        text_size=20,
        filled=True  # Чтобы добавить фоновый цвет к текстовому полю
    )
