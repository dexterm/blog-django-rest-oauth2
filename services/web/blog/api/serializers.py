from rest_framework import serializers
from django.contrib.auth.models import User, Group
#serializers
from users.api.serializers import ProfileSerializer, UserSerializer
#models
from blog.models import Post, Category, Comment, Tag, ObjectStatus
#get logger
import logging
stdlogger = logging.getLogger(__name__)

###
#  associate categories with a post
#  this is to make the create function more readable
###
def assign_categories(post, categories):
    try:
        stdlogger.info("Assigin categories to a post")
        for item in categories:
            #always ensure the id attribute is passed
            stdlogger.info("Assigning item[{}] to a post".format( item['id']) )
            if not 'id' in item.keys():
                exp_str = "valid ID attribute is required format is {\"id\":1, \"title\":'something'}"
                stdlogger.exception(exp_str)
                raise Exception(exp_str)
            #also ensure that the id exists in the categories table
            if Category.objects.filter(id = item["id"] ).exists():
                cat = Category.objects.get(id= item["id"] )
                post.categories.add(cat)
    except Exception as e:
        raise


###
#  associate tags with a post
#  this is to make the create function more readable
###
def assign_tags(post, tags):

    stdlogger.info("Call to assign_tags")
    try:
        stdlogger.debug("Entering list of tags to be associated")
        for item in tags:
            stdlogger.info("Processing individual tags")
            #always ensure the id attribute is passed
            if not 'id' in item.keys():
                raise Exception("valid ID attribute is required")
            #also ensure that the id exists in the categories table
            if Tag.objects.filter(id = item["id"] ).exists():
                tag = Tag.objects.get(id= item["id"] )
                post.tags.add(tag)
    except Exception as e:
        stdlogger.exception(e)
        raise

class TagSerializer(serializers.ModelSerializer):
    class Meta:

        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    #created_by = serializers.SerializerMethodField()
    #Instead of returning the integer id of the user that created the post, it will return the username

    class Meta:
        model = Category
        fields = ('id','title',)
        depth=1

class CommentSerializer(serializers.ModelSerializer):
    #post = PostSerializer(many=False, read_only=True)
    post_id = serializers.IntegerField(write_only=True)
    #created_at = serializers.DateTimeField()
    #updated_at = serializers.DateTimeField()

    # automatically set created_by_id as the current user's id
    stdlogger.info("automatically set created_by_id as the current user's id")
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='created_by', write_only=True, required=False,
        default=serializers.CurrentUserDefault()
        )
    #Instead of returning the integer id of the user that created the post, it will return the username
    #def get_created_by(self, obj):
    #  return obj.created_by.username

    def get_post_id(self, obj):
        return post_id

    class Meta:
        model = Comment
        #fields = '__all__'
        fields = ('id', 'content', 'cstatus', 'created_at', 'post_id', 'created_by_id')


class PostSerializer(serializers.ModelSerializer):
    #fetch data from users model and return them as fields in the Post model
    #the below fields are present in the User model and are connected to the User model via get_created_by
    #created_by is a foreignkey relationship between Post and User model
    #get a sub array of user information by linking profile with UserSerializer
    stdlogger.info("associate post with a user model")
    profile = UserSerializer(read_only=True, source='created_by')
    #categories returns a list of api urls incase the user would like to modify the category title
    #categories field must exist in the Post model as manytomany relation
    stdlogger.info("associate post with multiple categories")
    categories = CategorySerializer( many=True)

    stdlogger.info("associate post with multiple comments")
    comments = CommentSerializer( many=True)

    stdlogger.info("Alter date format")
    created_at = serializers.DateTimeField( format="%Y-%m-%d %H:%M:%S" )
    updated_at = serializers.DateTimeField( format="%Y-%m-%d %H:%M:%S" )

    class Meta:
        model = Post
        #depth = 1
        #fields are a mix of fields present in Post , Categories, and User models
        fields = ('id', 'title', 'categories', 'slug', 'content', 'created_by', 'updated_by',
        'pstatus', 'created_at', 'updated_at','comments', 'profile', 'total_comments')
        #extra_kwargs = {'created_by_id': {'read_only':True}, 'updated_by_id': {'read_only':True} }

###
# PostCreateSerializer
# will be returned if method is POST or for create purpose only
###
class PostCreateSerializer(serializers.ModelSerializer):
    #because the categories is passed as an array of dictionaries and must be verified before insertint into db
    categories = serializers.ListField(write_only=True)

    #because the categories is passed as an array of dictionaries and must be verified before insertint into db
    tags = serializers.ListField(write_only=True)

    stdlogger.info("automatically set created_by_id as the current user's id")
    # automatically set created_by_id as the current user's id
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(), source='created_by', write_only=True, required=False,
        default = serializers.CurrentUserDefault()
        )

    #created_by = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    created_by = serializers.SerializerMethodField(read_only=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    #because all is passed for the fields , the categories property will not be automatically included
    #thats why the need for get_categories
    def get_categories(self, instance):
        return categories

    #because all is passed for the fields , the created_by_id property will not be automatically included
    #thats why the need for get_created_by_id
    def get_created_by_id(self, instance):
        return created_by_id

    def get_created_by(self, instance):
      return instance.created_by.username

    #because all is passed for the fields , the categories property will not be automatically included
    #thats why the need for get_tags
    def get_tags(self, instance):
        return tags

    ###
    #  overide the default create method because, there is dependency with categories
    # and comments table, django serializer will not automatically update the relationship
    # this must be done by the coder
    # @post method
    ###
    def create(self, validated_data):

        try:
            #if 'user' not in validated_data:
            #    validated_data['user'] = self.context['request'].user.id
            #    print("######!!!!!!!!!!!!!!!!!!", validated_data['user'])
            #before saving the post remove the field categories to avoid errors
            categories = validated_data.pop('categories')
            #before saving the post remove the field tags to avoid errors
            tags = validated_data.pop('tags')
            post = Post.objects.create(**validated_data)
            user = serializers.CurrentUserDefault()
            print("#######", user)
            assign_categories(post, categories) #<-- custom function to associate
            assign_tags(post, tags) #<-- custom function to associate

        except Exception as e:
            raise
        else:
            return post
