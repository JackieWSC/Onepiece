from django.contrib import admin

# Register your models here.
from verity.models import RefereesMain, RefereesDetails, CaseStatus
from verity.forms import RefereesMainForm, RefereesDetailsForm

# class RefereesMainAdmin(admin.ModelAdmin):
#     list_display = ('details', 'actions')
#     search_fields = ('details',)

class RefereesMainAdmin(admin.ModelAdmin):
    list_display = ('details', 'actions')
    form = RefereesMainForm

class RefereesDetailsAdmin(admin.ModelAdmin):
    list_display = ('person_name', 'relationship', 'contact', 'remark')
    fields = ('person_name','relationship','contact','remark','main')
    form = RefereesDetailsForm
    search_fields = ('person_name',)


class CaseStatusAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'status')
    fields = ('date_time', 'status','details')


admin.site.register(RefereesMain, RefereesMainAdmin)
admin.site.register(RefereesDetails, RefereesDetailsAdmin)
admin.site.register(CaseStatus, CaseStatusAdmin)