from rest_framework import serializers
from .models import DematAccount

class DematFormSerializer(serializers.ModelSerializer):
     
     pan_card = serializers.ImageField(max_length=1)
     

     class Meta:
          model = DematAccount
          fields = ['user', 'account_number', 'pan_card']
          

     

