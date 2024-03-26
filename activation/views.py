#from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import  login, logout
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ( UserLoginSerializer, 
UserRegisterSerializer,
UserSerializer)
from rest_framework import permissions, status
from .models import AppUser
from .validations import custom_validation

from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from .emails import send_otp_via_email



#Register view logic here 

class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        
        serializer = UserRegisterSerializer(data=clean_data)

        if serializer.is_valid(raise_exception=True):
             user = serializer.create(clean_data)
             send_otp_via_email(serializer.validated_data['email'])

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


    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)

            token, token_created  = Token.objects.get_or_create(user=user)


        
            try:
            
                 return Response({
                    'email': user.email,
                    'account_number': user.account_number,
                    'access_token': token.key
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            



#logout view logic here
class UserLogout(APIView):
	permission_classes = (permissions.AllowAny,)
	authentication_classes = ()
	def post(self, request):
		logout(request)
		return Response(status=status.HTTP_200_OK)


#return the state of user with user data
class UserView(APIView):
	permission_classes = (permissions.IsAuthenticated,)
    
	authentication_classes = (TokenAuthentication,)
	def get(self, request):
		serializer = UserSerializer(request.user)
		return Response({'user': serializer.data}, status=status.HTTP_200_OK)
     


 



        


      



