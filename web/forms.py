from django import forms

from web.models import User, TaskList


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password', 'Пароли не совпали')
        return cleaned_data

    class Meta:
        model = User
        fields = ("name", "surname", "email", "password", "password2")
        widgets = {
            'password': forms.PasswordInput(),
        }


class AuthForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class TaskListForm(forms.ModelForm):

    def save(self, *args, **kwargs):
        self.instance.created_user = self.initial['user']
        return super(TaskListForm, self).save(*args, **kwargs)

    class Meta:
        model = TaskList
        fields = ('title',)
