from django.shortcuts import render
from django.http import HttpResponseRedirect

from users.models import User
from .forms import UserForm


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        # Make sure the form data is valid
        if form.is_valid():
            # Data appears to be good, so create a new user and redirect them to the success page
            user = User(email=form.cleaned_data['email'], city=form.cleaned_data['city'])
            user.save()
            return HttpResponseRedirect('/success/')
    else:
        form = UserForm()

    return render(request, 'signup.html', {'form': form})


def success(request):
    return render(request, 'success.html')
