import requests
from requests_oauthlib import OAuth2Session

from config import Config

class erRest:
    scope = 'blogger'
    api_key = Config.bloger_api_key2
    player_blog_id = '7248995940539759558'
    er_blog_id = '1966293608187192453'
    wp_post_id = '6424181253444860473'
    REST_BLOG_URL_FORMAT = f'https://www.googleapis.com/blogger/v3/blogs/{player_blog_id}'
    REST_NO_AUTH_BLOG_URL_REQUEST = f'{REST_BLOG_URL_FORMAT}?key={api_key}'
    creds = {"installed": {"client_id": "946832198726-eub0q1jk1b46emlsqdrbsj3aupsij1ue.apps.googleusercontent.com",
                           "project_id": "bloggertools-170622", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                           "token_uri": "https://oauth2.googleapis.com/token",
                           "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                           "client_secret": "kDiIp5JzdDVOeQrhdfGveiZ1", "redirect_uris": ["http://localhost"]}}
    # Inlcude your data
    client_id = creds['installed']['client_id']
    client_secret = creds['installed']['client_secret']
    redirect_uri = creds['installed']['redirect_uris'][0]
    user_blogs_url = "https://www.googleapis.com/blogger/v3/users/self/blogs"
    token_uri = creds['installed']['token_uri']
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?"

    @staticmethod
    def get_auth_code():
        payload = {'scope': erRest.scope, 'response_type':'code',
                   'state' : 'security_token3D138r57',
                    'redirect_uri': erRest.redirect_uri, 'client_id': erRest.client_id
                   }
        return requests.get(url="https://accounts.google.com/o/oauth2/v2/auth",params=payload)

 #        """https://accounts.google.com/o/oauth2/v2/auth?
 # scope=email%20profile&
 # response_type=code&
 # state=security_token%3D138r5719ru3e1%26url%3Dhttps%3A%2F%2Foauth2.example.com%2Ftoken&
 # redirect_uri=com.example.app%3A/oauth2redirect&
 # client_id=client_id"""


    @staticmethod
    def get_user_blogs_token(code):
        url = erRest.token_uri
        payload = {'code': code,
                   'client_id': erRest.client_id,
                   'client_secret': erRest.client_secret,
                   'redirect_uri': erRest.redirect_uri,
                   'grant_type': 'authorization code'
        }
        return requests.post(url=url, data=payload)
#     """POST /token HTTP/1.1
# Host: oauth2.googleapis.com
# Content-Type: application/x-www-form-urlencoded
#
# code=4/P7q7W91a-oMsCeLvIaQm6bTrgtp7&
# client_id=your_client_id&
# client_secret=your_client_secret&
# redirect_uri=http://127.0.0.1:9004&
# grant_type=authorization_code"""
    @staticmethod
    def get_user_blogs(token):
        headers = {'content-type': 'application/json', 'Authorization': f'Bearer {token}'}

        # Get your authenticated response
        resp = requests.get(erRest.user_blogs_url, headers=headers)
        return resp


# Authenticating with OAuth2 in Requests




# @staticmethod
    # def getOauthResource():
        # Authenticating with OAuth2 in Requests

        # Create a session object
        # oauth = OAuth2Session(erRest.client_id, redirect_uri=erRest.redirect_uri)

        # Fetch a token
        # token = oauth.fetch_token(erRest.creds['installed']['token_uri'], client_secret=erRest.client_secret)

        # Get your authenticated response
        # get_access_token("https://api.example.com/access_token", "abcde", "12345")
        #
        # return token




     # Create a session object
        # oauth = OAuth2Session(erRest.client_id, redirect_uri=erRest.redirect_uri)
        #
        # # Fetch a token
        # token = oauth.fetch_token(erRest.token_uri, client_secret=erRest.client_secret)
        # return token