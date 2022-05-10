from django.shortcuts import render, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_POST

from marks.models import Group, Student, Subject
from .predictor_module.exceptions import EmptyListOfSubjectsWithMark
from .predictor_module.main import predict_marks


def select_values_to_predict(request, group_id):
    """getting a list of students, which didn't have marks
     in some subjects. Also getting these subjects"""

    group = Group.objects.get(pk=group_id)
    students = Student.objects.filter(group=group)
    subjects = Subject.objects.filter(specialities__group=group)
    try:
        message = request.GET['message']
    except MultiValueDictKeyError:
        message = None

    return render(request, "prediction/select-predict-data.html",
                  context={
                      'group': group,
                      'students': students,
                      'subjects': subjects,
                      'message': message
                  })

@require_POST
def make_prediction(request, group_id):
    """parse the request to find which marks predict"""
    student_ids = request.POST['student_id_list'].split(',')
    subject_ids = request.POST['subject_id_list'].split(',')
    student_ids = [int(i) for i in student_ids]
    subject_ids = [int(i) for i in subject_ids]
    try:
        predictions = predict_marks(group_id, student_ids, subject_ids)
        subjects = Subject.objects.filter(pk__in=subject_ids).order_by('pk')
        group = Group.objects.get(pk=group_id)

        return render(request, "prediction/prediction.html",
                  context={
                      'group': group,
                      'subjects': subjects,
                      'predictions': predictions
                  })
    except EmptyListOfSubjectsWithMark:
        return HttpResponseRedirect(f'/structure/group/{group_id}/create-prediction/?message=недостаточно данных для предсказания')

