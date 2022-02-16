from rest_framework import serializers

from posts.models import Comment, Group, Post


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Post
        fields = ('id',
                  'text',
                  'author',
                  'image',
                  'group',
                  'pub_date',
                  )
        read_only_fields = ('author',)


class GroupSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='text'
    )

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description', 'posts')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'post')
