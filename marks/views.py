from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from .models import Student, Subject, Mark
from groups_app.models import Group
from .forms import UploadDataFileForm
from .importer.import_upload_data import file_to_str


def students_subjects_group_list(request, group_id):
    """getting a list of students and subjects of group.
    render the form to upload file with student's marks"""
    group = Group.objects.get(pk=group_id)
    students = Student.objects.filter(group_id=group_id).order_by('fullname')
    subjects = Subject.objects.distinct('pk').filter(mark__student__group_id=group_id).order_by('pk', 'semester')
    marks_by_students = []
    for student in students:
        marks = Mark.objects.defer('student').filter(student=student).order_by('subject__pk', 'subject__semester')
        marks.student = student
        marks_by_students.append(marks)

    file_form = UploadDataFileForm()
    status = request.GET.get('status')
    return render(request, "structure/group/details.html",
                  context={'group': group,
                           'subjects': subjects,
                           'marks': marks_by_students,
                           'file_form': file_form,
                           'status': status
                           })


@require_POST
def upload_marks_file(request, group_id):
    "handler for upload file with information about student's marks on server"
    form = UploadDataFileForm(require_POST, request.FILES)
    if form.is_valid():
        filestr = file_to_str(request.FILES['file'])

    return HttpResponseRedirect(f'/structure/group/{ group_id }/?status=success')

