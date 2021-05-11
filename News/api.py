
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.authentication import TokenAuthentication
from . import serializers
from django.contrib.auth.models import auth, User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .models import SavedNews
from News.serializers import SavedNewsSerializer, RegisterSerializer, SavedNewsShowSerializer
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404


class Register(APIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user).key
            data = {"response": "user created successfully", "token": token}
        else:
            data = serializer.errors
        return Response(data)

# class Login(APIView):
#     serializer_class = LoginSerializer
#     permission_classes = [permissions.AllowAny]
#
#     def post(self,request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         context = {}
#         username = serializer.validated_data["username"]
#         pass1 = serializer.validated_data["password"]
#         account = auth.authenticate(username = username ,password = pass1)
#         if account:
#             try:
#                 token = Token.objects.get(user = account)
#             except Token.DoesNotExist:
#                 token = Token.obejcts.create(user=account)
#             context["token"] = token.key
#         else:
#             context["response"] = "errors"
#             context["error_message"] = "Invalid credentials"
#         return Response(context)


class Login(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        context = {}
        try:
            username = request.data.get("username")
            password = request.data.get("password")
            print(username, password)
            us_db = User.objects.filter(username=username)
            print(us_db)
            if not us_db:
                data = {"user_id": "not registered", "login_type": "signup"}
                return Response(data, status=status.HTTP_200_OK)

            else:
                user = auth.authenticate(username=username, password=password)
                print(user)
                if user is not None:
                    try:
                        token = Token.objects.get(user=user)
                    except Token.DoesNotExist:
                        token = Token.objects.create(user=user)
                    context["token"] = token.key
                else:
                    context["response"] = "erros"
                    context["error_message"] = "Invalid Credentials"
                return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class savednews(APIView):
    serializer_class = SavedNewsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        saved_news = SavedNews.objects.filter(us_id=self.request.user.pk)
        serializer = serializers.SavedNewsShowSerializer(saved_news, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.SavedNewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_queryset(self):
#         return SavedNews.objects.filter(us_id = self.request.user.pk).all()


class savednewsdetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, article_id):
        try:
            saved_news = SavedNews.objects.get(
                us_id=self.request.user.pk, pk=article_id)
        except SavedNews.DoesNotExist:
            raise Http404
        serializer = serializers.SavedNewsShowSerializer(saved_news)
        return Response(serializer.data)

    def put(self, request,  article_id):
        try:
            save_news = SavedNews.objects.get(
                us_id=self.request.user.pk, pk=article_id)
        except SavedNews.DoesNotExist:
            raise Http404
        serializer = serializers.SavedNewsSerializer(
            save_news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, article_id):
        try:
            save_news = SavedNews.objects.get(
                us_id=self.request.user.pk, pk=article_id)
        except SavedNews.DoesNotExist:
            raise Http404
        save_news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
