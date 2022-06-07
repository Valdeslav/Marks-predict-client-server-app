from django.forms import ModelForm
from groups_app.models import Faculty


class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = ['name']
