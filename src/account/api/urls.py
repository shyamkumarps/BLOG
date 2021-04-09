from django.urls import path
from account.api.views import (
	registration_view,
	account_properties_view,
	update_account_view,
	ObtainAuthTokenView,
	ForgotPasswordEmailVerification,
)

from rest_framework.authtoken.views import obtain_auth_token

# obtain_auth_token is a built in django view looks for the user model (AUTH_USER_MODEL = 'account.Account')
# it asks for the requied parameter to login a user based on user model
app_name = "account"

urlpatterns = [
	path('login', ObtainAuthTokenView.as_view(), name="login"),#obtain_auth_tokenend removed ,,request to usrl containing in this case email and password and return ,generate token upon sucessfull login
	
	path('properties', account_properties_view, name="properties"),
	path('properties/update', update_account_view, name="upate_properties"),
	
	path('register', registration_view, name="register"),

	path('ForgotPasswordEmailVerification/', ForgotPasswordEmailVerification.as_view()),
	
]