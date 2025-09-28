web: python manage.py migrate && python manage.py collectstatic --no-input && gunicorn taskmanager.wsgi --log-file -
web: gunicorn taskmanager.wsgi
