from django.db import models


# Create your models here.

class Classification(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.CharField(max_length=255, null=False)
    classification = models.CharField(max_length=255, null=False)

    class Meta:
        managed = True
        db_table = "classification"



