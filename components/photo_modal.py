# components/photo_modal.py
import os

import flet as ft
import threading
import cv2
import base64

from django.utils.datetime_safe import datetime


class PhotoModalComponent(ft.AlertDialog):
    def __init__(self, folder, image_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stop_event = threading.Event()  # Событие для остановки потока
        self.photo_control = ft.Image(src="../photos/none.jpg", width=300, height=300)  # Контрол для отображения потока
        self.folder = folder
        self.image_name = image_name

        # Установка содержимого модального окна
        self.content = ft.Column(
            controls=[
                ft.Text("Сделай фотографию для подтверждения покупки."),
                self.photo_control,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Создание кнопок для модального окна
        self.actions = [
            ft.ElevatedButton("Отмена", on_click=self.close_modal),
            ft.ElevatedButton("Подтвердить", on_click=self.confirm_action),
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

        # Установка модального состояния
        self.modal = True

    def start_camera_stream(self):
        """Запускаем поток для захвата и отображения видеопотока с камеры."""
        self.stop_event.clear()
        threading.Thread(target=self.capture_stream, daemon=True).start()

    def capture_stream(self):
        """Захват кадров с камеры и отображение их в окне."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Ошибка: не удалось открыть камеру")
            return

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                break

            # Конвертируем кадр в JPEG и кодируем в base64
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer.tobytes()).decode('utf-8')

            # Обновляем изображение в контроле
            self.photo_control.src_base64 = jpg_as_text
            if hasattr(self, "page") and self.page:
                self.page.update()

        cap.release()
        cv2.destroyAllWindows()

    def capture_and_display_photo(self):
        """Функция для захвата и сохранения фото."""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Ошибка: не удалось открыть камеру")
            return

        ret, frame = cap.read()
        if ret:
            # Здесь можно добавить сохранение фото или иное действие с кадром
            photo_path = self.save_photo(frame)
            self.photo_control.src = photo_path
            self.page.update()

        cap.release()
        cv2.destroyAllWindows()

    def save_photo(self, frame):
        """Сохранение захваченного кадра в файл и возвращение пути к файлу."""

        os.makedirs(self.folder, exist_ok=True)

        photo_path = f"{self.folder}/{self.image_name}"
        cv2.imwrite(photo_path, frame)
        return photo_path

    def confirm_action(self, e=None):
        self.capture_and_display_photo()
        self.close_modal(e)

    def close_modal(self, e=None):
        """Закрытие модального окна и остановка потока камеры."""
        self.stop_event.set()  # Остановка видеопотока
        self.open = False
        if hasattr(self, "page") and self.page:
            self.page.close(self)
            self.page.update()
