
from activation.models import AppUser
from .models import Transaction
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .seriliazers import TransactionSerializer
from rest_framework import status, permissions
from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404





#logic for handling fund transfers
class BalanceTransferView(APIView):
      permission_classes = (permissions.IsAuthenticated,)
      authentication_classes = (SessionAuthentication, )
     
      def post(self, request):
            #balance transfer logic here
        
            

            sender = request.user
            receiver_name = request.data['receiver_name']
            receiver_account_number = request.data['receiver_account_number']
            amount = int(request.data['amount'])
            transaction_pin = request.data['transaction_pin']
            remarks = request.data.get('remarks')
           # print(sender)

         #   print(remarks)
          #  print(receiver)


            try:
                  receiver = get_object_or_404(AppUser, account_number=receiver_account_number, name=receiver_name)

            except AppUser.DoesNotExist:
                  return Response({'error': 'Invalid Transaction!! '}, status=status.HTTP_404_NOT_FOUND)
            
            if sender.account_balance < amount:
                  return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
            
            if transaction_pin != sender.transaction_pin:
                 return Response({'error': 'Invalid Transaction Pin'})
            
            #update account balance
            sender.account_balance -= amount
            receiver.account_balance += amount

            #create transaction record
            transaction = Transaction.objects.create(sender=sender, receiver=receiver, amount=amount, remarks=remarks)
            

            sender.save()
            receiver.save()

            serializer = TransactionSerializer(transaction)

            # return Response({
            #       'sender_name': sender.name,
            #       'sender_account_number': sender.account_number,
            #       'receiver_name': receiver.name,
            #       'receiver_account_number': receiver.account_number,
            #       'amount': transaction.amount,
            #       'category': category,
            #       'date': transaction.timestamp
            # }, status=status.HTTP_201_CREATED)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
      

#return the current balance of user 
class BalanceCheckView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
          balance = request.user.account_balance
          return Response({'account-balance': balance}, status=status.HTTP_200_OK)    


#return transaction records of user
class TransactionHistoryView(APIView):
      permission_classes = (permissions.IsAuthenticated,)

      def get(self, request):
            user = request.user

            #Retrieve the user's transaction history
            transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)

            #serializer the transactions
            serializer = TransactionSerializer(transactions, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
      

class TransactionSummary(APIView):
      permission_classes = (permissions.IsAuthenticated,)


      def get(self,request):
            user = request.user
            sent_transactions = Transaction.objects.filter(sender=user)
            received_transactions = Transaction.objects.filter(receiver=user)


            total_expenses = sent_transactions.aggregate(models.Sum('amount'))['amount__sum'] or 0
            total_income = received_transactions.aggregate(models.Sum('amount'))['amount__sum'] or 0

            return Response({
                  'total_income': total_income,
                  'total_expenses': total_expenses
            }, status=status.HTTP_200_OK)
      


# class TransactionByCategory(APIView):
#             permission_classes = (permissions.IsAuthenticated,)

#             def get(self, request): 
#                   user = request.user

#                   #Retrieve transactions based on category
#                   categories = Transaction.objects.filter(
#                         Q(sender=user) | Q(receiver=user)
#                    ).values_list('category', flat=True).distinct()
                  
#                   categories = [category for category in categories if category is not None]

#         # Initialize an empty dictionary to store transaction details for each category
#                   categories_data = {}

#         # Fetch details for each category
#                   for category in categories:
#                         transactions = Transaction.objects.filter(
#                 Q(sender=user, category=category) | Q(receiver=user, category=category)
#             )
                  
#                         serializer = TransactionSerializer(transactions, many=True)

#                         categories_data[category] = serializer.data

#                   return Response(categories_data, status=status.HTTP_200_OK)
            
