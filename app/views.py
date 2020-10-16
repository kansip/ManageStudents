from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import user_passes_test
from app.forms import *
from app.menu import *
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


@user_passes_test(lambda u: u.is_staff)
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
        courses.append(Course.objects.get(id=i.course_id.id))
    context['courses'] = courses
    return render(request, 'course/course_list.html', context)


@login_required
def course_view(request, course_id):
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}  # REGISTER_PAGE_NAME - заглушка
    user_id = request.user.id
    stud_list = StudentGroup.objects.filter(user_id=user_id)
    course = Course.objects.get(id=course_id)
    for i in stud_list:
        if i.course_id.id == course_id and i.course_id.open or request.user == course.teacher or request.user.is_superuser:
            context['lessons'] = course.lessons.all()
            context['date'] = timezone.now()
            context['course'] = course
            break
    context['syn'] = False
    if request.user.is_staff or request.user.is_superuser:
        context['syn'] = True
    return render(request, 'course/course.html', context)


@login_required
def lesson_view(request, course_id, lesson_id):
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}  # REGISTER_PAGE_NAME - заглушка
    user_id = request.user.id
    stud_list = StudentGroup.objects.filter(user_id=user_id)
    course = Course.objects.get(id=course_id)
    context['course'] = course
    for i in stud_list:
        if i.course_id.id == course_id:
            lesson = course.lessons.get(id=lesson_id)
            if lesson.open:
                context['course'] = course
                context['lesson'] = lesson
                context['blocks'] = lesson.blocks.all()
                if len(lesson.blocks.all()) > 0:
                    path = '/course/' + str(course_id) + '/' + str(lesson_id) + '/' + str(lesson.blocks.all()[0].id)
                    return redirect(path)
                break
    context['syn'] = False
    if request.user.is_staff:
        context['syn'] = True
    return render(request, 'course/lesson/lesson.html', context)


@login_required
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
        path = '/course/' + str(course_id) + '/' + str(lesson_id) + '/' + str(block_id)
        return redirect(path)
    for i in stud_list:
        if i.course_id.id == course_id:
            lesson = course.lessons.get(id=lesson_id)
            if lesson.open:
                block = lesson.blocks.get(id=block_id)
                context['course'] = course
                context['lesson'] = lesson
                context['blocks'] = lesson.blocks.all()
                context['tasks'] = block.tasks.all()
            break
    context['syn'] = False
    if request.user.is_staff:
        context['syn'] = True
    return render(request, 'course/lesson/lesson_block.html', context)


@user_passes_test(lambda u: u.is_superuser)
def task_view(request, task_id):
    context = {'menu': get_context_menu(request, REGISTER_PAGE_NAME)}  # REGISTER_PAGE_NAME - заглушка
    task = Task.objects.get(pk=task_id)
    context['task'] = task
    return render(request, 'tasks/task.html', context)


@user_passes_test(lambda u: u.is_superuser)
def add_course(request):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    context['teachers'] = User.objects.filter(is_staff=1)
    context['user_id'] = request.user.id
    if request.method == 'POST':
        form = AddCourse(request.POST)
        course_name = request.POST['course_name']
        description = request.POST['description']
        teacher = request.POST['teach']  # одинаковые названия
        courses = Course.objects.all()
        flag = True
        for i in courses:
            if i.name == course_name:
                flag = False
                break
        if flag:
            course = Course.objects.create(name=course_name, teacher=User.objects.get(username=teacher),
                                           description=description)
            course.save()
            stud_group = StudentGroup.objects.create(course_id=course)
            path = '/course/' + str(course.id)
            return redirect(path)

    return render(request, 'admin/add_course.html', context)


@user_passes_test(lambda u: u.is_staff)
def course_settings_view(request, course_id):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    context['course'] = Course.objects.get(id=course_id)
    context['group'] = StudentGroup.objects.get(course_id=course_id).name
    context['syn'] = False
    if request.user.is_superuser:
        context['syn'] = True
    return render(request, 'course/course_settings.html', context)


