from django.urls import path

from . import views

app_name = 'papers'
urlpatterns = [
    # ex: /papers/
    path('', views.index, name='index'),
    # ex: /papers/5/
    path('<int:paper_id>/', views.paperInfo, name='paperInfo'),
    # ex: /papers/bibtex/
    path('bibtex/', views.downloadBibtex, name='downloadBibtex'),
]
