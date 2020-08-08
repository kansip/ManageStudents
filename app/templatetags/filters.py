from django import template
from django.contrib.auth.models import User
from app.models import TaskAnswers, Task

register = template.Library()


@register.filter(name='get_username')
def get_username(id):
    user = User.objects.get(id=id)
    return user.username


@register.filter(name='get_max_score')
def get_max_score(user_id, task_id):
    task = Task.objects.get(id=task_id)
    res = -1
    for ans in task.answers.all():
        if ans.user.id == user_id:
            if ans.score > 0:
                res = ans.score
            else:
                res = 0
    if res == -1:
        return '-'
    else:
        return res
