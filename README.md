Mostly follows https://docs.djangoproject.com/en/2.2/intro/tutorial01/

django-admin startproject admin
mv admin research-paper-database
python3 manage.py startapp papers

Make modifications admin/settings.py, admin/urls.py

Make modifications to papers/ (admin.py, apps.py, urls.py, views.py, models.py), and add templates/

python3 manage.py makemigrations papers
python3 manage.py migrate

python3 manage.py createsuperuser

python3 manage.py runserver



rm -rf papers/migrations/ db.sqlite3



https://medium.com/@srijan.pydev_21998/complete-guide-to-deploy-django-applications-on-aws-ubuntu-16-04-instance-with-uwsgi-and-nginx-b9929da7b716
