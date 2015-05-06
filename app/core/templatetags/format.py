from django.utils.translation import ugettext_lazy as _
from django import template

from ..utils import helpers

register = template.Library()




def empty_text(value):
    """Render 'emtpy' string if given value is empty"""
    return value if value else _('not entered')


register.filter('empty_text', empty_text)


def dict_as_request_params(value, exclude):
    """Render 'a=1&b=2' like string based on dictionary"""
    return helpers.get_dict_as_request_params(value, exclude)


register.filter('dict_as_request_params', dict_as_request_params)

