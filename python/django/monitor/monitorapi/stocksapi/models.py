from django.db import models


# Create your models here.
class Visitor(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    page = models.CharField(null=True, max_length=50)
    latency = models.IntegerField()


class StockPriceStatistics(models.Model):
    stock = models.CharField(null=True, max_length=10)
    period = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=1)
    count = models.IntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=1)
    remark = models.CharField(null=True, max_length=50)


class StockDailyInfo(models.Model):
    date = models.DateField(db_column='date')
    stock = models.CharField(db_column='stock', null=True, max_length=10)
    high = models.DecimalField(db_column='high', max_digits=5, decimal_places=2)
    low = models.DecimalField(db_column='low', max_digits=5, decimal_places=2)
    close = models.DecimalField(db_column='close', max_digits=5, decimal_places=2)


class StockKDInfo(models.Model):
    date = models.DateField(db_column='date')
    stock = models.CharField(db_column='stock', null=True, max_length=10)
    high = models.DecimalField(db_column='high', max_digits=5, decimal_places=2)
    low = models.DecimalField(db_column='low', max_digits=5, decimal_places=2)
    close = models.DecimalField(db_column='close', max_digits=5, decimal_places=2)
    highest = models.DecimalField(db_column='highest', max_digits=5, decimal_places=2)
    lowest = models.DecimalField(db_column='lowest', max_digits=5, decimal_places=2)
    rsv = models.DecimalField(db_column='rsv', max_digits=5, decimal_places=4)
    k = models.DecimalField(db_column='k', max_digits=5, decimal_places=4)
    d = models.DecimalField(db_column='d', max_digits=5, decimal_places=4)


