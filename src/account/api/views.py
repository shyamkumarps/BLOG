from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from account.api.serializers import RegistrationSerializer ,AccountPropertiesSerializer

from rest_framework.decorators import api_view,permission_classes

from rest_framework.permissions import IsAuthenticated

from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from rest_framework.views import APIView


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data={}
        if serializer.is_valid():
            # het account object when it return account obj fron Registrationserializer
            account =serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = account.email
            data['username'] = account.username
            # data['phonenumber'] = account.phonenumber
            # query (return )the token that is generated to get
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.error
        return Response(data)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def account_properties_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer = AccountPropertiesSerializer(account)
        return Response(serializer.data)


@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        account = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method=='PUT':
        serializer = AccountPropertiesSerializer(account,data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account update success"
            return Response(data=data)
        return Response(serializer.error,status=status.HTTP_400_BAD_REQUEST)





class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = account.pk
			context['email'] = email
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)


class ForgotPasswordEmailVerification(APIView):

    def post(self, request):

        data = request.data

        email = data.get('email')

        response = {}

        user_check_email = User.objects.filter(email= email)

        if len(user_check_email) > 0:
            response['status'] = 'Valid Email Address'
            response['valid_email'] = email
            

            otp = random.randint(10000, 99999)

            response['otp'] = otp

            ForgotPasswordRequest.objects.create(email= email, otp= otp, status='unverified')

            message= 'Hi,\n This is an auto-generated email from EzTutor Application with reference to Forgot Password.\n \n For security reasons, your old password will not be shared. Verify with code to reconfigure your new password.\n VERIFICATION CODE:'+str(otp)+'\n In case of any issues, please contact us for further assistance.\n\n\nThanks\nAdmin'
            subject= 'Reset Password Verification Code',
            
            send_mail(
                subject, 
                message, 
                settings.EMAIL_HOST_USER, 
                [email], 
                fail_silently=False
            )

        else:
            response['status'] = 'Invalid Email Address'
            response['email'] = ''
        
        return Response(response)
