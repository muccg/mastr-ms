from django import template

register = template.Library()

@register.simple_tag
def version():
    module = __import__("mastrms")
    return module.VERSION