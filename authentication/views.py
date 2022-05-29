from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from urllib.parse import urlencode
from authentication.forms import UserRegistrationForm, LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/structure/faculty/list")
                else:
                    return render(request, 'auth/login.html', {'form': form, 'message': 'Неактивный аккаунт'})
            else:
                return render(request, 'auth/login.html',
                              {
                                'form': form,
                                'message': 'Не удалось войти. Убедитесь что ввели верные Логин и Пароль'
                              })
    else:
        message = request.GET.get("scmsg")
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form, 'scmsg': message})


def user_logout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            logout(request)
    return HttpResponseRedirect("/")

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            url_param = urlencode({'scmsg': 'Вы успешно зарегистрировались.\nТеперь вы можете войти в свой аккаунт'})
            http_response = HttpResponseRedirect(f'/login?{url_param}')

            return http_response
    else:
        user_form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'user_form': user_form})


