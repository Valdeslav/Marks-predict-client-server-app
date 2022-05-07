from django.shortcuts import render
from django.views.decorators.http import require_POST

from marks.models import Group, Student, Subject
from groups_app.models import Speciality



def select_values_to_predict(request, group_id):
    """getting a list of students, which didn't have marks
     in some subjects. Also getting these subjects"""

    group = Group.objects.get(pk=group_id)
    students = Student.objects.filter(group=group)
    subjects = Subject.objects.filter(specialities__group=group)

    return render(request, "prediction/select-predict-data.html",
                  context={
                      'group': group,
                      'students': students,
                      'subjects': subjects,
                  })

@require_POST
def make_prediction(request, group_id):
    """parse the request to find which marks predict"""
    student_ids = request.POST['student_id_list'].split(',')
    subject_ids = request.POST['subject_id_list'].split(',')
    student_ids = [int(i) for i in student_ids]
    subject_ids = [int(i) for i in subject_ids]
    print(student_ids)

