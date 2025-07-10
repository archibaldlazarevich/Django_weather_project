import requests
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.base import TemplateView
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from django.core.exceptions import ObjectDoesNotExist
from mysite import settings
from weather_site.models import City


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
                return redirect('weather_data')
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
            return redirect('weather_data')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'weather_site/login.html', {'form': form})

@login_required(login_url='login')
def weather_data_view(request):
    return render(request, 'weather_site/weather_data.html')


class WeatherView(TemplateView):
    template_name = "weather_site/weather_forecast.html"

    def is_data_expired(self, place_id):
        try:
            City.objects.get(place_id=place_id)
            return True
        except ObjectDoesNotExist:
            return None

    def get_cached_data(self, place_id):
        city = City.objects.get(place_id=place_id)
        return city.data

    def add_data_in_base(self, data, place_id):
        City(place_id = place_id, data = data).save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lat = self.request.GET.get('lat')
        lng = self.request.GET.get('lng')

        city = self.determ_city(coord=(lat, lng))

        if self.is_data_expired(place_id= city[1]):
            context['weather'] = self.get_cached_data(place_id= city[1])
        else:
            context['weather'] = self.fetch_from_api(latitude= lat, longitude= lng)

        for item in context['weather']['second']['list']:
            item['date_obj'] = datetime.strptime(item['date_obj'], '%Y-%m-%d %H:%M').date()
        return context

    def determ_city(self, coord):
        """
        Метод для определения города по координатам,
        запроса к бд для получения id города в бд city
        :param coord: координаты (latitude, longitude)
        :return: Название города если True или False,
        город не найден по данным координатам (пример: если это деревня, то None)
        """
        geolocator = Nominatim(user_agent="GetLoc", timeout=10)
        location = geolocator.reverse(query= coord, language='ru')
        if not location:
            return '"Местоположение не определено"'
        if "locality" in location.raw["address"]:
            answer = (
                f"около н.п. {location.raw['address']['locality']},"
                f" {location.raw['address']['city']}"
            )
        elif "village" in location.raw["address"]:
            answer = f"н.п. {location.raw['address']['village']}"
        elif "town" in location.raw["address"]:
            answer = f"н.п. {location.raw['address']['town']}"
        elif "city" in location.raw["address"]:
            answer = f"{location.raw['address']['city']}"
        else:
            answer = location
        return answer, location.raw['place_id']


    def fetch_from_api(self, latitude, longitude):
        url = (f'https://api.openweathermap.org/data/2.5/weather?'
               f'lat={latitude}&lon={longitude}&appid={settings.OPENWEATHER_API_KEY}&lang=ru&units=metric')
        city = self.determ_city(coord=(latitude, longitude))
        response = requests.get(url).json()
        response['name'] = city[0]
        dt_utc = datetime.fromtimestamp(response['dt'])
        dt_local = dt_utc + timedelta(hours=3)
        response['dt'] = dt_local.strftime('%d.%m.%Y %H:%M')

        second_url = (f"https://api.openweathermap.org/data/2.5/forecast?"
                      f"lat={latitude}&lon={longitude}&lang=ru&appid={settings.OPENWEATHER_API_KEY}&lang=ru&units=metric")
        sec_response = requests.get(second_url).json()

        for item in sec_response['list']:
            dt_utc = datetime.fromtimestamp(item['dt'])
            dt_local = dt_utc + timedelta(hours=3)
            item['dt_txt'] = dt_local.strftime('%Y-%m-%d %H:%M')
            item['date_obj'] = dt_local.strftime('%Y-%m-%d %H:%M')
        answer = {'first': response, 'second': sec_response}
        self.add_data_in_base(data= answer, place_id = city[1])
        return answer

