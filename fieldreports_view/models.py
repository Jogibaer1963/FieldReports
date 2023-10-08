from django.db import models
from datetime import date

# Create your models here.
class combine_reports(models.Model):
    report = models.IntegerField(primary_key=True,)
    machine = models.CharField(max_length=8)
    hours = models.IntegerField(blank=True)
    image = models.CharField(blank=True, max_length=2)
    report_date = models.DateField(blank=True)
    failure_date = models.DateField(blank=True)
    repair_date = models.DateField(blank=True)
    bgz_master = models.CharField(blank=True, max_length=9)
    part_number = models.CharField(blank=True, max_length=9)
    system_text = models.CharField(blank=True, max_length=455)
    harvest_text = models.CharField(blank=True, max_length=455)
    failure_code = models.CharField(blank=True, max_length=455)
    failure_long_text = models.CharField(blank=True, max_length=455)
    failure_diagnose_text = models.CharField(blank=True, max_length=455)
    remedy_text = models.CharField(blank=True, max_length=455)
    reason_text = models.CharField(blank=True, max_length=455)
    comment_text = models.CharField(blank=True, max_length=455)
    comment_ext_text = models.CharField(blank=True, max_length=455)
    long_text_extra = models.CharField(blank=True, max_length=455)
    repair_long_text = models.CharField(blank=True, max_length=455)
    # date_of_upload = models.DateTimeField()
