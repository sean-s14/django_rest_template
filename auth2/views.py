# Built-in
import json

# Django
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, get_user_model

# Rest Framework
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

# Custom
from .serializers import (
    ForeignUserSerializer,
    UserSerializer,
    UserVerificationSerializer,
    PasswordResetSerializer,
    PasswordChangeSerializer,
)
from .permissions import IsUserOrAdmin
from .email import send_email
from .utils import code_generator

UserModel = get_user_model()


class UserList(ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class ForeignUserList(ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = ForeignUserSerializer
    permission_classes = []
    authentication_classes = []


class UserCreate(CreateAPIView):
    """A view to create a new user. However only the admin can view all users."""
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            return Response(
                {"error": "Authenticated users cannot create users"},
                status=status.HTTP_403_FORBIDDEN
            )

        password1 = request.data.get('password', None)
        password2 = request.data.get('password2', None)
        if password1 != password2:
            return Response(
                { "password2": "Does not match first password" },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data = self.create(request, *args, **kwargs)  # ID, Email & Username
        # print(user_data)

        email_problem = Response(
                {"error": "There was an issue sending verification code try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            email = user_data.get('data', None).get('email', None)
            if email is not None:
                user = UserModel.objects.get(email=email)
            else: return email_problem
        except Exception as e:
            print(e)
            return email_problem

        msg = f"""Welcome to my Django React Template.
        Your verification code is: {user.code}"""
        send_email(email=email, html_content=msg) # TODO: uncomment this when ready

        headers = user_data.get('headers', None)
        return Response(
            {"success": f"Your account has been created, enter the six digit code sent to {email} to verify your account"}, 
            status=status.HTTP_201_CREATED,
            headers=headers
        )
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return {"data": serializer.data, "headers": headers} 


class ForeignUserDetail(RetrieveAPIView):
    """A view for anonymous users to view all users, typically for leaderboards."""
    queryset = UserModel.objects.all()
    serializer_class = ForeignUserSerializer
    permission_classes = []
    authentication_classes = []


class UserDetail(RetrieveUpdateDestroyAPIView):
    """A view to retrieve, update and delete a user. However only the user specified 
    in `request.user` can perform actions to update or delete"""
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrAdmin]

    def change_password(self, data):
        user = self.request.user

        # Fail if old password is None
        old_password = data.get("old_password", None)
        if old_password is None: return Response(
            {"error": "You must enter your current password first"},
            status=status.HTTP_400_BAD_REQUEST,
        )

        serializer = PasswordChangeSerializer(user, data=data)
        if serializer.is_valid():
            print(serializer.validated_data)
            print(serializer.errors)
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success": "Password has been updated!"})

    def patch(self, request, *args, **kwargs):
        body = request.body
        data = json.loads(body.decode('utf-8'))
        # print("\nData :", data)
        print("Keys:", list(data.keys()))
        image = data.get('imageURI', None)
        # print("Image:", image)
        if image is not None: print("\nImage:", image[100])
        # print("\nData :", data.get('imageURI', None)[100])

        if request.path == '/auth/user/change-password/':
            return self.change_password(data)

        # If using access token instead of pk
        if self.kwargs.get('pk', None) is None:
            # Get user_id from access token
            self.kwargs['pk'] = self.request._auth.get('user_id', None)
            kwargs['token'] = True
            return self.partial_update(request, *args, **kwargs)

        return self.partial_update(request, *args, **kwargs)

    # def get_object(self):
    #     return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        token = kwargs.pop('token', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        if token:
            refresh = RefreshToken.for_user(instance)
            refresh['username']    = instance.username
            refresh['email']       = instance.email
            refresh['is_verified'] = instance.is_verified
            refresh['is_active']   = instance.is_active
            refresh['date_joined'] = str(instance.date_joined)
            # Don't return imageURI everytime. Only when requested
            refresh['imageURI']   = instance.imageURI
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super().get(self, request, *args, **kwargs)

        request_token = request._auth
        if request_token is not None:
            request_token = str(request._auth)
            user = AccessToken(request_token)
            payload = user.payload
            # Remove unnecessary data
            del payload["token_type"]
            del payload["iat"]
            del payload["jti"]
            del payload["user_id"]
            del payload["exp"]

            return Response(payload, status=status.HTTP_200_OK)

        return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get('password', None)
        if password is None:
            return Response(
                {"error": "You must enter your password before deleting your account"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(password):
            return Response(
                {"error": "Wrong Password"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.delete()
        # TODO: Delete user Customer from stripe if one exists
        return Response(
            {"success": f"The account \"{user.username}\" has been deleted"},
            status=status.HTTP_200_OK,
            # status=status.HTTP_204_NO_CONTENT,
        )


class UserResetPassword(UpdateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = []
    authentication_classes = []

    def patch(self, request, *args, **kwargs):
        body = request.body
        data = json.loads(body.decode('utf-8'))
        keys = data.keys()

        stage = kwargs.get('stage', None)
        email = data.get("email", None)
        
        if email is None: 
            return Response(
                {"error": "No email was provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = UserModel.objects.get(email=email)
        except Exception as e:
            return Response(
                {"email": "No user exists with the specified email"},
                status=status.HTTP_404_NOT_FOUND
                )

        if stage == 1:
            # STEP 1: Send code as text/email
            if len(keys) == 1:
                user.code = code_generator()
                user.save()
                print("Code:", user.code)
                
                # TODO: Send text containing 6 digit code
                msg = f"Your Django Rest Template verification code is: {user.code}"
                send_email(email=email, html_content=msg)
                return Response(
                    {"success": f"A code has been sent to {email} with a verification code"},
                    status=status.HTTP_200_OK,
                )
        elif stage == 2:
            # STEP 2: Confirm the code sent
            serializer = PasswordResetSerializer(data=data)
            if serializer.is_valid():
                return Response(
                    {"success": "Code Confirmed! Enter your new password"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif stage == 3:
            # Step 3: Serialize data and save
            serializer = PasswordChangeSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"success": "Your password has been updated"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': 'Stage of specified number does not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserVerification(UpdateAPIView):
    serializer_class = UserVerificationSerializer
    queryset = UserModel.objects.all()
    permission_classes = []
    authentication_classes = []

    def patch(self, request, *args, **kwargs):
        print("\nRequest Data :", request.data)

        serializer = self.get_serializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        print('\nSerializer Data :', serializer.data, '\n')

        # serializer.data
        # print(serializer.data)

        username = serializer.data["username"]
        email = serializer.data["email"]
        password = serializer.data["password"]
        code = serializer.data["code"]
        print(username, email, password, code)

        user = authenticate(username=username, email=email, password=password)
        print("User:", user)

        if user is None:
            return Response(
                {"error": "Invalid username/email or password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_profile = user.userprofile
        if code == user_profile.code:
            user_profile.is_verified = True
            user_profile.save()
            return Response(
                {"success": "You have been verified"}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "The code you entered does not match the code that was sent to you."},
                status=status.HTTP_400_BAD_REQUEST,
            )
