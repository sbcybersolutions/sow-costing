from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quotes.urls')),  # ✅ This points root URL to your app
]
# This file defines the URL patterns for the core project.
# The `urlpatterns` list routes URLs to views. For more information please see:
