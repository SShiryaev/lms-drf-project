# lms-drf-project

## Основные зависимости:
- python = "^3.12"
- Django = "^5.0.6"
- psycopg2-binary = "^2.9.9"
- pillow = "^10.3.0"
- djangorestframework = "^3.15.1"
- python-dotenv = "^1.0.1"
- django-filter = "^24.2"
- djangorestframework-simplejwt = "^5.3.1"
- drf-yasg = "^1.21.7"
- stripe = "^9.12.0"
- celery = "^5.4.0"
- django-celery-beat = "^2.6.0"
- redis = "^5.0.6"
<li>Полный список зависимостей находится в requirements.txt</li>

## Для запуска проекта:
- установить зависимости из requirements.txt
- убрать .sample из .env.sample
- в .env добавить соответствующие значения
- в терминале запустить проект:
```text
python manage.py runserver
```

## Для запуска отложенных и периодических задач:
- запустить redis:
```text
redis-server
```
- запустить отложенную задачу на отправку уведомлений об обновлениях курса/урока:
```text
celery -A config worker -l INFO  # Для Unix систем
celery -A config worker -l INFO -P eventlet  # Для Windows
```
- запустить фоновую задачу на деактивацию пользователей по времени
```text
celery -A config beat -l info
```