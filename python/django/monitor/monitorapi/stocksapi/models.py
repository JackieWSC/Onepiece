from django.db import models

# Create your models here.
class Visitor(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    page = models.CharField(null=True, max_length=20)
    latency = models.IntegerField()


class StockPriceStatistics(models.Model):
    stock = models.CharField(null=True, max_length=10)
    period = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=1)
    count = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=1)
    remark = models.CharField(null=True, max_length=50)
