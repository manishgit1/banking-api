from django.db import models
from activation.models import AppUser

# Create your models here.

class DematAccount(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=30, unique=True)

    
    