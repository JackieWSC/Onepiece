# restaurants/urls.py
from django.urls import path
from verity import views

urlpatterns = [
    path('main/', views.MainPageView.as_view()), # add this /menu/ route
]
