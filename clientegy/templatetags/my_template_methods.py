from django import template

register = template.Library()


@register.filter(name = 'length')
def length(value):
    return len(value)