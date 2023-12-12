"""
URL configuration for todo_list project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from web.views import registration_view, auth_view, logout_view, TaskListCreateView, TaskListListView, \
    TaskListDetailView, TodoTaskCreateView, TaskListUpdateView, TodoTaskDetailView, TodoTaskUpdateView, \
    TaskListDeleteView, TodoTaskDeleteView

urlpatterns = [
    path("registration/", registration_view, name='registration'),
    path("auth/", auth_view, name='auth'),
    path("logout/", logout_view, name='logout'),
    path("task_lists/", TaskListListView.as_view(), name='main'),
    path("task_list/<str:title>/<int:id>/", TaskListDetailView.as_view(), name='task_list'),
    path("task_list/add/", TaskListCreateView.as_view(), name='task_list_add'),
    path("task_list/<str:title>/<int:id>/edit/", TaskListUpdateView.as_view(), name='task_list_edit'),
    path("task_list/<str:title>/<int:id>/delete/", TaskListDeleteView.as_view(), name='task_list_delete'),
    path("task_list/<str:task_list_title>/<int:task_list_id>/todo_task/<str:todo_task_title>/<int:todo_task_id>/",
         TodoTaskDetailView.as_view(), name='todo_task'),
    path("task_list/<str:title>/<int:id>/todo_task/add/", TodoTaskCreateView.as_view(), name='todo_task_add'),
    path("task_list/<str:task_list_title>/<int:task_list_id>/todo_task/<str:todo_task_title>/<int:todo_task_id>/edit/",
         TodoTaskUpdateView.as_view(), name='todo_task_edit'),
    path("task_list/<str:task_list_title>/<int:task_list_id>/todo_task/<str:todo_task_title>/<int:todo_task_id>/delete/",
         TodoTaskDeleteView.as_view(), name='todo_task_delete')
]
