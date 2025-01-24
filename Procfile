web: DJANGO_SETTINGS_MODULE=chat_project.settings daphne chat_project.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: DJANGO_SETTINGS_MODULE=chat_project.settings python manage.py runworker channels --settings=chat_project.settings -v2
