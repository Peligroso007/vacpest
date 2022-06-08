from django.db import models
from .job_record import job_record

class Service_report(models.Model):
    job_id = models.OneToOneField(job_record, on_delete=models.CASCADE)
    service_frequency = models.IntegerField(null=True)
    service_finished_time = models.TimeField(null=True)
    further_service = models.DateField(null=True)
    area_treated = models.CharField(max_length=500)
    unchecked_area = models.CharField(max_length=500)
    type_of_pest_control = models.CharField(max_length=100)
    other_type = models.CharField(max_length=100)
    service_report = models.CharField(max_length=300)


    def __str__(self):
        return self.job_id.first_name