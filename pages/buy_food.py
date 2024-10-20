# buy_food_page.py
import os
from datetime import datetime

import cv2
import flet as ft
from components.banner import BannerComponent
from components.employee_field import EmployeeField
from components.search import SearchComponent
from components.photo_modal import PhotoModalComponent  # Import the photo modal

from services.camera_manager import CameraManager
from services.http_client import HttpClient

client = HttpClient()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR)

from config import load_config


def buy_food_page(page: ft.Page):
    # Основные цвета и стили
    primary_color = ft.colors.BLUE_800
    background_color = ft.colors.WHITE
    card_background_color = ft.colors.GREY_200
    # Уведомление об ошибке (Banner)
    show_error, show_success = BannerComponent(page)
    config = load_config()

    # Корзина
    cart_items = []
    cart_total = ft.Text("Итого: 0 тенге", size=24, color=primary_color, weight=ft.FontWeight.BOLD)

    products_list = ft.ListView(expand=True, spacing=10, padding=ft.Padding(10, 10, 10, 10))

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
                            ft.Container(expand=True),
                            ft.Text(f"{item['price'] * item['quantity']} тенге", size=14, color=ft.colors.BLACK),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.colors.RED_500,
                                icon_size=20,
                                tooltip="Удалить",
                                on_click=lambda e, index=idx: remove_from_cart(index)
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

    def display_products(products):
        products_list.controls.clear()
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
                on_click=lambda e, p=product: add_to_cart(p),
                bgcolor=ft.colors.WHITE,
                height=70,
                width=300,
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=12),
                    padding=ft.Padding(20, 10, 20, 10),
                    color=ft.colors.BLACK,
                )
            )
            products_list.controls.append(product_button)
        page.update()

    # Поле поиска продуктов
    def search_products(query):
        try:
            products = client.get("/products")
            if products:
                filtered_products = [p for p in products if query.lower() in p['name'].lower()]
                display_products(filtered_products)
            else:
                show_error("Ошибка загрузки продуктов.")
        except Exception as e:
            show_error(f"Ошибка подключения: {str(e)}")

    search_input = SearchComponent(on_search=search_products)

    # Список товаров в корзине
    cart_items_list = ft.ListView(expand=True, spacing=10, padding=ft.Padding(10, 10, 10, 10))

    # Ввод ID сотрудника (сканирование)
    employee_id_input = EmployeeField()

    def confirm_purchase(e):
        total_amount = sum([item["price"] * item["quantity"] for item in cart_items])
        if total_amount == 0:
            show_error("Корзина пуста")
            return

        employee_id = employee_id_input.value
        if not employee_id:
            show_error("Пожалуйста, введите ID сотрудника")
            return

        # Define paths and capture photo
        path = f"{STATIC_ROOT}/photos/employees/{employee_id}"
        now = datetime.now()
        img_name = now.strftime("%d.%m.%Y-%H:%M:%S")
        photo_filename = f"{img_name}.png"
        camera_index = int(config.get('camera_index'))
        try:
            with CameraManager(camera_index=camera_index) as camera:
                photo_path = camera.capture_and_save_photo(path, photo_filename)

                if not photo_path:
                    show_error("Ошибка: Не удалось сохранить фото")
                    return
        except Exception as ex:
            show_error(f"Ошибка захвата фото: {str(ex)}")
            return

        # Open the photo file in binary mode
        try:
            # Send the POST request with the file
            response = client.post(
                '/buy_food',
                json={"employee_id": employee_id, "items": cart_items},
                files={'file': open(photo_path, 'rb')}
            )
        except Exception as ex:
            show_error(f"Ошибка отправки фото: {str(ex)}")
            return

        # Check the server response
        if response is None:
            show_error(f"Ошибка соединения с сервером")
        elif response.status_code == 200:
            show_success(f"Покупка прошла успешна")
            cart_items.clear()
            employee_id_input.value = ''
            update_cart()
        else:
            show_error(f"Ошибка: {response.json().get('message', 'Неизвестная ошибка')}")

        page.update()

    # Функция для открытия диалога подтверждения
    # buy_food_page.py
    def open_confirm_dialog(e):
        try:
            path = f"./photos/employees/test"
            now = datetime.now()
            img_name = now.strftime("%d.%m.%Y-%H:%M:%S")
            photo_path = f"/{img_name}.png"
            camera_index = int(config.get('camera_index'))

            # Создаем экземпляр PhotoModalComponent
            photo_modal = PhotoModalComponent(folder=path, image_name=photo_path,
                                              camera_index=camera_index)

            page.open(photo_modal)
            # Запускаем стрим камеры
            photo_modal.start_camera_stream()

        except Exception as ex:
            show_error(f"Ошибка при открытии модального окна: {str(ex)}")

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
        on_click=confirm_purchase
    )

    photo_button = ft.IconButton(
        icon=ft.icons.PHOTO_CAMERA,
        icon_size=30,
        tooltip="Настройки камеры",
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            padding=ft.Padding(20, 10, 20, 10),
            bgcolor=ft.cupertino_colors.ACTIVE_BLUE,
        ),
        on_click=open_confirm_dialog
    )

    # Вызываем функцию получения продуктов при открытии страницы
    def fetch_products():
        search_products("")

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
                                products_list,  # Отображение списка продуктов
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
                                ft.Row(
                                    controls=[
                                        confirm_button,
                                        photo_button
                                    ],
                                    spacing=20,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),

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
