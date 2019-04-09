from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from django.utils.html import mark_safe
from markdown import markdown
import math

# Create your models here.

class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_topic_count(self):
        return Topic.objects.filter(board = self).count()

    def get_post_count(self):
        return Post.objects.filter(topic__board = self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board = self).order_by('-created_at').first()

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)

    views = models.PositiveIntegerField(default = 0) # new field for view count

    def __str__(self):
        return self.subject

    def get_reply_count(self):
        return Post.objects.filter(topic = self).count()

    def get_last_reply(self):
        return Post.objects.filter(topic = self).order_by('-created_at').first()

    def get_page_count(self):
        count = self.posts.count()
        pages = count / 5
        return math.ceil(pages)

class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        trunc_msg = Truncator(self.message)
        return trunc_msg.chars(30)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, safe_mode='escape'))
