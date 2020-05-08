from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm
from django.contrib import messages

def index(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=448806cc70e2a3990fc53523f3603fbe'

	err_msg = ''
	message = ''
	message_class = ''

	if request.method == "POST":
		form = CityForm(request.POST)
		if form.is_valid():
			new_city = form.cleaned_data['name']
			existing_city_count = City.objects.filter(name=new_city).count()
			if existing_city_count == 0:
				r = requests.get(url.format(new_city)).json()
				if r['cod'] == 200:
					form.save()
					messages.success(request, f"City added successfully!")
				else:
					messages.warning(request, f"This city does not exists in the world.")
					err_msg = "This city does not exists in the world."
			else:
				messages.warning(request, f"This city has already been added.")
				err_msg = "This city has already been added.warning"

		if err_msg:
			message = err_msg
			message_class = 'is-danger'
		else:
			message = "City added successfully!"
			message_class = 'is-success'

	form = CityForm()

	cities = City.objects.all()

	weather_data = []

	for city in cities:

		r = requests.get(url.format(city)).json()

		city_weather = {
			'city': city.name,
			'temperature': r['main']['temp'],
			'description': r['weather'][0]['description'],
			'icon': r['weather'][0]['icon'],
		}

		weather_data.append(city_weather)

	context = {'weather_data': weather_data, 'form': form, 'message': message, 'message_class': message_class}
	return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
	City.objects.get(name=city_name).delete()
	messages.success(request, f"City deleted successfully")
	return redirect('home')
