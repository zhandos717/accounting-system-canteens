import flet as ft


def EmployeeField(width=600, height=60):
    return ft.TextField(
        label="Сканируйте QR-код сотрудника",
        prefix_icon=ft.icons.QR_CODE_SCANNER,
        text_size=20,
        width=width,
        height=height,
        border_radius=ft.border_radius.all(12),
    )
