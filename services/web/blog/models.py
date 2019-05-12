# Create your models here.
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

class ApprovalStatus(Enum):   # A subclass of Enum
    AP = "Approved"
    PE = "Pending"
    RE = "Rejected"

# a post must belong to a category and a category must belong to a blog a post can belong to multiple categories
# Lets assume there is a blog called PYTHON, this can have several categories, coding standards, pythonic coding, djang
# flask, bottle, wsgi etc
# post can be associated with 1 or more categories, w

#top level of navigation
class Category(models.Model):
    title = models.CharField(max_length=255,unique=True, blank=False, null=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return "{} - {}".format(self.title, self.created_by, self.created_at)

class Post(models.Model):
    # post title
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null = False, max_length=12000)
    slug = models.CharField(max_length=255, null=False, unique=True)
    short_description = models.TextField(null = False, max_length=1500)
    categories = models.ManyToManyField(Category, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='+')
    total_comments = models.IntegerField(null=False, blank=False, default=0)
    comments = models.ManyToManyField(Category,blank=False,null=False, related_name='comments')


    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("total_comments", "created_at",)
    def __str__(self):
        return "{} - {}".format(self.title, self.short_description, self.slug, self.created_by)

class Comment(models.Model):
    content = models.TextField(null = False, blank=False, max_length=1000)
    status = models.CharField(
      max_length=5,
      choices=[(tag, tag.value) for tag in ApprovalStatus]  # Choices is a list of Tuple
    )
    #post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ("status", "created_at",)

    def __str__(self):
        return "{} - {}".format(self.content, self.status, self.created_by, self.created_at)
