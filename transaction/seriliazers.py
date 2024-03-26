from rest_framework import serializers
from .models import Transaction


#Serializer for transaction details
class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField(source='sender.name')
    receiver = serializers.StringRelatedField(source='receiver.name')  
    sender_account_number = serializers.SerializerMethodField()
    receiver_account_number = serializers.SerializerMethodField()

        
    @staticmethod
    def mask_account_number(account_number):
    # Ensure account_number is a string
       account_number_str = str(account_number)

    # Determine the length of the account number
       num_digits = len(account_number_str)

    # Mask all but the last 4 digits
       masked_account_number = '*' * (num_digits - 7) + account_number_str[-7:]

       return masked_account_number



    def get_sender_account_number(self, obj):
        return self.mask_account_number(obj.sender.account_number)

    def get_receiver_account_number(self, obj):
        return self.mask_account_number(obj.receiver.account_number)    


    class Meta:
        model = Transaction
        fields= ['sender','sender_account_number', 'receiver','receiver_account_number','amount','remarks', 'timestamp']