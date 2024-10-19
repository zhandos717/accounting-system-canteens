import datetime
import flet as ft
from components.banner import BannerComponent
from components.product_list import ProductListComponent
from components.search import SearchComponent
from services.http_client import HttpClient
from services.capture_photo import capture_photo

client = HttpClient()


def buy_food_page(page: ft.Page):
    # Основные цвета и стили
    primary_color = ft.colors.BLUE_800
    background_color = ft.colors.WHITE
    card_background_color = ft.colors.GREY_200
    button_default_color = ft.colors.GREY_200

    # Уведомление об ошибке (Banner)
    show_error = BannerComponent(page)

    # Корзина
    cart_items = []
    cart_total = ft.Text("Итого: 0 тенге", size=24, color=primary_color, weight=ft.FontWeight.BOLD)

    # Обновление отображения корзины
    def update_cart():
        total = sum([item["price"] * item["quantity"] for item in cart_items])
        cart_total.value = f"Итого: {total} тенге"
        cart_items_list.controls.clear()

        # Отображение продуктов в корзине с кнопкой удаления
        for idx, item in enumerate(cart_items):
            cart_items_list.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(f"{item['name']} (x{item['quantity']})", size=16, weight=ft.FontWeight.BOLD,
                                    color=ft.colors.BLACK),
                            ft.Container(expand=True),  # Используем контейнер с expand=True для разделения
                            ft.Text(f"{item['price'] * item['quantity']} тенге", size=14, color=ft.colors.BLACK),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_size=20,
                                tooltip="Удалить",
                                on_click=lambda e, index=idx: remove_from_cart(index)  # Функция удаления
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=ft.Padding(10, 10, 10, 10),
                    bgcolor=card_background_color,
                    border_radius=ft.border_radius.all(10),
                )
            )
        page.update()

    # Функция для удаления продукта из корзины
    def remove_from_cart(index):
        del cart_items[index]
        update_cart()

    # Функция для добавления продукта в корзину
    def add_to_cart(product):
        for item in cart_items:
            if item["name"] == product["name"]:
                item["quantity"] += 1
                break
        else:
            cart_items.append({"name": product["name"], "price": product["price"], "quantity": 1})
        update_cart()

    # Создание компонента ProductListComponent и передача функции add_to_cart
    product_list = ProductListComponent(products=[], on_add_to_cart=add_to_cart)

    # Поле поиска продуктов
    def search_products(query):
        try:
            products = client.get("/products")
            if products:
                filtered_products = [p for p in products if query.lower() in p['name'].lower()]
                product_list.update(filtered_products)
            else:
                show_error("Ошибка загрузки продуктов.")
        except Exception as e:
            show_error(f"Ошибка подключения: {str(e)}")

    search_input = SearchComponent(on_search=search_products)

    # Список товаров в корзине
    cart_items_list = ft.ListView(expand=True, spacing=10, padding=ft.Padding(10, 10, 10, 10))

    # Ввод ID сотрудника (сканирование)
    employee_id_input = ft.TextField(
        label="Сканируйте QR-код сотрудника",
        prefix_icon=ft.icons.QR_CODE_SCANNER,
        text_size=20,
        border_radius=ft.border_radius.all(12),
    )

    # Функция для подтверждения покупки
    def buy_food(e):
        employee_id = employee_id_input.value
        photo_success = capture_photo(employee_id)
        if not employee_id:
            show_error("Пожалуйста, введите ID сотрудника")
            return

        total_amount = sum([item["price"] * item["quantity"] for item in cart_items])
        if total_amount == 0:
            show_error("Корзина пуста")
            return

        response = client.post('/buy_food', json={"employee_id": employee_id, "amount": total_amount})
        if response.status_code == 200:
            show_error(f"Покупка на сумму {total_amount} тенге успешна для {employee_id}")
            cart_items.clear()
            update_cart()
        else:
            show_error(f"Ошибка: {response.json()['detail']}")
        page.update()

    # Функция для захвата и отображения изображения с камеры
    def capture_and_display_photo(employee_id, page, image_control):
        photo_success = capture_photo(employee_id)
        if photo_success:
            current_date = datetime.datetime.now().strftime('%Y-%m-%d')
            image_control.src = f"./photos/{employee_id}/{current_date}/{datetime.datetime.now().strftime('%H-%M-%S')}.png"
            page.update()

    # Функция для открытия диалога подтверждения
    def open_confirm_dialog(e):
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    # Функция для закрытия диалога подтверждения
    def close_confirm_dialog(e=None):
        confirm_dialog.open = False
        page.update()

    # Создание диалога подтверждения
    photo_control = ft.Image(src="", width=300, height=300)
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Подтверждение покупки с фото", size=24),
        content=ft.Column(
            controls=[
                ft.Text("Пожалуйста, сделайте фото для подтверждения покупки."),
                photo_control,
                ft.ElevatedButton(
                    text="Сделать фото",
                    on_click=lambda e: capture_and_display_photo("employee123", page, photo_control),
                    bgcolor=ft.colors.BLUE_600,
                    color=ft.colors.WHITE,
                )
            ],
        ),
        actions=[
            ft.TextButton("Отмена", on_click=close_confirm_dialog),
            ft.ElevatedButton("Подтвердить", on_click=lambda e: confirm_purchase(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Функция для подтверждения покупки
    def confirm_purchase(e):
        buy_food(e)
        close_confirm_dialog()
        show_error("Покупка успешно подтверждена!")

    # Кнопка для возврата на главную страницу
    back_icon_button = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        icon_size=30,
        tooltip="Назад",
        on_click=lambda e: page.go("/"),
        style=ft.ButtonStyle(
            color=ft.colors.BLUE_800,
            padding=ft.Padding(20, 10, 20, 10),
        )
    )

    # Кнопка для подтверждения покупки
    confirm_button = ft.ElevatedButton(
        adaptive=True,
        bgcolor=ft.cupertino_colors.ACTIVE_GREEN,
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.SHOPPING_CART, color=background_color),
                ft.Text("Подтвердить", color=background_color),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        ),
        on_click=open_confirm_dialog
    )

    # Вызываем функцию получения продуктов при открытии страницы
    def fetch_products():
        try:
            products = client.get("/products")

            if products:
                product_list.update_products(products)
            else:
                show_error("Ошибка загрузки продуктов.")
            page.update()
        except Exception as e:
            show_error(f"Ошибка подключения: {str(e)}")

    fetch_products()

    # Разделяем экран на две части
    return ft.View(
        "/buy_food",
        controls=[
            # Баннер для ошибок
            ft.Row(
                controls=[
                    # Левая часть (поиск и продукты)
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[back_icon_button,
                                              ft.Text("Покупка продуктов", size=20, weight=ft.FontWeight.BOLD,
                                                      color=primary_color)],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                search_input,
                                product_list,  # Отображение списка продуктов
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                        padding=ft.Padding(20, 10, 10, 10),
                    ),
                    # Правая часть (корзина, ввод ID и кнопки)
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Корзина", size=32, weight=ft.FontWeight.BOLD, color=primary_color),
                                cart_items_list,
                                cart_total,
                                employee_id_input,
                                confirm_button
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                        padding=ft.Padding(20, 10, 10, 10),
                    ),
                ],
                expand=True,
            ),
        ],
    )
