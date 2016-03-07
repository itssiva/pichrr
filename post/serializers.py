from rest_framework import serializers
from .models import Post, Vote, Favorite, User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('ref_id', 'title', 'txt_tags', 'likes', 'comments', 'user')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields =('post', )


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields =('post', )


