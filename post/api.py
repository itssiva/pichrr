from .models import Post, Vote, Favorite, User
from .serializers import PostSerializer, LikeSerializer, FavoriteSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from itertools import chain
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]



class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(active=True)
    serializer_class = PostSerializer



class LikeList(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        print "user is", self.request.user
        return Vote.objects.filter(user= self.request.user)

    serializer_class = LikeSerializer

class FavoriteList(generics.ListCreateAPIView):

    def get_queryset(self):
        return Favorite.objects.filter(user= self.request.user)
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

