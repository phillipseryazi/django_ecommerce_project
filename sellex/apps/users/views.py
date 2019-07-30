from django.shortcuts import render, redirect
from django.views.generic import (View, )
from .forms import RegistrationForm


# Create your views here.

class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('auth:login')

        form = RegistrationForm()
        return render(request, 'users/register.html', {'form': form})
