from django.db import models

# Create your models here.
class user(models.Model):
    username=models.CharField(max_length=32)
    big_ope=models.FloatField()
    big_con = models.FloatField()
    big_ext = models.FloatField()
    big_agr = models.FloatField()
    big_neu = models.FloatField()

    def __str__(self):
        return self.username

