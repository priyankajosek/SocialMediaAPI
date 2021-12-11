from rest_framework import serializers
from .models import  Follow, Post, Like, Comment
from django.contrib.auth.models import User


class PostSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
        max_length=65, min_length=8)
    desc = serializers.CharField(
        max_length=65, min_length=8)
        
    class Meta:
        model = Post
        fields = ['id','title','desc','date_created']


class PostViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id','title','desc','like_count', 'all_comments','date_created']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['id']


class CommentSerializer(serializers.ModelSerializer):

    content = serializers.CharField(
        max_length= 255, min_length = 2, write_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content']

class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['id']