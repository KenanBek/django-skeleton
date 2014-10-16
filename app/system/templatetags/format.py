from django.utils.translation import ugettext_lazy as _
from django import template

register = template.Library()


def empty_text(value):
    """Render 'emtpy' string if given value is empty"""
    return value if value else _('not entered')

register.filter('empty_text', empty_text)

