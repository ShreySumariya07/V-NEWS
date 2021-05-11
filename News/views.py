from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.authentication import TokenAuthentication
from . import serializers
import requests
from django.contrib.auth.models import auth, User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .models import SavedNews
from News.serializers import SavedNewsSerializer, RegisterSerializer
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404

# Create your views here.


# def index(request):
#     return render(request,"index.html")

l = []
counter_id = 0
global_case = {}
india_case = {}


def home(request):
    global global_case, india_case
    respon = requests.get("https://api.covid19api.com/summary")
    response2 = respon.json()
    global_case = response2["Global"]
    new_confirmed = global_case["NewConfirmed"]
    total_confirm = global_case["TotalConfirmed"]
    new_deaths = global_case["NewDeaths"]
    total_death = global_case["TotalDeaths"]
    new_recovered = global_case["NewRecovered"]
    total_recovered = global_case["TotalRecovered"]

    country = response2["Countries"]
    for count in country:
        if count["Country"] == "India":
            global new_confirmed_india, total_confirm_india, new_deaths_india, total_death_india, new_recovered_india, total_recovered_india
            new_confirmed_india = count["NewConfirmed"]
            total_confirm_india = count["TotalConfirmed"]
            new_deaths_india = count["NewDeaths"]
            total_death_india = count["TotalDeaths"]
            new_recovered_india = count["NewRecovered"]
            total_recovered_india = count["TotalRecovered"]
        else:
            continue

    global_case = {
        "new_confirmed": new_confirmed,
        "total_confirm": total_confirm,
        "new_deaths": new_deaths,
        "total_death": total_death,
        "new_recovered": new_recovered,
        "total_recovered": total_recovered,
    }

    india_case = {
        "new_confirmed_india": new_confirmed_india,
        "total_confirm_india": total_confirm_india,
        "new_deaths_india": new_deaths_india,
        "total_death_india": total_death_india,
        "new_recovered_india": new_recovered_india,
        "total_recovered_india": total_recovered_india,
    }

    print(global_case)
    print(india_case)

    response = requests.get(
        "https://api.nytimes.com/svc/topstories/v2/world.json?api-key=AxJegn8UbsHdFMNGJYedGyrkdqgf8G4h")
    result = response.json()
    res = result['results']
    global l
    global counter_id
    for rest in res:
        title = rest["title"]
        abstract = rest["abstract"]
        web_url = rest["url"]
        image = rest["multimedia"]
        if not image:
            image_url = None
        else:
            image_url = image[0]["url"]
        pub_date = rest["published_date"]
        context = {
            'id': counter_id,
            'abstract': abstract,
            'web_url': web_url,
            'image_url': image_url,
            'headline': title,
            'pub_date': pub_date,
        }
        l.append(context)
        counter_id = counter_id + 1
    return render(request, "display_news.html", {'l': l, "global_case": global_case, "india_case": india_case})


def home1(request, id):
    user = User.objects.get(id=id)

    respon = requests.get("https://api.covid19api.com/summary")
    response2 = respon.json()
    global_case = response2["Global"]
    new_confirmed = global_case["NewConfirmed"]
    total_confirm = global_case["TotalConfirmed"]
    new_deaths = global_case["NewDeaths"]
    total_death = global_case["TotalDeaths"]
    new_recovered = global_case["NewRecovered"]
    total_recovered = global_case["TotalRecovered"]

    country = response2["Countries"]
    for count in country:
        if count["Country"] == "India":
            global new_confirmed_india, total_confirm_india, new_deaths_india, total_death_india, new_recovered_india, total_recovered_india
            new_confirmed_india = count["NewConfirmed"]
            total_confirm_india = count["TotalConfirmed"]
            new_deaths_india = count["NewDeaths"]
            total_death_india = count["TotalDeaths"]
            new_recovered_india = count["NewRecovered"]
            total_recovered_india = count["TotalRecovered"]
        else:
            continue

    global_case = {
        "new_confirmed": new_confirmed,
        "total_confirm": total_confirm,
        "new_deaths": new_deaths,
        "total_death": total_death,
        "new_recovered": new_recovered,
        "total_recovered": total_recovered,
    }

    india_case = {
        "new_confirmed_india": new_confirmed_india,
        "total_confirm_india": total_confirm_india,
        "new_deaths_india": new_deaths_india,
        "total_death_india": total_death_india,
        "new_recovered_india": new_recovered_india,
        "total_recovered_india": total_recovered_india,
    }

    print(global_case)
    print(india_case)

    response = requests.get(
        "https://api.nytimes.com/svc/topstories/v2/world.json?api-key=AxJegn8UbsHdFMNGJYedGyrkdqgf8G4h")
    result = response.json()
    res = result['results']
    global l
    global counter_id
    for rest in res:
        title = rest["title"]
        abstract = rest["abstract"]
        web_url = rest["url"]
        image = rest["multimedia"]
        if not image:
            image_url = None
        else:
            image_url = image[0]["url"]
        pub_date = rest["published_date"]
        context = {
            'id': counter_id,
            'abstract': abstract,
            'web_url': web_url,
            'image_url': image_url,
            'headline': title,
            'pub_date': pub_date,
        }
        l.append(context)
        counter_id = counter_id + 1
    return render(request, "display_news.html", {'l': l, 'user': user, "global_case": global_case, "india_case": india_case})


def login(request):
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def logout(request):
    global_cs = global_case
    india_cs = india_case
    liste = l
    return render(request, "display_news.html", {'l': liste, "global_case": global_cs, "india_case": india_cs})


def login_confirm(request):
    global_c = global_case
    india_c = india_case
    liste = l
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            return render(request, "display_news.html", {'user': user, 'l': liste, "global_case": global_c, "india_case": india_c})
        else:
            messages.info(request, "Invalid credentials")
            return redirect("News:login")
    else:
        messages.info(request, "Invalid method of request")
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
                messages.info(request, "email taken")
                return redirect("News:register")
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                user.save()
                return redirect("News:login")
        else:
            messages.info(request, "Password not same")
            return redirect("News:register")

    else:
        messages.info(request, "Inavlid Method")
        return redirect("News:register")


def saved_articles(request, id):
    saved = SavedNews.objects.filter(us_id=id)
    print(saved)
    user = User.objects.get(id=id)
    return render(request, "saved_articles.html", {"user": user, "saved": saved})


def save(request, id, user_id):
    global_ca = global_case
    india_ca = india_case
    lis = l
    liste = l[int(id)]
    if user_id == "None":
        return redirect("News:login")
    else:
        user_x = User.objects.get(id=user_id)
        users = User.objects.only("id").get(id=user_id)
        savenews = SavedNews.objects.create(us_id=users, abstract=liste["abstract"], web_url=liste["web_url"],
                                            image_url=liste["image_url"], title=liste["headline"], published_date=liste["pub_date"])
        messages.info(request, "saved successfully")
        return render(request, "display_news.html", {"user": user_x, "l": lis, "global_case": global_ca, "india_case": india_ca})


def delete(request, id, user_id):
    if user_id == "None":
        return redirect("News:login")
    else:
        delete_news = SavedNews.objects.get(id=id)
        delete_news.delete()
        saved_y = SavedNews.objects.filter(us_id=user_id)
        user_y = User.objects.get(id=user_id)
        return render(request, "saved_articles.html", {"user": user_y, "saved": saved_y})
