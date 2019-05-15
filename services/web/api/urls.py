#from django.conf.urls import url, include
from django.urls import path, include
from rest_framework import routers
from blog.api.viewsets import PostViewSet
from users.api.viewsets import ProfileViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('blogs', PostViewSet)
router.register('users', UserViewSet)
router.register('profile', ProfileViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('admin/', include('rest_framework.urls')),
]
