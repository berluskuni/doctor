from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .decorators import super_user_required, admin_required
from django.contrib.auth.decorators import login_required
from django.core.files import uploadhandler, uploadedfile
from uuslug import slugify
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.cache import cache
from clinika.models import *
from .apps import *
from .forms import *
from django.core.files.storage import default_storage
from extuser.forms import UserCreationForm
# Create your views here.


@login_required
def main(request):
    user = request.user
    path = '/adminka/dashboard/'
    admin, staff = determine_role(user)
    return render(request, 'index_admin.html', {
        'admin': admin,
    })

@login_required
def dashboard(request):
    return render(request, 'admin_dashboard.html', {'active': 'dash'})

### Авторизация ###
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if user.groups.filter(name='admin') or user.is_superuser:
                    return HttpResponseRedirect('/adminka/')
                elif user.groups.filter(name='staff'):
                    return HttpResponseRedirect('/staff/')
                else:
                    #logout(request)
                    return HttpResponseRedirect('/adminka/')
            else:
                message1 = 'Доступ закрыт'
                message2 = "Неверный логин или пароль"
                return render(request, 'login_denied.html', {'message1': message1,
                                 'message2': message2})
        else:
            message1 = 'Доступ закрыт'
            message2 = "Неверный логин или пароль"
            return render(request, 'login_denied.html', {'message1': message1,
                                                                'message2': message2})
    else:
        return render(request, 'page_login.html', {})

def accounts_login(request):
    return HttpResponseRedirect('/login/')

# функция выхода из системы
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/adminka/')

@login_required
@admin_required
def users_all(request):
    users = ExtUser.objects.all()

    return show_users(request, users)

def show_users(request, qw, D=None):
    user = request.user
    h3_top = 'Пользователи'
    admin, staff = determine_role(user)
    users = get_paginator(request, qw, 20)
    form_create = RegistrationForm()

    return render(request, 'admin_users.html', {
        'h3_top': h3_top, 'users': users,'title': 'Пользователи', 'form_create': form_create, 'active': 'users',
        'admin': admin,
    })

