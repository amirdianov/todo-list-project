import random
from datetime import timedelta

from django.core.management import BaseCommand
from django.utils.timezone import now

from web.models import TaskList, TodoTask, TaskType, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        current_day = now()
        type_tasks = TaskType.objects.filter(created_user_id=1)
        users = User.objects.all()
        todo_tasks = []
        for i in range(3):
            task_list = TaskList.objects.create(title=f'generated{i}', created_user_id=1)

            for j in range(random.randint(3, 5)):
                start_date = current_day + timedelta(hours=random.randint(1, 12))
                task = TodoTask(title=f'generated {i} - {j}', start_date=start_date,
                                task_list_id=task_list.id, created_user_id=1)
                todo_tasks.append(task)
        saved_tasks = TodoTask.objects.bulk_create(todo_tasks)
        todo_task_types = []
        todo_task_assigned_user = []

        for el in saved_tasks:
            for tag_index in range(random.randint(1, 2)):
                todo_task_types.append(TodoTask.task_type.through(todotask_id=el.id, tasktype_id=type_tasks[tag_index].id))
            for user_index in range(random.randint(1, 2)):
                todo_task_assigned_user.append(TodoTask.assigned_user.through(todotask_id=el.id, user_id=users[user_index].id))
        TodoTask.task_type.through.objects.bulk_create(todo_task_types)
        TodoTask.assigned_user.through.objects.bulk_create(todo_task_assigned_user)
