from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponse

class WelcomePageView(TemplateView):
    def get(self, request, **kwargs):

        if 'user_name' in request.GET:
            return HttpResponse('Welcome!~'+request.GET['user_name'])
        else:
            #return render_to_response('welcome.html',locals())
            context = {
                'name' : 'Jackie', 
            }
            
            return render(request, 'welcome.html', context)


def welcome(request):
    return render_to_response('welcome.html', locals())
