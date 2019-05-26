This directory is a Django project mostly based on the [Django sample project](https://docs.djangoproject.com/en/2.2/intro/tutorial01/) (v2.2 at the time of writing).

Make sure you have installed `python3` with `django`.

A rough outline:

```
django-admin startproject admin
mv admin paperserver
cv paperserver
python3 manage.py startapp papers

# Make modifications admin/settings.py, admin/urls.py

# Make modifications to papers/ (admin.py, apps.py, urls.py, views.py, models.py), and add templates/

python3 manage.py makemigrations papers
python3 manage.py migrate

python3 manage.py createsuperuser

python3 manage.py runserver
```
