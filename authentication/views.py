from rest_framework.views import APIView
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed

# GOOGLE

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

class SignupView(APIView):
    def post(self, request):
        try:
            print('cariolinasd.data ', request.data)
            credential = request.data.get('credential', None)
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(credential, requests.Request(), "224188928478-l145vhrguhv8jq2f5dbmnds2p5md8kjp.apps.googleusercontent.com")

            print('idinfo ', idinfo)
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            email = idinfo['email']
            
            print('carrrrrrrrrrrrrasrssdas ', email)

            print('idinfo ', idinfo)

            if not email:
                raise AuthenticationFailed('Invalid token or email not found.')

            # Check if the user exists in your Django database based on the email.
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # If the user does not exist, create a new user using the email.
                user = User.objects.create(email=email, username=email.split('@')[0])  # Set a default username based on the email prefix.

            # Log in the user by associating the user with the request session.
            login(request, user)

            idinfo['user_id'] = user.id

            return Response({'message': 'User authenticated successfully', 'userData': idinfo})


        except ValueError:
            # Invalid token
            pass
    
    

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1'
    client_class = OAuth2Client



from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView

...

class UserRedirectView(LoginRequiredMixin, RedirectView):
    """
    This view is needed by the dj-rest-auth-library in order to work the google login. It's a bug.
    """

    permanent = False

    def get_redirect_url(self):
        return "redirect-url"