from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


class Register(View):
    def get(self, request):
        # Blank registration form
        form = UserCreationForm
        context = {'form': form}
        return render(request, 'registration/register.html', context)

    def post(self, request):
        # Check and save data
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log in and redirect to home page
            login(request, new_user)
            return redirect('learning_logs:index')
        else:
            context = {'form': form}
            return render(request, 'registration/register.html', context)
