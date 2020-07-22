from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import user_passes_test
from app.forms import LoginForm, RegisterForm, ChangeProfile, TaskStringForm
from app.menu import get_context_menu, REGISTER_PAGE_NAME, LOGIN_PAGE_NAME, HOME_PAGE_NAME, USER_PAGE_NAME, \
    USER_LIST_NAME, USER_TASK_NAME, COURSE_LIST_NAME
from app.models import *
from django.utils import timezone
from app.checkers import *


def index(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    else:
        return redirect('/main')


def register_view(request):
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}

    if request.method == 'POST':
        errors = []

        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            login_data = register_form.cleaned_data['login']
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            password_data = register_form.cleaned_data['password']
            password_repeat_data = register_form.cleaned_data['password_repeat']

            if len(login_data) < 3:
                errors.append('Логин должен иметь длину больше 2 символов')

            if User.objects.filter(username=login_data).exists():
                errors.append('Пользователь с таким логином уже существует')

            if len(password_data) < 4:
                errors.append('Пароль должен иметь длину больше 3 символов')

            if password_data != password_repeat_data:
                errors.append('Пароли не совпадают')

            if len(errors) == 0:
                user = User.objects.create_user(username=login_data, password=password_data,
                                                first_name=first_name,
                                                last_name=last_name)
                user.save()

                if user is not None:
                    login(request, user)
                    return redirect('/')

                return redirect('/')
        else:
            errors.append('Заполните все поля')

        context['error'] = errors[0]

    return render(request, 'auth/register.html', context)


def login_view(request):
    context = {'menu': get_context_menu(request, LOGIN_PAGE_NAME)}

    if not request.user.is_authenticated:
        if request.method == 'POST':
            login_form = LoginForm(request.POST)

            if login_form.is_valid():
                login_data = login_form.cleaned_data['login']
                password_data = login_form.cleaned_data['password']

                print(login_data)
                print(password_data)

                user = authenticate(request, username=login_data, password=password_data)

                if user is not None:
                    login(request, user)
                    return redirect('/')

            context['error'] = 'Неверный логин или пароль'

        return render(request, 'auth/login.html', context)
    else:
        return redirect('/')


