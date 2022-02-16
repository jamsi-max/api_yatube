from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from posts.models import Comment, Group, Post
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class IfUserIsAuthor(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author != request.user:
            return False
        return True


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IfUserIsAuthor]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IfUserIsAuthor]

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        new_queryset = post.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)
