from string import lower
from django import template

register = template.Library()


@register.filter(name='str_replace')
def str_replace(value, arg):
    if lower( value.split('.')[-1]) == 'mp4':
        return value.replace('mp4', 'webm')

    return value.replace('.', arg)