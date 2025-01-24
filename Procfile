web: daphne chat_project.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=chat_project.settings -v2
