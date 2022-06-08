from django.db import models

class job_record(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    post_code = models.IntegerField(null=True)
    job_date = models.DateField(null=True)
    job_time = models.TimeField(null=True)
    job_detail = models.CharField(max_length=300)
    is_done = models.BooleanField(default=False)

    technician = models.CharField(max_length=50, null=True)



    def __str__(self):
        return self.first_name