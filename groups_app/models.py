from django.db import models


class Speciality(models.Model):
    name = models.CharField(max_length=100)


class Faculty(models.Model):
    name = models.CharField(max_length=100)


class Group(models.Model):
    number = models.DecimalField(decimal_places=2, max_digits=0)
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)
