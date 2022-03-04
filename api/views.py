from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from api import serializers


class CreateUserAPIView(generics.CreateAPIView):
    """
    View for create a new user
    """
    serializer_class = serializers.UserProfileSerializer


class ListUserAPIView(generics.ListAPIView):
    """
    View for listing all user
    """
    serializer_class = serializers.UserProfileSerializer
    queryset = get_user_model().objects.all()
    # Allow request accept token
    # authentication_classes and permission_classes always go together
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class RetrieveUserAPIView(generics.RetrieveAPIView):
    """
    View for retrieving a single user
    """
    serializer_class = serializers.UserProfileSerializer
    queryset = get_user_model().objects.all()
    # Allow request accept token
    # authentication_classes and permission_classes always go together
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class UserLoginView(ObtainAuthToken):
    """
    View for login
    """
    serializer_class = serializers.LoginSerializer
    # The ObtainAuthToken does not have renderer_classes by default
    # So we specify it here
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
