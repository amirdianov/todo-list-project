from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView

from web.forms import TaskListForm
from web.models import TaskList, TodoTask


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
    slug_field = "id"
    slug_url_kwarg = "id"
    model = TaskList

    def get_initial(self):
        return {"user": self.request.user}

    def get_success_url(self):
        return reverse("main")


class TaskListCreateView(TaskListMixin, CreateView):
    form_class = TaskListForm


class TaskListUpdateView(TaskListMixin, UpdateView):
    form_class = TaskListForm

    def get_context_data(self, **kwargs):
        return {
            **super(TaskListUpdateView, self).get_context_data(**kwargs),
            "id": self.kwargs[self.slug_url_kwarg],
            "title": self.object.title,
        }
