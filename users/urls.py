from . import views
from django.urls import include,path

urlpatterns = [
    path('', views.home, name = "home"),
    path('user', views.user, name = "user"),
    path('register', views.register, name = "register"),
]
