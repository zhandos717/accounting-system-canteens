import flet as ft

def ProductListComponent(products, on_add_to_cart):
    product_list = ft.ListView(expand=True, spacing=10, padding=ft.Padding(10, 10, 10, 10))

    for product in products:
        product_button = ft.ElevatedButton(
            content=ft.Text(f"{product['name']} - {product['price']} тенге", size=20),
            on_click=lambda e, p=product: on_add_to_cart(p),
            bgcolor=ft.colors.GREY_200,
            height=70,
            width=300,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREY_200,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding(20, 10, 20, 10),
                color=ft.colors.BLACK,
            )
        )
        product_list.controls.append(product_button)

    return product_list
