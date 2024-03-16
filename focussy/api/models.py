from django.db import models


# Create your models here.


class Client(models.Model):
    telegram_id = models.CharField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
