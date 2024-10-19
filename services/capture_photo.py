import os
import datetime
import cv2
import threading
import base64


def capture_photo(employee_id,camera_index=0 ):
    """Функция для захвата фото сотрудника и сохранения в папке по ID и дате."""
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        return False

    ret, frame = cap.read()

    if ret:
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        dir_path = f'./photos/{employee_id}/{current_date}/'

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        file_name = datetime.datetime.now().strftime('%H-%M-%S')
        full_path = os.path.join(dir_path, f'{file_name}.png')

        cv2.imwrite(full_path, frame)
        print(f"Фото сохранено как {full_path}")

        cap.release()
        cv2.destroyAllWindows()
        return True
    else:
        print("Ошибка: не удалось захватить изображение")
        cap.release()
        cv2.destroyAllWindows()
        return False


def capture_stream(photo_control, page, camera_index=0, stop_event=None):
    """Функция для захвата видеопотока с камеры и отображения в реальном времени."""

    def start_camera():
        cap = cv2.VideoCapture(camera_index)

        if not cap.isOpened():
            print("Ошибка: не удалось открыть камеру")
            return

        while not stop_event.is_set():  # Проверяем флаг для остановки
            ret, frame = cap.read()
            if not ret:
                break

            # Конвертируем кадр в формат JPEG и кодируем в base64
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer.tobytes()).decode('utf-8')

            # Устанавливаем полученное изображение в компонент Flet
            photo_control.src_base64 = jpg_as_text
            page.update()

        cap.release()
        cv2.destroyAllWindows()

    # Создаем поток для захвата кадров
    threading.Thread(target=start_camera, daemon=True).start()
