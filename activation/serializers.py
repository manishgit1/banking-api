from rest_framework import serializers 
from django.contrib.auth import  authenticate
from .models import AppUser, Transaction, BankAccount



class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    account_number = serializers.CharField(write_only=True)
    transaction_pin = serializers.CharField(max_length=4)

    class Meta:
        model =  AppUser
        fields = ['email', 'name', 'password', 'phone_number', 'account_number', 'transaction_pin']
    
    def validate_account_number(self, value):
        try:
            bank_account = BankAccount.objects.get(account_number=value)

        except BankAccount.DoesNotExist:
            raise serializers.ValidationError('Invalid account number')    


    def create(self, validated_data):

        user = AppUser.objects.create_user(email=validated_data['email'],
                                         password=validated_data['password'],
                                         name=validated_data['name'],
                                         phone_number=validated_data['phone_number'],
                                         account_number = validated_data['account_number'],
                                         transaction_pin = validated_data['transaction_pin'])   


        return user 
    

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
            user = authenticate(username=email, password=password)
            if user:
                return user
            

        if phone_number:
          try:  
             user = AppUser.objects.get(phone_number=phone_number)
             user = authenticate(username=user.email, password = password)  
             if user:
                return user  
          
          except AppUser.DoesNotExist:
              raise serializers.ValidationError('Invalid credentials!')

        return serializers.ValidationError('Invalid credentials!')    
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('email', 'name', 'phone_number', 'account_number', 'account_balance')


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(source='sender.name')
    receiver = serializers.StringRelatedField(source='receiver.name')
    sender_account_number  = serializers.StringRelatedField(source='sender.account_number')
    receiver_account_number = serializers.StringRelatedField(source='receiver.account_number')
   # transaction_pin = serializers.StringRelatedField(source='sender.transaction_pin')

    class Meta:
        model = Transaction
        fields= ['sender','sender_account_number', 'receiver', 'receiver_account_number','amount', 'timestamp']