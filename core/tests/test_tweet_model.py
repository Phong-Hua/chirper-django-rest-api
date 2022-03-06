from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from core.models import Tweet


class TweetModelTests(TestCase):
    """
    Test class for tweet model
    """

    def sample_long_text(self):
        """
        This sample text is 161 character long.
        """
        return 'Lorem ipsum dolor sit amet, consectetur adipiscing '\
               + 'elit, sed do eiusmod tempor incididunt ut labore et '\
               + 'dolore magna aliqua. Ut enim ad minim veniam, quis........'

    def setUp(self):
        """
        Setup first user and second user.
        """
        payload_1 = {
            'email': 'user1@test.com',
            'name': 'user1',
            'password': 'user1'
        }
        payload_2 = {
            'email': 'user2@test.com',
            'name': 'user2',
            'password': 'user2'
        }
        self.first_user = get_user_model().objects.create_user(**payload_1)
        self.second_user = get_user_model().objects.create_user(**payload_2)

    def test_create_tweet_successfully(self):
        """
        Test create tweet successfully.
        """
        payload = {
            'text': 'The sample tweet',
            'author': self.first_user,
            'replying_to': None
        }
        tweet = Tweet.objects.create(**payload)
        # Expect the info: text, author, replying_to match
        self.assertEqual(tweet.text, payload['text'])
        self.assertEqual(tweet.author, payload['author'])
        self.assertEqual(tweet.replying_to, payload['replying_to'])
        # Expect the first_user has a tweet
        tweet_count = self.first_user.tweets().count()
        self.assertEqual(tweet_count, 1)

    def test_create_tweet_with_empty_text(self):
        """
        Test create a tweet with empty content.
        This should fail
        """
        payload = {
            'text': '',
            'author': self.first_user,
            'replying_to': None
        }

        with self.assertRaises(ValueError):
            Tweet.objects.create(**payload)

    def test_create_tweet_with_long_text(self):
        """
        Test create a tweet exceed max length = 160 character.
        This should fail
        """
        payload = {
            'text': self.sample_long_text(),
            'author': self.first_user,
            'replying_to': None
        }

        with self.assertRaises(ValueError):
            Tweet.objects.create(**payload)

    def test_create_tweet_with_none_text(self):
        """
        Test create a tweet with content is none.
        This should fail
        """
        payload = {
            'text': None,
            'author': self.first_user,
            'replying_to': None
        }

        with self.assertRaises(ValueError):
            Tweet.objects.create(**payload)

    def test_create_tweet_with_missing_text(self):
        """
        Test create a tweet with content is missing in payload.
        This should fail
        """
        payload = {
            'author': self.first_user,
            'replying_to': None
        }

        with self.assertRaises(ValueError):
            Tweet.objects.create(**payload)

    def test_create_tweet_with_none_author(self):
        """
        Test create a tweet with author is none.
        This should fail
        """
        payload = {
            'text': 'A sample tweet',
            'author': None,
            'replying_to': None
        }

        with self.assertRaises(ValueError):
            Tweet.objects.create(**payload)

    def test_create_tweet_with_missing_author(self):
        """
        Test create a tweet with author is missing in payload.
        This should fail
        """
        payload = {
            'text': 'A sample tweet',
            'replying_to': None
        }

        with self.assertRaises(ValueError):
            Tweet.objects.create(**payload)

    def test_create_tweet_with_missing_replying_to(self):
        """
        Test create a tweet with replying_to is missing in payload.
        This should success.
        """
        payload = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**payload)
        # Expect info match
        self.assertEqual(tweet.text, payload['text'])
        self.assertEqual(tweet.author, payload['author'])
        self.assertEqual(tweet.replying_to, None)
        # Expect the first_user has tweet count = 1
        tweet_count = self.first_user.tweets().count()
        self.assertEqual(tweet_count, 1)

    def test_create_reply_successfully(self):
        """
        Test create a replying tweet.
        The first user creates a tweet, second user then reply.
        This should success
        """
        # Create a tweet
        tweet_payload = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**tweet_payload)

        # Create a reply
        reply_payload = {
            'text': 'A sample reply',
            'author': self.second_user,
            'replying_to': tweet
        }

        reply = Tweet.objects.create(**reply_payload)
        # Expect info match
        self.assertEqual(reply.text, reply_payload['text'])
        self.assertEqual(reply.author, reply_payload['author'])
        self.assertEqual(reply.replying_to, tweet)
        # Retrieve the reply from tweet
        reply_count = tweet.replies.count()
        self.assertEqual(reply_count, 1)

    def test_create_more_reply(self):
        """
        Test create more than one reply.
        This should success
        """
        # Create a tweet
        tweet_payload = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**tweet_payload)

        # Create a reply
        reply_payload = {
            'text': 'A sample reply',
            'author': self.second_user,
            'replying_to': tweet
        }

        Tweet.objects.create(**reply_payload)
        # Create a second reply
        reply_payload['text'] = 'A second reply'
        Tweet.objects.create(**reply_payload)
        # Retrieve the reply from tweet
        reply_count = tweet.replies.count()
        # Expect number of reply is 2
        self.assertEqual(reply_count, 2)

    def test_create_reply_with_long_text(self):
        """
        Test create a reply exceed max length (160 characters).
        This should fail
        """
        # Create tweet
        tweet_payload = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**tweet_payload)
        # Try to create a reply
        reply_payload = {
            'text': self.sample_long_text(),
            'author': self.second_user,
            'replying_to': tweet
        }
        # Expect create a reply raise exception
        with self.assertRaises(ValueError):
            Tweet.objects.create(**reply_payload)

        # Expect the reply count is 0
        reply_count = tweet.replies.count()
        self.assertEqual(reply_count, 0)

    def test_like_a_tweet(self):
        """
        Test like a tweet.
        First user create a tweet. Second user then like.
        This should success
        """
        # Create a tweet
        payload = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**payload)

        # Second user like the tweet
        tweet.toggle(self.second_user)
        # From all user like the tweet, expect to find second_user
        exist_1 = tweet.likes.filter(id=self.second_user.id).exists()
        self.assertTrue(exist_1)
        # From all the tweets that second_user likes, expect it has this tweet
        exist_2 = self.second_user.likes().filter(id=tweet.id).exists()
        self.assertTrue(exist_2)

    def test_remove_like_a_tweet(self):
        """
        Test remove like a tweet.
        First user like the tweet. Second user like it, then remove like.
        This should success
        """
        # Create a tweet
        payload = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**payload)
        # Second user like the tweet
        tweet.toggle(self.second_user)
        # Toggle again to remove like
        tweet.toggle(self.second_user)
        # From all user like the tweet, expect to not find second_user
        exist_1 = tweet.likes.filter(id=self.second_user.id).exists()
        self.assertFalse(exist_1)
        # From all the tweets that second_user likes,
        # expect it does not have this tweet
        exist_2 = self.second_user.likes().filter(id=tweet.id).exists()
        self.assertFalse(exist_2)

    def test_like_a_reply(self):
        """
        Test like a reply.
        First_user creates a tweet. Second user replies the tweet.
        First user like that reply.
        This should pass
        """
        # Create a tweet
        payload_1 = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**payload_1)

        # Create a reply
        payload_2 = {
            'text': 'A sample reply',
            'author': self.second_user,
            'replying_to': tweet
        }
        reply = Tweet.objects.create(**payload_2)

        # User 1 like the reply
        reply.toggle(self.first_user)

        # Expect first_user show in reply's likes
        exist_1 = reply.likes.filter(id=self.first_user.id).exists()
        self.assertTrue(exist_1)
        # Expect first_user likes include the reply
        exist_2 = self.first_user.likes().filter(id=reply.id).exists()
        self.assertTrue(exist_2)

    def test_remove_like_a_reply(self):
        """
        Test remove like a reply.
        First_user creates a tweet. Second _user replies the tweet.
        First_user like that reply, then toggle again to remove the like.
        This should pass
        """
        # Create a tweet
        payload_1 = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**payload_1)

        # Create a reply
        payload_2 = {
            'text': 'A sample reply',
            'author': self.second_user,
            'replying_to': tweet
        }
        reply = Tweet.objects.create(**payload_2)

        # User 1 like the reply, the toggle again
        reply.toggle(self.first_user)
        reply.toggle(self.first_user)

        # Expect first_user is not in reply's likes
        exist_1 = reply.likes.filter(id=self.first_user.id).exists()
        self.assertFalse(exist_1)
        # Expect first_user likes does not include the reply
        exist_2 = self.first_user.likes().filter(id=reply.id).exists()
        self.assertFalse(exist_2)

    def test_delete_reply(self):
        """
        Test delete a reply.
        The tweet still exist.
        """
        # Create a tweet
        payload_1 = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**payload_1)

        # Create a reply
        payload_2 = {
            'text': 'A sample reply',
            'author': self.second_user,
            'replying_to': tweet
        }
        reply = Tweet.objects.create(**payload_2)

        # Delete the reply
        reply.delete()

        # Expect the tweet does not have reply
        exist_1 = tweet.replies.filter(id=reply.id).exists()
        self.assertFalse(exist_1)

        # Expect the second_user does not have the reply
        exist_2 = self.second_user.tweets().filter(id=reply.id).exists()
        self.assertFalse(exist_2)

    def test_delete_a_tweet(self):
        """
        Test delete a tweet.
        All replies are delete as well.
        """
        # Create a tweet
        payload_1 = {
            'text': 'A sample tweet',
            'author': self.first_user
        }
        tweet = Tweet.objects.create(**payload_1)

        # Create a reply
        payload_2 = {
            'text': 'A sample reply',
            'author': self.second_user,
            'replying_to': tweet
        }
        reply = Tweet.objects.create(**payload_2)

        # Delete a tweet
        tweet.delete()

        # Expect the tweet does not exist
        exist_1 = Tweet.objects.filter(id=tweet.id).exists()
        self.assertFalse(exist_1)

        # Expect the first_user does not have this tweet
        exist_2 = self.first_user.tweets().filter(id=tweet.id).exists()
        self.assertFalse(exist_2)

        # Expect the reply is remove as well
        exist_3 = Tweet.objects.filter(id=reply.id).exists()
        self.assertFalse(exist_3)

        # Expect the second_user does not have reply
        exist_4 = self.second_user.tweets().filter(id=reply.id).exists()
        self.assertFalse(exist_4)
