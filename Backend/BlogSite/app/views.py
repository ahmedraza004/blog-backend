from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.response import Response
from .serializers import PostSerializer,registrationSerializer,CommentSerializer,CategorySerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from .models import Post,Comment,Category
from rest_framework.decorators import action
# Create your views here.

class RegisterView(generics.CreateAPIView):
    serializer_class = registrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('User is Register Successfully',status=status.HTTP_201_CREATED)
        raise serializers.ValidationError('Invalid credentials',status=status.HTTP_400_BAD_REQUEST)



    
class PostViewset(ModelViewSet):
    # views.py
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # ensure auth required

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'status': 'unliked'})
        else:
           post.likes.add(user)
           return Response({'status': 'liked'})
    
    

class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer

    
    def get_queryset(self):
            post_id = self.request.query_params.get('post')
            if post_id:
                return Comment.objects.filter(post_id=post_id)
            return Comment.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewset(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()



