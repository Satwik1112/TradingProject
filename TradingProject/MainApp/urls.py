from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name=''),
    path('upload_file', views.upload_file, name='upload_file')
]