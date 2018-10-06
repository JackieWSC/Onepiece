from django.db import models

# Create your models here.
class Visitor(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    page = models.CharField(null=True, max_length=20)
    latency = models.IntegerField()