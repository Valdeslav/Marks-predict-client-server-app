from django.db.models import ProtectedError, RestrictedError
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Student, Subject, Mark
from groups_app.models import Group
from .forms import UploadDataFileForm
from .importer.import_upload_data import import_data_from_file
from marks.response_objects import StudentMarks
from authentication.views import admin_required
from marks.forms import GroupForm, StudentForm, MarkForm


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


@login_required
@admin_required
def edit_group(request, group_id=None):
    if request.method == 'POST':
        if group_id:
            group = Group.objects.get(pk=group_id)
            form = GroupForm(request.POST, instance=group)
        else:
            form = GroupForm(request.POST)
        group = form.save()
        return HttpResponseRedirect(f'/structure/faculty/{group.speciality.faculty_id}/group/list/')

    else:
        try:
            message = request.GET['message']
        except MultiValueDictKeyError:
            message = None

        if group_id:
            group = Group.objects.get(pk=group_id)
            form = GroupForm(instance=group)

        else:
            form = GroupForm()
        return render(request,
                      'structure/group/edit.html',
                      context={
                          'group_id': group_id,
                          'form': form,
                          'message': message
                      })


@login_required
@admin_required
def delete_group(request, group_id):
    group = Group.objects.get(pk=group_id)
    faculty_id = group.speciality.faculty_id
    try:
        group.delete()
        return HttpResponseRedirect(f'/structure/faculty/{faculty_id}/group/list/')
    except ProtectedError:
        return HttpResponseRedirect(f'/structure/group/edit/{group_id}/?message=невозможно удалить группу')


@login_required
@admin_required
def edit_student(request, student_id=None):
    if request.method == 'POST':
        if student_id:
            student = Student.objects.get(pk=student_id)
            form = StudentForm(request.POST, instance=student)
        else:
            form = StudentForm(request.POST)
        student = form.save()
        return HttpResponseRedirect(f'/structure/group/{student.group_id}/')

    else:
        try:
            message = request.GET['message']
        except MultiValueDictKeyError:
            message = None

        if student_id:
            student = Student.objects.get(pk=student_id)
            form = StudentForm(instance=student)

        else:
            form = StudentForm()
        return render(request,
                      'structure/group/student/edit.html',
                      context={
                          'student_id': student_id,
                          'form': form,
                          'message': message
                      })


@login_required
@admin_required
def delete_student(request, student_id):
    student = Student.objects.get(pk=student_id)
    group_id = student.group_id
    try:
        student.delete()
        return HttpResponseRedirect(f'/structure/group/{group_id}/')
    except ProtectedError:
        return HttpResponseRedirect(f'/structure/student/edit/{student_id}/?message=невозможно удалить студента')
    except RestrictedError:
        return HttpResponseRedirect(f'/structure/student/edit/{student_id}/?message=невозможно удалить студента')


@login_required
@admin_required
def mark_list(request, student_id):
    """getting a list of marks of selected student"""
    student = Student.objects.get(pk=student_id)
    marks = Mark.objects.filter(student_id=student_id)

    return render(request,
                  'structure/mark/list.html',
                  context={"marks": marks, "student": student})


@login_required
@admin_required
def edit_mark(request, mark_id=None):
    if request.method == 'POST':
        if mark_id:
            mark = Mark.objects.get(pk=mark_id)
            form = MarkForm(request.POST, instance=mark)
        else:
            form = MarkForm(request.POST)
        mark = form.save()
        return HttpResponseRedirect(f'/structure/student/{mark.student_id}/marks/')

    else:
        try:
            message = request.GET['message']
        except MultiValueDictKeyError:
            message = None

        if mark_id:
            mark = Mark.objects.get(pk=mark_id)
            form = MarkForm(instance=mark)

        else:
            form = MarkForm()
        return render(request,
                      'structure/mark/edit.html',
                      context={
                          'mark_id': mark_id,
                          'form': form,
                          'message': message
                      })


@login_required
@admin_required
def delete_mark(request, mark_id):
    mark = Mark.objects.get(pk=mark_id)
    student_id = mark.student_id
    try:
        mark.delete()
        return HttpResponseRedirect(f'/structure/student/{student_id}/marks/')
    except ProtectedError:
        return HttpResponseRedirect(f'/structure/mark/edit/{mark_id}/?message=невозможно удалить оценку')
    except RestrictedError:
        return HttpResponseRedirect(f'/structure/mark/edit/{mark_id}/?message=невозможно удалить оценку')