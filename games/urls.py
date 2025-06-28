from django.urls import path
from . import views


urlpatterns = [
    path('get-settings', views.get_settings, name='getset'),
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('about/<str:game_tli>', views.about, name='about'),
    path('make-adw', views.make_adw, name='make-adw'),
    path('get-players', views.get_players, name='getpl'),
    path('join', views.join, name='join'),
    path('pregame<int:code>', views.pregame, name='pregame'),
    path('begin', views.begin, name='begin'),
    path('game<int:code>', views.play, name='play'),
    path('adw-game<int:code>', views.play_adw, name='play-adw'),
    path('get-state-adw', views.get_state_adw, name='gs-adw'),
    ]
