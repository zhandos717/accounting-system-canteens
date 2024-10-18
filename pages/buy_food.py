import flet as ft
import requests

from services.capture_photo import capture_photo
from components.product_list import ProductListComponent
from components.search import SearchComponent
from config import load_config
import threading

config = load_config()
API_URL = config.get("api_url", "http://localhost:8000")


def buy_food_page(page: ft.Page):
    # Основные цвета и стили
    primary_color = ft.colors.BLUE_800
    background_color = ft.colors.WHITE
    card_background_color = ft.colors.GREY_100
    button_confirm_color = ft.colors.GREEN_600
    button_cancel_color = ft.colors.RED_600
    button_default_color = ft.colors.GREY_200
    action_button_style = ft.ButtonStyle(color=ft.colors.WHITE)

    # Уведомление об ошибке (Banner)
    error_banner = ft.Banner(
        bgcolor=ft.colors.RED_500,
        leading=ft.Icon(ft.icons.ERROR_OUTLINE, color=ft.colors.WHITE, size=40),
        content=ft.Text("Ошибка", color=ft.colors.WHITE, size=18),
        actions=[
            ft.TextButton(text="Закрыть", style=action_button_style, on_click=lambda e: close_banner()),
        ],
    )

    def add_to_cart(product):
        for item in cart_items:
            if item["name"] == product["name"]:
                item["quantity"] += 1
                break
        else:
            cart_items.append({"name": product["name"], "price": product["price"], "quantity": 1})
        update_cart()

    product_list = ProductListComponent(products=[], on_add_to_cart=add_to_cart)

    # Функция для показа уведомлений с авто-закрытием
    def show_error(message):
        error_banner.content.value = message
        page.banner = error_banner
        page.banner.open = True
        page.update()

        # Запускаем таймер для авто-закрытия баннера через 3 секунды
        threading.Timer(3.0, close_banner).start()

    # Закрытие баннера
    def close_banner():
        page.banner.open = False
        page.update()

    def search_products(query):
        try:
            response = requests.get(f"{API_URL}/products")
            if response.status_code == 200:
                all_products = response.json()
                filtered_products = [p for p in all_products if query.lower() in p['name'].lower()]
                product_list.controls = ProductListComponent(filtered_products, add_to_cart).controls
                page.update()
            else:
                show_error(f"Ошибка загрузки продуктов: {response.status_code}")
        except Exception as e:
            show_error(f"Ошибка подключения: {str(e)}")

    # Поле поиска продуктов
    search_input = SearchComponent(on_search=search_products)

    # Список продуктов
    products_list = ft.ListView(expand=True, spacing=10, padding=ft.Padding(10, 10, 10, 10))
    all_products = []  # Список для хранения всех продуктов

    # Корзина
    cart_items = []
    cart_total = ft.Text("Итого: 0 тенге", size=24, color=primary_color, weight=ft.FontWeight.BOLD)

    # Ввод ID сотрудника (сканирование)
    employee_id_input = ft.TextField(
        label="Сканируйте QR-код сотрудника",
        prefix_icon=ft.icons.QR_CODE_SCANNER,
        width=600,
        height=60,
        text_size=20,
        filled=True,

        border_radius=ft.border_radius.all(12),
    )

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
                    margin=ft.Margin(5, 5, 5, 5),
                )
            )
        page.update()

    # Добавление продукта в корзину с увеличением количества, если уже добавлен
    def add_to_cart(product):
        for item in cart_items:
            if item["name"] == product["name"]:
                item["quantity"] += 1
                break
        else:
            cart_items.append({"name": product["name"], "price": product["price"], "quantity": 1})
        update_cart()

    # Удаление продукта из корзины
    def remove_from_cart(index):
        del cart_items[index]
        update_cart()

    # Отображение продуктов в списке
    def display_products(products):
        products_list.controls.clear()
        for product in products:
            product_button = ft.ElevatedButton(
                content=ft.Text(f"{product['name']} - {product['price']} тенге", size=20),
                on_click=lambda e, p=product: add_to_cart(p),
                bgcolor=button_default_color,
                height=70,
                width=300,
                style=ft.ButtonStyle(
                    bgcolor=button_default_color,
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=ft.Padding(20, 10, 20, 10),
                    color=ft.colors.BLACK,
                )
            )
            products_list.controls.append(product_button)
        page.update()

    # Получение списка продуктов с сервера
    def fetch_products():
        try:
            response = requests.get(f"{API_URL}/products")
            if response.status_code == 200:
                global all_products
                all_products = response.json()
                display_products(all_products)
            else:
                show_error(f"Ошибка загрузки продуктов: {response.status_code}")
            page.update()
        except Exception as e:
            show_error(f"Ошибка подключения: {str(e)}")

    # Логика для покупки продуктов
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

        response = requests.post(f"{API_URL}/buy_food", json={"employee_id": employee_id, "amount": total_amount})
        if response.status_code == 200:
            show_error(f"Покупка на сумму {total_amount} тенге успешна для {employee_id}")
            cart_items.clear()
            update_cart()
        else:
            show_error(f"Ошибка: {response.json()['detail']}")
        page.update()

    # Список товаров в корзине
    cart_items_list = ft.ListView(expand=True, spacing=10, padding=ft.Padding(10, 10, 10, 10))

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
        adaptive=True,  # a CupertinoButton will be rendered when running on apple-platform
        bgcolor=ft.cupertino_colors.ACTIVE_GREEN,
        content=ft.Row(
            [
                ft.Icon(name=ft.icons.SHOPPING_CART, color="white"),
                ft.Text("Подтвердить", color="white"),
            ],
            tight=True,
        ),
        on_click=buy_food
    )

    # Вызываем функцию получения продуктов при открытии страницы
    fetch_products()

    # Разделяем экран на две части
    return ft.View(
        "/buy_food",
        controls=[
            error_banner,  # Баннер для ошибок, отображается сверху
            ft.Row(
                controls=[
                    # Левая часть (поиск и продукты)
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Row(
                                    controls=[back_icon_button,
                                              ft.Text("Покупка продуктов", size=20, weight=ft.FontWeight.BOLD,
                                                      color=primary_color), ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                search_input,  # Поле поиска продуктов
                                products_list,  # Отображение списка продуктов
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                        padding=ft.Padding(20, 10, 10, 10),
                        alignment=ft.alignment.center
                    ),
                    # Правая часть (корзина, ввод ID и кнопки)
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text("Корзина", size=32, weight=ft.FontWeight.BOLD, color=primary_color),
                                cart_items_list,  # Список товаров в корзине
                                cart_total,  # Итого по корзине
                                employee_id_input,  # Ввод ID сотрудника перемещен сюда
                                confirm_button
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        expand=True,
                        padding=ft.Padding(20, 10, 10, 10),
                        alignment=ft.alignment.center
                    ),
                ],
                expand=True,
            ),
        ],
    )
