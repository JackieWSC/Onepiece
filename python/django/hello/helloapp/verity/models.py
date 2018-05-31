from django.db import models

# Create your models here.

class RefereesMain(models.Model):
    details = models.CharField(max_length=50)
    actions = models.CharField(max_length=200)

    def __str__(self):
        return self.details


class RefereesDetails(models.Model):
    person_name = models.CharField(max_length=20)
    relationship = models.CharField(max_length=50)
    contact = models.CharField(max_length=50, blank=True)
    remark = models.CharField(max_length=200)
    main = models.ForeignKey(RefereesMain, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.person_name


class CaseStatus(models.Model):
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    details = models.ForeignKey(RefereesDetails, on_delete=models.PROTECT)
