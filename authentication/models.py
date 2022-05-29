from django.db import models
from django.contrib.auth.models import AbstractUser
from marks.models import Student


class Role(models.Model):
    role_id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    student = models.OneToOneField(Student, on_delete=models.RESTRICT, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def is_admin(self):
        return self.role.role_id == 1

    def is_teacher(self):
        return self.role.role_id == 2
