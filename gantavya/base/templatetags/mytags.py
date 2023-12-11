from django import template

register = template.Library()

@register.filter
def get_by_index(value,i):
    return value[i-1]