mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

app:
	python manage.py startapp apps

dj:
	python manage.py runserver


db:
	python manage.py shell


google:
	pip install django-allauth


admin:
	python manage.py createsuperuser
