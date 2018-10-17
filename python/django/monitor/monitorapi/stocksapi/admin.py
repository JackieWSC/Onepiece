from django.contrib import admin

# Register your models here.
from stocksapi.models import StockPriceStatistics, Visitor


class StockPriceStatisticsAdmin(admin.ModelAdmin):
    list_display = ('stock', 'price', 'period', 'percentage', 'remark')
    fields = ('stock', 'price', 'period', 'percentage', 'remark')


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'page', 'latency')
    fields = ('page', 'latency')


admin.site.register(StockPriceStatistics, StockPriceStatisticsAdmin)
admin.site.register(Visitor, VisitorAdmin)