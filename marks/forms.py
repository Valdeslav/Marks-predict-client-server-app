from django import forms
from groups_app.models import Group
from marks.models import Student, Mark


class UploadDataFileForm(forms.Form):
    file = forms.FileField(label='выберите файл')


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['number', 'year', 'speciality']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['fullname', 'group']


class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['student', 'subject', 'mark']
