from django.db import models

class activity_log(models.Model):
    notification = models.CharField(max_length=500, null=True, blank=True)
    activity_date = models.DateField(auto_now_add=True, null=True)
    activity_time = models.TimeField(auto_now_add=True, null=True)
