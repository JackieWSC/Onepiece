"""monitorapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from stocksapi import views

urlpatterns = [
    path('', views.stock_kd),
    path('kd', views.stock_kd),
    path('kd/<stock_code>/', views.stock_kd),
    path('history', views.stock_history),
    path('history/<stock_code>/', views.stock_history),
    path('tools', views.playground),
    path('backtesting', views.backtesting),
    path('checker', views.checker),
    # RESTFUL API
    path('kdindex/<stock_code>/', views.get_kd_index),
    path('nextkdindex/<stock_code>/', views.get_next_kd_index),
    path('stockhistory/<stock_code>/<int:year>/', views.get_stock_price_history),
    path('dbdata/<stock_code>/<int:year>/', views.get_db_data),
    path('dbkddata/<stock_code>/<int:year>/', views.get_db_kd_data),
    # MANAGEABILITY
    path('create_api_data_to_db/<stock_code>/<int:year>/<input_type>/', views.create_api_data_to_db),
    path('create_kd_data_to_db/<stock_code>/<input_type>/', views.create_kd_data_to_db),
    # Notification
    path('checknextkdindex', views.check_next_kd_index),
    path('checkstocklistkdindex', views.check_stock_list_kd_index),
    # Utility
    path('playground/', views.playground),
    path('admin/', admin.site.urls),
]
