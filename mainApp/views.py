from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.

def index(request):
    cities = City.objects.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=cb0312035f33a01b441bb33458862c67'
    if request.method == 'POST':
            form = CityForm(request.POST)
            form.save()
    form = CityForm()
    weather_data = []
    for city in cities:
        
        city_weather = requests.get(url.format(city))
        city_weather = requests.get(url.format(city.name))
        if city_weather.status_code == 404:
            continue
        city_weather = city_weather.json()
        weather = {
                    'city' : city,
                    'temperature' : city_weather['main']['temp'],
                    'description' : city_weather['weather'][0]['description'],
                    'icon' : city_weather['weather'][0]['icon'],
                    'humidity': city_weather['main']['humidity'],
                    'pressure': city_weather['main']['pressure'],
                    'country': city_weather['sys']['country'],
                    'sunrise': city_weather['sys']['sunrise'],
                    'sunset': city_weather['sys']['sunset'],
                    'windspeed': city_weather['wind']['speed']
                }
        weather_data.append(weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'index.html', context)