# components/product_list.py

import flet as ft

class ProductListComponent(ft.UserControl):
    def __init__(self, products, on_add_to_cart):
        super().__init__()
        self.products = products
        self.on_add_to_cart = on_add_to_cart
        self.list_view = ft.ListView(expand=True, spacing=10, padding=ft.Padding(10, 10, 10, 10))

    def update_products(self, products):
        self.products = products  # Сохраняем переданный список продуктов
        self.list_view.controls.clear()
        for product in products:
            product_button = ft.ElevatedButton(
                content=ft.Row(
                    controls=[
                        ft.Text(f"{product['name']}", size=16, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                        ft.Container(expand=True),  # Используем контейнер с expand=True для разделения
                        ft.Text(f"{product['price']} тенге", size=14, color=ft.colors.BLACK),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                on_click=lambda e, p=product: self.on_add_to_cart(p),
                bgcolor=ft.colors.GREY_200,
                height=70,
                width=300,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=ft.Padding(20, 10, 20, 10),
                ),
            )
            self.list_view.controls.append(product_button)
        # Теперь здесь мы не вызываем self.update()

    def build(self):
        # Обновляем список продуктов после того, как компонент был добавлен на страницу
        self.update_products(self.products)
        return self.list_view
