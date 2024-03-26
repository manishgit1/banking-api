from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response  import Response

# Create your views here.

class DematFormSubmissionView(APIView):
     permission_classes = (permissions.AllowAny,)

     def post(self, request):
          
          name = request.data['name']
          phone_number = request.data['phone_number']
          account_number = request.data['account_number']
          pan_card = request.data['pan_card']

          #to be continued..

  
  