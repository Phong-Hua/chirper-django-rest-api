from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from django.contrib.auth import get_user_model
from api import serializers


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    View set for User profile
    """
    # To use ModelViewSet, define serializer_class and queryset
    serializer_class = serializers.UserProfileSerializer
    queryset = get_user_model().objects.all()


class UserLoginView(ObtainAuthToken):
    """
    View for login
    """
    serializer_class = serializers.LoginSerializer
    # The ObtainAuthToken does not have renderer_classes by default
    # So we specify it here
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
