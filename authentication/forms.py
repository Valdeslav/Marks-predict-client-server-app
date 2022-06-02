from django import forms
from authentication.models import User, Role
from marks.models import Student


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Логин", max_length=150)
    first_name = forms.CharField(label="Имя", max_length=150)
    last_name = forms.CharField(label="Фамилия", max_length=150)
    student = forms.ModelChoiceField(queryset=Student.objects.all(), required=False, label='Студент')
    email = forms.CharField(label="Электронная почта", widget=forms.EmailInput)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, label='Роль')
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'student', 'role')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']
