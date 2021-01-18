from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('image/upload/', views.upload, name='upload'),
    path('image/<int:pk>/', views.detail, name='detail'),
]
