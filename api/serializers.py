from rest_framework import serializers
from .models import Tag, Category, Item
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id','tag']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category']


class ItemSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    class Meta:
        model = Item
        fields = ['id','sku','name','category', 'tags', 'in_stock', 'available_stock']

    def create(self, validated_data):
        # Pop tags data from the validated data since it's a many-to-many field
        tags_data = validated_data.pop('tags', None)
        
        # Create the Item instance
        item = Item.objects.create(**validated_data)

        # If tags were provided, set them for the item
        if tags_data is not None:
            item.tags.set(tags_data)

        return item
    
class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','email','username', 'password', 'password2']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            print("user already exist")
            raise serializers.ValidationError("A user with that username already exists")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields didn't match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()
        return user