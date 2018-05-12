from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from verity.forms import RefereesMainForm
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
        referees_main = get_object_or_404(RefereesMain, id=1)

        form = RefereesMainForm(request.POST or None, instance = referees_main)
            
        id_value = request.POST.get("id_value", "")

        print("id_value:", id_value)

        if form.is_valid():
            # form = RefereesMainForm(request.POST, instance = referees_main)
            form.save()

        #print(form.errors)
        context = {
            'referees' : referees_main,
            'form' : form
        }

        return render(request, 'main.html', context)
        