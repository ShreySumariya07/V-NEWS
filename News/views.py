from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.authentication import TokenAuthentication

from . import serializers
import requests
from django.contrib.auth.models import auth, User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.renderers import TemplateHTMLRenderer
from News.models import SavedNews
from News.serializers import SavedNewsSerializer, RegisterSerializer
from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser, JSONParser
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


############################################## API ###################################################################

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
                # user_id = email_db.pk
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
        serializer = serializers.SavedNewsSerializer(saved_news, many=True)
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
    serializer_class = SavedNewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id, article_id):
        try:
            saved_news = SavedNews.objects.get(us_id=user_id, pk=article_id)
        except SavedNews.DoesNotExist:
            raise Http404
        serializer = serializers.SavedNewsSerializer(saved_news)
        return Response(serializer.data)

    def put(self, request, user_id, article_id):
        try:
            save_news = SavedNews.objects.get(us_id=user_id, pk=article_id)
        except SavedNews.DoesNotExist:
            raise Http404
        serializer = serializers.SavedNewsSerializer(
            save_news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)

    def delete(self, request, user_id, article_id):
        try:
            save_news = SavedNews.objects.get(us_id=user_id, pk=article_id)
        except SavedNews.DoesNotExist:
            raise Http404
        save_news.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
