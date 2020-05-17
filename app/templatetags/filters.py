from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.filter(name='get_username')
def get_username(id):
    user = User.objects.get(id=id)
    return user.username
