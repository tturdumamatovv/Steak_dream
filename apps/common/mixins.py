import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile


class ImageProcessingMixin:
    """
    Миксин для обработки изображений, преобразующий их в формат .webp и изменяющий размер.
    """

    def process_and_save_image(self, image_field, max_width=800, max_height=800, format='WEBP', quality=85):
        """ Обрабатывает и сохраняет изображение в заданном поле модели. """
        if not hasattr(self, image_field):
            raise ValueError(f"Модель не содержит поле {image_field}")

        image_file = getattr(self, image_field)
        if not image_file or image_file.name.endswith('.webp'):
            return

        # Путь к текущему файлу перед изменением
        old_path = image_file.path if image_file.name else None

        # Обработка изображения
        image = Image.open(image_file)
        original_width, original_height = image.size
        ratio = min(max_width / original_width, max_height / original_height)
        new_width = int(original_width * ratio)
        new_height = int(original_height * ratio)
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)

        image_io = BytesIO()
        resized_image.save(image_io, format=format, quality=quality)
        new_name = f"{image_file.name.rsplit('.', 1)[0]}.webp"

        image_file.save(new_name, ContentFile(image_io.getvalue()), save=False)

        # Удаление старого файла, если путь существует и файл был обновлён
        if old_path and old_path != image_file.path:
            if os.path.isfile(old_path):
                os.remove(old_path)



