from django.shortcuts import render

from web.forms import RegistrationForm
from web.models import User


def registration(request):
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
    return render(request, "web/base.html", {
        'form': reg_form, 'is_success': is_success
    })
