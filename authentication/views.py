from rest_framework.views import APIView
from rest_framework.response import Response
from google.oauth2 import id_token
from google.auth.transport import requests

class SignupView(APIView):
    def post(self, request):
        print('request ', request.data.get('credential', None))
        credential = request.data.get('credential', None)
        content = {'message': 'holi'}
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(credential, requests.Request(), "224188928478-l145vhrguhv8jq2f5dbmnds2p5md8kjp.apps.googleusercontent.com")

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
            print('idinfo ', idinfo)
        except ValueError:
            # Invalid token
            pass
        return Response(content)
