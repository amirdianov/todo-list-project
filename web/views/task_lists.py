from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from web.forms import TaskListForm
from web.models import TaskList, TodoTask


class TaskListListView(LoginRequiredMixin, ListView):
    template_name = "web/main.html"
    model = TaskList

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TaskList.objects.none()
        else:
            return TaskList.objects.filter(created_user=self.request.user)


class TaskListDetailView(LoginRequiredMixin, DetailView):
    template_name = 'web/task_list.html'
    slug_field = "id"
    slug_url_kwarg = "id"
    model = TaskList

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'tasks': TodoTask.objects.filter(task_list=self.object.id)
        }

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Проверяем, имеет ли пользователь доступ к объекту TaskList
        if request.user.id != self.object.created_user.id:
            raise Http404("У вас нет доступа к этому списку задач.")

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class TaskListMixin:
    template_name = "web/task_list_form.html"
    slug_field = "id"
    slug_url_kwarg = "id"
    model = TaskList

    def get_initial(self):
        return {"user": self.request.user}

    def get_success_url(self):
        return reverse("main")


class TaskListCreateView(TaskListMixin, LoginRequiredMixin, CreateView):
    form_class = TaskListForm


class TaskListUpdateView(TaskListMixin, LoginRequiredMixin, UpdateView):
    form_class = TaskListForm

    def get_context_data(self, **kwargs):
        return {
            **super(TaskListUpdateView, self).get_context_data(**kwargs),
            "id": self.kwargs[self.slug_url_kwarg],
            "title": self.object.title,
        }


class TaskListDeleteView(LoginRequiredMixin, DeleteView):
    model = TaskList
    slug_field = "id"
    slug_url_kwarg = "id"
    success_url = reverse_lazy("main")

    def delete(self, request, *args, **kwargs):
        # Удаляем объект
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
