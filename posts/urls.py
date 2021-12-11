from django.urls import path
from .views import PostAPIView, PostDetailView, LikeAPIView, UnlikeAPIView, CommentAPIView, FollowAPIView, UnfollowAPIView, UserDetailView

urlpatterns = [
    path('user/', UserDetailView.as_view()),
    path('posts/', PostAPIView.as_view()),
    path('posts/<int:pk>', PostDetailView.as_view()),
    path('like/<int:pk>', LikeAPIView.as_view()),
    path('unlike/<int:pk>', UnlikeAPIView.as_view()),
    path('follow/<int:pk>', FollowAPIView.as_view()),
    path('unfollow/<int:pk>', UnfollowAPIView.as_view()),
    path('comment/<int:pk>', CommentAPIView.as_view())
    
]
