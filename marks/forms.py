from django import forms
from groups_app.models import Group


class UploadDataFileForm(forms.Form):
    file = forms.FileField(label='выберите файл')


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['number', 'year', 'speciality']
