from django import forms

from web.models import User, TaskList, TodoTask


class DefaultBootstrapInputs:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
        for attr, value in self.fields.items():
            input_class = "form-select" if self.fields[attr].widget.input_type == "select" else "form-control"
            self.fields[attr].widget.attrs.update({"class": input_class})


class TodoListFilterForm(DefaultBootstrapInputs, forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={"placeholder": 'Поиск'}), required=False)


class RegistrationForm(DefaultBootstrapInputs, forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Повторный пароль')

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


class AuthForm(DefaultBootstrapInputs, forms.Form):
    email = forms.EmailField(label="Почта")
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')


class TaskListForm(DefaultBootstrapInputs, forms.ModelForm):

    def save(self, *args, **kwargs):
        self.instance.created_user = self.initial['user']
        return super(TaskListForm, self).save(*args, **kwargs)

    class Meta:
        model = TaskList
        fields = ('title',)


class TodoTaskForm(DefaultBootstrapInputs, forms.ModelForm):

    def save(self, *args, **kwargs):
        self.instance.created_user = self.initial['user']
        self.instance.task_list_id = self.initial['task_list_id']
        return super(TodoTaskForm, self).save(*args, **kwargs)

    class Meta:
        model = TodoTask
        exclude = ('created_user', 'task_list',)
        widgets = {
            "start_date": forms.DateTimeInput(attrs={"type": "datetime-local"},
                                              format='%Y-%m-%dT%H:%m'),
            "end_date": forms.DateTimeInput(attrs={"type": "datetime-local"},
                                            format='%Y-%m-%dT%H:%m'),
            "notify_at": forms.DateTimeInput(attrs={"type": "datetime-local"},
                                             format='%Y-%m-%dT%H:%m'),
            "assigned_user": forms.SelectMultiple(),
            "task_type": forms.SelectMultiple()
        }
