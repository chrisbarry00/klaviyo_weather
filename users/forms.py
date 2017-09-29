from django import forms

from cities.models import City
from users.models import User


class UserForm(forms.Form):
    email = forms.EmailField(label='Email Address')
    city = forms.ModelChoiceField(
        label='Loction',
        queryset=City.objects.all(),
        empty_label="Where do you live?"
    )

    def is_valid(self):
        # Run parent validation
        valid = super(UserForm, self).is_valid()
        if not valid:
            return valid

        # See if this email address is already subscribed
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error(None, 'This email address is already subcribed.')
            return False

        # No validation errors
        return True
