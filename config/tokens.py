# Simple JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenObtainSerializer,
    TokenRefreshSerializer,
    PasswordField,
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.state import token_backend

# Rest Framework
from rest_framework.exceptions import APIException
from rest_framework import status, serializers, exceptions

# Django
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _

# Custom
from auth2.email import send_email

UserModel = get_user_model()


class MyTokenObtainSerializer(TokenObtainSerializer):
    username_field = get_user_model().USERNAME_FIELD  # 'email'
    email_field = get_user_model().REQUIRED_FIELDS[0] # 'username'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(required=False)
        self.fields[self.email_field] = serializers.EmailField(required=False)
        self.fields["password"] = PasswordField()
        self.fields["code"] = serializers.CharField(min_length=6, max_length=6, required=False)

    def validate(self, attrs):
        authenticate_kwargs = {
            "password": attrs["password"],
        }
        if attrs.get(self.username_field, None) is not None:
            authenticate_kwargs[self.username_field] = attrs[self.username_field]
        if attrs.get(self.email_field, None) is not None:
            authenticate_kwargs[self.email_field] = attrs[self.email_field]
        if len(authenticate_kwargs.keys()) < 2:
            raise Exception("Unable to authenticate. Username or Email was not provided")
            
        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        return {}

    @classmethod
    def get_token(cls, user):
        return cls.token_class.for_user(user)


class UserNotVerifiedException(APIException):
    """An exception that is raised when a user has not yet been verified"""
    status_code = status.HTTP_423_LOCKED


class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if "code" in attrs:
            if user.code == attrs["code"]:
                user.is_verified = True
                user.save()
            else:
                raise APIException(detail="The code you entered was incorrect")

        # If user is not verified Raise Exception with Status 423
        if not user.is_verified:
            msg = f"Your Django Rest Template verification code is: {user.code}"
            print("Message :", msg)
            send_email(email=user.email, html_content=msg)
            raise UserNotVerifiedException(
                detail=f"This account has not yet been verified. An email has been sent to {user.email} with a verification code."
            )

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username']    = user.username
        token['email']       = user.email
        token['is_verified'] = user.is_verified
        token['is_active']   = user.is_active
        token['date_joined'] = str(user.date_joined)
        token['imageURI']    = user.imageURI
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_id = decoded_payload['user_id']
        user = UserModel.objects.get(pk=user_id)

        decoded_payload['username']   = user.username
        decoded_payload['email']      = user.email

        new_data = token_backend.encode(decoded_payload)

        data['access'] = new_data

        return data


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer