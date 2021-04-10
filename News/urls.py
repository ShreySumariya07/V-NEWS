from django.conf.urls import url

from . import views
from django.urls import path,include

app_name = 'News'

urlpatterns = [
    # path("",views.index,name="index"),
    path("",views.home,name='home'),
    path("<int:id>/",views.home1,name="home1"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("register",views.register,name="register"),
    path("login_confirm",views.login_confirm,name="login_confirm"),
    path("register_confirm",views.register_confirm,name="register_confirm"),
    path("saved_articles/<int:id>/",views.saved_articles,name="saved_articles"),
    url(r'^save/(?P<id>\w+)/(?P<user_id>\w+)/$',views.save,name="save"),
    url(r'^delete/(?P<id>\w+)/(?P<user_id>\w+)/$',views.delete,name="delete"),

    # path('api-token-auth/', views.obtain_auth_token),
    path("register/",views.Register.as_view()),
    path("login/",views.Login.as_view()),
    path("save_news/",views.savednews.as_view()),
    path("save_news/<str:user_id/<str:article_id>/",views.savednewsdetail.as_view())
]