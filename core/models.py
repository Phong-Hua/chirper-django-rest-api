from django.db import models
from django.core.validators import validate_email
from django.contrib.auth.models import AbstractBaseUser,\
    PermissionsMixin, BaseUserManager    # To create custom user model


class UserProfileManager(BaseUserManager):
    """
    Manager for user profiles.
    We customize create_user and create_superuser function.
    """
    def create_user(self, email, name, password, avatarURL=''):
        """
        Create a new user
        """
        if not email:
            raise ValueError('User must have an email')

        if not password:
            raise ValueError('User must have a password')

        if not name:
            raise ValueError('User must have a name')

        # Validate email, if email is not valid => throw Validation Error
        validate_email(email)

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, avatarURL=avatarURL)
        user.set_password(password)
        # Save to db
        # It's best practice to specifying db using 'using'
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, avatarURL=''):
        """
        Create user user
        """
        user = self.create_user(email, name, password, avatarURL)
        user.is_staff = True
        user.is_superuser = True
        # Save to db
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model use email as username.
    Fields: email, name, password, avatarURL
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    # With avatar, we use empty string instead of null to store in database
    avatarURL = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Because we customize user model, we need to define UserManager
    # And assign to objects
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self) -> str:
        return self.email
