from django.db import models


class Role(models.TextChoices):
    admin = "admin", "Администратор"
    head_of_dep = "head of department", 'Руководитель отдела'
    employee = "employee", "Сотрудник"
