from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from users.models import User


class Command(BaseCommand):
    SENDER = 'christopher.shaun.barry@gmail.com'

    help = '''Sends out weather newsletter to all users in database.
              Pass in debug_mode=True to print emails instead of send'''

    def add_arguments(self, parser):
        parser.add_argument('debug_mode', type=bool, nargs='?', default=False)

    def handle(self, *args, **options):
        failure_count = 0

        users = User.objects.all()
        for user in users:
            city_weather = user.city.get_weather()

            if city_weather:
                # Build Email Subject
                if ((city_weather['current_temp'] - city_weather['avg_temp']) >= 5 or
                        city_weather['condition'] == 'Clear'):
                    # if sunny (clear) or 5 degrees warmer than the average
                    subject = "It's nice out! Enjoy a discount on us."
                elif ((city_weather['current_temp'] - city_weather['avg_temp']) <= -5 or
                        city_weather['condition'] == 'Rain'):
                    # if precipitating or 5 degrees cooler than the average
                    subject = "Not so nice out? That's okay, enjoy a discount on us."
                else:
                    subject = "Enjoy a discount on us."

                # Build Email Body
                body = "Currently in {city}, {state} the weather is {condition} and the temperature is {temp}".format(
                    city=user.city.name,
                    state=user.city.state,
                    condition=city_weather['condition'],
                    temp=city_weather['current_temp_str']
                )

                if options['debug_mode']:
                    self.stdout.write('To ' + user.email + ': ' + subject + ' - ' + body)
                else:
                    send_mail(
                        subject,
                        body,
                        self.SENDER,
                        [user.email],
                        fail_silently=False,
                    )
            else:
                self.stdout.write('Was not able to send email to ' + user.email)
                failure_count += 1

        self.stdout.write('Sent ' + str(len(users)-failure_count) + ' emails.')
