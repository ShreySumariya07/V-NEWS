from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import fields, serializers
from .models import SavedNews


class SavedNewsShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedNews
        fields = '__all__'


class SavedNewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedNews
        fields = ["abstract", "web_url",
                  "image_url", "title", "published_date"]

    def create(self, validated_data):
        return SavedNews.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "email",
                  "first_name", "last_name", "password"]

    def create(self, validated_data):
        # pass1 = validated_data['password1']
        # pass2 = validated_data["password2"]
        # if pass1 == pass2:
        #     raise serializers.ValidationError({"password":"password does not match!"})
        user = User.objects.create(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            password=self.validated_data["password"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"]
        )
        user.save()
        return user

# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(write_only=True)
#     password = serializers.CharField(write_only=True)
