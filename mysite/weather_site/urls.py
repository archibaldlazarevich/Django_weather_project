from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import signup_view, init_view, login_view, weather_data_view, WeatherView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('', init_view, name='init'),
    path('login/', login_view, name= 'login'),
    path('logout/', LogoutView.as_view(next_page='init'), name='logout'),
    path('weather_data/', weather_data_view, name='weather_data'),
    path('weather_forecast/', WeatherView.as_view(), name='weather_forecast'),
]
