from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Student, Subject, Mark
from groups_app.models import Group
from .forms import UploadDataFileForm
from .importer.import_upload_data import import_data_from_file
from marks.response_objects import StudentMarks


@login_required
def students_subjects_group_list(request, group_id):
    """getting a list of students and subjects of group.
    render the form to upload file with student's marks"""
    group = Group.objects.get(pk=group_id)
    students = Student.objects.filter(group_id=group_id).order_by('fullname')
    subjects = Subject.objects.distinct('pk').filter(specialities=group.speciality).order_by('pk', 'semester')
    marks_by_students = []
    for student in students:
        marks = Mark.objects.defer('student').filter(student=student).order_by('subject__pk', 'subject__semester')
        student_marks = StudentMarks(student)
        for mark in marks:
            student_marks.marks[mark.subject.id] = mark.mark
        marks_by_students.append(student_marks)

    file_form = UploadDataFileForm()
    status = request.GET.get('status')
    return render(request, "structure/group/details.html",
                  context={'group': group,
                           'subjects': subjects,
                           'marks_by_st': marks_by_students,
                           'file_form': file_form,
                           'status': status
                           })


@login_required
@require_POST
def upload_marks_file(request, group_id):
    "handler for upload file with information about student's marks on server"
    form = UploadDataFileForm(require_POST, request.FILES)
    if form.is_valid():
        filestr = import_data_from_file(request.FILES['file'], group_id)

    return HttpResponseRedirect(f'/structure/group/{ group_id }/?status=success')

