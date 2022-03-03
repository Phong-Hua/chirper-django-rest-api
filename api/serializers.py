import email
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serialize user profile object
    """

    class Meta:
        # Specify the model
        model = get_user_model()
        # Specify the fields we want to be serialized
        fields = ('id', 'email', 'name', 'password', 'avatarURL')
        # Set special requirement for password
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
                'style': {
                    'input_type': 'password'
                }
            }
        }
    # Define create method
    def create(self, validated_data):
        """
        Create a user with data
        """
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            avatarURL=validated_data['avatarURL']
        )
        return user
    