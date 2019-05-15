from rest_framework import serializers
from django.contrib.auth.models import User, Group

from tips.models import Tip


class TipSerializer(serializers.ModelSerializer):
    author = serializers.RelatedField(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')


    class Meta:
        model = Tip
        fields = ('tip', 'code', 'link', 'author', 'approved', 'share_link', 'user')


class UserSerializera(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'date_joined', 'password')
