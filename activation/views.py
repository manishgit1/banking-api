from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (UserLoginSerializer, 
UserRegisterSerializer, 
UserSerializer, TransactionSerializer)
from rest_framework import permissions, status
from .validations import custom_validation
from .models import AppUser, Transaction

# Create your views here.

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        print(clean_data)
        serializer = UserRegisterSerializer(data=clean_data)

        if serializer.is_valid(raise_exception=True):
             user = serializer.create(clean_data)

        print("validation error: ", serializer.errors)
        
        if user:
                 return Response(
                       {'name': user.name,
                        'email': user.email,
                        'phone_number': user.phone_number,
                        'account_number': user.account_number,
                        'transaction_pin': user.transaction_pin}
                       , status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        print(data)
        
        serializer = UserLoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            
            try:
                 return Response(
                  {'email': user.email,
                   'account_number': user.account_number,
                   'access_token': access_token}, status=status.HTTP_200_OK)
           
            except Exception as e:
                  return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
	authentication_classes = (SessionAuthentication,)
	##
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)
      


class BalanceTransferView(APIView):
      permission_classes = (permissions.IsAuthenticated,)
      authentication_classes = (SessionAuthentication,)
     
      def post(self, request):
            #balance transfer logic here
        
            

            sender = request.user
            receiver_account_number = request.data.get('receiver_account_number')
            amount = int(request.data.get('amount'))
            transaction_pin = request.data.get('transaction_pin')

            try:
                  receiver = AppUser.objects.get(account_number=receiver_account_number)

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
            transaction = Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)

            sender.save()
            receiver.save()

            serializer = TransactionSerializer(transaction)

            return Response({
                  'sender_name': sender.name,
                  'sender_account_number': sender.account_number,
                  'receiver_name': receiver.name,
                  'receiver_account_number': receiver.account_number,
                  'amount': transaction.amount,
                  'date': transaction.timestamp
            }, status=status.HTTP_201_CREATED)
      

class BalanceCheckView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
          balance = request.user.account_balance
          return Response({'account-balance': balance}, status=status.HTTP_200_OK)    



class TransactionHistoryView(APIView):
      permission_classes = (permissions.IsAuthenticated,)

      def get(self, request):
            user = request.user

            #Retrieve the user's transaction history
            transactions = Transaction.objects.filter(sender=user) | Transaction.objects.filter(receiver=user)

            #serializer the transactions
            serializer = TransactionSerializer(transactions, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)