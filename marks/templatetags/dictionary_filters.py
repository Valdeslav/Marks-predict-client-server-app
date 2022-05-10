from django import template

register = template.Library()


@register.filter(name='dict_get_value')
def dict_get_value(dictionary, key):
    """Return value from dictionary by key"""

    return dictionary.get(key, None)
