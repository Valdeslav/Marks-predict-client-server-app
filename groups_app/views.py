from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError

from groups_app.models import Faculty, Speciality, Group
from authentication.views import admin_required
from groups_app.forms import FacultyForm, SpecialityForm


@login_required
def faculty_list(request):
    """getting a list of faculties"""
    faculties = Faculty.objects.all()
    return render(request, "structure/faculty/list.html", context={"faculties": faculties})


@login_required
def group_list(request, faculty_id):
    """getting a list of groups of selected faculty"""
    years_obj = Group.objects.only('year').filter(speciality__faculty_id=faculty_id).distinct('year').order_by('year')
    groups_by_years = []
    for year_obj in years_obj:
        groups = Group.objects.filter(year=year_obj.year, speciality__faculty_id=faculty_id).defer('year')
        groups.year = year_obj.year
        groups_by_years.append(groups)

    return render(request, "structure/group/list.html",
                  context={"groups": groups_by_years, "faculty_id": faculty_id})


@login_required
@admin_required
def edit_faculty(request, faculty_id=None):
    if request.method == 'POST':
        if faculty_id:
            faculty = Faculty.objects.get(pk=faculty_id)
            form = FacultyForm(request.POST, instance=faculty)
        else:
            form = FacultyForm(request.POST)
        form.save()
        return HttpResponseRedirect(f'/structure/faculty/list/')

    else:
        try:
            message = request.GET['message']
        except MultiValueDictKeyError:
            message = None

        if faculty_id:
            faculty = Faculty.objects.get(pk=faculty_id)
            form = FacultyForm(instance=faculty)

        else:
            form = FacultyForm()
        return render(request,
                      'structure/faculty/edit.html',
                      context={
                          'faculty_id': faculty_id,
                          'form': form,
                          'message': message
                      })


@login_required
@admin_required
def delete_faculty(request, faculty_id):
    faculty = Faculty.objects.get(pk=faculty_id)
    try:
        faculty.delete()
        return HttpResponseRedirect(f'/structure/faculty/list/')
    except ProtectedError:
        return  HttpResponseRedirect(f'/structure/faculty/edit/{faculty_id}?message=невозможно удалить факультет')


@login_required
@admin_required
def speciality_list(request, faculty_id):
    """getting a list of specialities of selected faculty"""
    faculty = Faculty.objects.get(pk=faculty_id)
    specialities = Speciality.objects.filter(faculty_id=faculty_id)

    return render(request, "structure/speciality/list.html",
                  context={"specialities": specialities, "faculty": faculty})


@login_required
@admin_required
def edit_speciality(request, speciality_id=None):
    if request.method == 'POST':
        if speciality_id:
            speciality = Speciality.objects.get(pk=speciality_id)
            form = SpecialityForm(request.POST, instance=speciality)
        else:
            form = SpecialityForm(request.POST)
        speciality = form.save()
        return HttpResponseRedirect(f'/structure/faculty/{speciality.faculty_id}/speciality/list/')

    else:
        try:
            message = request.GET['message']
        except MultiValueDictKeyError:
            message = None

        if speciality_id:
            faculty = Speciality.objects.get(pk=speciality_id)
            form = SpecialityForm(instance=faculty)

        else:
            form = SpecialityForm()
        return render(request,
                      'structure/speciality/edit.html',
                      context={
                          'speciality_id': speciality_id,
                          'form': form,
                          'message': message
                      })


@login_required
@admin_required
def delete_speciality(request, speciality_id):
    speciality = Speciality.objects.get(pk=speciality_id)
    faculty_id = speciality.faculty_id
    try:
        speciality.delete()
        return HttpResponseRedirect(f'/structure/faculty/{faculty_id}/speciality/list/')
    except ProtectedError:
        return HttpResponseRedirect(f'/structure/speciality/edit/{speciality_id}/?message=невозможно удалить специальность')