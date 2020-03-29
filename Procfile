web: ( cd src && gunicorn --workers 2 project.wsgi:application --bind 0.0.0.0:$PORT )
release: python src/manage.py migrate