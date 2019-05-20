# Create your models here.
from django.shortcuts import render
from django.db import models
from django.contrib.auth.models import User
from enum import Enum
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from blog.api.modelmanager import PostManager, CategoryManager, CommentManager
#https://django.cowhite.com/blog/dynamic-fields-in-django-rest-framwork-serializers/
#https://medium.com/@MicroPyramid/django-model-managers-and-properties-564ef668a04c

class ObjectStatus(Enum):   # A subclass of Enum
    #https://hackernoon.com/using-enum-as-model-field-choice-in-django-92d8b97aaa63
    AP = "Approved"
    PE = "Pending"
    RE = "Rejected"
    DR = "Draft"

###
# To avoid repetition of commonly used fields , a child model can inherit from this model
###
class TrackTimeObject(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)

###
# To avoid repetition of commonly used fields , a child model can inherit from this model
###
class TrackUserObject(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, blank=True, related_name='+')

    class Meta:
        abstract = True
        ordering = ('-created_by',)

class Tag(TrackTimeObject):
    title = models.CharField(max_length=100,unique=True, blank=False, null=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = []

# a post must belong to a category and a category must belong to a blog a post can belong to multiple categories
# Lets assume there is a blog called PYTHON, this can have several categories, coding standards, pythonic coding, djang
# flask, bottle, wsgi etc
# post can be associated with 1 or more categories, w

#top level of navigation
###
#  Post and Category share a bidirectional relationship for post-Categories
# i.e a post can belong to multiple categories and category can have many posts
###
class Category(TrackTimeObject):
    title = models.CharField(max_length=100,unique=True, blank=False, null=False)
    #last_updated = models.DateTimeField(auto_now_add=True)
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(null=True)
    #updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='+')
    objects = CategoryManager()      # The Custom Manager.

    def __str__(self):
        return "{} - {}".format(self.title,  self.created_at)

###
#  Post and Category share a bidirectional relationship for post-Categories
# i.e a post can belong to multiple categories and category can have many posts
# inherit from multiple tables
###
class Post(TrackTimeObject, TrackUserObject):
    # post title
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null = False, max_length=12000)
    slug = models.CharField(max_length=255, null=False, unique=True)
    #short_description = models.TextField(null = False, max_length=1500)
    #manytomany relationship between categories and posts
    categories = models.ManyToManyField(
        Category,
        related_name='posts'
    )
    #manytomany relationship between categories and posts
    tags = models.ManyToManyField(
        Tag,
        related_name='posts'
    )

    #tags = models.ManyToManyField(Tag)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(null=True)
    #comments = models.ManyToManyField(Comment,blank=False,null=False, related_name='comments')
    #status is an enum field, see how the default value is set as draft using Status.DR
    pstatus = models.CharField(
      max_length=5,
      choices=[(tag.name, tag.value) for tag in ObjectStatus],  # Choices is a list of Tuple
      default=ObjectStatus.DR
    )

    objects = PostManager()      # The Custom Manager.


    @property
    def comments(self):
        return self.comment_set.all()

    @property
    def short_description(self):
        return self.content

    @property
    def total_comments(self):
        return self.comments.filter(cstatus='AP').count()

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ("created_at",)
    def __str__(self):
        return "{} - {}".format(self.id, self.title, self.total_comments, self.created_by)

###
#  A comment can belong to one post only
# a Post can have multiple comments
# inherit from multiple abstract models
##
class Comment(TrackTimeObject, TrackUserObject):
    content = models.TextField(null = False, blank=False, max_length=1000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    cstatus = models.CharField(
      max_length=5,
      choices=[(tag.name, tag.value) for tag in ObjectStatus],  # Choices is a list of Tuple
      default=ObjectStatus.PE
    )
    #post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='comments')
    #created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(null=True)
    #updated_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='+')
    objects = CommentManager() #<-- custom query manager

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ("cstatus", "created_at",)

    def __str__(self):
        return "{} - {}".format(self.content, self.cstatus, self.created_by, self.created_at)

###
#  pivot table for manytomany between posts and categories and vice versa
# because a post can belong to many categories, and a category can have many posts
###
class PostCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

###
#  pivot table for manytomany between posts and tags and vice versa
# because a post can belong to many tags, and a tag can have many posts
###
class PostTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
