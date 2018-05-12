# restaurants/urls.py
from django.urls import path
from restaurants import views

urlpatterns = [
    path('menu/', views.MenuPageView.as_view()), # add this /menu/ route
    path('menu/<int:id>/', views.MenuPageView.as_view()),
    path('restaurants_list/', views.RestaurantsListPageView.as_view()),
    path('comment/<int:id>/', views.NewCommentPageView.as_view()),
    path('pdf/', views.GeneratePdfView.as_view()),
    path('set_cookie/', views.SetCookiesView.as_view()),
    path('get_cookie/', views.GetCookiesView.as_view()),
    path('test_sessoin/', views.TestSessionView.as_view()),
    path('test_sessoin_id/', views.TestSessionIdView.as_view()),
    
]
