from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Speciality(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Group(models.Model):
    number = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(10)])
    year = models.IntegerField(validators=[MaxValueValidator(6), MinValueValidator(1)])
    speciality = models.ForeignKey(Speciality, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.number) + ': ' + str(self.speciality)