@login_required
@super_user_required
def users_add_user(request):
    path = request.META.get('HTTP_REFERER', '/')
    errors = []
    if request.method == 'POST':
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        """
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            password1 = D.get('password1')
            password2 = D.get('password2')
            email = D.get('email')
            if ExtUser.objects.filter(email=email).exists():
                user = ExtUser.objects.get(email=email)
                if user.is_active:
                    error = 'Пользователь с таким E.mail уже зарегистрирован'
                    errors.append(error)
            if password1 and password2 and password1 != password2:
                error = 'Пароль и подтверждение не совпадают'
                errors.append(error)
            if errors:
                return render(request, 'admin_users.html', {
                    'errors': errors, 'email': email, 'open': True
                })

            new_user = ExtUser.objects.create(email=email)
            new_user.is_active = True
            new_user.set_password(password2)
            new_user.save()
    return HttpResponseRedirect(path)

def get_user_group_permissions(object):
    D = {}
    all_groups = Group.objects.all()
    groups = object.groups.all()
    for group in all_groups:
        if group in groups:
            D[group.name] = True
        else:
            D[group.name] = False
    return D

@login_required
def my_profile(request):
    user = request.user
    path = '/adminka/user/' + str(user.pk) + '/'
    return HttpResponseRedirect(path)

@login_required
def users_show_user(request, user_id):
    current_user = request.user
    admin = False
    admin_gr = Group.objects.get(name='admin')
    admins = admin_gr.user_set.all()
    if current_user in admins:
        admin = True
    user = get_object_or_404(ExtUser, pk=user_id)

    date_of_birth_stroke, age, own = '', '', False

    if user.date_of_birth:
        date_of_birth_stroke, age = determine_age(user)
    if current_user == user:
        own = True
    D = get_user_group_permissions(user)

    form = ChangeProfileForm(initial={'firstname': user.firstname, 'show_date_of_birth': user.show_date_of_birth,
                                      'lastname': user.lastname, 'middlename': user.middlename,
                                      'email': user.email, 'date_of_birth': user.date_of_birth, })
    perm_form = UserPermissionsGroup(initial=D)

    return render(request, 'admin_profile_base.html', {
        'user': user, 'admin': admin, 'perm_form': perm_form, 'form': form, 'date_of_birth_stroke': date_of_birth_stroke,
        'own': own
    })


# Изменение данных профиля
@login_required
def user_profile_change(request):
    current_user = request.user
    return_path = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        change_profile_form = ChangeProfileForm(request.POST)
        change_profile_form.full_clean()
        D = change_profile_form.cleaned_data
        user_pk = D.get('user_pk')
        try:
            user = ExtUser.objects.get(pk=int(user_pk))
        except:
            message1 = 'Пользователь не определен.'
            message2 = 'Вернитесь, обновите страницу и повторите запрос.'
            return render(request, 'access_denied.html', {
                'message1': message1, 'message2': message2
            })

        if user:
            if current_user != user and not current_user.groups.filter(name='admin').exists():
                message1 = 'Не являетесь данным пользователем или администратором.'
                return render(request, 'access_denied.html', {
                    'message1': message1,
                })
            firstname = D.get('firstname')
            lastname = D.get('lastname')
            middlename = D.get('middlename')
            email = D.get('email')
            date_of_birth = D.get('date_of_birth')
            password1 = D.get('password1')
            password2 = D.get('password2')

            if firstname:
                user.firstname = clean_word(firstname, '@#<>/?$%^')
            if lastname:
                user.lastname = clean_word(lastname, '@#<>/?$%^')
            if middlename:
                user.middlename = clean_word(middlename, '@#<>/?$%^')

            if email:
                if ExtUser.objects.filter(email=email).exists() and email != user.email:
                    user = ExtUser.objects.get(email=email)
                    if user.is_active:
                        message1 = 'Пользователь с таким E.mail уже зарегистрирован'
                        return render(request, 'access_denied.html', {
                            'message1': message1
                        })
                if email != user.email:
                    user.email = email
            if date_of_birth:
                user.date_of_birth = date_of_birth

            user.save()
            if password1 and password2:
                if password1 == password2:
                    user.set_password(D['password1'])
                    user.save()
                    return HttpResponseRedirect('/logout/')
                else:
                    message1 = 'Пароль не изменен. Новый пароль и подтверждение не совпадают'
                    return render(request, 'access_denied.html', {
                        'message1': message1
                    })
            return HttpResponseRedirect(return_path)

    return HttpResponseRedirect(return_path)

# Изменение данных профиля
@login_required
def profile_change_part(request, oper_name):
    current_user = request.user
    return_path = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            user_pk = D.get('user_pk')
            try:
                user = ExtUser.objects.get(pk=int(user_pk))
            except:
                message1 = 'Пользователь не определен.'
                message2 = 'Вернитесь, обновите страницу и повторите запрос.'
                return render(request, 'access_denied.html', {
                    'message1': message1, 'message2': message2
                })
            if user:
                if current_user != user and not current_user.groups.filter(name='admin').exists():
                    message1 = 'Не являетесь данным пользователем или администратором.'
                    return render(request, 'access_denied.html', {
                        'message1': message1,
                    })
                if oper_name == 'addemail':
                    email_add = D.get('email')
                    if email_add:
                        if not user.emails_set.filter(email=email_add).exists():
                            user.emails_set.create(email=email_add)
                if oper_name == 'addphone':
                    phone_add = D.get('phone')
                    if phone_add:
                        phone_add = clean_phone_number(phone_add)
                        if not user.phonenumber_set.filter(number=phone_add).exists():
                            user.phonenumber_set.create(number=phone_add)

                return HttpResponseRedirect(return_path)
    return HttpResponseRedirect(return_path)

# Изменение данных профиля (удаление почты или телефона)
@login_required
def profile_del_part(request, oper_name, one_id):
    current_user = request.user
    return_path = request.META.get('HTTP_REFERER', '/')
    objekt = ''
    if oper_name == 'delemail':
        try:
            objekt = Emails.objects.get(pk=one_id)
        except:
            objekt = ''
    if oper_name == 'delphone':
        try:
            objekt = PhoneNumber.objects.get(pk=one_id)
        except:
            objekt = ''
    if objekt:
        user = objekt.extuser
        if user == current_user or current_user.groups.filter(name='admin').exists():
            objekt.delete()
            return HttpResponseRedirect(return_path)
        else:
            message1 = 'Не являетесь владельцем или администратором.'
            return render(request, 'access_denied.html', {
                'message1': message1,
            })
    else:
        message1 = 'Объект не определен.'
        return render(request, 'access_denied.html', {
            'message1': message1,
        })

# Персональные разрешения
@login_required
@super_user_required
def adm_perms_personal(request):
    D = {}
    if request.method == 'POST':
        form = UserPermissionsGroup(request.POST)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            user = D.pop('extuser')

            create_perms(user, D)  # присвоение разрешений
            user.make_is_staff()

            return_path = request.META.get('HTTP_REFERER', '/')
            return HttpResponseRedirect(return_path)
    return_path = request.META.get('HTTP_REFERER', '/')
    return HttpResponseRedirect(return_path)

# принадлежность объекта группам
def create_perms(object, D):
    for x,y in D.items():
        if not Group.objects.filter(name=x).exists():
            Group.objects.create(name=x)
        if y == True:
            object.groups.add(Group.objects.get(name=x))
        else:
            object.groups.remove(Group.objects.get(name=x))

@login_required
def user_change_password(request):
    current_user = request.user
    return_path = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = ChangeProfileForm(request.POST)
        if form.is_valid():
            form.full_clean()
            D = form.cleaned_data
            user_pk = D.get('user_pk')
            try:
                user = ExtUser.objects.get(pk=int(user_pk))
            except:
                message1 = 'Пользователь не определен.'
                message2 = 'Вернитесь, обновите страницу и повторите запрос.'
                return render(request, 'access_denied.html', {
                    'message1': message1, 'message2': message2
                })
            if user:
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')
                if user.is_superuser and current_user != user:
                    message1 = 'Доступ закрыт'
                    message2 = "Нельзя изменить пароль этому пользователю"
                    return render(request, 'access_denied.html', {
                        'message1': message1, 'message2': message2,
                    })
                if not current_user.groups.filter(name='admin').exists():
                    message1 = 'У Вас нет прав администратора для этого действия'
                    return render(request, 'access_denied.html', {
                        'message1': message1
                    })
                username = current_user.email
                admin = authenticate(username=username, password=password1)
                if admin:
                    user.set_password(password2)
                    user.save()
                    return HttpResponseRedirect(return_path)
                else:
                    message1 = 'Вы неверно указали свой пароль.'
                    return render(request, 'access_denied.html', {
                        'message1': message1
                    })
        else:
            message1 = 'Данные не проходят валидацию'
            message2 = "Нельзя изменить пароль этому пользователю"
            return render(request, 'access_denied.html', {
                'message1': message1, 'message2': message2,
            })
    return HttpResponseRedirect(return_path)