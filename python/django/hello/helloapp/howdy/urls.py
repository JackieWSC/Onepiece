# howdy/urls.py
from django.urls import path
from howdy import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('about/', views.AboutPageView.as_view()), # add this /about/ route
    path('menu/', views.MenuPageView.as_view()), # add this /menu/ route
]
