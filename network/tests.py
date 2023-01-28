from django.test import TestCase

from .models import User, Post
# Create your tests here.

class PostTestCase(TestCase):
    def setUp(self):
        user1 = User(username='a1', email='random@gmail.com', password='abcdefgh')
        user2 = User(username='a2', email='random1@gmail.com', password='abcdefgh')
        user1.save()
        user2.save()

        post1 = Post(user=user1, text='hi')
        post2 = Post(user=user2 , text='hi1')
        post1.save()
        post2.save()

    def test_like(self):
        user2 = User.objects.get(username='a2')

        post1 = Post.objects.get(pk=1)

        user2.like_dislike(post1)

        self.assertEqual(post1.likes, 1)


        user2.like_dislike(post1)

        self.assertEqual(post1.likes, 0)

    def test_follow(self):
        user2 = User.objects.get(username='a2')
        user1 = User.objects.get(username='a1')
        user1.follow_unfollow(user2)
        self.assertTrue(user1.follows(user2))
        self.assertEqual(user1.following.all().first(), user2)
    
        user1.follow_unfollow(user2)
        self.assertEqual(user1.following.all().count(), 0)
        self.assertFalse(user1.follows(user2))
        self.assertFalse(user2.follows(user1))

