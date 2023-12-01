from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.auth.models import make_password
from django.db import models

from web.enums import Role


class UserManager(DjangoUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, role=Role.admin, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()

    name = models.CharField(max_length=30, verbose_name="Имя")
    surname = models.CharField(max_length=30, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Почта")
    role = models.CharField(choices=Role.choices, default=Role.employee, verbose_name='Роль')

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    @property
    def is_superuser(self):
        return self.role == Role.admin


# Create your models here.
class TypeTask(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    created_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name='Создатель типа задачи')


class TaskList(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок списка')
    created_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name='Создатель списка задач')


class TodoTask(models.Model):
    title = models.CharField(max_length=128, verbose_name='Наименование задачи')
    description = models.CharField(max_length=128, verbose_name='Описание', null=True, blank=True)
    start_date = models.DateTimeField(verbose_name='Дата начала', null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='Дата конца', null=True, blank=True)
    notify_at = models.DateTimeField(verbose_name='Время отправки уведомления', null=True, blank=True)
    task_type = models.ManyToManyField(TypeTask, verbose_name='Тип задачи', null=True, blank=True)
    created_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name='Создатель задачи')
    assigned_user = models.ManyToManyField(User, null=True, blank=True, verbose_name='Назначенный сотрудник',
                                           related_name='assigned_users')
    todo_task = models.ForeignKey(TaskList, null=True, blank=True, on_delete=models.SET_NULL,
                                  verbose_name='Список задач')
