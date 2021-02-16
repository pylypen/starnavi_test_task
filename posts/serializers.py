from rest_framework import serializers
from .models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    """
    Post Serializer
    """
    user = serializers.ReadOnlyField(source='user.first_name')
    user_id = serializers.ReadOnlyField(source='user.id')
    likes = serializers.SerializerMethodField()

    class Meta(object):
        model = Post
        fields = ('id', 'title', 'description', 'user', 'user_id', 'created', 'likes')

    def get_likes(self, post):
        return Like.objects.filter(post=post).count()


class LikeSerializer(serializers.ModelSerializer):
    """
    Like Serializer
    """
    class Meta:
        model = Like
        fields = ['id']
