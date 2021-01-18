from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import urlparse
from io import BytesIO

from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


def resize(image, width, height):
    """Возвращает изображение с измененным размером"""
    with Image.open(image.open()) as image_data:
        img_format = image_data.format
        resized_image = image_data.resize((width, height))
        output = BytesIO()
        resized_image.save(output, img_format)
        output.seek(0)

    return output


def get_image_from_url(url):
    """Загружает и проверяет изображение."""
    try:
        response = urlopen(url)
    except URLError:
        raise ValidationError('Ошибка загрузки изображения.')

    if not response.getheader('content-type').startswith('image'):
        raise ValidationError('Ссылка не указывает на изображение.')

    try:
        img = Image.open(BytesIO(response.read()))
    except UnidentifiedImageError:
        raise ValidationError('Изображение повреждено.')

    img_name = urlparse(url).path.split('/')[-1]
    img_format = img.format

    output = BytesIO()
    img.save(output, img_format)
    output.seek(0)

    return output, img_name
