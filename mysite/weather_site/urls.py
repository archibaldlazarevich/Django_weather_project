from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import signup_view, weather_view, init_view, login_view

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('', init_view, name='init'),
    path('data/', weather_view, name='weather_data'),
    path('login', login_view, name= 'login'),
    path('logout/', LogoutView.as_view(next_page='init'), name='logout'),
]
