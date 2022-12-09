from django import template

register = template.Library()

@register.simple_tag
def changeStatement(status):
    return 0
