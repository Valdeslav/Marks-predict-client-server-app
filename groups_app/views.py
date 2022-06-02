from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Faculty, Speciality, Group


@login_required
def faculty_list(request):
    """getting a list of faculties"""
    faculties = Faculty.objects.all()
    return render(request, "structure/faculty/list.html", context={"faculties": faculties})


@login_required
def group_list(request, faculty_id):
    """getting a list of specialities of selected faculty"""
    years_obj = Group.objects.only('year').filter(speciality__faculty_id=faculty_id).distinct('year').order_by('year')
    groups_by_years = []
    for year_obj in years_obj:
        groups = Group.objects.filter(year=year_obj.year, speciality__faculty_id=faculty_id).defer('year')
        groups.year = year_obj.year
        groups_by_years.append(groups)

    return render(request, "structure/group/list.html",
                  context={"groups": groups_by_years, "faculty_id": faculty_id})
