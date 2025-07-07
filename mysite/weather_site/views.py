import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from mysite import settings
from .models import WeatherData

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('weather_site/weather_data.html')
    else:
        form = UserCreationForm()
    return render(request, 'weather_site/signup.html', {'form': form})


def init_view(request):
    return render(request, 'weather_site/init.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('init')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'weather_site/login.html', {'form': form})


@login_required(login_url='signup')
def weather_view(request):
    city = request.GET.get('city')

    weather_current = None
    weather_forecast = None

    if city:
        # Проверяем, есть ли уже данные в БД
        try:
            weather_data = WeatherData.objects.get(city=city)
            weather_current = weather_data.current_weather
            weather_forecast = weather_data.forecast_5days
        except WeatherData.DoesNotExist:
            # Если нет — делаем запрос к OpenWeatherMap API
            api_key = settings.OPENWEATHER_API_KEY
            # Текущая погода
            url_current = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}&lang=ru"
            # Прогноз на 5 дней
            url_forecast = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}&lang=ru"

            resp_current = requests.get(url_current)
            resp_forecast = requests.get(url_forecast)

            if resp_current.status_code == 200 and resp_forecast.status_code == 200:
                weather_current = resp_current.json()
                weather_forecast = resp_forecast.json()

                WeatherData.objects.create(
                    city=city,
                    current_weather=weather_current,
                    forecast_5days=weather_forecast
                )
            else:
                weather_current = None
                weather_forecast = None

    context = {
        'weather_current': weather_current,
        'weather_forecast': weather_forecast,
        'city': city,
    }
    return render(request, 'weather_site/init.html', context)