# restaurants/urls.py
from django.urls import path
from restaurants import views

urlpatterns = [
    path('menu/', views.MenuPageView.as_view()), # add this /menu/ route
]
