from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

# Add about views
class AboutPageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'about.html', context=None)

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

        context = {
            "foods" : foods,
        }

        return render(request, 'menu.html', context)