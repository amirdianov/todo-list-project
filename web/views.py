from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView

from web.forms import RegistrationForm, AuthForm, TaskListForm, TodoTaskForm
from web.models import User, TaskList, TodoTask


class TaskListView(ListView):
    template_name = "web/main.html"
    model = TaskList

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TaskList.objects.none()
        else:
            return TaskList.objects.filter(created_user=self.request.user)


class TaskListDetailView(DetailView):
    template_name = 'web/task_list.html'
    slug_field = "id"
    slug_url_kwarg = "id"
    model = TaskList

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'tasks': TodoTask.objects.filter(task_list=self.object.id)
        }


class TaskListMixin:
    template_name = "web/task_list_form.html"

    def get_initial(self):
        return {"user": self.request.user}

    def get_success_url(self):
        return reverse("main")


class TaskListCreateFormView(TaskListMixin, CreateView):
    form_class = TaskListForm


class TodoTaskCreateFormView(TaskListMixin, CreateView):
    form_class = TodoTaskForm
    template_name = "web/todo_task_form.html"


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
