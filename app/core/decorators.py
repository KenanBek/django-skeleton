from functools import wraps


def use_theme(theme):
    """
    Injects theme folder name into 'template' argument of 'django.shortcuts.render'.
    """

    def wrapper(fn):
        def inner_wrapper(request, *args, **kwargs):
            template = fn.func_defaults[0]
            context = fn.func_defaults[1]
            theme_template = "{0}/{1}".format(theme, template)
            return fn(request, theme_template, context)

        return wraps(fn)(inner_wrapper)

    return wrapper

