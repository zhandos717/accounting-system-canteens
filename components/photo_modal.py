# components/photo_modal.py
import base64
import flet as ft
import threading
import cv2
import os

class PhotoModalComponent(ft.AlertDialog):
    def __init__(self, employee_id, on_confirm, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_id = employee_id
        self.on_confirm = on_confirm
        self.stop_event = threading.Event()  # Initialize stop_event

        # Create an image control to show the camera stream
        self.photo_control = ft.Image(src="", width=300, height=300)

        # Set up the modal content and actions
        self.setup_modal_content()

        self.modal = True

    def setup_modal_content(self):
        """Set up the main content and actions of the modal."""
        self.content = ft.Column(
            controls=[
                ft.Text("Пожалуйста, сделайте фото для подтверждения покупки."),
                self.photo_control,
                ft.ElevatedButton(
                    text="Сделать фото",
                    on_click=self.capture_and_display_photo,
                    bgcolor=ft.colors.BLUE_600,
                    color=ft.colors.WHITE,
                )
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.actions = [
            ft.ElevatedButton("Отмена", on_click=self.close_modal),
            ft.ElevatedButton("Подтвердить", on_click=self.confirm_purchase),
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def start_camera_stream(self):
        """Start a thread to capture and display the camera stream."""
        self.stop_event.clear()
        threading.Thread(target=self.capture_stream, daemon=True).start()

    def capture_stream(self):
        """Continuously capture frames from the camera and display them as a stream."""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return  # Do not proceed if the camera can't be opened

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                continue

            # Convert frame to JPEG and encode to base64
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer.tobytes()).decode('utf-8')

            # Set the base64 string with the proper prefix
            self.photo_control.src_base64 = jpg_as_text
            self.update()

        cap.release()

    def capture_and_display_photo(self, e=None):
        """Capture a single photo and display it in the modal."""
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return

        ret, frame = cap.read()
        if ret:
            photo_path = self.save_photo(frame)
            self.photo_control.src = photo_path
            self.update()

        cap.release()

    def save_photo(self, frame):
        """Save a captured frame to a file and return the file path."""
        temp_folder = "./temp"
        os.makedirs(temp_folder, exist_ok=True)

        photo_path = f"{temp_folder}/{self.employee_id}_capture.png"
        cv2.imwrite(photo_path, frame)
        return photo_path

    def confirm_purchase(self, e=None):
        """Handle the confirmation of the purchase."""
        self.on_confirm(e)
        self.close_modal()

    def close_modal(self, e=None):
        """Close the modal and stop the camera stream."""
        self.stop_event.set()
        self.open = False
        self.update()
