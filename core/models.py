from django.db import models
from django.conf import settings
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

    def tweets(self):
        """
        Return a queryset of of tweet made by this user
        """
        return self.tweet_set.all()

    def likes(self):
        """
        Return a query set of tweet that this user like
        """
        return self.like_set.all()

    def __str__(self) -> str:
        return self.email


class TweetManager(models.Manager):
    """
    Manager for tweet
    """
    def create(self, text=None, author=None, **extra_kwargs):
        """
        Create a tweet
        """
        if not text or len(text.strip()) == 0:
            raise ValueError('The text is required')
        if len(text) > 160:
            raise ValueError('The text should not exceed 160 characters')
        if not author:
            raise ValueError('The author is required')
        
        tweet = Tweet(text=text, author=author, **extra_kwargs)
        tweet.save(using=self._db)

        return tweet


class Tweet(models.Model):
    """
    Tweet model
    """
    text = models.TextField(
        max_length=160
    )
    # ForeignKey => One-Many-relationship
    # One user can create many tweets
    # related_name='tweet_set': the user can get a query set of all tweet
    # has created by user.tweet_set.all()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tweet_set'
    )
    # ManyToMany: One user can like many tweets.
    # One tweet can have many users like.
    # blank=True: This field is not required
    # related_name='likes_set'. The user can get all tweet they like by
    # user.like.set.all()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='like_set'
    )
    # ForeignKey => One-Many-relationship.
    # 'self' refer to Tweet. One tweet can have many reply Tweet.
    # blank=True: This field is not required.
    # null=True: The database accept NULL value for tweet object does not have
    # this fields.
    # related_name='replies', a tweet can access all replies
    # by tweet.replies.all()
    replying_to = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        related_name='replies',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    objects = TweetManager()

    def replies(self):
        """
        Get a queryset of replies of this tweet
        """
        return self.replies.all()

    # Handle like/remove a tweet
    def toggle(self, user):
        # If user already like, remove like
        if self.likes.filter(id=user.id).exists():
            self.likes.remove(user)
        else:
            self.likes.add(user)

    def __str__(self) -> str:
        return self.text
