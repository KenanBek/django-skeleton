from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from django.contrib import messages
from django.shortcuts import redirect


def anonymous_required(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated():
            messages.add_message(request, messages.ERROR, _('You are already registered and logged in.'))
            return redirect(reverse('website_index'))
        else:
            return function(request, *args, **kwargs)

    return wrap

