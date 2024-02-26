from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from web.forms import TaskListForm, TodoListFilterForm, TodoTaskFilterForm
from web.models import TaskList, TodoTask, TaskType


class FilterClass:
    def filter_queryset(self, qs):
        self.search = self.request.GET.get("search", None)
        if self.search:
            qs = qs.filter(Q(title__icontains=self.search))
        return qs


class TaskListListView(LoginRequiredMixin, ListView, FilterClass):
    template_name = "web/main.html"
    model = TaskList
    paginate_by = 1

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return TaskList.objects.none()
        queryset = TaskList.objects.filter(created_user=self.request.user)
        return self.filter_queryset(queryset)

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'filter_form': TodoListFilterForm(self.request.GET)
        }


class TaskListDetailView(LoginRequiredMixin, DetailView, FilterClass):
    template_name = 'web/task_list.html'
    slug_field = "id"
    slug_url_kwarg = "id"
    model = TaskList

    def filter_queryset(self, qs):
        qs = super().filter_queryset(qs)
        self.type_of_task = self.request.GET.get("type_of_task", None)
        if self.type_of_task:
            type_task = TaskType.objects.get(id=self.type_of_task)
            qs = qs.filter(task_type__in=[type_task])
        return qs

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            'tasks': self.filter_queryset(
                TodoTask.objects.filter(task_list=self.object.id).prefetch_related('task_type').select_related(
                    'created_user')),
            'filter_form': TodoTaskFilterForm(self.request.GET)
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
