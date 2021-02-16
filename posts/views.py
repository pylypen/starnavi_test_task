from rest_framework import permissions, status
from rest_framework.generics import (CreateAPIView, ListCreateAPIView)
from rest_framework.mixins import DestroyModelMixin
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post, Like
from .serializers import PostSerializer, LikeSerializer


class PostList(ListCreateAPIView):
    """
    Create Post View
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Create Post
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LikeCreate(CreateAPIView, DestroyModelMixin):
    """
    Like and Unlike Post View
    """
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Like.objects.filter(user=user, post=post)

    # Like Post
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

    # Unlike Post
    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You never liked for this post...silly!')