@login_required
def user_page_view(request, user_id):
    context = {'menu': get_context_menu(request, USER_PAGE_NAME)}

    user = User.objects.get(pk=user_id)
    context['syn'] = "Ученик"
    if user.is_staff:
        context['syn'] = "Модератор"
    if user.is_superuser:
        context['syn'] = "Админ"
    if request.user.is_authenticated and request.user == user or request.user.is_staff or request.user.is_superuser:
        context['permission'] = False
        if request.user.is_superuser:
            context['permission'] = True
        context['user'] = user
        return render(request, 'user/user.html', context)

    return redirect('/')


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def main_page_view(request):
    context = {'menu': get_context_menu(request, HOME_PAGE_NAME)}
    if request.user.is_superuser:
        context['syn'] = "Admin"
        return render(request, 'admin/main.html', context)

    if request.user.is_staff:
        context['syn'] = "Moder"
        return render(request, 'admin/main.html', context)
    return render(request, 'index.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_page_changes_view(request, user_id):
    context = {'menu': get_context_menu(request, USER_PAGE_NAME)}
    user = User.objects.get(pk=user_id)

    context['user'] = user
    context['syn'] = "Student"
    if user.is_superuser:
        context['syn'] = "Admin"
    elif user.is_staff:
        context['syn'] = "Moder"
    if request.method == 'POST':
        change_form = ChangeProfile(request.POST)

        login_data = change_form.cleaned_data['username']
        password_data = change_form.cleaned_data['password']
        repit_password_data = change_form.cleaned_data['repit_password']
        first_name = change_form.cleaned_data['first_name']
        last_name = change_form.cleaned_data['last_name']
        group = change_form.cleaned_data['group']
        bans = change_form.changed_data['bans']
        syn = change_form.CHOICES
        print(login_data)
        print(password_data)

        user = authenticate(request, username=login_data, password=password_data)

        if user is not None:
            login(request, user)
            return redirect('/')

        context['error'] = 'Неверный логин или пароль'

        return render(request, 'auth/login.html', context)
    else:
        return render(request, 'user/user_settings.html', context)


@user_passes_test(lambda u: u.is_staff)
def user_list_page(request):
    context = {'menu': get_context_menu(request, USER_LIST_NAME)}
    context["users"] = User.objects.all()
    context['setting'] = False
    if request.user.is_superuser:
        context['setting'] = True
    return render(request, 'admin/user_list.html', context)


def task_list_view(request):
    context = {'menu': get_context_menu(request, USER_TASK_NAME)}  # REGISTER_PAGE_NAME - заглушка
    context['tasks'] = Task.objects.all()
    return render(request, 'admin/task_list.html', context)


@login_required
def course_list_view(request):
    context = {'menu': get_context_menu(request, COURSE_LIST_NAME)}  # REGISTER_PAGE_NAME - заглушка
    user_id = request.user.id
    courses_id = StudentGroup.objects.filter(user_id=user_id)  # refactor
    courses = []
    for i in courses_id:
        courses.append(Course.objects.get(id=i.id))
    context['courses'] = courses
    return render(request, 'course/course_list.html', context)


@login_required
def course_view(request, course_id):
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}  # REGISTER_PAGE_NAME - заглушка
    user_id = request.user.id
    stud_list = StudentGroup.objects.filter(user_id=user_id)
    course = Course.objects.get(id=course_id)
    context['course_name'] = "ХЗ"
    for i in stud_list:
        if i.course_id.id == course_id:
            context['lessons'] = course.lessons.all()
            context['date'] = timezone.now()
            context['course'] = course
            break

    return render(request, 'course/course.html', context)


@login_required
def lesson_view(request, course_id, lesson_id):
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}  # REGISTER_PAGE_NAME - заглушка
    user_id = request.user.id
    stud_list = StudentGroup.objects.filter(user_id=user_id)
    course = Course.objects.get(id=course_id)
    for i in stud_list:
        if i.course_id.id == course_id:
            lesson = course.lessons.get(id=lesson_id)
            context['course'] = course
            context['lesson'] = lesson
            context['blocks'] = lesson.blocks.all()
            if len(lesson.blocks.all()) > 0:
                path = '/course/' + str(course_id) + '/' + str(lesson_id) + '/' + str(lesson.blocks.all()[0].id)
                return redirect(path)
            break
    return render(request, 'course/lesson/lesson.html', context)


def lesson_block_view(request, course_id, lesson_id, block_id):
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}  # REGISTER_PAGE_NAME - заглушка
    user_id = request.user.id
    stud_list = StudentGroup.objects.filter(user_id=user_id)
    course = Course.objects.get(id=course_id)
    context['user_id'] = user_id
    if request.method == 'POST':
        form = TaskStringForm(request.POST)
        if form.is_valid():
            task_id = form.cleaned_data['task_id']
            answer = form.cleaned_data['data']
            allocation(task_id, user_id, answer)
        lesson = course.lessons.get(id=lesson_id)
        path = '/course/' + str(course_id) + '/' + str(lesson_id) + '/' + str(lesson.blocks.all()[0].id)
        return redirect(path)
    for i in stud_list:
        if i.course_id.id == course_id:
            lesson = course.lessons.get(id=lesson_id)
            block = lesson.blocks.get(id=block_id)

            context['course'] = course
            context['lesson'] = lesson
            context['blocks'] = lesson.blocks.all()
            context['tasks'] = block.tasks.all()
            break
    return render(request, 'course/lesson/lesson_block.html', context)


def task_view(request, task_id):
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}  # REGISTER_PAGE_NAME - заглушка
    task = Task.objects.get(pk=task_id)
    context['task'] = task
    return render(request, 'tasks/task.html', context)
