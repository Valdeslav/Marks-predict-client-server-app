from django.shortcuts import render
from .models import Student, Subject, Mark
from groups_app.models import Group


def students_subjects_group_list(request, group_id):
    """getting a list of students and subjects of group"""
    group = Group.objects.get(pk=group_id)
    students = Student.objects.filter(group_id=group_id)
    subjects = Subject.objects.distinct('pk').filter(mark__student__group_id=group_id).order_by('pk', 'semester')

    return render(request, "structure/group/details.html",
                  context={'group': group, 'students': students, 'subjects': subjects})

