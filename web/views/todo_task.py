from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from web.forms import TodoTaskForm
from web.models import TodoTask


class TodoTaskDetailView(LoginRequiredMixin, DetailView):
    template_name = 'web/todo_task.html'
    slug_field = "id"
    slug_url_kwarg = "todo_task_id"
    model = TodoTask

    def get_context_data(self, **kwargs):
        return {
            **super(TodoTaskDetailView, self).get_context_data(**kwargs),
            "task_list_id": self.kwargs['task_list_id'],
            "task_list_title": self.kwargs['task_list_title'],
        }


class TodoTaskMixin:
    template_name = "web/todo_task_form.html"
    slug_field = "id"
    model = TodoTask

    def get_success_url(self):
        return reverse("main")


class TodoTaskCreateView(TodoTaskMixin, LoginRequiredMixin, CreateView):
    form_class = TodoTaskForm
    slug_url_kwarg = "id"

    def get_initial(self):
        return {"user": self.request.user, "task_list_id": self.kwargs[self.slug_url_kwarg]}


class TodoTaskUpdateView(TodoTaskMixin, LoginRequiredMixin, UpdateView):
    form_class = TodoTaskForm
    slug_url_kwarg = "todo_task_id"

    def get_initial(self):
        return {"user": self.request.user, "task_list_id": self.kwargs["task_list_id"]}

    def get_context_data(self, **kwargs):
        return {
            **super(TodoTaskUpdateView, self).get_context_data(**kwargs),
            "id": self.kwargs["todo_task_id"],
            "title": self.object.title,
        }


class TodoTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = TodoTask
    slug_field = "id"
    slug_url_kwarg = "todo_task_id"

    def delete(self, request, *args, **kwargs):
        # Удаляем объект
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy("task_list",
                            args=[self.kwargs['task_list_title'], self.kwargs['task_list_id']])
