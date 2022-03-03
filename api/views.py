from rest_framework import viewsets
from django.contrib.auth import get_user_model
from api import serializers

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    View set for User profile
    """
    # To use ModelViewSet, define serializer_class and queryset
    serializer_class = serializers.UserProfileSerializer
    queryset = get_user_model().objects.all()