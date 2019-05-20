from rest_framework import serializers
from django.contrib.auth.models import User, Group

from users.models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    #https://github.com/guidocecilio/django-restframework-userprofile/blob/master/src/api/serializers.py
    user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    user = serializers.ReadOnlyField(source='user.id')
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = Profile
        depth = 1
        fields = ('url', 'id', 'username', 'email', 'first_name', 'last_name',
                  'user', 'user_url')

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        # retrieve the User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        # retrieve Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile_url = serializers.HyperlinkedIdentityField(
        view_name='profile-detail')
    class Meta:
        model = User
        #depth = 1
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email',
                    'profile_url')
