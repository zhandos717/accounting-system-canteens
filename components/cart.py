import flet as ft

def CartComponent(cart_items, on_remove_from_cart, cart_total):
    cart_items_list = ft.ListView(expand=True, spacing=10, padding=ft.Padding(10, 10, 10, 10))

    for idx, item in enumerate(cart_items):
        cart_items_list.controls.append(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"{item['name']} (x{item['quantity']})", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                        ft.Container(expand=True),
                        ft.Text(f"{item['price'] * item['quantity']} тенге", size=14, color=ft.colors.BLACK),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_size=20,
                            tooltip="Удалить",
                            on_click=lambda e, index=idx: on_remove_from_cart(index)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=ft.Padding(10, 10, 10, 10),
                bgcolor=ft.colors.GREY_100,
                border_radius=ft.border_radius.all(10),
                margin=ft.Margin(5, 5, 5, 5),
            )
        )

    return ft.Column(
        controls=[cart_items_list, cart_total],
        spacing=20
    )
