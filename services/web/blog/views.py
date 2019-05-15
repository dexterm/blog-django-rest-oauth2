from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from rest_framework import generics, permissions

from blog.models import Post
from .serializers import PostSerializer
#from rest_framework.response import Response
from django.http import JsonResponse
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
