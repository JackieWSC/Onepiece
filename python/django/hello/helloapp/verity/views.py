from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from verity.forms import RefereesMainForm, RefereesDetailsForm
from verity.models import RefereesMain, RefereesDetails, CaseStatus

# Create your views here.
class MainPageView(TemplateView):
    def get(self, request, **kwargs):
        referees = RefereesMain.objects.all()
        form = RefereesMainForm(request.POST, referees[0])

        context = {
            'referees' : referees[0],
            'form' : form
        }

        return render(request, 'main.html', context)


    def post(self, request, **kwargs):
        #referees = RefereesMain.objects.all()
                
        id_value = request.POST.get("id_value", "")
        form_name = request.POST.get("form_name", "")
        actions = request.POST.get("actions", "")

        print(request.POST)
        print("id_value:", id_value)
        print("form_name:", form_name)

        if 'refereesMain' in form_name:

            id_value = request.POST.get("id_value", "")
            referees_main = get_object_or_404(RefereesMain, id=id_value)
            form = RefereesMainForm(request.POST or None, instance = referees_main)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)

        elif 'refereesDetails' in form_name:

            id_value = request.POST.get("id_value", "")
            referees_details = get_object_or_404(RefereesDetails, id=id_value)
            referees_details_form = RefereesDetailsForm(request.POST or None, instance = referees_details)

            referees_main = referees_details.main
            form = RefereesMainForm(request.POST or None, instance = referees_main)
            
            if referees_details_form.is_valid():
                referees_details_form.save()
            else:
                print(referees_details_form.errors)

        #print(form.errors)
        context = {
            'referees' : referees_main,
            'form' : form
        }

        return render(request, 'main.html', context)
        