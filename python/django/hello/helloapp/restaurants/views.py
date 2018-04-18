from django.shortcuts import render
from django.views.generic import TemplateView
from restaurants.models import Restaurant, Food

# Create your views here.

# Add menu views
class MenuPageView(TemplateView):
    def get(self, request, **kwargs):
        
        food1 = { 
            'name':'coffee',
            'price':'$38',
            'comment':'good',
            'is_spicy':'false'
        }


        food2 = { 
            'name':'milk tea',
            'price':'$18',
            'comment':'good',
            'is_spicy':'false'
        }

        foods = [food1, food2]

        restaurants = Restaurant.objects.all()

        print(restaurants[0])

        context = {
            "restaurants" : restaurants,
        }

        return render(request, 'menu.html', context)