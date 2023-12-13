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
    def is_staff(self):
        return self.role in (Role.admin, Role.head_of_dep)
    @property
    def is_superuser(self):
        return self.role == Role.admin

    def __str__(self):
        return f'{self.name} ({self.role})'


# Create your models here.
class TaskType(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    created_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                     verbose_name='Создатель типа задачи')

    def __str__(self):
        return f'{self.title}'


class TaskList(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок списка')
    created_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                     verbose_name='Создатель списка задач')

    class Meta:
        verbose_name = 'Лист заданий'
        verbose_name_plural = 'Листы с заданиями'

    def __str__(self):
        return f'Список заданий {self.id} "{self.title}"'


class TodoTask(models.Model):
    title = models.CharField(max_length=128, verbose_name='Наименование задачи')
    description = models.CharField(max_length=128, verbose_name='Описание', null=True, blank=True)
    start_date = models.DateTimeField(verbose_name='Дата начала', null=True, blank=True)
    end_date = models.DateTimeField(verbose_name='Дата конца', null=True, blank=True)
    notify_at = models.DateTimeField(verbose_name='Время отправки уведомления', null=True, blank=True)
    task_type = models.ManyToManyField(TaskType, verbose_name='Тип задачи')
    created_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                     verbose_name='Создатель задачи')
    assigned_user = models.ManyToManyField(User, verbose_name='Назначенный сотрудник',
                                           related_name='assigned_users')
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE,
                                  verbose_name='Список задач')

    def __str__(self):
        return f'Задание {self.id} "{self.title}"'
