"""
URL configuration for whu_raid project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app.view import RegisterView,LoginView,UserView,TeamView,EnterTeamView,QuitTeamView,ReserveStartTimeView,StartTimeView,EndTimeView,PositionView
urlpatterns = [
    path('v6/register',RegisterView.as_view({'post':'create'})),
    path('v6/login',LoginView.as_view()),
    path('v6/user',UserView.as_view({'get':'list'})),
    path('v6/user/<int:pk>',UserView.as_view({'get':'retrieve','delete':'destroy'})),
    path('v6/team',TeamView.as_view({'get':'list','post':'create'})),
    path('v6/team/<int:pk>',TeamView.as_view({'get':'retrieve','delete':'destroy'})),
    path('v6/enter_team',EnterTeamView.as_view()),
    path('v6/quit_team/<int:pk>',QuitTeamView.as_view({'put':'partial_update'})),
    path('v6/reserve_start_time',ReserveStartTimeView.as_view({'get':'list'})),
    path('v6/reserve_start_time/<int:pk>',ReserveStartTimeView.as_view({'get':'retrieve','put':'update'})),
    path('v6/start_time',StartTimeView.as_view({'get':'list'})),
    path('v6/start_time/<int:pk>',StartTimeView.as_view({'get':'list','put':'update'})),
    path('v6/end_time',EndTimeView.as_view({'get':'list'})),
    path('v6/end_time/<int:pk>',EndTimeView.as_view({'get':'list','put':'update'})),
    path('v6/position',PositionView.as_view({'get':'list'})),
    path('v6/position/<int:pk>',PositionView.as_view({'get':'retrieve','put':'update'})),
]
