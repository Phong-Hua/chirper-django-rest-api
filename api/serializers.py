import email
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


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


# Since we use custom model that use email as username,
# We need to define custom serializer for login
class LoginSerializer(serializers.Serializer):
    """
    Custom Serializer for login view
    """
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        style = {
            'input_type': 'password'
        }
    )

    # We override the validate function
    def validate(self, attrs):
        """
        We need to validate data
        email, password
        """
        email = attrs['email']
        password = attrs['password']

        # Authenticate user
        user = authenticate(
            # 1st argument => request you want to authenticate
            request=self.context.get('request'),
            username=email,
            password=password
        )

        # Authentication fail
        if not user:
            msg = ('Unable to authenticate with provided credential')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs