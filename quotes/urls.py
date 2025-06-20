from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('builder/', views.builder, name='builder'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_item, name='delete_item'),
    path('clear-all/', views.clear_all, name='clear_all'),
    path('api/get-totals/', views.get_totals, name='get_totals'),
    path('export/excel/', views.export_excel, name='export_excel'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
    path('quote-review/', views.quote_review, name='quote_review'),
    path('new-quote/', views.new_quote, name='new_quote'),
    path('quotes/', views.quote_list, name='quote_list'),
    path('quote/<int:quote_id>/resume/', views.resume_quote, name='resume_quote'),
    path('quote/<int:quote_id>/review/', views.review_specific_quote, name='review_specific_quote'),
    path('quote/<int:quote_id>/clone/', views.clone_quote, name='clone_quote'),
    path('quote/<int:quote_id>/archive/', views.toggle_archive, name='toggle_archive'),
    path('quote/<int:quote_id>/update-status/', views.update_status, name='update_status'),
]

