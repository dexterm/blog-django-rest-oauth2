from rest_framework import serializers
from django.contrib.auth.models import User, Group
#models
from blog.models import Post, Category, Comment


class PostSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.SerializerMethodField()
    #Instead of returning the integer id of the user that created the post, it will return the username
    def get_created_by(self, obj):
      return obj.created_by.username

    class Meta:
        model = Post
        fields = ('title', 'content', 'slug', 'short_description', 'created_at', 'created_by', 'total_comments')
