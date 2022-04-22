from django.db import models
from django.core.validators import MaxValueValidator


class Speciality(models.Model):
    name = models.CharField(max_length=100)


class Faculty(models.Model):
    name = models.CharField(max_length=100)


class Group(models.Model):
    number = models.IntegerField(validators=[MaxValueValidator(100)])
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
