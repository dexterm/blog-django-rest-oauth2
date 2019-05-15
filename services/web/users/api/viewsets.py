from django.http import HttpResponse
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from users.models import Profile
#from blog.serializers import PostSerializer
from .serializers import UserSerializer, ProfileSerializer
from api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework import generics, permissions, viewsets
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from api.permissions import (
    IsOwnerOrReadOnly, IsAdminUserOrReadOnly, IsSameUserAllowEditionOrReadOnly
)

def index(request):
    return HttpResponse("If you stumbled on this page, please use api to access this feature.")



class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSameUserAllowEditionOrReadOnly, TokenHasReadWriteScope)

#API CALL TO RETURN LOGGED IN USER PROFILE
class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that returns logged in user profile.
    """
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #queryset = User.objects.all().order_by('-date_joined')


    def retrieve(self, request, *args, **kwargs):
        """
        If provided 'pk' is "me" then return the current user.
        """
        if kwargs.get('pk') == 'me':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, args, kwargs)

    #def get_profile(self, request, *args, **kwargs):
    #    permission_classes = (IsAuthenticated,)
    #    serializer_class = UserProfileSerializer
    #    if kwargs.get('pk') == 'me':
    #                queryset = Item.objects.all().filter(user=request.user)
