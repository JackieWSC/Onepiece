from django.contrib import admin

# Register your models here.
from stocksapi.models import StockPriceStatistics, Visitor, StockDailyInfo, StockKDInfo


class StockPriceStatisticsAdmin(admin.ModelAdmin):
    list_display = ('stock', 'price', 'period', 'percentage', 'remark')
    fields = ('stock', 'price', 'period', 'percentage', 'remark')


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'page', 'latency')
    fields = ('page', 'latency')


class StockDailyInfoAdmin(admin.ModelAdmin):
    list_display = ('date', 'stock', 'high', 'low', 'close')
    fields = ('date', 'stock', 'high', 'low', 'close')


class StockKDInfoAdmin(admin.ModelAdmin):
    list_display = ('date', 'stock', 'high', 'low', 'close', 'highest', 'lowest', 'rsv', 'k', 'd')
    fields = ('date', 'stock', 'high', 'low', 'close', 'highest', 'lowest', 'rsv', 'k', 'd')


admin.site.register(StockPriceStatistics, StockPriceStatisticsAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(StockDailyInfo, StockDailyInfoAdmin)
admin.site.register(StockKDInfo, StockKDInfoAdmin)