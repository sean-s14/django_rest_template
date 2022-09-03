import os
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from rest_framework import serializers
# from .models import User

UserModel = get_user_model()


class ForeignUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ("id", "username", "imageURI")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'username', 'password', 'is_verified', 'is_active', 'date_joined', 'imageURI')
        read_only_fields = ('id', )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, username):
        print('Validating Username...')
        blacklist = None
        try:
            file = os.path.dirname(os.path.realpath(__file__)) + '/yt-blacklisted-words.txt'
            blacklist = open(file, "r").read().split(',')
        except FileNotFoundError as e:
            print(e)

        if blacklist is not None:
            for item in blacklist:
                if item.lower().strip() in username:
                    raise serializers.ValidationError("This username is not allowed")

        if '@' in username:
            raise serializers.ValidationError("The symbol @ cannot be in a username")
        
        return username

    def validate_email(self, email):
        print('Validating Email...')
        try:
            user = UserModel.objects.get(email=email)
            print('Error: email validation')
            raise serializers.ValidationError("A user with this email already exists")
        except UserModel.DoesNotExist as e:
            pass
        return email

    def validate_password(self, password):
        print('Validating Password...')
        if len(password) < 8:
            raise serializers.ValidationError("Passwords must be at least 8 characters long")
        if len(password) > 128:
            raise serializers.ValidationError("Passwords must be less than 128 characters long")
        return password

    def create(self, validated_data):
        print('Creating Password...')
        # Create hash from Password
        validated_data['password'] = make_password(validated_data['password'])
        print('Creating User...')
        user = UserModel.objects.create(**validated_data)
        return user


class UserVerificationSerializer(serializers.Serializer):
    """Serializer with 1 field 'code'."""
    code = serializers.CharField(min_length=6, max_length=6)

    class Meta:
        fields = ('code')


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate_code(self, value):
        email = self._kwargs.get('data', None).get('email', None)

        try:
            user = UserModel.objects.get(email=email)
        except Exception as e:
            raise serializers.ValidationError("No user exists with the specified email")

        if user.code is None or value != user.code:
            raise serializers.ValidationError("The code entered is incorrect")

        try:
            int(value)
        except ValueError as e:
            raise serializers.ValidationError("Code cannot contain letters")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    code = serializers.CharField(min_length=6, max_length=6, required=False,)
    old_password = serializers.CharField(min_length=8, max_length=128, write_only=True, required=False)
    new_password = serializers.CharField(min_length=8, max_length=128, write_only=True,)
    new_password2 = serializers.CharField(min_length=8, max_length=128, write_only=True,)

    def validate_email(self, value):
        try:
            user = UserModel.objects.get(email=value)
        except Exception as e:
            raise serializers.ValidationError("No user exists with the specified email")

        return value

    def validate(self, attrs):
        old_password = attrs.get("old_password", None)
        email = attrs.get("email", None)
        code = attrs.get("code", None)
        print(email, code)
        if (email is None or code is None) and old_password is None:
            raise serializers.ValidationError({"error": "Sorry, something went wrong try again later"})

        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password2": "Password fields didn't match"})
        return attrs

    def update(self, instance, validated_data):
        old_password = validated_data.get("old_password", None)
        email = validated_data.get("email", None)
        code = validated_data.get("code", None)
        print(validated_data)
        if (email is not None) and (code is not None) and (old_password is None): pass
        else:
            password = validated_data.get("old_password", None)
            if not instance.check_password(password):
                raise serializers.ValidationError({"error": "Old password is incorrect"})

        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserVerificationSerializer(serializers.Serializer):
    """Serializer with 1 field \"code\"."""
    code = serializers.CharField(min_length=6, max_length=6)

    class Meta:
        fields = ('code')
