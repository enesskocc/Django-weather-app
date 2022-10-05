from django.shortcuts import render, get_object_or_404, redirect
from decouple import config
import requests
from pprint import pprint
from .models import City
from django.contrib import messages

# Create your views here.

def home(request):
    api_key= config('api_key')
    user_city = request.GET.get('city')
    if user_city :
        url =f'https://api.openweathermap.org/data/2.5/weather?q={user_city}&appid={api_key}&units=metric'
        r = requests.get(url)
        if r.status_code == 200 :  # yada bunun yerine sadece r.ok yazsakda olur!
            content = r.json()
            r_city = content.get('name')
            if City.objects.filter(city=r_city):
                messages.warning(request, "City already exists")
                return redirect('home')
            else:
                City.objects.create(city = r_city)
                messages.success(request, "City Created")
                return redirect('home')

        else:
            messages.error(request, "City does not exists")
            return redirect('home')
    cities = City.objects.all()
    city_data = []
    for city in cities:
        url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        r = requests.get(url)
        content = r.json() ##dictory ceviriyor!
        data= {
            'city': city,
            'temp': content.get('main').get('temp'),
            'description' : content.get('weather')[0].get('description'),
            'icon' : content.get('weather')[0].get('icon')
        }
        city_data.append(data)

    context = {
        'city_data' : city_data
    }



    return render(request, "Weatherapplication/home.html", context) 


def delete(request, id):
    city = get_object_or_404(City, id=id)
    city.delete()
    messages.success(requests, 'City Deleted')
    return redirect('home')
    