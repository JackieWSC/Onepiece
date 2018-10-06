from django.contrib import admin

# Register your models here.
from stocksapi.models import Visitor

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('date_time','page', 'latency')
    fields = ('page', 'latency')


admin.site.register(Visitor, VisitorAdmin)