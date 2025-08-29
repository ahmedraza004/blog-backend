from rest_framework import serializers
from .models import User,Post,Comment,Category
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password


    
class registrationSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(required= True)
        password = serializers.CharField(write_only = True,validators =[validate_password])

        class Meta:
            model = User
            fields = ('username','email','password')
    
        def validate_email(self,value):
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError('user already exists')
            
            # validate_email[value]
            return value
        def create(self,validated_data):
            user = User(
                username= validated_data['username'],
                email = validated_data['email'],
            )
            user.set_password(validated_data['password'])
            user.is_active = True
            user.save()
            return user

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


# serializers.py
class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'author', 'created_at', 'likes_count', 'is_liked']
        read_only_fields = ['author']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()

    def create(self, validated_data):
        user = self.context['request'].user
        return Post.objects.create(author=user, **validated_data)

        