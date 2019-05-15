from rest_framework import serializers
from django.contrib.auth.models import User, Group
#models
from blog.models import Post, Category, Comment



class CategorySerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.SerializerMethodField()
    #Instead of returning the integer id of the user that created the post, it will return the username
    def get_created_by(self, obj):
      return obj.created_by.username

    class Meta:
        model = Category
        fields = ('title', 'created_by')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.SerializerMethodField()
    #Instead of returning the integer id of the user that created the post, it will return the username
    def get_created_by(self, obj):
      return obj.created_by.username

    class Meta:
        model = Comment
        fields = ('content','status', 'created_by', 'created_at', 'updated_at', 'status')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    #fetch data from users model and return them as fields in the Post model
    created_by = serializers.SerializerMethodField(source='created_by.username')
    user = serializers.ReadOnlyField(source='created_by.id')
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='created_by.username', read_only=True)
    email = serializers.CharField(source='created_by.email')
    first_name = serializers.CharField(source='created_by.first_name')
    last_name = serializers.CharField(source='created_by.last_name')

    #categories returns a list of api urls incase the user would like to modify the category title
    #categories field must exist in the Post model as manytomany relation
    categories = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=False,
        queryset=Category.objects.all(),
        view_name='category-detail'
    )

    #if you require the actual name of the category then link with CategorySerializer
    #cat field need not be preset in the Post model
    #result is: {post:{id,title,cat:[title:python],created_at}}
    cat = CategorySerializer(source="categories", read_only=True, many=True)

    #Instead of returning the integer id of the user that created the post, it will return the username
    def get_created_by(self, obj):
      return obj.created_by.username

    class Meta:
        model = Post
        #depth = 1
        fields = ('title', 'id', 'cat', 'content', 'user','username', 'email','first_name', 'last_name', 'slug', 'short_description', 'categories','created_at', 'created_by', 'total_comments', 'status')
