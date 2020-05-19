from django import forms


class RegisterForm(forms.Form):
    login = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField()
    password_repeat = forms.CharField()


class LoginForm(forms.Form):
    login = forms.CharField()
    password = forms.CharField()


class CharFormTask(forms.Form):
    data = forms.CharField()


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
