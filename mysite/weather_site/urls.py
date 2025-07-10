from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    WeatherView,
    init_view,
    login_view,
    signup_view,
    weather_data_view,
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("", init_view, name="init"),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="init"), name="logout"),
    path("weather_data/", weather_data_view, name="weather_data"),
    path("weather_forecast/", WeatherView.as_view(), name="weather_forecast"),
]
