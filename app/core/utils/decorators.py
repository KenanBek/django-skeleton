import timeit

import jsonpickle
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages


def log(fn):
    """
    Logger decorator.
    Logs function Executing and Executed info and total Executed Time.
    """

    def wrapper(*args, **kwargs):
        # Get information about executing function
        function_name = "'(%(type)s) %(module)s.%(name)s'" % \
                        {'module': fn.__module__, 'type': fn.__class__.__name__, 'name': fn.__name__}
        # Log about start of the function
        settings.LOGIC_LOGGER.info('Start %s', function_name)
        # Function start time
        start = timeit.default_timer()
        # Executing function itself
        fn_result = fn(*args, **kwargs)
        # Function end time
        stop = timeit.default_timer()
        # Calculate function executing time
        time = stop - start
        # Log about end of the function
        settings.LOGIC_LOGGER.info('End %s in %.5f SECs', function_name, time)
        return fn_result

    return wrapper


def json(fn):
    """
    Gets view method response and returns it in JSON format.
    """

    def wrapper(request, *args, **kwargs):
        try:
            # Executing function itself
            fn_result = fn(request, *args, **kwargs)
            # Prepare JSON dictionary for successful result
            json_result = {'is_successful': True, 'result': fn_result}
        except Exception as e:
            # If AJAX_DEBUG is enabled raise exception
            if settings.JSON_DEBUG:
                raise
            # Else prepare JSON result object with error message
            error_message = e.message.upper()
            json_result = {'is_successful': False, 'message': error_message}
        # Wrap result with JSON HTTPResponse and return
        return HttpResponse(jsonpickle.encode(json_result, unpicklable=False), content_type='application/json')

    return wrapper


def anonymous_required(function):
    """
    Check either user registered or not. If it is already registered user will redirect to 'INDEX'.
    """

    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            messages.add_message(request, messages.ERROR, _('You are already registered and logged in.'))
            return redirect(reverse('index'))
        else:
            return function(request, *args, **kwargs)

    return wrap

