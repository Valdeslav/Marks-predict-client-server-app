from django.forms import ModelForm
from groups_app.models import Faculty, Speciality


class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = ['name']


class SpecialityForm(ModelForm):
    class Meta:
        model = Speciality
        fields = ['name', 'faculty']
