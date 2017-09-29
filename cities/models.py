from django.db import models
from requests.exceptions import ConnectionError
import requests
import datetime


class City(models.Model):
    SENDER = 'christopher.shaun.barry@gmail.com'
    APIKEY = '4748aabd079c7c4a'
    BASEURL = 'http://api.wunderground.com/api/{key}/conditions/q/{state}/{city}.json'
    HISTORYURL = 'http://api.wunderground.com/api/{key}/planner_{date}/q/{state}/{city}.json'
    TODAY = datetime.datetime.now().strftime("%m%d")

    name = models.CharField(max_length=255)
    state = models.CharField(max_length=2)
    order = models.IntegerField()

    class Meta:
        ordering = ['order', ]

    def __str__(self):
        return '#' + str(self.order) + ' - ' + str(self.name) + ', ' + str(self.state)

    def get_weather(self):
        # Get the current weather
        current_url = self.BASEURL.format(
            key=self.APIKEY,
            state=self.state,
            city=self.name
        )

        try:
            r = requests.get(current_url)
        except ConnectionError as e:
            print(e)
            r = "Could not connect to Weather Underground API"

        try:
            current_weather = r.json()['current_observation']
        except KeyError:
            print('Could not find current weather for ' + self.name + ', ' + self.state)
            return {}

        # Get average temperature for this location for this time of year
        # Unclear requirements - For lack of a better way, calculating this by getting the historical
        # weather data for today's date, getting the average high and average low, and averaging those
        history_url = self.HISTORYURL.format(
            key=self.APIKEY,
            state=self.state,
            city=self.name,
            date=self.TODAY + self.TODAY
        )
        r = requests.get(history_url)
        try:
            historical_weather = r.json()['trip']
        except KeyError:
            print('Could not find historical weather for ' + self.name + ', ' + self.state)
            return {}

        avg_temp = (
                  int(historical_weather['temp_high']['avg']['F']) +
                  int(historical_weather['temp_low']['avg']['F'])
              ) / 2

        return {
            'condition': current_weather['weather'],
            'current_temp': current_weather['temp_f'],
            'current_temp_str': current_weather['temperature_string'],
            'avg_temp': avg_temp
        }
