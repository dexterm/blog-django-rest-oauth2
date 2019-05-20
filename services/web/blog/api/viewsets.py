from django.contrib.auth.models import User, Group
from api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics, permissions, viewsets
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

#models
from blog.models import Post, Category, Comment, Tag,  ObjectStatus
#serializers
from .serializers import PostSerializer, PostCreateSerializer, CategorySerializer, CommentSerializer, TagSerializer

def home(request):
    """
    Display home page.
    """
    #return Response({'data': 'You must suffix api/<feature>'})
    return JsonResponse({'error': 'Some error'}, status=401)


class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = TagSerializer
    queryset = Tag.objects.all().order_by('-title')


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    #authentication_classes = [OAuth2Authentication]
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created_at', 'pstatus')

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return  PostSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by('-created_at')


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    #permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-created_at', 'cstatus')
