from django.contrib.sessions.models import Session
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from email.mime.application import MIMEApplication
from restaurants.forms import CommentForm
from restaurants.models import Restaurant, Food, Comment
from restaurants.utils import render_to_pdf, render_to_pdf_file



import datetime

from easy_pdf.rendering import render_to_pdf

# Create your views here.

# Add menu views
class MenuPageView(TemplateView):
    def get(self, request, **kwargs):
        
        if 'id' in kwargs.keys():
            r = Restaurant.objects.get(id=kwargs['id'])

            context = {
                'r' : r
            }

            return render(request, 'menu.html', context)
        elif 'id' in request.GET:
            print(type(request.GET['id']))

            restaurants = Restaurant.objects.all()
            r = Restaurant.objects.get(id=request.GET['id'])

            context = {
                'restaurants' : restaurants,
                'r' : r
            }

            #values = request.META.items()
            # for k, v in values:
            #     print('{0} ---------- {1}'.format(k,v))

            return render(request, 'menu.html', context)
        else:
            return HttpResponseRedirect("/restaurants/restaurants_list/")


class RestaurantsListPageView(TemplateView):
    def get(self, request, **kwargs):
        
        restaurants = Restaurant.objects.all()
        request.session['restaurants'] = restaurants
        
        context = {
            'restaurants' : restaurants
        }

        return render(request, 'restaurants_list.html', context)


class CommentPageView(TemplateView):
    def get(self, request, **kwargs):
        if 'id' in kwargs.keys():
            r = Restaurant.objects.get(id=kwargs['id'])

            errors = []

            context = {
                'r' : r,
                'errors' : errors,
            }

            return render(request, 'comments.html', context)

        else:
            return HttpResponseRedirect("/restaurants/restaurants_list/")


    def post(self, request, **kwargs):
        r = Restaurant.objects.get(id=kwargs['id'])
        
        errors = []

        if 'ok' in request.POST:
            user = request.POST['user']
            content = request.POST['content']
            email = request.POST['email']
            date_time = datetime.datetime.now()

            if not user or not content or not email:
                errors.append('* Please fill in all informations.')
            if '@' not in email:
                errors.append('* The email format is invalid.')
            if not errors:
                Comment.objects.create(
                    user=user, email=email, content=content, date_time=date_time, restaurant=r)

                user = ''
                content = ''
                email = ''

        context = {
            'r' : r,
            'errors' : errors,
            'user' : user,
            'content' : content,
            'email' : email,
        }

        return render(request, 'comments.html', context)

class NewCommentPageView(TemplateView):
    def get(self, request, **kwargs):
        if 'id' in kwargs.keys():
            r = Restaurant.objects.get(id=kwargs['id'])
            form = CommentForm()
            errors = []

            context = {
                'r' : r,
                'form' : form,
                'errors' : errors,
            }

            return render(request, 'comments.html', context)

        else:
            return HttpResponseRedirect("/restaurants/restaurants_list/")


    def post(self, request, **kwargs):
        r = Restaurant.objects.get(id=kwargs['id'])


        if 'ok' in request.POST:
            form = CommentForm(request.POST)

            if form.is_valid():
                user = form.cleaned_data['user']
                content = form.cleaned_data['content']
                email = form.cleaned_data['email']
                date_time = datetime.datetime.now()

                c = Comment.objects.create(
                        user=user, email=email, content=content, date_time=date_time, restaurant=r)
                c.save()
                form = CommentForm(initial={'content':'No comments'})
        else:
            form = CommentForm(initial={'content':'No comments'})

        context = {
            'r' : r,
            'form' : form,
        }

        return render(request, 'comments.html', context)

class GeneratePdfView(TemplateView):
    def get(self, request, **kwargs):
        restaurants = Restaurant.objects.all()

        data = {
            'today': '2018', 
            'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }

        pdf = render_to_pdf('invoice.html', data)
        #pdf = render_to_pdf_file('invoice.html', data)


        # if pdf:
        #     response = HttpResponse(pdf, conten_type='applicatoin/pdf')
        #     filename = "Invoice_%s.pdf" %('123')
        #     content = "inline; filename='%s'" %(filename)

        #     response['Content-Disposition'] = content
        #     return response


        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'jackiewong613@gmail.com',
        #     ['window613@gmail.com'],
        #     fail_silently=False,
        # )

        email = EmailMessage(
            'Test attachment',
            'Hi yuen. Please find the attachement.',
            'jackiewong613@gmail.com',
            ['window613@gmail.com']
        )

        #email.attach_file(pdfFile, 'application/pdf')
        email.attach('yuen.pdf', pdf, 'application/pdf')
        email.send()

        return HttpResponse("Email Send")
        #return HttpResponse(pdf, content_type='application/pdf')

class SetCookiesView(TemplateView):
    def get(self, request, **kwargs):
        luncky_number = 21
        response = HttpResponse('Set your lucky number as {0}'.format(luncky_number))
        response.set_cookie('luncky_number', luncky_number)
        return response

class GetCookiesView(TemplateView):
    def get(self, request, **kwargs):
        if 'luncky_number' in request.COOKIES:
            return HttpResponse('Your luncky_number us {0}'.format(request.COOKIES['luncky_number']))
        else:
            return HttpResponse('No cookies.')

class TestSessionView(TemplateView):
    def get(self, request, **kwargs):
        request.session['luncky_number'] = 8

        if 'luncky_number' in request.session:
            luncky_number = request.session['luncky_number']
            response = HttpResponse('Your luncky_number is {0}'.format(luncky_number))

        del request.session['luncky_number']

        return response

class TestSessionIdView(TemplateView):
    def get(self, request, **kwargs):
        sid = request.COOKIES['sessionid']
        sid2 = request.session.session_key
        s = Session.objects.get(pk=sid)
        s_info = 'Session ID 1:' + sid + '<br>' + \
                 'Session ID 2:' + sid2 + '<br>' + \
                 'Expire_date:' + str(s.expire_date) + '<br>' + \
                 'Data:' + str(s.get_decoded())
        
        return HttpResponse(s_info)
