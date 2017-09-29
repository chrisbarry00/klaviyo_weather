from django.test import TestCase
from cities.models import City


class CityWeatherTest(TestCase):
    def test_weather_check(self):
        city = City.objects.create(
            name="Boston",
            state="MA",
            order=1
        )
        city_weather = city.get_weather();
        self.assertGreater(len(city_weather['condition']), 0)
        self.assertGreater(len(city_weather['current_temp_str']), 0)
        self.assertIsInstance(city_weather['current_temp'], float)
        self.assertIsInstance(city_weather['avg_temp'], float)
