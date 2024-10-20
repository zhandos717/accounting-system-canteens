# services/camera_manager.py
import os

import cv2

class CameraManager:
    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.cap = None

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise RuntimeError("Ошибка: не удалось открыть камеру")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def capture_frame(self):
        """Захватить один кадр с камеры."""
        if not self.cap.isOpened():
            raise RuntimeError("Ошибка: камера не открыта")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Ошибка: не удалось захватить изображение")
        return frame

    def capture_and_save_photo(self, directory, filename):
        """Захватить фото и сохранить его в указанную директорию."""
        frame = self.capture_frame()
        if frame is None:
            return None

        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Save the captured frame to the specified path
        success = cv2.imwrite(file_path, frame)
        if not success:
            raise RuntimeError("Ошибка: не удалось сохранить фото")
        return file_path
