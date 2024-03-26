from django.db import models

from activation.models import AppUser

# Create your models here.


class Transaction(models.Model):
     transaction_id = models.AutoField(primary_key=True, unique=True)
     sender = models.ForeignKey(AppUser, related_name='sent_transactions', on_delete=models.CASCADE, default='')
     receiver = models.ForeignKey(AppUser, related_name='received_transactions', on_delete=models.CASCADE, default='')
     amount = models.DecimalField(max_digits=10, decimal_places=2)
     remarks = models.CharField(max_length=20, blank=True, null=True)
     timestamp = models.DateTimeField(auto_now_add=True)
