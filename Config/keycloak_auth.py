from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from keycloak import KeycloakOpenID
import requests
from django.conf import settings
import base64

keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_CONFIG['SERVER_URL'],
    client_id=settings.KEYCLOAK_CONFIG["CLIENT_ID"],
    verify=settings.KEYCLOAK_CONFIG["VERIFY_SSL"],
    realm_name=settings.KEYCLOAK_CONFIG["REALM"]
)

class KeycloakUser:
    def __init__(self, user_info):
        self.user_info = user_info
        self.is_authenticated = True

    def __str__(self):
        return self.user_info.get("preferred_username", "unknown")

class KeycloakAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            user_info = keycloak_openid.decode_token(
                token,
                key=None,  # clave pública del realm
            )
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Token inválido o expirado: {str(e)}")
        user = KeycloakUser(user_info)
        return (user, None)