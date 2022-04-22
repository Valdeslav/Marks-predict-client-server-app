from django.shortcuts import render
from .models import Faculty


def faculty_list(request):
    """getting a list of faculties"""
    faculties = Faculty.objects.all()
    return render()

