from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
#from django.contrib.auth.models import User, Group

from blog.models import Blog
from .serializers import BlogSerializer
#from rest_framework.response import Response
#from django.http import JsonResponse
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
