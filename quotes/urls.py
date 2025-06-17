from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('builder/', views.builder, name='builder'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_item, name='delete_item'),
    path('clear-all/', views.clear_all, name='clear_all'),
    path('api/get-totals/', views.get_totals, name='get_totals'),
]

