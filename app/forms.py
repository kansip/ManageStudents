from django import forms
from app.models import User


class RegisterForm(forms.Form):
    login = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()
    password_repeat = forms.CharField()


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField()


class TaskStringForm(forms.Form):
    data = forms.CharField()
    task_id = forms.IntegerField()


class ChangeProfile(forms.Form):
    CHOICES = [('Ученик', 'Ученик'),
               ('Модератор', 'Модератор'),
               ('Админ', 'Админ')]
    login = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()
    password_repeat = forms.CharField()
    group = forms.CharField()
    bans = forms.BooleanField()
    syns = forms.ChoiceField(choices=CHOICES)


class AddCourse(forms.Form):
    course_name = forms.CharField()
    TEACHER_LIST = []
    for teache in User.objects.filter(is_staff=1):
        TEACHER_LIST.append((teache.id, teache.username))
    TEACHER_LIST = tuple(TEACHER_LIST)
    teach = forms.ChoiceField(widget=forms.Select, choices=TEACHER_LIST)
