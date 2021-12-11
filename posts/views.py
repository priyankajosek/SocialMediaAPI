from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from .models import Post, Like, Follow, Comment
from .serializers import PostSerializer, LikeSerializer, CommentSerializer, FollowSerializer, PostViewSerializer
from rest_framework import permissions, status
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import HttpResponse
from django.core.paginator import Paginator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class UserDetailView(APIView):
   
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        user=request.user
        username= user.username
        follower_count = user.followers.all().count()
        followings_count = Follow.objects.filter(follower=user).count()
        data ={
            "username":username,
            "follower_count": follower_count,
            "followings_count": followings_count
        }
        return Response(data)


class PostAPIView(APIView):

    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
   
    def get(self, request):

    # Pagination
        p = Paginator(Post.objects.filter(owner=request.user), 10)
        page = request.GET.get('page')
        posts = p.get_page(page)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # Swagger request body documentation
    @swagger_auto_schema(
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['title','desc'],
                             properties={
                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                 'desc': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),
                         operation_description='Add a post')

    def post(self, request):
        # 
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):

    serializer_class = PostViewSerializer
    permission_classes = (permissions.IsAuthenticated,)
        
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return -1

    def get(self, request,pk):

        post = self.get_object(pk)
        
        if post == -1:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostViewSerializer(post)
        return Response(serializer.data)

    @swagger_auto_schema(
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['title','desc'],
                             properties={
                                 'title': openapi.Schema(type=openapi.TYPE_STRING),
                                 'desc': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),
                         operation_description='Modify a post')
    def put(self, request,pk):

        post = self.get_object(pk)
       
        if post == -1:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request,pk):

        post = self.get_object(pk)
        
        if post == -1:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeAPIView(APIView):

    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, pk):
        serializer = LikeSerializer(data=request.data)
        
        try:
            post = Post.objects.get(pk=pk)
            like = Like.objects.filter(post=post,liked_by=request.user).first()
            if like is None:
                if serializer.is_valid():
                    serializer.save(liked_by=request.user,post=post)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_304_NOT_MODIFIED)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        
class UnlikeAPIView(APIView):

    serializer_class = LikeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        
        try:
            post =  Post.objects.get(pk=pk)
        
            like = Like.objects.get(liked_by=request.user,post=post)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            
        except Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentAPIView(APIView):

    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # Swagger documentation
    @swagger_auto_schema(
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             required=['content'],
                             properties={
                                 'content': openapi.Schema(type=openapi.TYPE_STRING),
                                                              },
                         ),
                         operation_description='Add a comment')
    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save(comment_by=request.user,post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowAPIView(APIView):

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, pk):
        serializer = FollowSerializer(data=request.data)
        try:
            user = User.objects.get(pk=pk)
            follow = Follow.objects.filter(user=user, follower=request.user).first()
            if follow is None:
                if serializer.is_valid():
                    serializer.save(user=user,follower=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_304_NOT_MODIFIED)

        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        

class UnfollowAPIView(APIView):

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, pk):
        
        try:
            user = User.objects.get(pk=pk)
       
        
            follow = Follow.objects.filter(user=user, follower=request.user).first()
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except User.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        except Follow.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)
