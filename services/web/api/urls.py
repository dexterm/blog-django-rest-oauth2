#from django.conf.urls import url, include
from django.urls import path, include
from rest_framework import routers
from blog.api.viewsets import PostViewSet, CommentViewSet, CategoryViewSet
from users.api.viewsets import ProfileViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('blogs', PostViewSet)
router.register('categories', CategoryViewSet)
router.register('comments', CommentViewSet)
router.register('users', UserViewSet)
router.register('profile', ProfileViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('admin/', include('rest_framework.urls')),
]
