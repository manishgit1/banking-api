
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
import uuid

class AppUserManager(BaseUserManager):
    def create_user(self, email, name, password, phone_number, account_number, transaction_pin):
        if not email:
            raise ValueError('An email is required.')
        if not name:
            raise ValueError('A username is required.')
        if not password:
            raise ValueError('A password is required.')
        if not phone_number:
            raise ValueError('A phone number is required.')
        if not account_number:
            raise ValueError('An account number is required.')
        if not transaction_pin:
            raise ValueError('A transaction pin is required.')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone_number=phone_number, account_number=account_number, transaction_pin=transaction_pin)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password, phone_number, account_number):
        if not email:
            raise ValueError('An email is required.')
        if not name:
            raise ValueError('A username is required.')
        if not password:
            raise ValueError('A password is required.')
        if not phone_number:
            raise ValueError('A phone number is required.')
        if not account_number:
            raise ValueError('An account number is required.')

        user = self.create_user(email, name, password, phone_number, account_number)
        user.is_superuser = True
        user.save()
        return user

class AppUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, default='', blank=True, null=True)
    account_number = models.CharField(max_length=30, default='', unique=True, blank=True, null=True)
    account_balance= models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    transaction_pin = models.CharField( null=False, max_length = 4)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number', 'account_number', 'transaction_pin']
    objects = AppUserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='appuser_groups',
        related_query_name='appuser_group',
        blank=True,
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='appuser_user_permissions',
        related_query_name='appuser_user_permission',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.name
    


class BankAccount(models.Model):
     
     account_holder_name = models.CharField(max_length=25)
     account_number = models.CharField( max_length=30,unique=True)



class Transaction(models.Model):
     transaction_id = models.AutoField(primary_key=True, unique=True)
     sender = models.ForeignKey(AppUser, related_name='sent_transactions', on_delete=models.CASCADE, default='')
     receiver = models.ForeignKey(AppUser, related_name='received_transactions', on_delete=models.CASCADE, default='')
     amount = models.DecimalField(max_digits=10, decimal_places=2)
     timestamp = models.DateTimeField(auto_now_add=True)


    

     
         
