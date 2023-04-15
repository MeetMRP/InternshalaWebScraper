from django.urls import path
from . import views

urlpatterns = [
    path('', views.ScrapperApi, name='ScrapperApi'),
]