@user_passes_test(lambda u: u.is_staff)
def course_settings_users_view(request, course_id):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    course = Course.objects.get(id=course_id)
    context['course'] = course
    users = []
    group = StudentGroup.objects.get(course_id=course_id)
    for styd in group.user_id.all():
        users.append(User.objects.get(id=styd.id))
    context['users'] = users
    context['syn'] = False
    if request.user.is_superuser:
        context['syn'] = True
    # POST
    if request.method == 'POST':
        id_data = request.POST['user_id']
        if int(User.objects.order_by("-id")[0].id) >= int(id_data):
            user = User.objects.filter(id=id_data)
            if len(user) != 0:
                group.user_id.add(User.objects.get(id=id_data))
            path = '/course/' + str(course.id) + '/settings/users'
            return redirect(path)
        else:
            context['message'] = "Такого пользователя нет"
    return render(request, 'course/course_settings_users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete_course_view(request, course_id, user_id):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    for i in StudentGroup.objects.get(course_id=course_id).user_id.all():
        if i == User.objects.get(id=user_id):
            StudentGroup.objects.get(course_id=course_id).user_id.remove(i)
    path = '/course/' + str(course_id) + '/settings/users'
    return redirect(path)


@user_passes_test(lambda u: u.is_superuser)
def lesson_delete_course_view(request, course_id, lesson_id):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    for i in Course.objects.get(id=course_id).lessons.all():
        if i == Lesson.objects.get(id=lesson_id):
            Course.objects.get(id=course_id).lessons.remove(i)
            Lesson.objects.get(id=lesson_id).delete()
    path = '/course/' + str(course_id) + '/maintenance'
    return redirect(path)


@user_passes_test(lambda u: u.is_staff)
def course_dashboard_view(request, course_id):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    context['course'] = Course.objects.get(id=course_id)
    context['syn'] = False
    if request.user.is_superuser:
        context['syn'] = True
    return render(request, 'course/course_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser)
def course_maintenance_view(request, course_id):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    context['course'] = Course.objects.get(id=course_id)
    context['lessons'] = Course.objects.get(id=course_id).lessons.all()
    context['syn'] = False
    if request.user.is_superuser:
        context['syn'] = True
    return render(request, 'course/course_maintenance.html', context)


@user_passes_test(lambda u: u.is_superuser)
def course_settings_methodical_plan(request, course_id):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    context['course'] = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = AddInstruction(request.POST)
        if form.is_valid():
            if form.cleaned_data['main_instr_id'] == -1:
                global_instruction = MethodicalInstructionsGlobal()
                global_instruction.name = form.cleaned_data['topic']
                global_instruction.save()
                Course.objects.get(id=course_id).methodical_instructions.add(global_instruction)
            else:
                instruction = MiniSubject()
                instruction.name = form.cleaned_data['topic']
                instruction.save()
                global_instruction = MethodicalInstructionsGlobal.objects.get(id=form.cleaned_data['main_instr_id'])
                global_instruction.mini_subject.add(instruction)

    context['syn'] = False
    if request.user.is_superuser:
        context['syn'] = True
    return render(request, 'course/course_methodical_plan.html', context)


@user_passes_test(lambda u: u.is_superuser)
def course_global_instuction_del(request, course_id, global_instuction):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    instuction = MethodicalInstructionsGlobal.objects.get(id=global_instuction)
    for i in instuction.mini_subject.all():
        MiniSubject.objects.get(id=i.id).delete()
    instuction.delete()
    path = '/course/' + str(course_id) + '/settings/methodical_plan'
    return redirect(path)


@user_passes_test(lambda u: u.is_superuser)
def course_lesson_add_view(request, course_id):
    lesson = Lesson()
    lesson.teacher = Course.objects.get(id=course_id).teacher
    lesson.save()
    Course.objects.get(id=course_id).lessons.add(lesson)
    path = '/course/' + str(course_id) + '/maintenance'
    return redirect(path)


@user_passes_test(lambda u: u.is_staff)
def teaching(request):
    context = {'menu': get_context_menu(request, COURSE_ADD_NAME)}
    context['courses'] = Course.objects.filter(teacher=request.user.id)
    context['syn'] = False
    if request.user.is_superuser:
        context['syn'] = True
    return render(request, 'teaching/teaching.html', context)


@user_passes_test(lambda u: u.is_superuser)
def course_list_admin(request):
    context = {'menu': get_context_menu(request, TEACHING_PAGE_NAME)}
    context['courses'] = Course.objects.all()
    return render(request, 'admin/course_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def course_main_info_settings(request, course_id):
    context = {'menu': get_context_menu(request, TEACHING_PAGE_NAME)}
    context['course'] = Course.objects.get(id=course_id)
    context['teachers'] = User.objects.filter(is_staff=1)
    if request.method == "POST":
        form = AddCourse(request.POST)
        course_name = request.POST['course_name']
        description = request.POST['description']
        teacher = request.POST['teach']
        open = request.POST['open']  # одинаковые названия
        if open == 'on':
            open = True
        else:
            open = False
        courses = Course.objects.all()
        flag = True
        for i in courses:
            if i.name == course_name:
                flag = False
                break
        if flag:
            course = Course.objects.get(id=course_id)
            course.name = course_name
            course.teacher = User.objects.get(username=teacher)
            course.description = description
            course.open = open
            course.save()
            path = '/course/' + str(course.id)
            return redirect(path)
    context['syn'] = False
    if request.user.is_superuser:
        context['syn'] = True
    return render(request, 'course/course_main_info.html', context)
