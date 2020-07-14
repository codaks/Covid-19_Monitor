from . import views
from django.urls import include,path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('dashboard', views.dashboard, name = "dashboard"),
    path('dashboard/register', views.register, name = "register"),
    path('dashboard/patients', views.patientList, name = "patientList"),
    path('dashboard/profile', views.search, name = "search"),
    path('dashboard/<int:question_id>/profile/X_rayAnalyzier', views.x_rayAnaluzier, name = "x_rayAnaluzier"),
    path('dashboard/<int:question_id>/profile', views.profile, name = "profile"),
    path('dashboard/logout', views.logout, name = "logout"),
    path('dashboard/<int:question_id>/recovered', views.recovered, name = "recovered"),
    path('dashboard/<int:question_id>/dead', views.dead, name = "dead"),
]

