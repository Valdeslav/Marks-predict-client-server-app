from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from groups_app.models import Group


class Student(models.Model):
    fullname = models.CharField(max_length=150)
    group = models.ForeignKey(Group, on_delete=models.PROTECT)

    def __str__(self):
        return self.fullname


class Subject(models.Model):
    name = models.CharField(max_length=100)
    semester = models.IntegerField(validators=[MaxValueValidator(12), g])

    def __str__(self):
        return self.name


class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    mark = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])
