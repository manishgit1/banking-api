from rest_framework import serializers 
from django.contrib.auth import  authenticate
from .models import AppUser, BankAccount
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from rest_framework.response import Response



#Serializer for user registration

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    account_number = serializers.CharField(write_only=True)
    transaction_pin = serializers.CharField(max_length=4)

    class Meta:
        model =  AppUser
        fields = ['email', 'name', 'password', 'phone_number', 'account_number', 'transaction_pin']
    
    def validate_account_number(self, value):
        try:
            #Check if the provided account number exists in the BankAccount model
            bank_account = BankAccount.objects.get(account_number=value)

        except BankAccount.DoesNotExist:
            raise serializers.ValidationError('Invalid account number')    

    

    
    def create(self, validated_data):
         #create a new user with the provided data
        user = AppUser.objects.create_user(email=validated_data['email'],
                                         password=validated_data['password'],
                                         name=validated_data['name'],
                                         phone_number=validated_data['phone_number'],
                                         account_number = validated_data['account_number'],
                                         transaction_pin = validated_data['transaction_pin'],
                                         )  
       

        
        return user
    
    
        
    
#Serializer for user login
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField()
    phone_number = serializers.CharField(required=False)

    def check_user(self, validated_data):

        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        password = validated_data['password']


        if not email and not phone_number:
            raise serializers.ValidationError('Either email or phone number is required..')
        
        if email:
            #Authenticate user using email and password
            user = authenticate(username=email, password=password)
            if user:
                return user
            else:
                return Response({'error': 'Invalid credentials!'})
            

        if phone_number:
          try:  
             #Authenticate user using phone number and password
             user = AppUser.objects.get(phone_number=phone_number)
             user = authenticate(username=user.email, password = password)  
             if user:
                return user  
          
          except AppUser.DoesNotExist:
              raise serializers.ValidationError('Invalid credentials!')

        return serializers.ValidationError('Invalid credentials!')    

#Serializer for user details
            
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('email', 'name', 'phone_number', 'account_number', 'account_balance')





