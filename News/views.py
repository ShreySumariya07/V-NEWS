from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from django.contrib.auth.models import *
from rest_framework.decorators import api_view

from rest_framework.renderers import TemplateHTMLRenderer
from News.models import SavedNews
from News.serializers import  SavedNewsSerializer
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser,FormParser,MultiPartParser,JSONParser
from django.http import Http404

# Create your views here.


# def index(request):
#     return render(request,"index.html")

l=[]
counter_id = 0


def home(request):
    response = requests.get("https://api.nytimes.com/svc/topstories/v2/world.json?api-key=AxJegn8UbsHdFMNGJYedGyrkdqgf8G4h")
    result = response.json()
    res = result['results']
    global l
    global counter_id
    for rest in res:
        title = rest["title"]
        abstract = rest["abstract"]
        web_url = rest["url"]
        image = rest["multimedia"]
        if not image :
            image_url = None
        else:
            image_url = image[0]["url"]
        pub_date = rest["published_date"]
        context = {
            'id':counter_id,
            'abstract':abstract,
            'web_url': web_url,
            'image_url':image_url,
            'headline':title,
            'pub_date':pub_date,
        }
        l.append(context)
        counter_id = counter_id + 1
    return render(request,"display_news.html",{'l':l})

def home1(request,id):
    user = User.objects.get(id=id)
    response = requests.get("https://api.nytimes.com/svc/topstories/v2/world.json?api-key=AxJegn8UbsHdFMNGJYedGyrkdqgf8G4h")
    result = response.json()
    res = result['results']
    global l
    global counter_id
    for rest in res:
        title = rest["title"]
        abstract = rest["abstract"]
        web_url = rest["url"]
        image = rest["multimedia"]
        if not image :
            image_url = None
        else:
            image_url = image[0]["url"]
        pub_date = rest["published_date"]
        context = {
            'id':counter_id,
            'abstract':abstract,
            'web_url': web_url,
            'image_url':image_url,
            'headline':title,
            'pub_date':pub_date,
        }
        l.append(context)
        counter_id = counter_id + 1
    return render(request,"display_news.html",{'l':l,'user':user})

def login(request):
    return render(request,"login.html")


def register(request):
    return render(request,"register.html")

def logout(request):
    liste = l
    return render(request,"display_news.html",{'l':liste})

def login_confirm(request):
    liste = l
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            return render(request,"display_news.html",{'user':user,'l':liste})
        else:
            messages.info(request,"Invalid credentials")
            return redirect("News:login")
    else:
        messages.info(request,"Invalid method of request")
        return redirect("News:login")


def register_confirm(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"email taken")
                return redirect("News:register")
            else:
                user = User.objects.create_user(username=username,email=email,password=password1,first_name=first_name,last_name=last_name)
                user.save()
                return redirect("News:login")
        else:
            messages.info(request,"Password not same")
            return redirect("News:register")

    else:
        messages.info(request,"Inavlid Method")
        return redirect("News:register")

def saved_articles(request,id):
    saved = SavedNews.objects.filter(us_id=id)
    print(saved)
    user = User.objects.get(id=id)
    return render(request,"saved_articles.html",{"user":user,"saved":saved})

def save(request, id, user_id):
    lis = l
    liste = l[int(id)]
    if user_id == "None":
        return redirect("News:login")
    else:
        # users = User.objects.filter(id=user_id)
        # print(users)
        # save_news = SavedNews.objects.filter(user=users.id)
        user_x = User.objects.get(id=user_id)
        users = User.objects.only("id").get(id=user_id)
        savenews = SavedNews.objects.create(us_id=users,abstract=liste["abstract"],web_url=liste["web_url"],image_url=liste["image_url"],title=liste["headline"],published_date=liste["pub_date"])
        messages.info(request,"saved successfully")
        return render(request,"display_news.html",{"user":user_x,"l":lis})

def delete(request, id, user_id):
    if user_id == "None":
        return redirect("News:login")
    else:
        delete_news = SavedNews.objects.get(id=id)
        print(delete_news)
        delete_news.delete()
        saved_y = SavedNews.objects.filter(us_id=user_id)
        user_y = User.objects.get(id=user_id)
        return render(request, "saved_articles.html", {"user": user_y, "saved": saved_y})