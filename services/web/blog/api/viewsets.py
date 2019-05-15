from django.contrib.auth.models import User, Group
from api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import generics, permissions, viewsets
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

#models
from blog.models import Post
#serializers
from .serializers import PostSerializer

def home(request):
    """
    Display home page.
    """
    #return Response({'data': 'You must suffix api/<feature>'})
    return JsonResponse({'error': 'Some error'}, status=401)

class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-created_at')
