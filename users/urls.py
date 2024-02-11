from django.urls import path
from . import views

urlpatterns = [
    path('', views.frontpage, name="frontpage"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('home', views.home, name="home"),
    path('signout', views.signout, name="signout"),
    path('home/user/<str:username>', views.user, name="user"),
]