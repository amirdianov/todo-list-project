from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from web.forms import RegistrationForm, AuthForm
from web.models import User


def registration_view(request):
    reg_form = RegistrationForm()
    is_success = False
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            print(reg_form.cleaned_data)
            create_user = User(name=reg_form.cleaned_data['name'],
                               surname=reg_form.cleaned_data['surname'],
                               email=reg_form.cleaned_data['email'])
            create_user.set_password(reg_form.cleaned_data['password'])
            create_user.save()
            is_success = True
    return render(request, "web/registration.html", {
        'form': reg_form, 'is_success': is_success
    })


def auth_view(request):
    auth_form = AuthForm()
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            user = authenticate(**auth_form.cleaned_data)
            if user is None:
                auth_form.add_error(None, "Введены некорректные данные")
            else:
                login(request, user)
                return redirect('main')
    return render(request, "web/auth.html", {
        'form': auth_form
    })


def logout_view(request):
    logout(request)
    return redirect("main")
