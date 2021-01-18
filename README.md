Сервис, на основе фреймворка Django, который позволяет загружать изображения с компьютера пользователя, или по ссылке, а затем изменять их размер.

### Установка зависимостей

Создать виртуальное окружение

    python3 -m venv venv
    source venv/bin/activate

Установить зависимости

    pip install -r requirements.txt

или использовать pipenv

    pipenv install --ignore-pipfile

### Запуск

    python manage.py migrate
    python manage.py runserver
