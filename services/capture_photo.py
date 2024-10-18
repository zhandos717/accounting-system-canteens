import os
import datetime
import cv2


def capture_photo(employee_id):
    # Открываем камеру (0 — это индекс первой камеры)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        return False

    # Захват кадра с камеры
    ret, frame = cap.read()

    if ret:
        # Форматируем текущую дату и время
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')

        # Определяем директорию для фотографий сотрудника по текущей дате
        dir_path = f'./photos/{employee_id}/{current_date}/'

        # Создаем директорию, если она не существует
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Имя файла для сохранения изображения
        file_name = datetime.datetime.now().strftime('%H-%M-%S')  # Время сохранения фото
        full_path = os.path.join(dir_path, f'{file_name}.png')

        # Сохраняем изображение на диск
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
